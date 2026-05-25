# Endpoint Hardening Policy

## Scope: macOS Corporate Fleet (Managed via Kandji/Intune)

| Control | CIS Benchmark Ref | Enforcement Method | Pass Criteria | Risk if Failing |
| ------- | ----------------- | ------------------ | ------------- | --------------- |
| SIP enabled | CIS macOS 3.1 | Kandji profile | config_flag=1 | HIGH — core OS protections disabled |
| FileVault enabled | CIS macOS 2.6.1 | Kandji profile | encrypted=1 | HIGH — data readable if device lost/stolen |
| Firewall enabled | CIS macOS 2.5.2 | Intune policy | global_state=1 | MEDIUM — unsolicited inbound connections allowed |
| Screen lock <= 5min | CIS macOS 2.11.2 | Intune compliance | delay<=300s | MEDIUM — unattended device accessible |
| Gatekeeper enabled | CIS macOS 2.7.1 | Kandji profile | enabled=1 | HIGH — unsigned/untrusted apps can execute |
| EDR agent installed | Internal policy | Kandji app install | app present | HIGH — no endpoint detection or response capability |

## Verification Method
All controls verified via osquery fleet queries run against managed devices.
Cross-reference with native OS commands where osquery results are inconsistent
(e.g. fdesetup for FileVault, socketfilterfw for firewall).

## Known Exceptions
- FileVault: osquery disk_encryption table returns false negatives on newer
  macOS versions. Authoritative source is fdesetup status until resolved.

## Remediation SLA
| Risk Level | Remediation Window |
| ---------- | ------------------ |
| HIGH | 24 hours |
| MEDIUM | 7 days |
| LOW | 30 days |

## References
- CIS Apple macOS Benchmark: https://www.cisecurity.org/benchmark/apple_os
- Kandji MDM Documentation: https://support.kandji.io
- Microsoft Intune macOS: https://learn.microsoft.com/en-us/mem/intune
