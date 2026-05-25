# Endpoint Hardening Findings

## Baseline Source
osquery v5.x — local machine audit

## Results

| Control | osquery Result | Actual Status | Notes |
| ------- | -------------- | ------------- | ----- |
| SIP | PASS (sip:1) | PASS | Confirmed enabled |
| FileVault | FAIL (0) | PASS | osquery false negative on macOS — verified via fdesetup status |
| Firewall | FAIL (0) | REMEDIATED | Was disabled — enabled via socketfilterfw |
| EDR | No results | FAIL | No CrowdStrike Falcon or equivalent detected |

## Remediation Performed
- Firewall was found disabled during audit and has since been enabled
- Verified via: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
- Firewall is now active and confirmed running

## Known Issues & Investigation Items
- **FileVault false positive**: osquery reported FileVault as disabled (0) however
  fdesetup status confirms FileVault is enabled on this device. This appears to be
  an osquery compatibility issue with the current macOS version. Requires further
  investigation into why the disk_encryption table is returning incorrect values —
  possible causes include macOS version incompatibility, osquery build mismatch,
  or APFS volume reporting differences. Native fdesetup command should be used
  as the authoritative source until resolved.

## Tooling Note
osquery disk_encryption table has known accuracy issues on newer
macOS versions. Always cross-reference with native OS commands
(fdesetup, socketfilterfw) for production fleet audits.

## Outstanding Gaps
- EDR agent not installed (HIGH risk)
- Remediation: deploy CrowdStrike Falcon via Kandji/Intune
