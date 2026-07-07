/**
 * CoverageMap.jsx — ASCII-style SOC telemetry flow diagram.
 *
 * The diagram is path-specific: it shows this path's telemetry
 * sources on the left, flowing into the SIEM, through detection
 * and routing, down to triage, containment, and reporting.
 *
 * Rendered in a <pre> block with Space Mono for perfect character
 * alignment. The flow list below walks through how an event moves
 * through the pipeline.
 */

// Path-specific diagram strings — plain text, Space Mono ensures alignment
const DIAGRAMS = {
  microsoft_native: `
  [Entra ID  sign-ins + audit]   ──┐
  [Defender for Endpoint  EDR]   ──┤
  [Defender for Office  email]   ──┼──►  [Microsoft Sentinel  — SIEM]
  [Firewall / DNS  syslog]       ──┤      analytics rules + cost watch
  [Azure + M365  audit logs]     ──┘                 │
                                                     ▼
                                   [Defender XDR  — correlated incidents]
                                                     │
                                  P1/P2 ► page on-call   P3/P4 ► daily queue
                                                     │
                                                     ▼
                          [Triage ► Contain: isolate host / revoke sessions]
                                                     │
                                                     ▼
                          [Case notes ► weekly tuning ► monthly scorecard]
`,
  open_source: `
  [Wazuh agents + Sysmon  endpoints] ──┐
  [Security Onion  Suricata + Zeek]  ──┤
  [Pi-hole / Technitium  DNS logs]   ──┼──►  [Wazuh  — SIEM + rules]
  [Firewall / VPN  syslog]           ──┤      curated Sigma detections
  [M365 / Google  audit APIs]        ──┘               │
                                                       ▼
                                         [Shuffle  — SOAR routing]
                                                       │
                                                       ▼
                                         [TheHive  — cases + timeline]
                                                       │
                                                       ▼
                        [Triage ► Contain: firewall block / disable account]
                                                       │
                                                       ▼
                        [Post-incident review ► rule tuning ► metrics]
`,
  best_of_breed: `
  [CrowdStrike Falcon  EDR]       ──┐
  [Proofpoint  email verdicts]    ──┤
  [Umbrella  DNS + web]           ──┼──►  [Splunk  — SIEM + ES risk-based alerting]
  [Corelight  network metadata]   ──┤                  │
  [Okta  identity events]         ──┤                  │
  [Tenable  vuln context]         ──┘ (enrichment)     ▼
                                          [Tines  — enrich + route]
                                                       │
                                    P1 ► PagerDuty       P3/P4 ► analyst queue
                                                       │
                                                       ▼
                        [Triage ► Contain: Falcon network containment, 1 click]
                                                       │
                                                       ▼
                        [Case system ► purple-team validation ► SOC scorecard]
`,
};

// How an event moves through the pipeline, start to finish
const FLOW_STEPS = [
  "Endpoint, identity, email, network, and cloud telemetry all land in the SIEM — one searchable source of truth for every investigation.",
  "Detection rules mapped to MITRE ATT&CK evaluate events as they arrive; only high-confidence correlations become alerts.",
  "Alerts are enriched automatically — asset owner, user context, threat intel — before a human ever sees them.",
  "The severity matrix routes the alert: P1/P2 pages the on-call immediately; P3/P4 waits in the daily triage queue.",
  "Every alert becomes a case with an owner, a timeline, and an outcome — nothing gets dismissed silently.",
  "Containment actions (isolate host, disable account, block domain) execute from the console in minutes, with an audit trail.",
  "False positives feed the weekly tuning loop — noisy rules get fixed, suppressed, or retired, keeping the queue humanly reviewable.",
  "Monthly metrics — MTTD, MTTR, coverage %, phishing report rate, patch SLA compliance — roll into a one-page scorecard for leadership.",
];

export default function CoverageMap({ pathId }) {
  const diagram = DIAGRAMS[pathId] || DIAGRAMS.open_source;

  return (
    <div className="diagram-section">
      <div className="diagram-section__title">SOC Telemetry Flow</div>

      {/* ASCII diagram */}
      <div className="diagram-container">
        <pre className="diagram-pre">{diagram}</pre>
      </div>

      {/* Pipeline walkthrough */}
      <div style={{ marginTop: "var(--space-6)" }}>
        <div className="diagram-section__title">How An Alert Moves Through It</div>
        <ol className="integration-steps">
          {FLOW_STEPS.map((step, i) => (
            <li key={i} className="integration-step">
              <span className="integration-step__text">{step}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
