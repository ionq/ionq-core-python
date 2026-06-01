#!/usr/bin/env python3
"""
Capture API baseline for compatibility testing.

Runs against the current IonQ API on 'main' branch to establish
expected response schemas for compatibility monitoring.

Usage:
    export IONQ_API_KEY="your-api-key"
    python scripts/capture_api_baseline.py --version 1.0.3 --endpoint-user qiskit-ionq
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

# Add parent directory to path to import ionq_core
sys.path.insert(0, str(Path(__file__).parent.parent))

from ionq_core import IonQClient
from ionq_core.api.backends import get_backend
from ionq_core.api.characterizations import get_characterizations_for_backend
from ionq_core.api.default import (
    create_job,
    delete_job,
    get_job,
)
from ionq_core.models.circuit_job_creation_payload import CircuitJobCreationPayload


def get_git_info():
    """Get current git branch and commit."""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
            cwd=Path(__file__).parent.parent
        ).strip()
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            cwd=Path(__file__).parent.parent
        ).strip()
        return branch, commit
    except subprocess.CalledProcessError:
        return "unknown", "unknown"


def capture_job_submission_baseline(client):
    """Capture POST /jobs baseline."""
    print("  Creating test job...")
    test_circuit = {
        "type": "ionq.circuit.v1",
        "backend": "simulator",
        "shots": 100,
        "input": {
            "gateset": "qis",
            "qubits": 2,
            "circuit": [
                {"gate": "h", "target": 0},
                {"gate": "cnot", "control": 0, "target": 1},
            ],
        },
    }

    body = CircuitJobCreationPayload.from_dict(test_circuit)
    resp = create_job.sync_detailed(client=client, body=body)

    response_dict = resp.parsed.to_dict()

    return {
        "request_example": test_circuit,
        "response_schema": {
            "status_code": resp.status_code.value,
            "required_fields": list(response_dict.keys()),
            "field_types": {
                k: type(v).__name__ if v is not None else "NoneType"
                for k, v in response_dict.items()
            }
        },
        "critical_fields": ["id", "status"],
        "notes": "qiskit-ionq requires 'id' to track job, 'status' for state machine",
    }, resp.parsed.id


def capture_job_retrieval_baseline(client, job_id):
    """Capture GET /jobs/{job_id} baseline."""
    print(f"  Retrieving job {job_id}...")
    job = get_job.sync(uuid=job_id, client=client)
    job_dict = job.to_dict()

    # Extract nested field keys
    results_keys = list(job_dict.get("results", {}).keys()) if job_dict.get("results") else []
    metadata_keys = list(job_dict.get("metadata", {}).keys()) if job_dict.get("metadata") else []

    return {
        "response_schema": {
            "status_code": 200,
            "required_fields": list(job_dict.keys()),
            "nested_fields": {
                "results": results_keys,
                "metadata": metadata_keys,
            },
            "field_types": {
                k: type(v).__name__ if v is not None else "NoneType"
                for k, v in job_dict.items()
            }
        },
        "critical_fields": ["id", "status", "results", "metadata"],
        "notes": "qiskit-ionq parses metadata for circuit reconstruction",
    }


def capture_backend_baseline(client):
    """Capture GET /backends/{backend} baseline."""
    print("  Getting backend info...")
    backend = get_backend.sync("simulator", client=client)
    backend_dict = backend.to_dict()

    return {
        "response_schema": {
            "status_code": 200,
            "required_fields": list(backend_dict.keys()),
            "field_types": {
                k: type(v).__name__ if v is not None else "NoneType"
                for k, v in backend_dict.items()
            }
        },
        "critical_fields": ["qubits"],
        "notes": "qiskit-ionq uses for get_n_qubits() helper",
    }


def capture_characterization_baseline(client):
    """Capture GET /backends/{backend}/characterizations baseline."""
    print("  Getting characterization data...")
    try:
        resp = get_characterizations_for_backend.sync("qpu.forte-1", client=client, limit=1)
        if resp and resp.characterizations:
            char = resp.characterizations[0].to_dict()
            return {
                "response_schema": {
                    "status_code": 200,
                    "required_fields": ["characterizations"],
                    "nested_fields": {
                        "characterizations[]": list(char.keys())
                    }
                },
                "critical_fields": [
                    "characterizations[].qubits",
                    "characterizations[].connectivity"
                ],
                "notes": "qiskit-ionq uses for backend.calibration() method",
            }
    except Exception as e:
        print(f"    Warning: Could not capture characterization baseline: {e}")

    # Fallback minimal schema
    return {
        "response_schema": {
            "status_code": 200,
            "required_fields": ["characterizations"],
        },
        "critical_fields": [],
        "notes": "Baseline capture failed - using minimal schema",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Capture API baseline for compatibility testing"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Version to capture baseline for (e.g., 1.0.3)"
    )
    parser.add_argument(
        "--endpoint-user",
        required=True,
        help="Endpoint user name (e.g., qiskit-ionq)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: tests/compatibility_baselines/{endpoint_user}_v{version}.json)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("IONQ_API_KEY")
    if not api_key:
        print("Error: IONQ_API_KEY environment variable not set")
        print("Set it with: export IONQ_API_KEY='your-api-key'")
        return 1

    client = IonQClient(api_key=api_key)

    # Get git info
    branch, commit = get_git_info()

    print(f"\n{'='*70}")
    print(f"Capturing API Baseline")
    print(f"{'='*70}")
    print(f"Endpoint User: {args.endpoint_user}")
    print(f"Version: {args.version}")
    print(f"Git Branch: {branch}")
    print(f"Git Commit: {commit[:8]}")
    print(f"{'='*70}\n")

    # Initialize baseline structure
    baseline = {
        "metadata": {
            "version": args.version,
            "endpoint_user": args.endpoint_user,
            "captured_at": datetime.datetime.utcnow().isoformat() + "Z",
            "api_version": "v0.4",
            "branch": branch,
            "commit": commit,
        },
        "endpoints": {}
    }

    test_job_id = None

    try:
        # 1. POST /jobs
        print("1. Capturing POST /jobs...")
        job_baseline, test_job_id = capture_job_submission_baseline(client)
        baseline["endpoints"]["POST /jobs"] = job_baseline

        # 2. GET /jobs/{job_id}
        print("2. Capturing GET /jobs/{job_id}...")
        baseline["endpoints"]["GET /jobs/{job_id}"] = capture_job_retrieval_baseline(
            client, test_job_id
        )

        # 3. GET /backends/{backend}
        print("3. Capturing GET /backends/{backend}...")
        baseline["endpoints"]["GET /backends/{backend}"] = capture_backend_baseline(client)

        # 4. GET /backends/{backend}/characterizations
        print("4. Capturing GET /backends/{backend}/characterizations...")
        baseline["endpoints"]["GET /backends/{backend}/characterizations"] = (
            capture_characterization_baseline(client)
        )

        # 5. Add remaining endpoints with manual schemas (no live capture needed)
        print("5. Adding manual schemas for remaining endpoints...")

        baseline["endpoints"]["GET /jobs/{job_id}/results/probabilities"] = {
            "response_schema": {
                "status_code": 200,
                "response_type": "object",
                "value_constraints": {"all_values": "float", "range": [0.0, 1.0]}
            },
            "critical_fields": ["*"],
            "notes": "qiskit-ionq expects dict[str, float] with keys as bitstrings"
        }

        baseline["endpoints"]["GET /jobs/{job_id}/circuits/{lang}"] = {
            "response_schema": {
                "status_code": 200,
                "response_type": "string",
            },
            "critical_fields": None,
            "notes": "qiskit-ionq.compiled_circuit() returns this directly"
        }

        baseline["endpoints"]["PUT /jobs/{job_id}/status/cancel"] = {
            "response_schema": {"status_code": 200, "required_fields": ["id", "status"]},
            "critical_fields": ["status"],
            "notes": "qiskit-ionq checks status after cancel"
        }

        baseline["endpoints"]["DELETE /jobs/{job_id}"] = {
            "response_schema": {"status_code": 200, "required_fields": ["id"]},
            "critical_fields": ["id"],
            "notes": "qiskit-ionq verifies deletion by ID"
        }

        baseline["endpoints"]["GET /jobs/estimate"] = {
            "response_schema": {
                "status_code": 200,
                "required_fields": ["estimated_cost", "cost_unit", "estimated_execution_time"]
            },
            "critical_fields": ["estimated_cost", "estimated_execution_time"],
            "notes": "qiskit-ionq displays cost estimates to users"
        }

    finally:
        # Cleanup: Delete test job
        if test_job_id:
            try:
                print(f"\nCleaning up: Deleting test job {test_job_id}...")
                delete_job.sync(uuid=test_job_id, client=client)
            except Exception as e:
                print(f"  Warning: Could not delete test job: {e}")

    # Save baseline
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = (
            Path(__file__).parent.parent
            / "tests"
            / "compatibility_baselines"
            / f"{args.endpoint_user}_v{args.version}.json"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(baseline, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✅ Baseline Saved")
    print(f"{'='*70}")
    print(f"Location: {output_path}")
    print(f"Endpoints Captured: {len(baseline['endpoints'])}")
    print(f"{'='*70}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
