# Security Policy

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Email [security@ionq.co](mailto:security@ionq.co) with the subject line `[ionq-core-python]`.

Please include enough detail to reproduce the issue, and redact your API key from any logs or response payloads you share.

## Response Expectations

- We aim to acknowledge receipt within **3 business days** and follow up with a triage assessment within **10 business days**.
- We follow **coordinated disclosure**. Please do not publicly disclose, share working exploits, or notify third parties until a fix is released and an advisory is published. Our default disclosure window is **90 days** from acknowledgement; we may agree on a shorter or longer timeline depending on severity and where the fix needs to land.
- For confirmed vulnerabilities in this package, we request CVEs through GitHub's CNA via the [repository security advisory](https://docs.github.com/en/code-security/security-advisories) workflow.

## Safe Harbor

When conducting security research consistent with this policy, we consider your research to be authorized and lawful. Specifically:

- We will not initiate or support legal action against you for accidental, good-faith violations of this policy under applicable anti-hacking laws (such as the U.S. Computer Fraud and Abuse Act).
- We will not bring a claim against you for circumvention of technical controls under relevant anti-circumvention laws (such as DMCA section 1201).
- If a third party initiates legal action against you for activities conducted in good-faith compliance with this policy, we will take steps to make it known that your actions were authorized.

In return, we ask that you comply with all applicable laws, make reasonable efforts to avoid privacy violations, service disruption, and destruction of data, limit testing to your own account or accounts you control, and use the channels above to discuss vulnerabilities with us.

If you are unsure whether a planned activity is consistent with this policy, contact <security@ionq.co> before proceeding. Safe harbor applies only to claims within IonQ's control; this policy does not bind independent third parties.

## Supported Versions

`ionq-core` is pre-1.0. While the package is in the `0.x` series, **only the latest released minor receives security fixes**. This policy will harden once `1.0` is released.

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
