# API Compatibility Testing Guide

## Overview

The compatibility test suite monitors IonQ API response schemas to detect breaking changes that would affect downstream consumers like qiskit-ionq. Tests warn on schema violations but **do not fail CI** - they only alert teams to potential issues.

## Quick Start

### 1. One-Time Setup: Capture Baseline

```bash
cd /Users/far.mckon/dev/ionq/ionq-core-python

# Set API key
export IONQ_API_KEY="your-api-key"

# Capture baseline from current API
python scripts/capture_api_baseline.py \
    --version 1.0.3 \
    --endpoint-user qiskit-ionq

# Output: tests/compatibility_baselines/qiskit_ionq_v1.0.3.json
```

### 2. Run Compatibility Tests

```bash
# Run all compatibility tests
pytest -m compatibility tests/test_compatibility_qiskit_ionq.py -v -s

# Run specific test
pytest -m compatibility tests/test_compatibility_qiskit_ionq.py::TestQiskitIonQCompatibilityV1_0_3::test_job_submission_response_schema -v -s
```

### 3. Interpret Results

**✅ All tests PASS** → No breaking changes detected

**⚠️ Tests SKIP with warnings** → Breaking changes detected:
```
======================================================================
API COMPATIBILITY WARNING
======================================================================
Endpoint User: qiskit-ionq
Version: 1.0.3
Test: test_job_retrieval_response_schema
Issue: Required field 'metadata' missing from response
======================================================================
```

---

## Architecture

### Components

```
ionq-core-python/
├── tests/
│   ├── compatibility_conftest.py              # Decorator & fixtures
│   ├── compatibility_baselines/
│   │   └── qiskit_ionq_v1.0.3.json           # Expected schemas
│   └── test_compatibility_qiskit_ionq.py      # Actual tests
├── scripts/
│   └── capture_api_baseline.py                # Baseline generator
└── pyproject.toml                              # pytest configuration
```

### How It Works

1. **Baseline Capture**: Script queries live API and saves response schemas
2. **Tests Run**: Compare live API responses against baseline
3. **Decorator**: `@warn_team_on_fail` converts failures to warnings
4. **Output**: Warnings print to stdout, tests skip (not fail)

---

## File Descriptions

### 1. `compatibility_conftest.py` - Testing Infrastructure

**Key Components:**

#### `@warn_team_on_fail` Decorator
```python
@warn_team_on_fail
def test_endpoint(self, ...):
    assert "critical_field" in response
    # If fails → prints warning, test skips
```

Behavior:
- Catches `AssertionError`
- Prints formatted warning with version/endpoint_user
- Marks test as SKIPPED (not FAILED)

#### `check_schema_compatibility` Fixture
```python
def test_endpoint(check_schema_compatibility):
    response = api_call()
    check_schema_compatibility("POST /jobs", response, status_code=201)
```

Validates:
- Status codes match baseline
- Required fields present
- Critical fields exist (those qiskit-ionq uses)
- Field types match expectations
- Handles nested fields like `metadata.qiskit_header`

#### `compatibility_baseline` Fixture
```python
@pytest.fixture(scope="session")
def compatibility_baseline():
    """Loads tests/compatibility_baselines/qiskit_ionq_v1.0.3.json"""
```

---

### 2. `capture_api_baseline.py` - Baseline Generator

**What It Does:**
1. Connects to IonQ API
2. Submits test Bell circuit
3. Captures response schemas from 9 endpoints
4. Saves to JSON with metadata (version, git commit, timestamp)
5. Cleans up test job

**Usage:**
```bash
python scripts/capture_api_baseline.py \
    --version 1.0.3 \
    --endpoint-user qiskit-ionq \
    --output custom/path.json  # optional
```

**Output Format:**
```json
{
  "metadata": {
    "version": "1.0.3",
    "endpoint_user": "qiskit-ionq",
    "captured_at": "2026-06-01T10:00:00Z",
    "branch": "main",
    "commit": "abc123def"
  },
  "endpoints": {
    "POST /jobs": {
      "response_schema": { ... },
      "critical_fields": ["id", "status"],
      "notes": "qiskit-ionq requires..."
    },
    ...
  }
}
```

---

### 3. `test_compatibility_qiskit_ionq.py` - Test Suite

**Structure:**
```python
@pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
class TestQiskitIonQCompatibilityV1_0_3:
    """One test per critical endpoint"""

    @warn_team_on_fail
    def test_job_submission_response_schema(self, ...):
        """POST /jobs - validate job creation"""

    @warn_team_on_fail
    def test_job_retrieval_response_schema(self, ...):
        """GET /jobs/{id} - validate job details"""

    # ... 8 more endpoint tests
```

**10 Endpoints Tested:**
1. POST /jobs - Job submission
2. GET /jobs/{id} - Job retrieval
3. GET /jobs/{id}/results/probabilities - Results
4. GET /backends/{backend} - Backend info
5. GET /backends/{backend}/characterizations - Calibration
6. GET /jobs/{id}/circuits/{lang} - Compiled circuit
7. PUT /jobs/{id}/status/cancel - Cancel
8. DELETE /jobs/{id} - Delete
9. GET /jobs/estimate - Cost estimation
10. (Metadata and nested fields)

---

## Usage Patterns

### Pattern 1: On-Demand Testing (Developer)

```bash
# Before making API changes
pytest -m compatibility tests/test_compatibility_qiskit_ionq.py -v -s

# Check if any consumers would break
```

### Pattern 2: Scheduled Monitoring (CI/CD)

```yaml
# .github/workflows/compatibility-check.yml
name: API Compatibility Check
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:      # Manual trigger

jobs:
  compatibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run compatibility tests
        env:
          IONQ_API_KEY: ${{ secrets.IONQ_API_KEY }}
        run: |
          pytest -m compatibility tests/test_compatibility_qiskit_ionq.py -v -s
        continue-on-error: true  # Don't fail workflow, just report
```

### Pattern 3: Pre-Release Validation

```bash
# Before deploying API changes
pytest -m compatibility tests/ -v -s > compatibility_report.txt

# Review warnings
grep "API COMPATIBILITY WARNING" compatibility_report.txt

# Notify affected teams if warnings found
```

### Pattern 4: Multiple Consumer Versions

```bash
# Add tests for different versions
python scripts/capture_api_baseline.py --version 2.0.0 --endpoint-user qiskit-ionq
python scripts/capture_api_baseline.py --version 1.5.0 --endpoint-user cirq-ionq

# Test all versions
pytest -m compatibility tests/test_compatibility_*.py -v
```

---

## Adding Tests for New Consumers

### Step 1: Capture Baseline

```bash
python scripts/capture_api_baseline.py \
    --version 0.5.0 \
    --endpoint-user cirq-ionq
```

### Step 2: Create Test File

```python
# tests/test_compatibility_cirq_ionq.py

@pytest.mark.compatibility(version="0.5.0", endpoint_user="cirq-ionq")
class TestCirqIonQCompatibilityV0_5_0:

    @warn_team_on_fail
    def test_job_submission(self, client, check_schema_compatibility):
        """Test critical fields for cirq-ionq"""
        # ... similar to qiskit-ionq tests
```

### Step 3: Document Critical Fields

In baseline JSON, note which fields cirq-ionq relies on:
```json
{
  "critical_fields": ["job_id", "state"],
  "notes": "cirq-ionq uses 'job_id' not 'id'"
}
```

---

## Configuration

### pytest.ini / pyproject.toml

```toml
[tool.pytest.ini_options]
markers = [
    "compatibility: API compatibility monitoring tests",
]
addopts = "-m 'not integration and not compatibility'"  # Skip by default
```

### Running Only Compatibility Tests

```bash
# Explicit selection
pytest -m compatibility

# Exclude from normal runs
pytest  # compatibility tests skipped automatically
```

---

## Maintenance

### Updating Baselines

When API changes intentionally and consumer updated:

```bash
# 1. Capture new baseline
python scripts/capture_api_baseline.py \
    --version 1.0.4 \
    --endpoint-user qiskit-ionq

# 2. Update test marker
# Edit tests/test_compatibility_qiskit_ionq.py:
@pytest.mark.compatibility(version="1.0.4", endpoint_user="qiskit-ionq")

# 3. Commit both files
git add tests/compatibility_baselines/qiskit_ionq_v1.0.4.json
git add tests/test_compatibility_qiskit_ionq.py
git commit -m "Update qiskit-ionq compatibility baseline to v1.0.4"
```

### Archiving Old Versions

```python
# Keep for historical reference
@pytest.mark.skip(reason="qiskit-ionq 1.0.3 deprecated")
@pytest.mark.compatibility(version="1.0.3", endpoint_user="qiskit-ionq")
class TestQiskitIonQCompatibilityV1_0_3:
    ...
```

---

## Troubleshooting

### Issue: "Baseline file not found"

**Solution:** Run baseline capture
```bash
python scripts/capture_api_baseline.py --version 1.0.3 --endpoint-user qiskit-ionq
```

### Issue: "IONQ_API_KEY not set"

**Solution:** Set environment variable
```bash
export IONQ_API_KEY="your-api-key"
```

### Issue: Tests fail (not skip)

**Possible causes:**
- Test code has syntax error
- Import error (missing dependency)
- Decorator not applied

**Not expected:** Tests should SKIP with warning, not FAIL

### Issue: No warnings when expected

**Check:**
1. Decorator applied: `@warn_team_on_fail`
2. Running with `-s` flag to show stdout
3. Baseline file exists and is loaded

### Issue: "No completed jobs available"

**Solution:** Normal for `test_completed_job_results_schema`
- Test will skip if no completed jobs
- Or wait for previous job to complete

---

## Best Practices

### 1. Capture Baselines from Stable API

- Run from `main` branch
- After API is deployed
- Before announcing version to consumers

### 2. Run Tests Regularly

- **Weekly:** Detect drift early
- **Before releases:** Validate no breaking changes
- **After incidents:** Verify API restored correctly

### 3. Review Warnings Promptly

When warnings appear:
1. Identify affected consumer version
2. Check if consumer needs updating
3. Coordinate with consumer team
4. Document breaking change

### 4. Version Baselines Carefully

- One baseline per consumer version
- Include git commit in metadata
- Archive old baselines (don't delete)

### 5. Document Critical Fields

In baseline JSON, explain why fields are critical:
```json
{
  "critical_fields": ["metadata.qiskit_header"],
  "notes": "qiskit-ionq uses metadata.qiskit_header for circuit reconstruction. Removing this breaks job.result()."
}
```

---

## Examples

### Example 1: Detect Breaking Change

```bash
# API removes 'metadata' field from job response
pytest -m compatibility tests/test_compatibility_qiskit_ionq.py -v -s

# Output:
======================================================================
API COMPATIBILITY WARNING
======================================================================
Endpoint User: qiskit-ionq
Version: 1.0.3
Test: test_job_retrieval_response_schema
Issue: Required field 'metadata' missing from response
======================================================================

# Action: Alert qiskit-ionq team before deploying
```

### Example 2: Add New Consumer

```bash
# New consumer: pennylane-ionq v0.1.0

# 1. Capture baseline
python scripts/capture_api_baseline.py \
    --version 0.1.0 \
    --endpoint-user pennylane-ionq

# 2. Create test file
cat > tests/test_compatibility_pennylane_ionq.py << 'EOF'
@pytest.mark.compatibility(version="0.1.0", endpoint_user="pennylane-ionq")
class TestPennylaneIonQCompatibilityV0_1_0:
    @warn_team_on_fail
    def test_job_submission(self, ...):
        ...
EOF

# 3. Run tests
pytest -m compatibility tests/test_compatibility_pennylane_ionq.py -v -s
```

### Example 3: CI Integration

```yaml
# Slack notification on breaking changes
- name: Check compatibility
  run: |
    OUTPUT=$(pytest -m compatibility tests/ -v -s 2>&1)
    echo "$OUTPUT"

    if echo "$OUTPUT" | grep -q "API COMPATIBILITY WARNING"; then
      curl -X POST $SLACK_WEBHOOK \
        -d "{\"text\":\"⚠️ API Breaking Changes Detected\n\`\`\`$OUTPUT\`\`\`\"}"
    fi
```

---

## Summary

**What This System Provides:**
- ✅ Early warning of breaking API changes
- ✅ Consumer-specific compatibility monitoring
- ✅ Non-blocking warnings (tests don't fail CI)
- ✅ Detailed context (version, endpoint, field)
- ✅ Versioned baselines for historical tracking

**When to Use:**
- 🔄 Regular monitoring (weekly/monthly)
- 🚀 Before API releases
- 🛠️ During API development
- 📊 Consumer impact analysis

**Who Benefits:**
- **API Team:** Catch breaking changes before deployment
- **Consumer Teams:** Early notification of incompatibilities
- **QA:** Validate backward compatibility
- **Product:** Coordinate releases across teams

---

## Support

For questions or issues:
1. Check phase-specific guides: `PHASE1_TESTING.md`, `PHASE2_BASELINE_CAPTURE.md`, `PHASE3_COMPATIBILITY_TESTS.md`
2. Review this README
3. Contact IonQ API team
