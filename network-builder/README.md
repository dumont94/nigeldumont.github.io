# Your First Network — SOHO Infrastructure Builder

A portfolio project by Nigel Dumont.

A web application that walks a non-technical business owner through building a real SOHO network from scratch. The user answers four questions and the tool produces a step-by-step build plan — covering every component from ISP failover to monitoring — with plain-English explanations, specific product recommendations, pricing, alternatives, and configuration steps.

**Live portfolio:** [nigeldumont.github.io](https://dumont94.github.io/nigeldumont.github.io/)

---

## What It Does

1. User answers four questions (business type, team size, budget, management style).
2. Flask backend routes the answers to one of three build paths:
   - **Budget DIY** — FortiGate 40F + UniFi switch + UniFi U7 Lite APs (~$4,500 Year 1)
   - **Enterprise DIY** — Palo Alto PA-400/FortiGate 60F + UniFi Pro Max switches + SolarWinds NPM (~$13,000–16,000 Year 1)
   - **Fully Outsourced** — Meraki cloud stack managed by an MSP (~$700–1,200/mo)
3. Frontend walks through 10 build steps one at a time (ISP → Firewall → Switch → APs → Wireless Security → VLANs → NAT → SD-WAN → Monitoring → Test & Verify).
4. Each step shows: what it is, why it matters, recommended products with pricing, alternatives and trade-offs, patching/licensing notes, and configuration steps.
5. Summary screen shows the full stack, a network topology diagram, and links to all vendor sites for current pricing.

---

## Architecture

```
network-builder/
├── backend/
│   ├── app.py              Flask routes — thin HTTP layer only
│   ├── data.py             All product/pricing data (structured Python dict)
│   ├── recommendations.py  Routing logic: questionnaire answers → path → steps
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json        Vite + React 18
    ├── vite.config.js      Dev proxy: /api → localhost:5000
    └── src/
        ├── App.jsx         State machine: questionnaire → loading → walkthrough → summary
        ├── App.css         Single stylesheet, CSS custom properties, dark mode
        └── components/
            ├── Questionnaire.jsx   Four questions, selectable card UI
            ├── Walkthrough.jsx     Step sidebar + step card + prev/next nav
            ├── StepCard.jsx        Color-coded sections: what/why/products/alts/patch/config
            ├── NetworkDiagram.jsx  Path-specific ASCII topology diagram
            ├── ProgressBar.jsx     Step progress indicator
            └── Summary.jsx         Full stack table, costs, vendor sources
```

**Design decisions:**

- **Flask over FastAPI or Django** — the backend is genuinely thin (three routes). Flask's simplicity makes the code easier for a hiring manager to read at a glance. No ORM, no models, no migrations.
- **All data in `data.py`, not a database** — the recommendation data is structured, editable, and version-controlled. A hiring manager can read and verify every product recommendation without running a query.
- **React + Vite over Next.js** — this is a single-page tool with no SEO requirements. Vite's build speed is a better fit than Next's SSR overhead.
- **Pure CSS over Tailwind** — explicit CSS makes the design system legible without knowing utility class names. Everything is in `App.css` with CSS custom properties.
- **Security posture is always enterprise-grade** — a conscious design choice. Budget determines tooling, not whether controls exist. This mirrors how real infrastructure decisions should work.

---

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm

---

## Running Locally

You need two terminal windows — one for the backend, one for the frontend.

### Terminal 1 — Flask Backend

```bash
cd network-builder/backend

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
# → Running on http://localhost:5000
```

### Terminal 2 — React Frontend

```bash
cd network-builder/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
# → Running on http://localhost:5173
```

Open **http://localhost:5173** in your browser.

The Vite dev server proxies `/api/*` requests to Flask on port 5000, so no CORS configuration is needed during development.

---

## API Reference

### `GET /api/health`
Liveness check.

```json
{ "status": "ok" }
```

### `POST /api/recommend`

**Request body:**
```json
{
  "business_type":    "startup",
  "size":             "1-10",
  "budget":           "budget_conscious",
  "management_style": "diy"
}
```

**Valid values:**
| Field | Values |
|---|---|
| `business_type` | `"startup"` |
| `size` | `"1-10"`, `"11-50"`, `"51+"` |
| `budget` | `"budget_conscious"`, `"enterprise"` |
| `management_style` | `"diy"`, `"outsourced"` |

**Response:** Full recommendation object with `path`, `path_info`, `steps` (10 items), and `sources`.

---

## Extending the Data

All product recommendations live in `backend/data.py`. The file is structured as two top-level dicts:

- `PATHS` — metadata for each build path (name, costs, description)
- `BUILD_STEPS` — 10 steps, each with a `recommendations` dict keyed by path ID

**To add a new product recommendation:** find the step in `BUILD_STEPS`, find the path in its `recommendations` dict, and add to the `products` list.

**To add a new build path:** add an entry to `PATHS`, then add a matching key to each step's `recommendations` dict. No other files need to change.

**To add a new business type:** add it to `BUSINESS_TYPES` in `Questionnaire.jsx` (remove the `disabled` flag), then add routing logic in `recommendations.py`.

---

## Product Sources

All pricing is approximate as of 2026. Verify current pricing at:

| Vendor | URL | What's covered |
|---|---|---|
| Ubiquiti (UniFi) | https://www.ui.com | Switches, APs, Cloud Controller |
| Fortinet | https://www.fortinet.com | FortiGate firewalls, SD-WAN, ATP |
| Palo Alto Networks | https://www.paloaltonetworks.com | PA-400 series, Cortex XDR, Strata |
| Cisco Meraki | https://meraki.cisco.com | Cloud-managed MX/MS/MR stack |
| Cisco | https://www.cisco.com | Catalyst switches, Firepower NGFW |
| SolarWinds | https://www.solarwinds.com | NPM, Observability |
| Inseego | https://www.inseego.com | 5G LTE failover modems |
