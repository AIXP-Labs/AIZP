# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the AIZP protocol specification or reference artifacts, please report it responsibly through GitHub's private security advisory channel:

**[Report a vulnerability on GitHub](https://github.com/AIXP-Labs/AIZP/security/advisories/new)**

This keeps the report private until a fix is released and coordinated disclosure is complete.

Please include:

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact assessment
- Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Resolution Plan**: Within 14 days

## Scope

This security policy covers:

- The AIZP protocol specification (`specification/AIZP_Protocol.md`)
- The canonical enum registry (`specification/registry.md`)
- The AIZP proto definition (`specification/proto/aizp.proto`)
- The JSON Schemas (`schemas/`) and examples (`examples/`)
- Official documentation in `docs/` and `docs_cn/`

## Out of Scope (by design)

AIZP is a **runtime safety layer**, not a complete solution. The following are documented honest limits, not vulnerabilities:

- Reward hacking as a structural equilibrium — see [docs/Reward-Hacking-Limits.md](docs/Reward-Hacking-Limits.md).
- Out-of-band actions that bypass AIZP's observation path — see [docs/Reward-Hacking-Limits.md](docs/Reward-Hacking-Limits.md) §10.
- Threats AIZP explicitly does not defend against — see [docs/Threat-Model.md](docs/Threat-Model.md) §1.

## Coordinated Disclosure

We follow a coordinated disclosure process. Please do not publicly disclose vulnerabilities until a fix has been released and announced.

---

Align Axiom 0: Human Sovereignty and Wellbeing. AIZP V0.6. www.aizp.dev
