"""Retry transport for httpx with exponential backoff."""

import asyncio
import calendar
import email.utils
import logging
import random
import time
from collections.abc import Iterator
from typing import NoReturn

import httpx

from ._exceptions import APIConnectionError, APITimeoutError, raise_for_status

logger = logging.getLogger("ionq_core")

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, *range(520, 530)})
DEFAULT_MAX_RETRIES = 2
_MAX_RETRY_AFTER = 60.0
_IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS"})


def _parse_retry_after(response: httpx.Response) -> float | None:
    header = response.headers.get("retry-after")
    if header is None:
        return None
    try:
        return max(0.0, float(header))
    except ValueError:
        parsed = email.utils.parsedate(header)
        if parsed is not None:
            return max(0.0, calendar.timegm(parsed) - time.time())
        return None


def _backoff_delays(max_retries: int) -> Iterator[float]:
    yield 0.0
    for attempt in range(max_retries):
        base = 0.5 * (2**attempt)
        yield base + random.random() * base * 0.5


def _parse_error_body(response: httpx.Response) -> dict | str | None:
    try:
        return response.json()
    except Exception:
        text = response.text
        return text[:500] if text else None


def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    body = _parse_error_body(response)
    message = body.get("message") or body.get("error") if isinstance(body, dict) else None
    request_id = response.headers.get("x-request-id")
    raise_for_status(response.status_code, body, _parse_retry_after(response), message, request_id=request_id)


def _retry_delay(delay: float, last_response: httpx.Response | None) -> float:
    if last_response is not None:
        retry_after = _parse_retry_after(last_response)
        if retry_after is not None:
            return min(max(retry_after, delay), _MAX_RETRY_AFTER)
    return delay


def _raise_exhausted(last_response: httpx.Response | None, last_exc: Exception | None) -> NoReturn:
    if last_response is not None:
        _raise_for_response(last_response)
    if isinstance(last_exc, httpx.TimeoutException):
        raise APITimeoutError(str(last_exc)) from last_exc
    if last_exc is not None:
        raise APIConnectionError(str(last_exc)) from last_exc
    raise APIConnectionError("Request failed with no response")


def _should_retry(request: httpx.Request, response: httpx.Response, retryable: frozenset[int]) -> bool:
    """Return True if this response should be retried.

    Non-idempotent methods (POST) are only retried on 429 (rate limit)
    since the server may have already processed the request on 5xx.
    """
    if response.status_code not in retryable:
        return False
    return request.method in _IDEMPOTENT_METHODS or response.status_code == 429


def _is_retryable_exc(request: httpx.Request, exc: Exception) -> bool:
    """Return True if this exception warrants a retry.

    Connect errors are always retryable (no data was sent).
    Other network/timeout errors are only retryable for idempotent methods.
    """
    if isinstance(exc, httpx.ConnectError):
        return True
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return request.method in _IDEMPOTENT_METHODS
    return False


class RetryTransport(httpx.BaseTransport):
    """Wraps an httpx transport with retry logic and error raising."""

    def __init__(
        self,
        transport: httpx.BaseTransport,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
    ) -> None:
        self._transport = transport
        self._max_retries = max_retries
        self._retryable = retryable_status_codes

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        last_exc: Exception | None = None
        last_response: httpx.Response | None = None

        for delay in _backoff_delays(self._max_retries):
            if delay > 0:
                wait = _retry_delay(delay, last_response)
                logger.debug("Retrying request to %s after %.1fs", request.url, wait)
                time.sleep(wait)

            try:
                response = self._transport.handle_request(request)
            except Exception as exc:
                if not _is_retryable_exc(request, exc):
                    raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
                last_exc, last_response = exc, None
                continue

            if _should_retry(request, response, self._retryable):
                last_response, last_exc = response, None
                continue

            _raise_for_response(response)
            return response

        _raise_exhausted(last_response, last_exc)

    def close(self) -> None:
        self._transport.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """Wraps an async httpx transport with retry logic and error raising."""

    def __init__(
        self,
        transport: httpx.AsyncBaseTransport,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retryable_status_codes: frozenset[int] = RETRYABLE_STATUS_CODES,
    ) -> None:
        self._transport = transport
        self._max_retries = max_retries
        self._retryable = retryable_status_codes

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        last_exc: Exception | None = None
        last_response: httpx.Response | None = None

        for delay in _backoff_delays(self._max_retries):
            if delay > 0:
                wait = _retry_delay(delay, last_response)
                logger.debug("Retrying request to %s after %.1fs", request.url, wait)
                await asyncio.sleep(wait)

            try:
                response = await self._transport.handle_async_request(request)
            except Exception as exc:
                if not _is_retryable_exc(request, exc):
                    raise APIConnectionError(f"{type(exc).__name__}: {exc}") from exc
                last_exc, last_response = exc, None
                continue

            if _should_retry(request, response, self._retryable):
                last_response, last_exc = response, None
                continue

            _raise_for_response(response)
            return response

        _raise_exhausted(last_response, last_exc)

    async def aclose(self) -> None:
        await self._transport.aclose()
