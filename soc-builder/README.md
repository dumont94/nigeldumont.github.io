# SOC Foundations Builder — Your First 90 Days

A portfolio project by Nigel Dumont.

A web application that thinks like a SOC engineer walking into a new company as the first (or only) security hire. Answer four questions about the environment and the tool produces a 10-step, first-90-days plan for monitoring and securing it — what to check on day one, which tools to deploy, what they cost, alternatives and trade-offs, and how to stand each one up.

**Live tool:** [dumont94.github.io/nigeldumont.github.io/soc-builder/app/](https://dumont94.github.io/nigeldumont.github.io/soc-builder/app/)
**Live portfolio:** [nigeldumont.github.io](https://dumont94.github.io/nigeldumont.github.io/)

Companion piece to the [Network Infrastructure Builder](../network-builder/) — same design system, same questionnaire → walkthrough → summary flow, applied to security operations instead of network hardware.

---

## What It Does

1. User answers four questions (environment, company size, current security state, budget posture).
2. The routing logic picks one of three SOC build paths:
   - **Microsoft-Native SOC** — Defender XDR + Sentinel; squeeze the licensing you already pay for (≈ $25k–60k Year 1 @ 100 users)
   - **Open-Source / Lean SOC** — Wazuh, Security Onion, Greenbone, TheHive, free CISA services (≈ $4k–12k Year 1)
   - **Best-of-Breed SOC** — CrowdStrike, Splunk, Tenable, Proofpoint, Okta (≈ $70k–140k Year 1 @ 100 users)
3. The walkthrough covers 10 steps in first-90-days priority order:
   Asset & Identity Inventory → Crown Jewels & Attack Surface → Identity Security & MFA → EDR → Centralized Logging & SIEM → Email Security → Vulnerability Management → Network Visibility → Detections, Alerting & Triage → Incident Response & Resilience.
4. Each step shows: what it is, why it matters, **what a SOC engineer looks for on day one**, recommended tooling with pricing, alternatives and trade-offs, licensing/care-and-feeding notes, and implementation steps.
5. The summary screen shows the full security stack, a SOC telemetry-flow diagram, and vendor links for current pricing.

---

## Architecture

```
soc-builder/
├── app/                    Committed static build (served by GitHub Pages)
└── frontend/
    ├── index.html
    ├── package.json        Vite + React 18
    ├── vite.config.js      base: /nigeldumont.github.io/soc-builder/app/
    └── src/
        ├── App.jsx             State machine: questionnaire → loading → walkthrough → summary
        ├── App.css             Single stylesheet, CSS custom properties, dark default
        ├── socData.json        All path/step/product/pricing data (3 paths × 10 steps)
        ├── recommendations.js  Routing logic: answers → path → steps
        └── components/
            ├── Questionnaire.jsx   Four questions, selectable card UI
            ├── Walkthrough.jsx     Step sidebar + step card + prev/next nav
            ├── StepCard.jsx        Color-coded sections incl. day-one look-fors
            ├── CoverageMap.jsx     Path-specific ASCII telemetry-flow diagram
            ├── ProgressBar.jsx     Step progress indicator
            └── Summary.jsx         Full stack table, costs, vendor sources
```

**Design decisions:**

- **Environment routes before budget** — a Microsoft 365 shop should exhaust Business Premium/E5 licensing before buying anything, regardless of budget. Only non-Microsoft environments split on lean vs. funded.
- **Coverage philosophy: visibility before shiny tools** — every path covers the same ten domains. There is no "skip monitoring" option; budget determines *which tools* do the work, never whether a domain gets covered. This mirrors the Network Builder's "security is always enterprise-grade" stance.
- **A "day one look-fors" section per step** — the thing that distinguishes a SOC engineer from a tool installer is knowing what to check before deploying anything (stale admins, p=none DMARC, firewall logs going nowhere, backups that were never restore-tested).
- **All data in `socData.json`, not a backend** — the tool runs as a pure static site; the recommendation data is structured, editable, and reviewable in one file.
- **Dark mode by default** — analysts live in dark dashboards. Light mode is one click away.
- **Honest pricing and honest trade-offs** — open-source paths call out the engineering-time cost; commercial paths call out negotiation realities and vendor lock-in.

---

## Running Locally

```bash
cd soc-builder/frontend
npm install
npm run dev
# → http://localhost:5174
```

To rebuild the committed static app in `soc-builder/app/`:

```bash
npm run build
```

---

## Routing Logic

| Environment | Budget | Path |
|---|---|---|
| Microsoft 365 / Azure | any | `microsoft_native` |
| Hybrid or Google/Mixed | Lean | `open_source` |
| Hybrid or Google/Mixed | Funded | `best_of_breed` |

Company size and current security state are captured for context (and future path variants) but do not change the routing today.

---

## Extending the Data

All content lives in `frontend/src/socData.json`:

- `PATHS` — metadata for each build path (name, costs, description)
- `BUILD_STEPS` — 10 steps, each with path-independent `what` / `why` / `day_one` and a `recommendations` dict keyed by path ID
- `SOURCES` — vendor/reference links shown on the summary screen

**To add a tool recommendation:** find the step in `BUILD_STEPS`, find the path in its `recommendations` dict, and add to the `products` list.

**To add a new path:** add an entry to `PATHS`, add a matching key to each step's `recommendations`, and update `determinePath()` in `recommendations.js`.

---

## Sources

All pricing is approximate as of 2026 and security licensing is heavily negotiated — verify with vendors. Key references: Microsoft Security, CISA free services (Cyber Hygiene, KEV catalog), MITRE ATT&CK, Wazuh, Security Onion, CrowdStrike, SentinelOne, Splunk, Tenable, Greenbone, Proofpoint, KnowBe4, Okta, TheHive, NIST SP 800-61, SigmaHQ.
