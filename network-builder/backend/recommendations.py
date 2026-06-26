"""
recommendations.py — Recommendation engine.

Routes questionnaire answers to one of three build paths and assembles
the full response payload. Keeping this logic in its own module (separate
from app.py and data.py) makes it easy to unit-test the routing rules
without spinning up the Flask server.
"""

from data import PATHS, BUILD_STEPS, SOURCES


# Valid values for each field — used for input validation in app.py
VALID_BUSINESS_TYPES = ["startup"]
VALID_SIZES = ["1-10", "11-50", "51+"]
VALID_BUDGETS = ["budget_conscious", "enterprise"]
VALID_MANAGEMENT_STYLES = ["diy", "outsourced"]


def determine_path(business_type: str, size: str, budget: str, management_style: str) -> str:
    """
    Route questionnaire answers to one of the three build paths.

    Routing logic:
      outsource flag → outsourced  (management preference overrides budget)
      enterprise budget → enterprise_diy
      budget_conscious → budget_diy

    Adding a new path: add it to PATHS in data.py, then add a branch here.
    """
    if management_style == "outsourced":
        return "outsourced"
    if budget == "enterprise":
        return "enterprise_diy"
    return "budget_diy"


def build_recommendation(
    business_type: str,
    size: str,
    budget: str,
    management_style: str,
) -> dict:
    """
    Assemble a complete recommendation payload for the frontend.

    Returns a dict containing:
      path         — the selected path ID
      path_info    — metadata about that path (name, costs, description)
      steps        — 10 build steps with path-specific products and guidance
      sources      — vendor links for the summary screen
    """
    path_id = determine_path(business_type, size, budget, management_style)
    path_info = PATHS[path_id]

    # Surface the path-specific recommendation for each step at the top level
    # so the frontend doesn't need to know about the recommendations dict structure.
    steps = []
    for step in BUILD_STEPS:
        path_rec = step["recommendations"][path_id]
        steps.append({
            "id": step["id"],
            "order": step["order"],
            "title": step["title"],
            "icon": step["icon"],
            "what": step["what"],
            "why": step["why"],
            "products": path_rec["products"],
            "alternatives": path_rec["alternatives"],
            "patching_notes": path_rec["patching_notes"],
            "config_steps": path_rec["config_steps"],
        })

    return {
        "path": path_id,
        "path_info": path_info,
        "steps": steps,
        "sources": SOURCES,
        # Echo the inputs back so the frontend can display a summary of choices
        "inputs": {
            "business_type": business_type,
            "size": size,
            "budget": budget,
            "management_style": management_style,
        },
    }
