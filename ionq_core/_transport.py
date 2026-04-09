"""Retry transport for httpx with exponential backoff."""

import logging
import random
import time
from collections.abc import Generator
from typing import Never

import httpx

from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    raise_for_status,
)

logger = logging.getLogger("ionq_core")

RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503})
DEFAULT_MAX_RETRIES = 2


def _parse_retry_after(response: httpx.Response) -> float | None:
    header = response.headers.get("retry-after")
    if header is None:
        return None
    try:
        return float(header)
    except ValueError:
        return None


def _backoff_delays(max_retries: int) -> Generator[float]:
    yield 0.0
    for attempt in range(max_retries):
        base = 0.5 * (2**attempt)
        yield base + random.random() * base * 0.5  # noqa: S311


def _parse_error_body(response: httpx.Response) -> dict | str | None:
    try:
        return response.json()
    except Exception:
        return response.text or None


def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    body = _parse_error_body(response)
    message = body.get("message") or body.get("error") if isinstance(body, dict) else None
    raise_for_status(response.status_code, body, _parse_retry_after(response), message)


def _retry_wait(delay: float, last_response: httpx.Response | None) -> float:
    if last_response is not None:
        retry_after = _parse_retry_after(last_response)
        if retry_after is not None:
            return max(retry_after, delay)
    return delay


def _raise_exhausted(last_response: httpx.Response | None, last_exc: Exception | None) -> Never:
    if last_response is not None:
        _raise_for_response(last_response)
        raise APIError(last_response.status_code)  # unreachable; satisfies type checker
    if isinstance(last_exc, httpx.TimeoutException):
        raise APITimeoutError(str(last_exc)) from last_exc
    if last_exc is not None:
        raise APIConnectionError(str(last_exc)) from last_exc
    raise APIConnectionError("Request failed with no response")


class RetryTransport(httpx.BaseTransport):
    """Wraps an httpx transport with retry logic and error raising."""

    def __init__(self, transport: httpx.BaseTransport, max_retries: int = DEFAULT_MAX_RETRIES) -> None:
        self._transport = transport
        self._max_retries = max_retries

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        last_exc: Exception | None = None
        last_response: httpx.Response | None = None

        for delay in _backoff_delays(self._max_retries):
            if delay > 0:
                wait = _retry_wait(delay, last_response)
                logger.debug("Retrying request to %s after %.1fs", request.url, wait)
                time.sleep(wait)

            try:
                response = self._transport.handle_request(request)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                last_response = None
                continue

            if response.status_code in RETRYABLE_STATUS_CODES:
                last_response = response
                last_exc = None
                continue

            _raise_for_response(response)
            return response

        _raise_exhausted(last_response, last_exc)

    def close(self) -> None:
        self._transport.close()


class AsyncRetryTransport(httpx.AsyncBaseTransport):
    """Wraps an async httpx transport with retry logic and error raising."""

    def __init__(self, transport: httpx.AsyncBaseTransport, max_retries: int = DEFAULT_MAX_RETRIES) -> None:
        self._transport = transport
        self._max_retries = max_retries

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        import asyncio

        last_exc: Exception | None = None
        last_response: httpx.Response | None = None

        for delay in _backoff_delays(self._max_retries):
            if delay > 0:
                wait = _retry_wait(delay, last_response)
                logger.debug("Retrying request to %s after %.1fs", request.url, wait)
                await asyncio.sleep(wait)

            try:
                response = await self._transport.handle_async_request(request)
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                last_response = None
                continue

            if response.status_code in RETRYABLE_STATUS_CODES:
                last_response = response
                last_exc = None
                continue

            _raise_for_response(response)
            return response

        _raise_exhausted(last_response, last_exc)

    async def aclose(self) -> None:
        await self._transport.aclose()
