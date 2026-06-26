"""
data.py — Network recommendation data module.

All product specs, pricing, and build guidance live here. This file is
intentionally self-contained so a hiring manager (or you, six months from now)
can open it and immediately understand every recommendation without touching
the rest of the codebase. Add a new build path by adding a key to each step's
'recommendations' dict and a matching entry in PATHS.

Three paths are defined:
  budget_diy      — lean, DIY, tight budget (5–10 person startup)
  enterprise_diy  — redundant, full observability, still self-managed
  outsourced      — MSP runs everything, zero hands-on

Pricing note: all figures are approximate 2026 market rates.
Always verify at vendor sites before purchasing (see SOURCES below).
"""

# ---------------------------------------------------------------------------
# Path metadata — displayed on the summary screen and in the app header
# ---------------------------------------------------------------------------
PATHS = {
    "budget_diy": {
        "id": "budget_diy",
        "name": "Budget DIY",
        "tagline": "Lean, self-managed, startup-grade security on a tight budget",
        "audience": "1–10 person team, single location, cost-conscious founder",
        "year1_cost": "$4,500 – $5,500",
        "recurring_cost": "~$3,000 / yr (Year 2+)",
        "description": (
            "You own the gear and the config. UniFi handles the LAN side (switches + APs) "
            "with no recurring fees. A FortiGate 40F covers your WAN edge, firewall, and SD-WAN. "
            "Security posture matches Enterprise — budget only changes which tools, "
            "not whether controls exist."
        ),
    },
    "enterprise_diy": {
        "id": "enterprise_diy",
        "name": "Enterprise DIY",
        "tagline": "High-end gear, full redundancy, and deep observability — still self-managed",
        "audience": "1–50 person team with technical staff, room to grow, compliance requirements",
        "year1_cost": "$13,000 – $16,000",
        "recurring_cost": "~$7,000 – $9,000 / yr (Year 2+)",
        "description": (
            "Dual ISPs, redundant switches, Wi-Fi 7 APs, and a Palo Alto or FortiGate 60F at the edge. "
            "Full IPS, sandboxing, DLP, 802.1X RADIUS auth, and a SolarWinds monitoring stack. "
            "Built to scale from 5 to 500 without re-architecting."
        ),
    },
    "outsourced": {
        "id": "outsourced",
        "name": "Fully Outsourced",
        "tagline": "Zero hands-on — a managed service provider runs everything",
        "audience": "Business owner who wants predictable monthly cost and no IT headcount",
        "year1_cost": "$8,400 – $14,400 / yr",
        "recurring_cost": "~$700 – $1,200 / mo (ongoing)",
        "description": (
            "A Meraki cloud-managed stack deployed and maintained by an MSP (e.g. CDW, Mindsight). "
            "No upfront hardware capex — the vendor owns the gear. Includes 24/7 support desk, "
            "firmware management, and threat-intel renewals. You open tickets; they fix things."
        ),
    },
}

# ---------------------------------------------------------------------------
# Vendor source links — displayed on the summary screen
# ---------------------------------------------------------------------------
SOURCES = [
    {
        "vendor": "Ubiquiti (UniFi)",
        "url": "https://www.ui.com",
        "note": "Switches, APs, UniFi Cloud Controller — no per-device licensing",
    },
    {
        "vendor": "Fortinet",
        "url": "https://www.fortinet.com",
        "note": "FortiGate firewalls, SD-WAN, ATP/UTP licensing, FortiCloud",
    },
    {
        "vendor": "Palo Alto Networks",
        "url": "https://www.paloaltonetworks.com",
        "note": "PA-400 series NGFWs, Cortex XDR, Strata Cloud Manager",
    },
    {
        "vendor": "Cisco Meraki",
        "url": "https://meraki.cisco.com",
        "note": "Cloud-managed MX firewall, MS switches, MR APs, MV cameras",
    },
    {
        "vendor": "Cisco",
        "url": "https://www.cisco.com",
        "note": "Catalyst switches, Firepower NGFW, enterprise routing",
    },
    {
        "vendor": "SolarWinds",
        "url": "https://www.solarwinds.com",
        "note": "NPM, Observability (free tier available), network monitoring SaaS",
    },
    {
        "vendor": "Inseego",
        "url": "https://www.inseego.com",
        "note": "MiFi M3000 and enterprise 5G LTE failover modems",
    },
]

# ---------------------------------------------------------------------------
# Build steps — 10 components in sequential deployment order.
#
# Structure per step:
#   id, order, title, icon — metadata
#   what  — plain-English explanation (assume zero networking knowledge)
#   why   — business justification (why does this matter to the owner?)
#   recommendations[path_id]:
#     products      — list of {name, price, role, note}
#     alternatives  — list of {name, comparison}
#     patching_notes — licensing / update / renewal guidance
#     config_steps  — ordered list of setup actions
# ---------------------------------------------------------------------------
BUILD_STEPS = [

    # -----------------------------------------------------------------------
    # 1. ISP & Failover
    # -----------------------------------------------------------------------
    {
        "id": "isp_failover",
        "order": 1,
        "title": "ISP & Failover",
        "icon": "isp",
        "what": (
            "Think of your ISP connection as your city water supply — if the pipe breaks, everything stops. "
            "A failover connection is a backup water tank: when the main supply drops, your network "
            "automatically switches to the backup within seconds, so nobody even notices the outage."
        ),
        "why": (
            "Even 'reliable' business ISPs drop for hours several times a year. Lost connectivity means "
            "lost sales, lost video calls, and lost access to cloud tools. A 5G failover costs about "
            "$60–80/month — far cheaper than the cost of a 2-hour outage. The failover also gives you "
            "leverage when negotiating your next ISP contract."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "Comcast Business (or AT&T Business / Verizon Fios)",
                        "price": "~$100–150 / mo",
                        "role": "Primary ISP",
                        "note": (
                            "Aim for 300+ Mbps symmetric. Business-tier SLAs include faster repair "
                            "windows than residential and a static IP address for hosting VPN."
                        ),
                    },
                    {
                        "name": "UniFi 5G Backup or Inseego MiFi M3000",
                        "price": "~$99 upfront + $60–80 / mo data plan",
                        "role": "5G LTE Failover",
                        "note": (
                            "Plugs into the FortiGate WAN2 port. Failover triggers in 10–30 seconds "
                            "if the primary drops. Inseego M3000 supports dual SIM for carrier diversity."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Secondary wired ISP (instead of 5G)",
                        "comparison": (
                            "More reliable than cellular but requires a second physical line. "
                            "~$80–120/mo for low-tier fiber. Good if the building already has dual-provider fiber."
                        ),
                    },
                    {
                        "name": "Starlink Business",
                        "comparison": (
                            "~$250 upfront + $140/mo. Works anywhere with sky view — good for rural locations "
                            "or offices where 5G signal is weak. Slightly higher latency (~40ms) than wired."
                        ),
                    },
                ],
                "patching_notes": (
                    "ISPs push modem/ONT firmware automatically — no action required. Review your ISP SLA "
                    "annually and negotiate a speed upgrade if pricing has dropped. Set a calendar reminder "
                    "30 days before contract renewal."
                ),
                "config_steps": [
                    "Plug primary ISP modem into FortiGate WAN1 port.",
                    "Plug 5G modem into FortiGate WAN2 port.",
                    "In FortiGate SD-WAN, set WAN1 as primary (priority 10) and WAN2 as failover (priority 20).",
                    "Set health-check ping targets (8.8.8.8 and 1.1.1.1) so FortiGate detects real WAN failures, not just link-down events.",
                    "Test: unplug WAN1, confirm all traffic shifts to WAN2 within 30 seconds.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "Comcast Business Gigabit + Verizon Fios 500 Mbps",
                        "price": "~$250–300 / mo combined (~$3,000 / yr)",
                        "role": "Dual Primary ISPs (different carriers)",
                        "note": (
                            "Two different carriers means a single carrier outage doesn't take you down. "
                            "Route latency-sensitive traffic (VoIP, video) over whichever path has the best "
                            "real-time performance."
                        ),
                    },
                    {
                        "name": "Inseego MiFi M3000 or Cradlepoint E300",
                        "price": "~$299 upfront + $60–80 / mo",
                        "role": "5G Tertiary Failover",
                        "note": (
                            "Third failover path. Cradlepoint E300 adds enterprise-grade cellular management "
                            "via Cradlepoint NetCloud Manager — worth the premium if you manage multiple sites."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "MPLS / SD-WAN overlay from ISP",
                        "comparison": (
                            "If you have multiple offices, consider ISP-managed SD-WAN (AT&T, Comcast). "
                            "More expensive but simplifies multi-site routing. Not needed for a single location."
                        ),
                    },
                    {
                        "name": "Starlink Business as tertiary",
                        "comparison": (
                            "Excellent rural/backup option. Pairs well with dual wired primary. "
                            "Same ~$140/mo cost. Use as tertiary behind both wired ISPs."
                        ),
                    },
                ],
                "patching_notes": (
                    "Review ISP contracts annually. For dual ISP, stagger renewal dates so you're never "
                    "negotiating both simultaneously. Enable SNMP on ISP-provided equipment if available — "
                    "this feeds SolarWinds with WAN interface telemetry."
                ),
                "config_steps": [
                    "Plug ISP 1 into Firewall WAN1, ISP 2 into WAN2, 5G modem into WAN3.",
                    "Configure SD-WAN zones: WAN1 + WAN2 as primary zone, WAN3 as backup zone.",
                    "Set per-application SD-WAN rules: VoIP prefers lowest-latency path, bulk backup uses highest-bandwidth path.",
                    "Configure health probes on each WAN (ping + HTTP) to detect asymmetric failures (link up but no routing).",
                    "Set hysteresis timers (5-second failover, 30-second failback) to prevent route flapping.",
                    "Test all three failover scenarios under realistic load before going live.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "MSP-provisioned dual ISP (Comcast + Verizon or regional equivalent)",
                        "price": "~$150–200 / mo (included in MSP bundle)",
                        "role": "Dual WAN — provisioned and managed by MSP",
                        "note": (
                            "Your MSP handles ISP selection, contract negotiation, and failover configuration. "
                            "You pay a single monthly line item. ISP outages are your MSP's problem to resolve."
                        ),
                    },
                    {
                        "name": "5G Failover (MSP-managed Meraki cellular)",
                        "price": "Included in MSP bundle",
                        "role": "Automatic cellular backup",
                        "note": (
                            "Meraki MX cellular failover card or MSP-managed 5G modem. "
                            "Monitored 24/7 via Meraki Dashboard. Failover events are logged and reported monthly."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Single ISP + managed failover only",
                        "comparison": (
                            "Some MSPs offer a lighter package with one wired ISP + 5G failover only. "
                            "Lower monthly cost but less redundancy. Fine for low-criticality offices."
                        ),
                    },
                ],
                "patching_notes": (
                    "Your MSP monitors ISP health and handles all modem/router firmware. "
                    "You should receive monthly uptime reports. Ask for SLA documentation showing "
                    "guaranteed uptime percentage and escalation procedures."
                ),
                "config_steps": [
                    "Sign ISP contracts (your MSP may negotiate on your behalf — this is a value-add to ask for).",
                    "MSP schedules ISP installation day — you just need to be on-site to let the technician in.",
                    "MSP configures Meraki MX dual-WAN and validates failover before handing off.",
                    "Request a live failover test before signing off on deployment: watch the MSP pull WAN1 and confirm switchover.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 2. Firewall / Gateway
    # -----------------------------------------------------------------------
    {
        "id": "firewall",
        "order": 2,
        "title": "Firewall / Gateway",
        "icon": "firewall",
        "what": (
            "A firewall is the bouncer at your office door. Every piece of data that enters or leaves "
            "your network passes through it. The firewall checks each packet against a ruleset — "
            "allowing legitimate traffic and blocking anything suspicious. It also hides your internal "
            "network behind a single public IP address (NAT) so the internet can't directly address "
            "your computers."
        ),
        "why": (
            "Without a firewall, your devices are exposed directly to the internet. Bots scan the "
            "entire IPv4 space in under an hour — an unprotected device gets probed within minutes "
            "of going online. The firewall also handles SD-WAN (routing across your ISPs), VPN "
            "(letting remote workers securely connect), and threat inspection (blocking known malware "
            "before it reaches your devices)."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "FortiGate 40F with 1-Year UTP Bundle",
                        "price": "~$800–1,200 upfront + ~$400–500 / yr renewal",
                        "role": "Firewall, Gateway, SD-WAN",
                        "note": (
                            "UTP = Unified Threat Protection. Includes IPS, application control, "
                            "web filtering, antivirus, and threat-intel updates in one license. "
                            "RENEWAL TRAP: Hardware keeps routing if you let the license lapse, "
                            "but ALL threat protection stops updating. Set a calendar reminder 90 days "
                            "before expiry — an unpatched FortiGate is a high-value target."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi Dream Machine Pro",
                        "comparison": (
                            "~$379 upfront, no recurring license. Solid firewall with IDS/IPS. "
                            "Weaker threat-intel than FortiGate and no SD-WAN. Good if you want "
                            "an all-UniFi stack and want to skip annual renewals."
                        ),
                    },
                    {
                        "name": "pfSense (on Protectli Vault or similar)",
                        "comparison": (
                            "Free software, ~$200–400 hardware. Very capable — used by many MSPs internally. "
                            "Steeper learning curve and no vendor support. Great for technical founders; "
                            "risky for non-technical ones."
                        ),
                    },
                    {
                        "name": "Meraki MX64",
                        "comparison": (
                            "~$700 hardware + ~$600/yr license. Cloud-managed — much easier to configure "
                            "than FortiGate. Higher ongoing cost. A good bridge toward the Outsourced path."
                        ),
                    },
                ],
                "patching_notes": (
                    "FortiGate firmware releases come quarterly. Apply within 30 days of release — "
                    "FortiGate CVEs are actively exploited in the wild (CVE-2024-21762 is a well-known example). "
                    "Enable auto-update notifications in FortiGuard. UTP license must renew annually — "
                    "diarize 90 days ahead."
                ),
                "config_steps": [
                    "Factory-reset the FortiGate before deployment (hold reset button 10 seconds until LEDs cycle).",
                    "Connect WAN1 to primary ISP modem, WAN2 to 5G modem.",
                    "Connect LAN port to the switch uplink.",
                    "Access admin UI at 192.168.1.99 — change the default admin password immediately (use a password manager).",
                    "Register device with FortiGuard portal to activate UTP license.",
                    "Create SD-WAN interface grouping WAN1 and WAN2.",
                    "Create DHCP scopes for each VLAN subnet.",
                    "Create firewall policies: Data VLAN → internet (allow), Guest → internal VLANs (deny), enable IPS on all outbound.",
                    "Enable FortiCloud logging (free tier) so you have a log trail from day one.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "Palo Alto PA-410 or PA-415",
                        "price": "~$1,500–2,500 hardware + ~$1,200–1,800 / yr license",
                        "role": "Next-Gen Firewall, Gateway, SD-WAN",
                        "note": (
                            "Industry-leading App-ID (identifies applications by behavior, not port) and "
                            "User-ID (ties traffic to individual users). Decrypts and inspects TLS traffic "
                            "without breaking modern apps. Integrates with Cortex XDR for threat correlation. "
                            "Right-sized for 20–50 users with compliance requirements."
                        ),
                    },
                    {
                        "name": "FortiGate 60F with ATP Bundle (cost-optimized alternative)",
                        "price": "~$800–1,200 hardware + ~$600–800 / yr license",
                        "role": "Firewall, Gateway, SD-WAN",
                        "note": (
                            "ATP (Advanced Threat Protection) adds sandboxing and advanced malware detection "
                            "on top of the UTP bundle. Solid choice if PA-400 is over budget."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Cisco Firepower 1010E",
                        "comparison": (
                            "~$1,200 hardware + Cisco SmartNet. Managed via FMC (Firepower Management Center) "
                            "which adds complexity. Better if the team is already Cisco-certified."
                        ),
                    },
                    {
                        "name": "Meraki MX84 or MX85",
                        "comparison": (
                            "Cloud-managed, easy to configure, strong telemetry. ~$1,500 hardware + ~$800/yr. "
                            "Less granular policy control than PA-400. Right choice if you want enterprise "
                            "features without deep firewall expertise."
                        ),
                    },
                ],
                "patching_notes": (
                    "Palo Alto releases two update categories: content updates (threat signatures — weekly, "
                    "can be automated) and PAN-OS (quarterly, requires a maintenance window — plan 2 hours). "
                    "Subscribe to Palo Alto Security Advisories email list. PA CVEs (e.g. PAN-SA-2024-0015) "
                    "are high-severity and targeted quickly."
                ),
                "config_steps": [
                    "Factory-reset PA-400, connect to Panorama or use local web management.",
                    "Configure WAN interfaces with ISP addresses; set up SD-WAN zones (untrust, trust-data, trust-dev, guest, mgmt, VoIP, IoT).",
                    "Define address objects for each VLAN subnet.",
                    "Create security policies: deny-all default, then explicit allow rules (use App-ID, not port numbers).",
                    "Enable SSL Forward Proxy (TLS inspection) for outbound traffic — create trusted certificate and push via GPO/MDM.",
                    "Enable Threat Prevention profile on all internet-facing security rules.",
                    "Configure GlobalProtect VPN for remote workers.",
                    "Connect to Cortex XDR or FortiAnalyzer for centralized log aggregation.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki MX64 (small office) or MX250 (medium/larger)",
                        "price": "No upfront — included in MSP monthly fee (vendor owns the hardware)",
                        "role": "Cloud-Managed Firewall, Gateway, SD-WAN",
                        "note": (
                            "MSP manages the Meraki Dashboard. You can view dashboards read-only but "
                            "not make config changes. All firmware, threat-intel, and license renewals "
                            "are handled by your MSP — this is the core value of the Outsourced path."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "FortiGate managed by MSP",
                        "comparison": (
                            "Some MSPs use FortiGate instead of Meraki. More configurable but requires "
                            "more MSP expertise. Ask which platform your MSP is certified on — that "
                            "matters more than the brand."
                        ),
                    },
                ],
                "patching_notes": (
                    "Your MSP owns all firewall patching. You should receive a monthly change report "
                    "listing firmware updates applied. If you haven't received one in 60 days, escalate — "
                    "firewall firmware management is a core MSP deliverable, not optional."
                ),
                "config_steps": [
                    "MSP ships a pre-configured Meraki MX to your office.",
                    "You plug WAN ports into ISP modems and the LAN port into the switch — that's your entire job.",
                    "MSP activates the device remotely via Meraki Dashboard and validates all configuration.",
                    "MSP provisions read-only dashboard access for you — request this during onboarding.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 3. Switches
    # -----------------------------------------------------------------------
    {
        "id": "switches",
        "order": 3,
        "title": "Switches",
        "icon": "switch",
        "what": (
            "A network switch is like a smart power strip for your network cables. Every wired device — "
            "desktops, printers, IP phones, access points — plugs into a port on the switch. "
            "The switch learns which device is on which port and routes traffic directly between them "
            "without broadcasting to everyone else. PoE (Power over Ethernet) switches also deliver "
            "power over the ethernet cable, so your APs and VoIP phones don't need separate adapters."
        ),
        "why": (
            "The firewall connects to the switch, and the switch fans out to every device. Without a "
            "managed switch you can't create VLANs (separate network segments), can't prioritize VoIP "
            "traffic with QoS, and can't power your APs cleanly. Managed switches also give you "
            "visibility into which ports are active and how much bandwidth each device is using."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "UniFi Switch Lite 8 PoE",
                        "price": "~$109 (one-time, no licensing)",
                        "role": "8-port managed PoE switch",
                        "note": (
                            "52W PoE budget — enough to power 2 APs (~15W each) and 2–3 VoIP phones "
                            "(~5W each). Managed via UniFi Network Controller (free, self-hosted or "
                            "UniFi Cloud). No recurring licensing fee. One-click firmware updates."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi Switch Flex Mini (5-port)",
                        "comparison": (
                            "~$29. Non-PoE, no VLAN support on its own. Use as a desktop port expander, "
                            "not as your primary switch."
                        ),
                    },
                    {
                        "name": "TP-Link TL-SG108PE (8-port PoE)",
                        "comparison": (
                            "~$70. Unmanaged switch — no VLAN support. Fine for a home, too limited "
                            "for a business that needs network segmentation."
                        ),
                    },
                    {
                        "name": "Cisco Catalyst 1000 8-port",
                        "comparison": (
                            "~$300. Cisco CLI management. Enterprise-grade but significant price jump "
                            "over UniFi. Only worth it if your team already has Cisco CLI skills."
                        ),
                    },
                ],
                "patching_notes": (
                    "UniFi switch firmware updates through the UniFi Network Controller — one-click upgrade. "
                    "No licensing fee. Schedule updates during off-hours (2–4 AM). A switch reboot takes "
                    "~60 seconds. Check for updates monthly or when a CVE advisory is published."
                ),
                "config_steps": [
                    "Plug switch uplink port into FortiGate LAN port (this will be a trunk link).",
                    "Adopt switch in UniFi Network Controller (it auto-discovers when on the same subnet).",
                    "Create VLANs in UniFi: VLAN 10 (Data/Default, 10.10.10.0/24), VLAN 20 (Guest, 10.10.20.0/24), VLAN 30 (VoIP, 10.10.30.0/24).",
                    "Set uplink port profile to 'All' (carries all VLAN tags to FortiGate).",
                    "Assign each device port to its VLAN (desk ports → VLAN 10, AP ports → trunk, VoIP → VLAN 30).",
                    "Enable PoE on AP and VoIP ports; disable on ports not using it (saves power, prevents accidents).",
                    "Enable Storm Control and STP (Spanning Tree) to prevent network loops.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "UniFi Switch Pro Max 24 PoE (×2)",
                        "price": "~$449 each (~$900 total)",
                        "role": "24-port L3 managed PoE switch — redundant pair",
                        "note": (
                            "400W PoE budget per switch — powers 4 enterprise APs plus full desk "
                            "infrastructure. L3 routing enables inter-VLAN routing at the switch layer, "
                            "reducing firewall load. Stack two for redundancy and aggregate uplinks via LAG."
                        ),
                    },
                    {
                        "name": "Cisco Catalyst 1300 24-port (alternative)",
                        "price": "~$800 each",
                        "role": "24-port managed L2/L3 switch",
                        "note": (
                            "Cisco CLI and web management. No cloud licensing required for basic management. "
                            "Better integration with Cisco Catalyst Center (DNA Center) if you're going "
                            "full Cisco stack."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Meraki MS120 (cloud-managed)",
                        "comparison": (
                            "~$800 hardware + ~$400/yr license. Excellent telemetry and cloud dashboard. "
                            "Higher cost but integrates seamlessly with Meraki MX if you chose that firewall."
                        ),
                    },
                    {
                        "name": "HPE Aruba Instant On 1960",
                        "comparison": (
                            "~$600, 24-port PoE L3. App-managed. Good middle ground between UniFi "
                            "simplicity and Cisco complexity. Strong in HPE/Aruba environments."
                        ),
                    },
                ],
                "patching_notes": (
                    "UniFi: same one-click process. For Cisco Catalyst, updates require IOS XE knowledge — "
                    "use Cisco Software Manager. Major IOS XE version upgrades should be tested in a "
                    "maintenance window (plan 2 hours). Cisco SmartNet (~$150/yr per switch) provides "
                    "TAC support and next-business-day hardware replacement."
                ),
                "config_steps": [
                    "Connect Switch 1 uplink to Firewall LAN1 via 10G SFP+.",
                    "Connect Switch 2 uplink to Switch 1 via LAG (Link Aggregation) for redundancy — or to Firewall LAN2.",
                    "Create 7 VLANs: 10=Data, 20=Dev, 30=Guest, 40=Management, 50=IoT, 60=VoIP, 70=Security Appliances.",
                    "Configure inter-VLAN routing at the firewall (not the switch) — firewall routing gives more granular policy control.",
                    "Set port profiles: uplinks = trunk all VLANs, workstation = access VLAN 10, AP ports = trunk data+guest, VoIP = access VLAN 60.",
                    "Enable RSTP (Rapid Spanning Tree) across both switches.",
                    "Configure SNMPv3 on both switches for SolarWinds monitoring integration.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki MS120 or MS225 (MSP-managed)",
                        "price": "No upfront — included in MSP monthly fee",
                        "role": "Cloud-managed switch",
                        "note": (
                            "MSP pre-configures VLANs, port profiles, and PoE settings before shipping. "
                            "You rack it and plug in cables; MSP validates the config remotely. "
                            "All firmware updates happen automatically during MSP-set maintenance windows."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi switch managed by MSP",
                        "comparison": (
                            "No per-switch licensing fee — lower monthly cost. Some MSPs prefer UniFi. "
                            "Confirm your MSP agreement explicitly covers UniFi management and firmware updates."
                        ),
                    },
                ],
                "patching_notes": (
                    "MSP owns all switch firmware and configuration changes. You should be in a "
                    "change-approval workflow — MSP notifies you 48 hours before any config change "
                    "that could cause downtime. Emergency changes (security patches) may be faster."
                ),
                "config_steps": [
                    "MSP ships Meraki switch pre-configured and labeled with port assignments.",
                    "Rack the switch, connect uplink to firewall, connect labeled device cables to labeled ports.",
                    "MSP activates the device via Meraki Dashboard and validates VLAN configuration remotely.",
                    "Request the port assignment diagram from MSP — you need this for physical troubleshooting.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 4. Access Points
    # -----------------------------------------------------------------------
    {
        "id": "access_points",
        "order": 4,
        "title": "Access Points",
        "icon": "wifi",
        "what": (
            "Access points (APs) are the devices that broadcast your Wi-Fi signal. Unlike a home router's "
            "built-in Wi-Fi, enterprise APs are dedicated devices that plug into your PoE switch and are "
            "managed centrally. This means every AP shares the same SSID, security settings, and config — "
            "your laptop roams between APs without dropping its connection as you move around the office."
        ),
        "why": (
            "Home-grade routers can't handle 10+ simultaneous devices well, don't support multiple SSIDs "
            "per VLAN (data vs. guest on the same hardware), and can't be centrally managed or monitored. "
            "Business APs also support WPA3 and 802.1X authentication — required for the security posture "
            "this build delivers."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "UniFi U7 Lite (×2)",
                        "price": "~$149 each (~$298 total)",
                        "role": "Tri-band Wi-Fi 7 access points",
                        "note": (
                            "2.4 GHz + 5 GHz + 6 GHz. Wi-Fi 7 (802.11be) supports up to 5.8 Gbps max. "
                            "More than sufficient for a 10-person office. PoE-powered from your switch. "
                            "No subscription required. Managed via UniFi Network Controller."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi U6 Lite (Wi-Fi 6, no 6 GHz)",
                        "comparison": (
                            "~$99 each. Slightly slower max throughput but perfectly fine for most offices. "
                            "Good if the U7 Lite is out of stock or you need to cut cost."
                        ),
                    },
                    {
                        "name": "TP-Link EAP670 (Wi-Fi 6E)",
                        "comparison": (
                            "~$130 each. Managed via TP-Link Omada Controller (free). Solid budget option "
                            "but less ecosystem integration than UniFi if you're already on that stack."
                        ),
                    },
                    {
                        "name": "Meraki MR36 (Wi-Fi 6)",
                        "comparison": (
                            "~$400 hardware + ~$350/yr license. Integrates with Meraki MX firewall "
                            "but licensing costs make it expensive for this path."
                        ),
                    },
                ],
                "patching_notes": (
                    "UniFi AP firmware updates through UniFi Network Controller — one-click, same process "
                    "as the switch. Schedule updates during off-hours; APs reboot (~30 seconds of Wi-Fi "
                    "outage per AP). Update every 60–90 days or immediately when a security advisory is published."
                ),
                "config_steps": [
                    "Mount APs on the ceiling or high on a wall for best coverage — avoid corners and metal surfaces.",
                    "Connect AP ethernet cable to a PoE-enabled port on your switch.",
                    "Adopt AP in UniFi Network Controller (auto-discovered on the local subnet).",
                    "Create two SSIDs: 'YourCompany' (VLAN 10, data) and 'YourCompany-Guest' (VLAN 20, isolated).",
                    "Set both SSIDs to WPA3 security mode (or WPA2/WPA3 transitional for devices older than 2018).",
                    "Enable 802.11r (Fast BSS Transition) for seamless roaming between the two APs.",
                    "Set minimum RSSI to –75 dBm to prevent 'sticky client' syndrome (devices clinging to a distant AP).",
                    "Enable band steering to push capable devices to 5/6 GHz rather than crowded 2.4 GHz.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "UniFi U7 Pro Wi-Fi 7 (×4)",
                        "price": "~$189 each (~$756 total)",
                        "role": "Tri-band Wi-Fi 7 APs with 2.5G uplink",
                        "note": (
                            "Higher AP count for better per-device performance in a larger office. "
                            "2.5G wired uplink handles high-density client loads. "
                            "6 GHz band offloads modern devices from congested 5 GHz."
                        ),
                    },
                    {
                        "name": "UniFi U7 Pro XGS (upgrade option)",
                        "price": "~$299 each",
                        "role": "Wi-Fi 7 AP with dedicated spectrum-scanning radio",
                        "note": (
                            "Adds a dedicated radio for spectrum analysis and rogue AP detection — "
                            "valuable for compliance environments (SOC 2, ISO 27001)."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Meraki MR56 (Wi-Fi 6E)",
                        "comparison": (
                            "~$600 hardware + Meraki license. Best-in-class telemetry and AI-driven "
                            "channel optimization. Right choice if already on Meraki MX/MS."
                        ),
                    },
                    {
                        "name": "Cisco Catalyst 9130 (Wi-Fi 6E)",
                        "comparison": (
                            "~$900 each. Cisco CleanAir spectrum management and integration with "
                            "Cisco DNA Center. Enterprise Cisco shops only — requires full Cisco ecosystem."
                        ),
                    },
                    {
                        "name": "Aruba AP-635 (Wi-Fi 6E)",
                        "comparison": (
                            "~$650 each. HPE Aruba, managed via Aruba Central (~$5/device/mo). "
                            "Excellent spectrum management, strong in healthcare and education verticals."
                        ),
                    },
                ],
                "patching_notes": (
                    "Same one-click UniFi firmware update process. For Meraki APs, auto-update with "
                    "maintenance window controls via Meraki Dashboard. For Cisco Catalyst APs, "
                    "updates via Cisco DNA Center with IOS XE knowledge required."
                ),
                "config_steps": [
                    "Plan AP placement using UniFi's site survey tool or a Wi-Fi analyzer app — aim for 1 AP per ~1,500 sq ft.",
                    "Mount 4 APs: 1 per floor or zone, ceiling-mounted for best coverage.",
                    "Create 3 SSIDs: 'Company' (VLAN 10 data), 'Company-Dev' (VLAN 20), 'Company-Guest' (VLAN 30).",
                    "Set Company and Company-Dev to WPA3-Enterprise (802.1X RADIUS — configured in next step).",
                    "Enable AI-Driven RF Optimization in UniFi for automatic channel and power adjustment.",
                    "Deploy rogue AP detection if using U7 Pro XGS — configure alerts for unauthorized SSIDs.",
                    "Enable AP-level client isolation on the Guest SSID (guests cannot see each other).",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki MR46 or MR57 (Wi-Fi 6 / 6E)",
                        "price": "No upfront — included in MSP monthly fee",
                        "role": "Cloud-managed wireless APs",
                        "note": (
                            "MSP handles placement, configuration, and RF optimization via Meraki Dashboard. "
                            "Meraki's 'Air Marshal' feature detects rogue APs and deauthenticates rogue "
                            "clients automatically — a meaningful security control."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi APs managed by MSP",
                        "comparison": (
                            "Lower cost (no per-AP license). Some MSPs prefer UniFi for small-to-mid offices. "
                            "Confirm your MSP has UniFi certification before choosing this option."
                        ),
                    },
                ],
                "patching_notes": (
                    "Meraki AP firmware is auto-updated by Cisco through the Meraki Dashboard during MSP-set "
                    "maintenance windows. No action required from you. This is a core advantage of "
                    "cloud-managed gear."
                ),
                "config_steps": [
                    "MSP ships pre-provisioned Meraki APs labeled with physical mounting locations.",
                    "Mount APs per MSP placement diagram.",
                    "Connect each AP to the switch PoE port using the labeled cable.",
                    "APs auto-register to Meraki Dashboard — no on-site configuration required.",
                    "MSP validates signal coverage and SSID configuration remotely, often within 15 minutes of mounting.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 5. Wireless Security
    # -----------------------------------------------------------------------
    {
        "id": "wireless_security",
        "order": 5,
        "title": "Wireless Security",
        "icon": "security",
        "what": (
            "Wireless security controls who can connect to your Wi-Fi and how their traffic is encrypted. "
            "WPA3 is the current standard — it encrypts each device's traffic individually, so even if "
            "one device is compromised, others on the same network aren't exposed. "
            "802.1X (RADIUS) goes further: instead of a shared Wi-Fi password, each user authenticates "
            "with their own credentials (username + password, or a device certificate), so you can "
            "revoke access for a departed employee without changing the Wi-Fi password."
        ),
        "why": (
            "WPA2 with a shared password has a critical flaw: anyone who knows the password can "
            "capture other users' traffic offline using the PMKID attack. WPA3 eliminates this. "
            "For business use, 802.1X means Wi-Fi credentials are tied to your identity provider — "
            "when you offboard an employee in Azure AD or Google Workspace, their Wi-Fi access "
            "is instantly revoked with no password rotation required."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "WPA3-Personal (UniFi built-in)",
                        "price": "Free — built into UniFi APs",
                        "role": "Wireless encryption standard",
                        "note": (
                            "Enable WPA3 (or WPA2/WPA3 transitional for devices older than 2018) on your "
                            "main SSID. This is the minimum acceptable security for a business Wi-Fi. "
                            "WPA3 uses SAE (Simultaneous Authentication of Equals) to prevent offline "
                            "dictionary attacks against captured handshakes."
                        ),
                    },
                    {
                        "name": "UniFi Guest Hotspot (built-in captive portal)",
                        "price": "Free — built into UniFi Network Controller",
                        "role": "Guest Wi-Fi authentication",
                        "note": (
                            "Guests see a branded splash page before getting internet access. "
                            "Optionally collects email for records. Isolates guest traffic from the "
                            "internal network at the VLAN level."
                        ),
                    },
                    {
                        "name": "FreeRADIUS (optional, self-hosted)",
                        "price": "Free / open-source (requires a Raspberry Pi or small VM)",
                        "role": "802.1X per-user Wi-Fi authentication",
                        "note": (
                            "Enables per-user Wi-Fi auth without a cloud identity provider. "
                            "Higher setup complexity — optional for Budget path but recommended "
                            "if you have any technical staff on hand."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "WPA2-Personal (legacy fallback only)",
                        "comparison": (
                            "Only use if you have devices older than 2018 that don't support WPA3. "
                            "If you must use WPA2, enable PMKID protection in UniFi settings."
                        ),
                    },
                    {
                        "name": "Cloudflare Access (Zero Trust Network Access)",
                        "comparison": (
                            "~$0–7/user/mo. Replaces corporate Wi-Fi auth with browser-based SSO. "
                            "More suited to cloud-first companies than traditional office environments."
                        ),
                    },
                ],
                "patching_notes": (
                    "WPA3 is a protocol standard — no separate patching needed. FreeRADIUS updates via "
                    "Linux package manager (apt update) — set a monthly reminder to patch the host OS. "
                    "UniFi controller updates (which include guest portal security fixes) ship with "
                    "firmware updates; apply the same way as AP/switch updates."
                ),
                "config_steps": [
                    "In UniFi Network Controller, open the 'YourCompany' SSID settings.",
                    "Set Security Protocol to 'WPA3' (or 'WPA2/WPA3' if older devices are in use).",
                    "For the Guest SSID: enable 'Client Device Isolation' (guests can't see each other).",
                    "Enable the UniFi Hotspot Portal — customize with your company name and logo.",
                    "Set guest session timeout (e.g. 8 hours) and bandwidth limits (e.g. 10 Mbps per client).",
                    "Optional FreeRADIUS: install on Ubuntu VM, configure with AP MAC addresses as RADIUS clients, test EAP-TTLS authentication.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "WPA3-Enterprise + Microsoft NPS (RADIUS)",
                        "price": "Free — NPS is included with Windows Server",
                        "role": "802.1X RADIUS authentication backed by Active Directory",
                        "note": (
                            "NPS (Network Policy Server) is Microsoft's RADIUS implementation. "
                            "Users authenticate to Wi-Fi with their domain credentials. "
                            "When an account is disabled in Active Directory, Wi-Fi access is immediately revoked — "
                            "no password rotation required."
                        ),
                    },
                    {
                        "name": "Azure AD (Entra ID) + Foxpass RADIUS proxy",
                        "price": "~$3/user/mo (Foxpass) + existing M365 license",
                        "role": "Cloud identity RADIUS authentication (no on-prem AD required)",
                        "note": (
                            "If you're cloud-first with no on-prem domain controller, Foxpass proxies "
                            "RADIUS requests to Azure AD. Enables MFA for Wi-Fi authentication."
                        ),
                    },
                    {
                        "name": "Okta RADIUS Agent",
                        "price": "~$4–8 / user / mo (included in some Okta tiers)",
                        "role": "Identity-provider-backed RADIUS via Okta",
                        "note": (
                            "If you use Okta for SSO, the Okta RADIUS Agent extends Okta identity to Wi-Fi. "
                            "Enables adaptive auth (block logins from unusual locations) and instant revocation."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Cisco ISE (Identity Services Engine)",
                        "comparison": (
                            "~$15,000+ deployment. Enterprise NAC — supports device compliance checks "
                            "(is this laptop patched?) before allowing Wi-Fi. Overkill for small teams; "
                            "right-sized for 100+ users with SOC 2 / PCI requirements."
                        ),
                    },
                    {
                        "name": "Aruba ClearPass",
                        "comparison": (
                            "Aruba's NAC solution, similar capability to Cisco ISE at lower cost. "
                            "~$5,000+ for a small deployment. Strong in HPE/Aruba environments."
                        ),
                    },
                ],
                "patching_notes": (
                    "Windows NPS: patch monthly with Windows Update (NPS is a Windows Server role — "
                    "it gets patched with the OS). Azure AD / Okta: SaaS, vendor-patched. "
                    "Rotate RADIUS shared secrets every 90 days. Audit RADIUS logs monthly for "
                    "failed auth spikes — these are early indicators of credential-stuffing attacks."
                ),
                "config_steps": [
                    "Deploy the Windows NPS role on a domain-joined server (or Azure VM for cloud AD).",
                    "Register each UniFi AP as a RADIUS client in NPS with a unique shared secret per AP.",
                    "Create NPS Network Policy: match 'Domain Users' group, require EAP-PEAP with MSCHAPv2.",
                    "In UniFi, set Company and Company-Dev SSIDs to WPA3-Enterprise; enter NPS server IP and shared secret.",
                    "Push 802.1X EAP configuration to managed devices via Group Policy or Microsoft Intune.",
                    "Test: connect a domain-joined device, verify it authenticates with domain credentials.",
                    "Enable RADIUS Accounting in NPS to log every Wi-Fi session (who, when, from which MAC).",
                    "Set up a RADIUS accounting log archive — required for compliance audits.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki WPA3 + Meraki Systems Manager (MDM)",
                        "price": "Included in MSP bundle",
                        "role": "Managed wireless security + device compliance enforcement",
                        "note": (
                            "Meraki Air Marshal monitors for rogue APs continuously. "
                            "Systems Manager (MDM) enforces device compliance (is antivirus running? is the OS patched?) "
                            "before allowing Wi-Fi access. MSP configures and monitors all security policies."
                        ),
                    },
                    {
                        "name": "Meraki Guest Portal (built-in captive portal)",
                        "price": "Included",
                        "role": "Guest authentication with email, SMS, or social login",
                        "note": "Configured by MSP. Options include email auth, SMS verification, and sponsored access.",
                    },
                ],
                "alternatives": [
                    {
                        "name": "Third-party captive portal (Cloudguest, Cucku Wi-Fi)",
                        "comparison": (
                            "More customization for branded guest portals. MSP integrates via Meraki splash URL. "
                            "Adds ~$20–50/mo but enables GDPR-compliant data capture for guest sessions."
                        ),
                    },
                ],
                "patching_notes": (
                    "MSP manages all wireless security configuration and Meraki firmware. "
                    "Request a monthly security report covering: rogue AP detections, failed auth attempts, "
                    "and policy changes made. This is your audit evidence — keep it on file."
                ),
                "config_steps": [
                    "Provide MSP with your identity provider details (Azure AD, Google Workspace) for RADIUS integration.",
                    "MSP configures WPA3 and guest portal during initial deployment.",
                    "MSP provisions read-only Meraki dashboard access for you.",
                    "On-site test: connect to the Guest SSID, verify splash page appears, verify guest cannot reach internal resources.",
                    "On-site test: connect to Company SSID with your credentials, verify authentication succeeds.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 6. VLANs & Segmentation
    # -----------------------------------------------------------------------
    {
        "id": "vlans_segmentation",
        "order": 6,
        "title": "VLANs & Segmentation",
        "icon": "vlan",
        "what": (
            "A VLAN (Virtual LAN) divides your single physical network into multiple isolated logical networks. "
            "Think of it like having separate hallways in your office: guests can't wander into the server room, "
            "VoIP phones can't interfere with data traffic, and an infected laptop on the guest network "
            "can't reach your file server. All of this happens on the same cables and switch hardware — "
            "VLANs are defined entirely in software."
        ),
        "why": (
            "Segmentation is the most impactful security control in a network. If ransomware lands on "
            "a guest laptop, a flat network (no VLANs) lets it spread to every other device instantly. "
            "With VLANs, the infected device is trapped in its segment — it can't reach your servers, "
            "printers, or other workstations. VLANs also let you apply different firewall policies "
            "per segment (VoIP gets QoS priority, IoT gets no internet access except manufacturer cloud)."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "VLANs via UniFi Network Controller + FortiGate",
                        "price": "Included — no additional cost",
                        "role": "Network segmentation — 3 VLANs",
                        "note": (
                            "Define VLANs in UniFi (switch + AP config), enforce inter-VLAN firewall "
                            "policies in FortiGate. A 3-VLAN design is sufficient and maintainable "
                            "for a 10-person office."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "VLANs are configuration, not software — no separate patching. Review VLAN assignments "
                    "quarterly: are new device types appearing (smart TVs, IoT sensors, cameras) that need "
                    "their own segment? Update FortiGate firewall policies whenever you add a new VLAN."
                ),
                "config_steps": [
                    "VLAN 10 — Data (default): all workstations and servers. Subnet 10.10.10.0/24. DHCP from FortiGate.",
                    "VLAN 20 — Guest: visitor devices, isolated internet-only. Subnet 10.10.20.0/24. Blocked from VLANs 10 and 30.",
                    "VLAN 30 — VoIP: IP phones and softphones. Subnet 10.10.30.0/24. QoS DSCP marking, SIP/RTP to carrier only.",
                    "FortiGate policy: Data → Internet: allow. Guest → Internet: allow. Guest → Data: deny. Guest → VoIP: deny.",
                    "VoIP policy: VLAN 30 → Internet: allow SIP/RTP ports only. Block all other outbound from VoIP VLAN.",
                    "Segmentation test: from a guest device, ping a Data VLAN address — should fail with no response.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "VLANs via UniFi + Palo Alto PA-400 (or FortiGate 60F)",
                        "price": "Included — no additional cost",
                        "role": "Network segmentation — 7 VLANs with zero-trust enforcement",
                        "note": (
                            "Zero-trust inter-VLAN routing: deny-all between all segments by default, "
                            "explicit allow rules only. Palo Alto App-ID enforces application-level "
                            "policies (not just port-based) — more granular and harder to bypass."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "Review inter-VLAN firewall policies monthly. As the team grows and new tools are "
                    "onboarded, update rules accordingly. Audit unused rules quarterly — rule bloat "
                    "creates security gaps and degrades firewall performance."
                ),
                "config_steps": [
                    "VLAN 10 — Data: workstations. 10.10.10.0/24.",
                    "VLAN 20 — Dev: developer machines and dev servers. 10.10.20.0/24. Deny-all to Data VLAN by default.",
                    "VLAN 30 — Guest: visitor devices. 10.10.30.0/24. Internet only, deny all internal traffic.",
                    "VLAN 40 — Management: firewalls, switches, APs. 10.10.40.0/24. Accessible only from Data VLAN admin accounts.",
                    "VLAN 50 — IoT: smart TVs, printers, sensors. 10.10.50.0/24. Internet allow-list: vendor cloud domains only.",
                    "VLAN 60 — VoIP: IP phones. 10.10.60.0/24. QoS DSCP EF, SIP/RTP to SIP carrier only.",
                    "VLAN 70 — Security Appliances: cameras, door access. 10.10.70.0/24. Isolated — no internet except vendor cloud.",
                    "Palo Alto security policy: each zone pair explicitly defined, deny-all implicit at bottom. Use App-ID for allow rules, not port numbers.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki VLANs (MSP-configured)",
                        "price": "Included in MSP bundle",
                        "role": "Managed network segmentation",
                        "note": (
                            "MSP designs and configures VLAN architecture based on your business requirements. "
                            "Meraki templates let them replicate the exact design across future locations "
                            "with zero reconfiguration time."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "Request a network segmentation diagram from your MSP showing each VLAN, its purpose, "
                    "and inter-VLAN firewall policies. This document is required for cyber insurance "
                    "applications and SOC 2 evidence packages."
                ),
                "config_steps": [
                    "Provide MSP with a complete list of device types (workstations, phones, cameras, IoT, printers) and their business purpose.",
                    "MSP designs VLAN architecture and presents it for your review and approval before deployment.",
                    "Review and sign off on the design — you own the security requirements even if the MSP owns the config.",
                    "Request quarterly VLAN policy reviews from your MSP as the business grows.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 7. NAT Rules
    # -----------------------------------------------------------------------
    {
        "id": "nat_rules",
        "order": 7,
        "title": "NAT Rules",
        "icon": "nat",
        "what": (
            "NAT (Network Address Translation) is what lets all your devices share a single public IP "
            "address from your ISP. Your ISP gives you one public IP (e.g. 203.0.113.50). "
            "NAT translates outbound traffic from internal addresses (10.10.10.x) to that public IP, "
            "then reverse-translates the response back to the right internal device. "
            "Port forwarding (DNAT) is the reverse: it maps a specific port on your public IP to a "
            "specific internal server — so external users can reach your VPN endpoint or web app."
        ),
        "why": (
            "Without NAT, you'd need a public IP for every single device — expensive and directly "
            "exposed to the internet. Port forwarding lets you host services (VPN, web apps) while "
            "keeping everything else hidden. Be conservative: every open port is a potential attack surface. "
            "Only forward ports that are actively needed, and document why."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "FortiGate NAT + Virtual IPs (built-in)",
                        "price": "Included with FortiGate 40F",
                        "role": "Source NAT (outbound) and Destination NAT / port forwarding",
                        "note": (
                            "FortiGate handles outbound NAT automatically. You only need to configure "
                            "explicit port forwarding rules for services you're hosting. "
                            "FortiGate calls port-forwarding rules 'Virtual IPs' (VIPs)."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "NAT rules are configuration, not software — no patching needed. Audit open port "
                    "forwards every 6 months. Close any ports no longer in use. "
                    "Document each rule: what service, who requested it, when it was created."
                ),
                "config_steps": [
                    "Source NAT (outbound): FortiGate auto-creates SNAT for all internal-to-internet traffic using the primary WAN IP. Verify this is working with a basic connectivity test.",
                    "Port forwarding (inbound): only create rules for explicitly needed services (e.g. VPN endpoint on UDP 51820).",
                    "For each port forward: create a Virtual IP (VIP) object in FortiGate mapping public-IP:port → internal-IP:port.",
                    "Create a firewall policy using that VIP as the destination, limited to the source IPs that need access (not 0.0.0.0/0 if avoidable).",
                    "NEVER forward RDP (TCP 3389) directly to the internet — require VPN access instead.",
                    "Test: from a cellular connection, verify intended services are reachable and unintended ports are blocked.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "Palo Alto NAT Policies (PA-400) or FortiGate NAT",
                        "price": "Included",
                        "role": "Source NAT, Destination NAT, and IP pool NAT",
                        "note": (
                            "Palo Alto evaluates security policy before NAT — architecturally cleaner "
                            "and harder to misconfigure. Supports IP pools for egress traffic diversity "
                            "when you have a subnet of public IPs from your ISP."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "Review asymmetric routing when adding NAT rules with dual ISPs — ensure return "
                    "traffic uses the same interface that received the request. Document every NAT rule: "
                    "purpose, requested by, approved by, and date created. This documentation is required "
                    "for SOC 2 change management evidence."
                ),
                "config_steps": [
                    "Define NAT source zones (trust) and destination zones (untrust) in Palo Alto.",
                    "Configure IP pools if ISP provides a public subnet — use for outbound NAT diversity.",
                    "Configure DNAT for any internet-facing services (apply source-IP restrictions wherever possible).",
                    "Verify security policy is evaluated before NAT (Palo Alto default behavior — do not change this).",
                    "Document every NAT rule with: purpose, requested by, approved by, and date created.",
                    "Test from external: verify intended ports respond, unintended ports are dropped (not rejected — drop is safer).",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki MX NAT (MSP-configured)",
                        "price": "Included",
                        "role": "Managed NAT and port forwarding",
                        "note": (
                            "MSP handles all NAT configuration. Submit port-forward requests via your "
                            "MSP ticketing system — MSP implements, documents, and confirms the change."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "All NAT changes go through your MSP's change management process. "
                    "Insist on a ticketing system — every port forward should have an approval record. "
                    "Review open port forwards with your MSP quarterly."
                ),
                "config_steps": [
                    "Submit NAT and port-forwarding requests to MSP via ticket, including: what service needs to be exposed, which internal server, which public port.",
                    "MSP implements, tests, and documents the change.",
                    "MSP provides change confirmation email — keep this as your approval record.",
                    "Review all open port forwards with your MSP quarterly and close any that are no longer needed.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 8. SD-WAN Rules
    # -----------------------------------------------------------------------
    {
        "id": "sdwan_rules",
        "order": 8,
        "title": "SD-WAN Rules",
        "icon": "sdwan",
        "what": (
            "SD-WAN (Software-Defined Wide Area Network) is an intelligent traffic director. "
            "When you have two internet connections, SD-WAN decides which one each type of traffic uses — "
            "automatically, in real time. A Zoom call needs low latency and no jitter, so SD-WAN routes it "
            "over whichever ISP performs best right now. Large backups can go over the cheaper or less-loaded "
            "connection. And if one ISP fails, SD-WAN switches traffic over within seconds."
        ),
        "why": (
            "Without SD-WAN, you either use one ISP (wasted capacity, single point of failure) or "
            "configure static routing that doesn't adapt. SD-WAN gives you automatic redundancy, "
            "better performance for latency-sensitive apps (VoIP, video conferencing), and ISP health "
            "visibility — all managed from a single dashboard. You're getting enterprise-grade WAN "
            "management at a startup budget."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "FortiGate SD-WAN (built into FortiOS)",
                        "price": "Included with FortiGate 40F — no extra license",
                        "role": "WAN steering, failover, per-application routing",
                        "note": (
                            "FortiGate's SD-WAN is surprisingly capable at this price point. "
                            "Per-application routing rules, link health monitoring with SLA-based "
                            "failover, and performance dashboards — no extra cost."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "UniFi Dream Machine Pro WAN failover",
                        "comparison": (
                            "Basic WAN failover with load balancing but no per-application routing "
                            "or SLA-based steering. Adequate for simple failover-only setups."
                        ),
                    },
                ],
                "patching_notes": (
                    "SD-WAN rules are configuration — no separate patching. Review monthly by checking "
                    "the FortiGate SD-WAN Performance dashboard: degrading ISP quality (rising latency, "
                    "jitter, or packet loss) shows up here before users start complaining."
                ),
                "config_steps": [
                    "Create an SD-WAN interface in FortiGate grouping WAN1 and WAN2.",
                    "Set SD-WAN member priority: WAN1 = 10 (primary), WAN2 = 20 (failover), LTE = 30 (last resort).",
                    "Create health-check probes on each WAN: ping 8.8.8.8 every 5 seconds.",
                    "Set SLA thresholds that trigger failover: latency >150ms, jitter >30ms, or packet loss >5%.",
                    "Create SD-WAN rules: VoIP and video → prefer lowest-latency WAN. All other → prefer highest-bandwidth WAN.",
                    "Enable session persistence (SD-WAN sticky sessions) so active downloads don't reset on failover.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "Palo Alto SD-WAN via Strata Cloud Manager",
                        "price": "~$200–400 / mo (Panorama or Strata Cloud Manager license)",
                        "role": "Multi-ISP orchestration with App-ID-aware routing",
                        "note": (
                            "Uses Palo Alto App-ID to identify applications (not just ports) and route them "
                            "based on real-time path quality. Centrally managed from Panorama or "
                            "Strata Cloud Manager — scales to multiple sites from one pane of glass."
                        ),
                    },
                    {
                        "name": "FortiGate 60F SD-WAN (if using FortiGate over PA-400)",
                        "price": "Included with FortiOS — no extra license",
                        "role": "Advanced SD-WAN with 3-WAN support and per-app SLA rules",
                        "note": (
                            "Add FortiManager (~$500/yr) for centralized SD-WAN management if you "
                            "have or plan multiple office locations."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Cisco Catalyst SD-WAN (Viptela)",
                        "comparison": (
                            "Enterprise-grade SD-WAN for multi-site deployments. ~$200–500/mo per site "
                            "including vManage. Overkill for a single location but industry standard for 10+ sites."
                        ),
                    },
                    {
                        "name": "Meraki MX SD-WAN",
                        "comparison": (
                            "Cloud-managed, excellent dashboard with drag-and-drop priority rules. "
                            "Right choice if already on the Meraki stack."
                        ),
                    },
                ],
                "patching_notes": (
                    "Palo Alto SD-WAN features receive updates via content releases (automated). "
                    "Review SD-WAN policy quarterly as your application portfolio grows — new apps may need "
                    "explicit steering rules. Audit path-quality logs for ISP degradation trends "
                    "(rising baseline latency often precedes a major outage by hours or days)."
                ),
                "config_steps": [
                    "Configure three WAN zones: ISP1, ISP2, LTE-Backup.",
                    "Define SLA profiles per traffic class: Realtime (VoIP) = <50ms latency, <1% loss; Business (SaaS) = <100ms; Bulk = best-effort.",
                    "Create App-ID-based traffic profiles: Microsoft Teams → Realtime profile. Microsoft 365 → Business profile. Backups/sync → Bulk profile.",
                    "Set path preference per rule: Realtime → prefer ISP1 or ISP2 based on real-time health; avoid LTE unless both wired ISPs fail.",
                    "Configure failback hysteresis: ISP must be stable for 30 seconds before returning traffic to avoid flapping.",
                    "Integrate with Palo Alto Strata Cloud Manager for centralized SD-WAN visibility and policy management.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki MX SD-WAN (MSP-managed)",
                        "price": "Included in MSP bundle",
                        "role": "Managed SD-WAN — MSP configures and monitors",
                        "note": (
                            "Meraki Dashboard shows real-time WAN health and auto-generates failover event reports. "
                            "MSP sets traffic steering rules and monitors for ISP degradation 24/7."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "MSP monitors SD-WAN performance and alerts on ISP degradation. "
                    "Request monthly WAN performance reports showing uptime percentage, average latency, "
                    "and all failover events with duration and cause."
                ),
                "config_steps": [
                    "Provide MSP with a list of critical business applications (video conferencing platform, VoIP provider, key SaaS tools).",
                    "MSP configures traffic steering rules optimized for your application profile.",
                    "During deployment sign-off, witness a live failover test — MSP pulls WAN1, you confirm traffic continues via WAN2.",
                    "MSP delivers monthly WAN health reports — review them; escalate any ISP that shows degradation trends.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 9. Monitoring & Incident Response
    # -----------------------------------------------------------------------
    {
        "id": "monitoring",
        "order": 9,
        "title": "Monitoring & Incident Response",
        "icon": "monitoring",
        "what": (
            "Network monitoring is your smoke detector. It watches your infrastructure 24/7 and alerts "
            "you when something is wrong — or better, when something is about to go wrong. "
            "A proper monitoring stack tracks: device availability (is the firewall up?), "
            "performance (is the WAN at 95% capacity?), security events (is someone scanning your internal network?), "
            "and change detection (did someone modify the firewall config at 2 AM?)."
        ),
        "why": (
            "Most breaches are detected weeks or months after the attacker gained initial access. "
            "Monitoring closes that gap: unusual traffic patterns, failed login spikes, or unexpected "
            "config changes are often the first visible signs of an active intrusion. "
            "Performance monitoring catches ISP degradation and bandwidth saturation before users "
            "start complaining — you want to know about the problem before your CEO does."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "SolarWinds Observability (free tier)",
                        "price": "Free for up to 5 monitored nodes",
                        "role": "Network performance monitoring and alerting",
                        "note": (
                            "Monitors WAN availability, bandwidth utilization, and alerts on thresholds. "
                            "Free tier covers a small office's firewall and switch. "
                            "Upgrade to paid (~$29/mo) when you exceed 5 monitored devices."
                        ),
                    },
                    {
                        "name": "UniFi Network Dashboard (built-in)",
                        "price": "Free — included with UniFi controller",
                        "role": "LAN and Wi-Fi visibility",
                        "note": (
                            "Shows all connected clients, per-client bandwidth, AP health, "
                            "switch port utilization, and event logs. Sufficient for day-to-day "
                            "visibility of everything on the LAN side."
                        ),
                    },
                    {
                        "name": "FortiCloud (free tier)",
                        "price": "Free — 7-day log retention included with FortiGate",
                        "role": "Firewall log visibility and security event review",
                        "note": (
                            "Sends FortiGate logs to Fortinet's cloud. Reveals blocked connections, "
                            "IPS alerts, and firewall policy hits. Upgrade to paid FortiCloud for "
                            "30-day retention, which is recommended for incident investigation."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Grafana + Prometheus (self-hosted)",
                        "comparison": (
                            "Free, open-source, very powerful. Requires a dedicated server and meaningful "
                            "setup time. Right choice if you have technical staff who want full control "
                            "over dashboards and metrics retention."
                        ),
                    },
                    {
                        "name": "Uptime Robot",
                        "comparison": (
                            "Free tier monitors 50 endpoints with 5-minute intervals. Good for external "
                            "service monitoring (is your website up?). Not a substitute for internal "
                            "network monitoring."
                        ),
                    },
                ],
                "patching_notes": (
                    "SolarWinds Observability is SaaS — vendor-patched. FortiCloud: no local patching. "
                    "UniFi Controller: update with firmware releases. More important than patching: "
                    "keep alert thresholds tuned. Revisit every 90 days to eliminate false positives "
                    "that cause alert fatigue."
                ),
                "config_steps": [
                    "Sign up for SolarWinds Observability free tier at solarwinds.com.",
                    "Configure SNMP v2c on FortiGate (System > SNMP) and add the FortiGate as a monitored node in SolarWinds.",
                    "Add the UniFi switch as a monitored node.",
                    "Create alerts: WAN latency >50ms, WAN packet loss >1%, any monitored device offline >2 minutes.",
                    "Configure alert delivery to email or Slack.",
                    "In FortiGate, enable FortiCloud logging: Security Fabric > Logging > FortiCloud.",
                    "Create a simple incident response runbook (one page): who gets the alert, what to check first, who to call if it looks like a breach.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "SolarWinds NPM (Network Performance Monitor)",
                        "price": "~$12–25 / mo (SaaS) or $2,000+ perpetual (self-hosted)",
                        "role": "Full-stack network monitoring with topology maps and capacity planning",
                        "note": (
                            "Auto-discovers network topology, creates visual maps, tracks performance over time. "
                            "SNMP polling across all managed devices. Integrates with PagerDuty and ServiceNow "
                            "for incident management workflows."
                        ),
                    },
                    {
                        "name": "Palo Alto Cortex XDR or FortiAnalyzer",
                        "price": "~$100–200 / mo",
                        "role": "Security event monitoring and threat correlation",
                        "note": (
                            "Aggregates logs from firewall, endpoints, and APs into a unified security "
                            "event timeline. Detects lateral movement, unusual traffic patterns, and policy "
                            "violations. Required for SOC 2 or ISO 27001 compliance evidence."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Datadog Network Performance Monitoring",
                        "comparison": (
                            "~$5/host/mo. Strong if already using Datadog for application monitoring — "
                            "unifies network and application observability. Less network-specific than SolarWinds NPM."
                        ),
                    },
                    {
                        "name": "PRTG Network Monitor",
                        "comparison": (
                            "~$1,800 perpetual for 500 sensors. Long-standing enterprise tool with "
                            "excellent SNMP support. More mature on-prem deployment model than SolarWinds SaaS."
                        ),
                    },
                ],
                "patching_notes": (
                    "SolarWinds: apply quarterly patches within 30 days. Note: SolarWinds was the vector "
                    "for the 2020 SUNBURST supply-chain attack — their security practices have significantly "
                    "improved since, but this warrants ongoing vendor due diligence. "
                    "FortiAnalyzer: patch with FortiOS releases. Cortex XDR: SaaS, auto-patched by Palo Alto."
                ),
                "config_steps": [
                    "Deploy SolarWinds NPM (SaaS recommended for small teams; self-hosted if data residency matters).",
                    "Configure SNMPv3 on all managed devices with unique credentials per device.",
                    "Add all devices to SolarWinds for polling.",
                    "Integrate alerts with PagerDuty or Slack; set up on-call rotation.",
                    "Deploy FortiAnalyzer (VM or SaaS) and configure FortiGate syslog to point to it.",
                    "Create correlation rules: alert on >5 failed logins in 60 seconds; alert on any management VLAN access from non-management subnet.",
                    "Write an incident response playbook: breach indicators, containment steps, contact list, communication templates.",
                    "Run a quarterly tabletop exercise simulating a ransomware event using the playbook — update it based on what you learn.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "Meraki Dashboard Monitoring (built-in to Meraki stack)",
                        "price": "Included in Meraki license",
                        "role": "Real-time device health and client visibility",
                        "note": (
                            "Meraki provides real-time device health, client connection logs, and event history. "
                            "Your MSP monitors this 24/7 and receives alerts automatically."
                        ),
                    },
                    {
                        "name": "MSP-managed SolarWinds or Datto RMM",
                        "price": "Included in MSP monthly fee",
                        "role": "Proactive alerting and incident response by MSP",
                        "note": (
                            "MSP receives alerts and responds within contracted SLA (typically 1 hour for critical). "
                            "You receive an incident report after resolution — keep these reports for compliance evidence."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Read-only access to MSP monitoring dashboard",
                        "comparison": (
                            "Ask your MSP for read-only access to their monitoring dashboard. "
                            "You should be able to see device health and alerts without making changes. "
                            "Any MSP that refuses this is a red flag."
                        ),
                    },
                ],
                "patching_notes": (
                    "MSP owns all monitoring infrastructure. You should receive: monthly performance reports, "
                    "quarterly security reviews, and immediate notification (within 1 hour) for any "
                    "security incident. These SLAs must be in your MSP contract — if they're not, add them."
                ),
                "config_steps": [
                    "Define alert SLAs with MSP: which events trigger immediate notification to you vs. auto-resolved by MSP.",
                    "Request read-only access to monitoring dashboard during onboarding.",
                    "Establish incident response chain: who does MSP contact first if they detect a breach? Who on your side can approve emergency changes?",
                    "Schedule quarterly security review meetings with MSP to walk through incident trends and open items.",
                ],
            },
        },
    },

    # -----------------------------------------------------------------------
    # 10. Test & Verify
    # -----------------------------------------------------------------------
    {
        "id": "test_verify",
        "order": 10,
        "title": "Test & Verify",
        "icon": "test",
        "what": (
            "Testing is how you prove the network actually does what you think it does — not just "
            "what the configuration looks like it should do. Network configs have a way of having gaps: "
            "a VLAN that was supposed to be isolated but isn't, a firewall rule that accidentally allows "
            "too much, a failover that works but takes 5 minutes instead of 30 seconds. "
            "Testing finds these gaps before an attacker or an outage does."
        ),
        "why": (
            "You can't trust what you haven't tested. A firewall policy that looks correct in the UI "
            "might have an implicit allow rule that overrides your intent. Testing also establishes a "
            "baseline — 'the WAN normally uses 40% capacity at 2 PM on Tuesdays' — so you'll notice "
            "when that number doubles without explanation. Document your test results: this is your "
            "network baseline and your audit evidence."
        ),
        "recommendations": {
            "budget_diy": {
                "products": [
                    {
                        "name": "nmap (free, open-source)",
                        "price": "Free",
                        "role": "Port scanning and network discovery",
                        "note": (
                            "Run from outside your network (phone on LTE or a cloud VM) to verify what "
                            "ports are externally visible. Run internally to discover unexpected open "
                            "services. The most useful tool in the network engineer's toolkit."
                        ),
                    },
                    {
                        "name": "iPerf3 (free, open-source)",
                        "price": "Free",
                        "role": "Bandwidth and throughput measurement",
                        "note": (
                            "Install on two devices, run a test between them — confirms your switch and APs "
                            "are delivering the expected bandwidth. Good for identifying underperforming cables "
                            "or misconfigured interfaces."
                        ),
                    },
                    {
                        "name": "Wireshark (free, open-source)",
                        "price": "Free",
                        "role": "Packet capture and traffic analysis",
                        "note": (
                            "Captures packets to verify VLAN tagging is correct, DHCP is working per segment, "
                            "and no unexpected broadcasts are crossing VLAN boundaries."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "Testing is ongoing — not a one-time event. Run the full test suite: after any config "
                    "change, after firmware updates, and at least quarterly as a baseline check. "
                    "Document all results with timestamps."
                ),
                "config_steps": [
                    "External scan: from a cellular connection (not your office Wi-Fi), run: nmap -sV -p 1-65535 [your-public-IP]. Verify only intended ports are open.",
                    "Internal discovery: from Data VLAN, run: nmap -sn 10.10.0.0/16 to find all devices on all subnets. Investigate unexpected hosts.",
                    "Segmentation test: from a Guest VLAN device, attempt to ping a Data VLAN address (e.g. 10.10.10.1) — must fail.",
                    "Segmentation test: from Guest VLAN, attempt to browse to your switch management UI — must fail.",
                    "Failover test: physically unplug the WAN1 cable. Confirm all traffic shifts to WAN2 within 30 seconds. Plug WAN1 back in and confirm it returns as primary.",
                    "Wi-Fi test: connect to Guest SSID, verify internet works; verify internal resources (file shares, printers) are unreachable.",
                    "Throughput test: run iPerf3 between two wired devices; compare to your ISP speed — should be within 5% of expected.",
                    "Document all test results with timestamps — this is your network baseline for future comparison.",
                ],
            },
            "enterprise_diy": {
                "products": [
                    {
                        "name": "Nessus Essentials (free for up to 16 IPs)",
                        "price": "Free for non-commercial use",
                        "role": "Vulnerability scanning across all VLAN subnets",
                        "note": (
                            "Scans for known CVEs, misconfigured services, default credentials, and "
                            "unpatched software. Run monthly or after any major config change. "
                            "Identifies gaps your firewall rules can't see (application-layer vulnerabilities)."
                        ),
                    },
                    {
                        "name": "SolarWinds NPM Baseline Reports",
                        "price": "Included in SolarWinds subscription",
                        "role": "Automated performance baselining and anomaly detection",
                        "note": (
                            "SolarWinds auto-generates performance baselines over 30 days. "
                            "Compare current utilization against baselines to detect anomalies "
                            "that may indicate a security event or capacity issue."
                        ),
                    },
                ],
                "alternatives": [
                    {
                        "name": "Qualys FreeScan",
                        "comparison": (
                            "Free external vulnerability scan from the internet. Shows what an attacker "
                            "sees from outside. Good complement to internal Nessus scans."
                        ),
                    },
                    {
                        "name": "Tenable.io",
                        "comparison": (
                            "~$200–400/mo. Continuous vulnerability management with CVSS scoring and "
                            "remediation tracking. Right choice for compliance environments."
                        ),
                    },
                ],
                "patching_notes": (
                    "Run Nessus scans on a recurring schedule — not just when you think something changed. "
                    "Prioritize findings by CVSS score: Critical (9.0+) within 24 hours, High (7.0+) within "
                    "7 days, Medium within 30 days. Patch outside these windows only if there's a documented "
                    "business reason."
                ),
                "config_steps": [
                    "Run all Budget DIY tests first — they are the foundation.",
                    "Run Nessus Essentials scan on all 7 VLAN subnets. Remediate all Critical and High findings before considering the build complete.",
                    "Test 802.1X: connect an unauthorized device to the corporate SSID — should receive an EAP-Failure and be denied access.",
                    "Zero-trust test: from each VLAN, attempt to reach every other VLAN. Document which paths are allowed vs. blocked and confirm it matches your policy documentation.",
                    "Run iPerf3 between each VLAN pair to baseline inter-VLAN throughput.",
                    "Test all three ISP failover scenarios: WAN1 down (WAN2 active), WAN2 down (WAN1 only), both wired down (LTE only).",
                    "Test SD-WAN traffic steering: verify VoIP traffic takes the lowest-latency path using a packet capture or SD-WAN dashboard.",
                    "Test monitoring alerts: manually trigger a condition (disconnect a monitored device) and verify the alert fires within the configured threshold.",
                    "Produce a signed network baseline document before the build goes live.",
                ],
            },
            "outsourced": {
                "products": [
                    {
                        "name": "MSP-conducted formal acceptance testing",
                        "price": "Included in MSP deployment fee",
                        "role": "Documented network acceptance testing before go-live",
                        "note": (
                            "Your MSP runs the test suite as part of deployment. Be present (or have a "
                            "technical contact on-site) to witness the tests. Do NOT sign deployment "
                            "acceptance until testing is complete and documented."
                        ),
                    },
                ],
                "alternatives": [],
                "patching_notes": (
                    "Request a formal test report from your MSP before signing deployment acceptance. "
                    "This document is your network baseline and is required for cyber insurance applications "
                    "and compliance audits. If the MSP won't provide it, find a new MSP."
                ),
                "config_steps": [
                    "Request a written test plan from MSP before deployment day — know exactly what will be tested.",
                    "Be present (or have a technical point-of-contact on-site) during all failover testing.",
                    "Verify: Guest Wi-Fi works, Corporate Wi-Fi works, internet is reachable from all expected VLANs.",
                    "Verify segmentation: from Guest network, attempt to access internal resources — confirm failure.",
                    "Witness failover test: MSP disconnects primary ISP, you confirm traffic continues within agreed SLA window.",
                    "Do not sign deployment acceptance until all tests pass and MSP delivers the written test results.",
                    "Schedule a 30-day check-in call with MSP to review early performance data.",
                ],
            },
        },
    },

]  # end BUILD_STEPS
