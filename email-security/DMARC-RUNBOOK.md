# DMARC Implementation Runbook — Google Workspace

## Overview
This runbook documents the step-by-step process for implementing DMARC
across a Google Workspace organization, hardening email authentication
from monitoring-only through full enforcement. It also covers anti-phishing
controls and phishing simulation program design.

---

## Phase 1: Monitor (p=none) — Weeks 1-2

### Goal
Collect data on who is sending email on behalf of your domain without
blocking or filtering anything. This phase is required — skipping directly
to p=reject will block legitimate email and cause an outage.

### Steps
1. Add DMARC TXT record to DNS:
   - Record name: _dmarc.yourdomain.com
   - Record value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
   - TTL: 3600

2. Enable Google Postmaster Tools:
   - Go to postmaster.google.com
   - Add and verify your domain
   - Monitor: Domain Reputation, SPF/DKIM compliance rates, delivery errors

3. Review daily aggregate reports (rua) for 2 weeks:
   - Identify all legitimate sending sources (CRM, marketing tools, HR systems)
   - Ensure each source has valid SPF and DKIM configured
   - Document all sources in a sender inventory

### Success Criteria
- All legitimate senders identified and documented
- SPF and DKIM passing rate > 95% for known senders
- No unexpected sending sources found

---

## Phase 2: Quarantine (p=quarantine) — Weeks 3-4

### Goal
Begin enforcing DMARC by sending failing emails to spam rather than
the inbox. Start at 25% to limit blast radius if legitimate mail is
accidentally caught.

### Steps
1. Update DMARC record:
   - Record value: v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@yourdomain.com
   - pct=25 means policy applies to 25% of failing messages only

2. Verify all legitimate senders have valid SPF and DKIM:
   - Run email_auth_audit.py against all sending domains
   - Fix any WARN or FAIL results before increasing pct

3. Monitor for 1 week then increase coverage:
   - Update pct=50, monitor for 3 days
   - Update pct=100, monitor for 3 days
   - Watch Postmaster Tools for any spike in legitimate mail failures

### Success Criteria
- No legitimate mail going to spam at pct=100
- Rejection rate for unauthorized senders increasing
- Zero complaints from internal teams about missing email

---

## Phase 3: Enforce (p=reject) — Week 5+

### Goal
Fully enforce DMARC — unauthorized emails are blocked outright and
never delivered. This is the gold standard configuration.

### Steps
1. Update DMARC record:
   - Record value: v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com

2. Monitor rejection rates in Postmaster Tools:
   - Alert on any spike in legitimate mail failures
   - Review aggregate reports weekly for the first month
   - Review monthly ongoing

3. Set up alerting:
   - Alert if SPF/DKIM compliance rate drops below 95%
   - Alert if domain reputation drops in Postmaster Tools

### Success Criteria
- p=reject active with no legitimate mail blocked
- Unauthorized spoofing attempts visible in aggregate reports and blocked
- Domain reputation HIGH in Google Postmaster Tools

---

## Anti-Phishing Controls in Google Workspace

### Admin Console Configuration
Path: Admin Console → Apps → Google Workspace → Gmail → Safety

### Enable the following controls:

| Setting | Purpose | Recommended Action |
| ------- | ------- | ------------------ |
| Enhanced pre-delivery message scanning | Scans links and attachments before delivery | Enable |
| Attachments with scripts from untrusted senders | Blocks macro-enabled docs from unknown senders | Quarantine |
| Anomalous attachment protection | Flags unusual attachment types | Enable |
| Unauthenticated email | Email failing SPF/DKIM | Quarantine |
| Spoofing of employee names | Display name spoofing protection | Enable |
| Intra-domain spoofing | Protects against internal domain spoofing | Enable |

---

## Phishing Simulation Program (GoPhish)

### Overview
GoPhish is a free open-source phishing simulation platform. Running
regular simulations measures employee susceptibility and feeds the
security awareness training program.

### Setup
1. Download GoPhish from github.com/gophish/gophish (free, open source)
2. Run locally: ./gophish (default admin port 3333)
3. Configure sending profile with test SMTP credentials
4. Access admin UI at https://localhost:3333

### Campaign Design
- Templates: mimic internal IT alerts, HR notices, vendor invoices, package delivery
- Targets: import from directory — start with 10% of org per campaign
- Schedule: quarterly campaigns minimum, monthly for high-risk teams (finance, HR, exec)

### Metrics to Track Monthly

| Metric | Baseline Target | Mature Target |
| ------ | -------------- | ------------- |
| Click rate | < 20% | < 5% |
| Credential submission rate | < 10% | < 1% |
| Report rate | > 10% | > 40% |
| Repeat clickers | < 5% | 0% |

### Awareness Program Feedback Loop
- Users who click: immediate 2-minute micro-training module
- Users who submit credentials: mandatory 30-minute training + manager notification
- Campaign results feed quarterly awareness training curriculum
- Metrics reported to CISO and board quarterly
- Annual trend report showing improvement over time

### Reporting Template
| Quarter | Click Rate | Report Rate | Repeat Clickers | Training Completions |
| ------- | ---------- | ----------- | --------------- | -------------------- |
| Q1 2026 | % | % | % | % |
| Q2 2026 | % | % | % | % |
| Q3 2026 | % | % | % | % |
| Q4 2026 | % | % | % | % |

