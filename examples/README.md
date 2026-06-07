# IonQ Core Examples

This directory contains runnable examples for building downstream SDK integrations on top of `ionq-core`.
The examples submit a Bell-state circuit to the free `simulator` backend, wait for completion, and print
the result probabilities.

## Setup

Install the package:

```sh
pip install ionq-core
```

Create an IonQ Cloud account at <https://identity.ionq.com/create-account>, then export your API key:

```sh
export IONQ_API_KEY="your-api-key"
```

## Downstream SDK Integration

Run the sync example:

```sh
python examples/downstream_integration.py
```

Run the async example:

```sh
python examples/downstream_integration_async.py
```

Both examples demonstrate how a downstream SDK can pass a `ClientExtension` to `IonQClient` to customize
client behavior without modifying `ionq-core`:

- `user_agent_token` identifies the downstream SDK in the `User-Agent` header.
- `default_headers` adds SDK-specific request headers.
- `EventHook` and `AsyncEventHook` observe request and response activity.
- `error_mapper` wraps `ionq-core` exceptions in SDK-defined exception types.
