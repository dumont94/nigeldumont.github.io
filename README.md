# nigeldumont.github.io

Personal portfolio site for Nigel Dumont — Senior Systems & Infrastructure Engineer based in Chicago, IL.

**Live site:** [https://dumont94.github.io/nigeldumont.github.io/](https://dumont94.github.io/nigeldumont.github.io/)

---

## About

A single-file static portfolio built with plain HTML and CSS — no frameworks, no build tools. Everything lives in `index.html`. Also includes a full interactive network infrastructure builder tool built with React + Vite, deployed as a static app, and links out to the [SOC Posture Tool](https://github.com/dumont94/soc-builder-tool) — a five-pillar SOC maturity assessment in its own repo.

Hosted on GitHub Pages, served directly from the `main` branch.

---

## Stack

- **HTML/CSS/JS** — no frameworks for the main site
- **React + Vite** — network builder tool (`/network-builder/app/`)
- **Google Fonts** — Space Grotesk + Space Mono
- **GitHub Pages** — static hosting, deploys automatically on push to `main`

---

## Structure

```
nigeldumont.github.io/
├── index.html              # main portfolio — styles, layout, and content
├── network-builder/
│   ├── app/                # built React app (served by GitHub Pages)
│   └── frontend/           # React + Vite source
├── p-net1.png – p-net8.png # Networking work sample images
├── p-ep1.png – p-ep4.png   # Endpoint work sample images
├── p-iam1.jpeg – p-iam4.png # IAM work sample images
├── p-voip.png, p-printer.png # VoIP & Print work sample images
├── p-auto1.jpeg, p-auto2.jpeg # Automation work sample images
└── README.md
```

---

## Features

- Fixed nav with blur backdrop and light/dark mode toggle
- Light mode default with persistent dark mode via localStorage
- Skills grid built from resume — exact categories, no fluff
- Work history with win tags pulled from real deliverables
- Work samples section with 5 slideshow categories: Networking, Endpoint, IAM, VoIP & Print, Automation
- Lightbox image viewer
- Side projects with live demo links
- Credentials section with certs and education
- Fully responsive — mobile layout via CSS
- **Network Builder Tool** — interactive SOHO infrastructure planner, pure client-side React, no backend required
- **SOC Posture Tool** — five-pillar SOC maturity assessment: visibility, detection engineering, alert management, compliance, org standing → a posture read with levels, gaps, and fix-first priorities

---

## Network Builder Tool

Located at `/network-builder/`. A guided questionnaire that recommends a full network build path (budget DIY, enterprise DIY, or outsourced) with step-by-step hardware and configuration guidance.

- Pure static — no Flask backend, all logic runs client-side via `recommendations.js`
- Data exported from Python to `networkData.json` and bundled at build time
- Build with: `cd network-builder/frontend && npm run build`

---

## SOC Posture Tool

The security-operations companion to the network builder, in its own repo: [github.com/dumont94/soc-builder-tool](https://github.com/dumont94/soc-builder-tool) · **Live:** [dumont94.github.io/soc-builder-tool](https://dumont94.github.io/soc-builder-tool/)

A five-pillar SOC maturity assessment — visibility, detection engineering, alert management, compliance posture, and organizational standing. Fourteen questions score each pillar into four maturity levels (Ad Hoc → Reactive → Managed → Optimized); the output is a posture read with per-pillar diagnoses, named blind spots, and a fix-first priority list. Deploys automatically to GitHub Pages via Actions on every push to its `main`.

---

## Deployment

Push to `main`. GitHub Pages picks it up automatically within ~60 seconds.

No CI. Just push.

---

## Contact

- Email: [dumontnigel@gmail.com](mailto:dumontnigel@gmail.com)
- LinkedIn: [linkedin.com/in/nigeldumont](https://linkedin.com/in/nigeldumont)
- GitHub: [github.com/dumont94](https://github.com/dumont94)
