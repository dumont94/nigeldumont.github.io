/**
 * recommendations.js — Routing logic for the SOC Foundations Builder.
 *
 * Maps questionnaire answers to one of three SOC build paths:
 *   - microsoft_native  — M365/Azure shops: Defender XDR + Sentinel
 *   - open_source       — lean budgets: Wazuh, Security Onion, CISA free services
 *   - best_of_breed     — funded orgs: CrowdStrike, Splunk, Tenable, Proofpoint
 *
 * Environment wins first (a Microsoft shop should exhaust its licensing
 * before buying anything), then budget decides between open-source and
 * best-of-breed for everyone else.
 */

import socData from "./socData.json";

const { PATHS, BUILD_STEPS, SOURCES } = socData;

function determinePath(environment, budget) {
  if (environment === "m365") return "microsoft_native";
  if (budget === "funded") return "best_of_breed";
  return "open_source";
}

export function buildRecommendation({ environment, size, maturity, budget }) {
  const pathId = determinePath(environment, budget);
  const pathInfo = PATHS[pathId];

  const steps = BUILD_STEPS.map((step) => {
    const pathRec = step.recommendations[pathId];
    return {
      id: step.id,
      order: step.order,
      title: step.title,
      icon: step.icon,
      what: step.what,
      why: step.why,
      day_one: step.day_one,
      products: pathRec.products,
      alternatives: pathRec.alternatives,
      ops_notes: pathRec.ops_notes,
      config_steps: pathRec.config_steps,
    };
  });

  return {
    path: pathId,
    path_info: pathInfo,
    steps,
    sources: SOURCES,
    inputs: { environment, size, maturity, budget },
  };
}
