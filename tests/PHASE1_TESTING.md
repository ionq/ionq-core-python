# Phase 1: Testing the Decorator

## What We've Created

1. **`compatibility_conftest.py`** - Core decorator and fixtures
   - `@warn_team_on_fail` decorator
   - `compatibility_baseline` fixture (loads JSON)
   - `check_schema_compatibility` fixture (validates schemas)
   - Pytest hooks for marker injection

2. **`test_compatibility_decorator.py`** - Tests to verify decorator works
   - Passing tests work normally
   - Failing tests print warnings and skip
   - Version/endpoint_user extracted from marker

3. **`pyproject.toml`** - Updated configuration
   - Added `compatibility` marker
   - Excluded compatibility tests by default
   - Added CompatibilityWarning to filterwarnings

## Testing Instructions

### Step 1: Verify Decorator Behavior

Run the decorator tests to see warnings in action:

```bash
cd /Users/far.mckon/dev/ionq/ionq-core-python

# Run compatibility tests with verbose output
pytest -m compatibility tests/test_compatibility_decorator.py -v -s

# Expected output:
# - test_passing_test_unchanged: PASSED (no warning)
# - test_failing_test_warns_and_skips: SKIPPED (prints warning)
# - test_missing_field_warns: SKIPPED (prints warning)
# - test_type_mismatch_warns: SKIPPED (prints warning)
```

### Step 2: Verify Warning Format

Look for output like:

```
======================================================================
API COMPATIBILITY WARNING
======================================================================
Endpoint User: qiskit-ionq
Version: 1.0.3
Test: test_failing_test_warns_and_skips
Issue: This is a test breaking change
======================================================================
```

### Step 3: Verify Default Behavior

Confirm compatibility tests are skipped by default:

```bash
# Run all tests without -m flag
pytest tests/test_compatibility_decorator.py -v

# Should output:
# "SKIPPED [5] pyproject.toml:103: Skipped: not in the list of explicitly selected markers"
```

### Step 4: Verify Normal Tests Unaffected

```bash
# Run the non-decorated test
pytest tests/test_compatibility_decorator.py::test_without_decorator -v

# Should PASS normally
```

## Expected Results

✅ **Success Criteria:**
1. Passing tests with decorator work normally
2. Failing tests with decorator print warnings and skip
3. Warning message includes version and endpoint_user
4. Compatibility tests excluded from default test run
5. Regular tests without decorator unaffected

❌ **Failure Cases to Watch For:**
- Decorator causes passing tests to fail
- Warnings not printed to stdout
- Version/endpoint_user not extracted from marker
- Regular tests affected by decorator

## Troubleshooting

### "No module named 'compatibility_conftest'"

Make sure you're running from the repository root:
```bash
cd /Users/far.mckon/dev/ionq/ionq-core-python
```

### Warnings not showing

Add `-s` flag to show stdout:
```bash
pytest -m compatibility tests/test_compatibility_decorator.py -v -s
```

### Import errors

Install dev dependencies:
```bash
pip install -e .[dev]
# or with Poetry
poetry install
```

## Next Steps

Once Phase 1 tests pass, we'll move to:

**Phase 2: Baseline Capture**
- Create `scripts/capture_api_baseline.py`
- Run against live API to capture schemas
- Generate `tests/compatibility_baselines/qiskit_ionq_v1.0.3.json`

Let me know when Phase 1 tests are working!
