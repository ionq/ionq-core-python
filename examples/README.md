# ionq-core examples

Runnable scripts that demonstrate how downstream SDKs integrate with `ionq-core`
through the [extension API](https://ionq.github.io/ionq-core-python/ionq_core/extensions.html).

## Setup

```sh
pip install ionq-core
export IONQ_API_KEY=your-api-key
```

Create a free account at [identity.ionq.com/create-account](https://identity.ionq.com/create-account) if you need an API key. Both scripts target the free `simulator` backend.

On Windows PowerShell:

```powershell
$env:IONQ_API_KEY = "your-api-key"
python examples/downstream_integration.py
```

From a clone of this repository you can also use:

```sh
uv run python examples/downstream_integration.py
```

## Scripts

| Script | What it demonstrates |
| --- | --- |
| [`downstream_integration.py`](downstream_integration.py) | Sync `ClientExtension`: `user_agent_token`, `default_headers`, `EventHook`, `error_mapper`, Bell-state job lifecycle |
| [`downstream_integration_async.py`](downstream_integration_async.py) | Same flow with `AsyncEventHook`, `async_wait_for_job`, and `asyncio` endpoints |

Each script configures a `ClientExtension` with:

- `user_agent_token` — downstream SDK identity in the `User-Agent` header
- `default_headers` — SDK-specific headers on every request
- `EventHook` / `AsyncEventHook` — request, response, and error logging
- `error_mapper` — wraps `APIError` and `RateLimitError` (including `request_id`) into SDK types when a real API call fails

After submitting a Bell-state circuit and waiting for completion, the scripts print
the job id, status, and measured probabilities (expect roughly equal weight on
`|00⟩` and `|11⟩`).

```sh
python examples/downstream_integration.py
python examples/downstream_integration_async.py
```
