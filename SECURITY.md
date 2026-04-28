# Security Policy

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report privately through either channel:

- **GitHub Private Vulnerability Reporting** (preferred): [Report a vulnerability](https://github.com/ionq/ionq-core-python/security/advisories/new). The report is visible only to repository maintainers and people you invite to the advisory.
- **Email**: [security@ionq.co](mailto:security@ionq.co) with the subject line `[ionq-core-python]`.

Please include enough detail to reproduce the issue, and redact your API key from any logs or response payloads you share.

## Response Expectations

- We aim to acknowledge receipt within **3 business days** and follow up with a triage assessment within **10 business days**.
- We follow **coordinated disclosure**. Please do not publicly disclose, share working exploits, or notify third parties until a fix is released and an advisory is published. Our default disclosure window is **90 days** from acknowledgement; we may agree on a shorter or longer timeline depending on severity and where the fix needs to land.
- For confirmed vulnerabilities in this package, we request CVEs through GitHub's CNA via the [repository security advisory](https://docs.github.com/en/code-security/security-advisories) workflow.

## Supported Versions

`ionq-core` is pre-1.0. While the package is in the `0.x` series, **only the latest released minor receives security fixes**. This policy will harden once `1.0` is released.

| Version           | Supported |
| ----------------- | --------- |
| `0.1.x` (latest)  | Yes       |
| Older `0.x`       | No        |

## Scope

This policy covers the source code in this repository and the `ionq-core` distribution published to PyPI from it.

### In scope

- Supply-chain integrity of the published artifact (e.g., compromised release, tampered wheel).
- API-key leakage paths in the SDK (e.g., logging, exception messages, `repr()` output, telemetry).
- Insecure transport defaults (e.g., TLS verification, redirect handling, retry behavior that enables replay).
- Unsafe deserialization, code execution, or SSRF reachable through documented SDK usage.
- CVEs in pinned dependencies that are exploitable through documented SDK usage.

### Out of scope

- Vulnerabilities in IonQ's API, quantum cloud backend, control plane, or QPUs. Still email `security@ionq.co`; we will route them internally.
- Issues that require an attacker to already have arbitrary code execution in the user's Python process or write access to their environment or `IONQ_API_KEY`.
- Findings only reproducible against a forked or locally-modified copy of the SDK.
- Theoretical issues without a working proof-of-concept.

## Credit

We credit reporters in published advisories by default. If you prefer to remain anonymous, please tell us in your report.
