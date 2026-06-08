# Examples

Runnable, copy-pasteable scripts that exercise `ionq-core` end to end against
the free `simulator` backend.

## Setup

```sh
source .venv/bin/activate # Run in project root directory
pip install ionq-core     # To ensure latest version
export IONQ_API_KEY=...   # Create a key at https://identity.ionq.com/create-account
```

## Scripts

| Script | What it shows |
| --- | --- |
| [`downstream_integration.py`](downstream_integration.py) | Synchronous downstream-SDK integration via the [extension API](https://ionq.github.io/ionq-core-python/ionq_core/extensions.html): a `ClientExtension` with a `user_agent_token`, `default_headers`, an `EventHook`, and an `error_mapper`, then a Bell-state job submitted, polled, and read back. |
| [`downstream_integration_async.py`](downstream_integration_async.py) | The same flow on the async path with an `AsyncEventHook` and the `asyncio` endpoint variants. |

Run either with:

```sh
python examples/downstream_integration.py
python examples/downstream_integration_async.py
```

Each prints the per-request hook log lines and the measured Bell-state
probabilities.
