/**
 * recommendations.js — JS port of the Python recommendation engine.
 *
 * Mirrors the routing logic from backend/recommendations.py so the app
 * can run as a pure static site without the Flask backend.
 */

import networkData from "./networkData.json";

const { PATHS, BUILD_STEPS, SOURCES } = networkData;

function determinePath(managementStyle, budget) {
  if (managementStyle === "outsourced") return "outsourced";
  if (budget === "enterprise") return "enterprise_diy";
  return "budget_diy";
}

export function buildRecommendation({ business_type, size, budget, management_style }) {
  const pathId = determinePath(management_style, budget);
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
      products: pathRec.products,
      alternatives: pathRec.alternatives,
      patching_notes: pathRec.patching_notes,
      config_steps: pathRec.config_steps,
    };
  });

  return {
    path: pathId,
    path_info: pathInfo,
    steps,
    sources: SOURCES,
    inputs: { business_type, size, budget, management_style },
  };
}
