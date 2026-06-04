# Examples

These examples show direct `ionq-core` usage close to the IonQ REST API.

## Downstream SDK Integration

`downstream_integration.py` and `downstream_integration_async.py` demonstrate
how a higher-level SDK can wrap `ionq-core` with the extension API while still
using the generated endpoint modules for job submission and result retrieval.

The examples configure:

- a downstream SDK `User-Agent` token
- SDK-specific default headers
- sync or async HTTP event hooks for request, response, and error logging
- an error mapper that wraps `APIError` and `RateLimitError` into an
  SDK-defined exception type

Install and run the sync example:

```sh
pip install ionq-core
export IONQ_API_KEY=your-api-key
python examples/downstream_integration.py
```

Run the async example:

```sh
python examples/downstream_integration_async.py
```

On Windows PowerShell, set the API key with:

```powershell
$env:IONQ_API_KEY = "your-api-key"
python examples/downstream_integration.py
python examples/downstream_integration_async.py
```

Both scripts submit a Bell-state circuit to the free `simulator`, wait for the
job to complete, and print the returned probabilities.
