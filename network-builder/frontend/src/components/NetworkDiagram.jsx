/**
 * NetworkDiagram.jsx — ASCII-style network topology diagram.
 *
 * The diagram is path-specific: Budget shows simpler gear labels,
 * Enterprise shows the dual-ISP / redundant switch configuration,
 * Outsourced labels everything as MSP-managed with Meraki branding.
 *
 * Rendered in a <pre> block with Space Mono for perfect character alignment.
 * The integration steps list below the diagram walks through how the
 * physical connections are made in sequential order.
 */

// Path-specific diagram strings — plain text, Space Mono ensures alignment
const DIAGRAMS = {
  budget_diy: `
  [Comcast/AT&T Business]  ──┐
                             ├──►  [FortiGate 40F]  ──►  [UniFi SW Lite 8 PoE]  ──►  [U7 Lite APs  ×2]
  [5G LTE / Inseego MiFi]  ──┘         SD-WAN                    │                           │
                                                          [Wired Desks / Devices]       [WiFi Clients]
                                                                  │
                                                    [SolarWinds Observability (free)]
                                                                  │
                                                    [UniFi Dashboard + FortiCloud]
`,
  enterprise_diy: `
  [Comcast Business 1 Gbps]  ──┐
                               ├──►  [PA-400 / FortiGate 60F]  ──►  [UniFi Pro Max 24 PoE  ×2]  ──►  [U7 Pro APs  ×4]
  [Verizon Fios 500 Mbps]  ────┤          SD-WAN + NGFW                    │  LAG                           │
                               │                                    [7 VLANs / QoS]               [WiFi Clients]
  [5G LTE Tertiary Backup]  ───┘       802.1X RADIUS                       │
                                       SSL Inspection             [Wired Devices]
                                              │
                                 [SolarWinds NPM + Cortex XDR]
                                              │
                                 [FortiAnalyzer / Palo Alto Panorama]
`,
  outsourced: `
  [ISP 1  (MSP-selected)]  ──┐
                             ├──►  [Meraki MX  (cloud-managed)]  ──►  [Meraki MS Switch]  ──►  [Meraki MR APs]
  [ISP 2  (MSP-selected)]  ──┤         SD-WAN / NGFW                        │                       │
                             │       Meraki Dashboard                 [VLANs + QoS]          [WiFi Clients]
  [5G Failover  (MSP)]  ─────┘                                               │
                                                                    [Wired Devices]
                                          │
                              [MSP 24/7 Monitoring  (SolarWinds / Datto)]
                                          │
                              [MSP Support Desk  — 1-hr SLA]
`,
};

// Integration steps that describe the physical wiring sequence
const INTEGRATION_STEPS = [
  "Both primary ISPs terminate into the dual-WAN firewall (FortiGate / Palo Alto / Meraki MX).",
  "The 5G/LTE modem connects into the firewall's WAN3 or dedicated cellular port.",
  "The firewall monitors WAN health via ping probes; failover triggers automatically when a link degrades past the configured SLA threshold.",
  "The firewall's LAN port connects to the switch's uplink via a 1G or multi-gig link (tagged trunk carrying all VLANs).",
  "The switch delivers PoE power and data to APs and wired devices across all VLAN segments.",
  "VLANs are tagged on the switch trunk and enforced by the firewall's inter-VLAN security policies.",
  "The monitoring agent (SolarWinds / Meraki-native / FortiAnalyzer) collects device metrics via SNMP v3 and syslog.",
  "Everything is managed from a single dashboard: UniFi Cloud / Meraki Dashboard / FortiCloud / Palo Alto Strata.",
];

export default function NetworkDiagram({ pathId }) {
  const diagram = DIAGRAMS[pathId] || DIAGRAMS.budget_diy;

  return (
    <div className="diagram-section">
      <div className="diagram-section__title">Network Topology</div>

      {/* ASCII diagram */}
      <div className="diagram-container">
        <pre className="diagram-pre">{diagram}</pre>
      </div>

      {/* Integration walkthrough */}
      <div style={{ marginTop: "var(--space-6)" }}>
        <div className="diagram-section__title">How It All Connects</div>
        <ol className="integration-steps">
          {INTEGRATION_STEPS.map((step, i) => (
            <li key={i} className="integration-step">
              <span className="integration-step__text">{step}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
