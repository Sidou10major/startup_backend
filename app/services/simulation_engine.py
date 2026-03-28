from copy import deepcopy


ALLOWED_DECISIONS = {
    "reduce_costs": {
        "label": "Reduce Costs",
        "description": "Decrease burn rate and slightly improve adaptability."
    },
    "increase_marketing": {
        "label": "Increase Marketing",
        "description": "Increase burn rate but improve traction and product-market fit."
    },
    "hire_team": {
        "label": "Hire Team",
        "description": "Increase burn rate but improve team strength and reduce decision delay."
    },
    "improve_product": {
        "label": "Improve Product",
        "description": "Increase burn rate slightly, improve PMF and retention, reduce tech debt."
    },
    "refactor_technology": {
        "label": "Refactor Technology",
        "description": "Reduce tech debt and improve scalability with a small increase in burn rate."
    },
    "delay_decision": {
        "label": "Delay Decision",
        "description": "Postpone action, increasing delay and slightly hurting PMF and traction."
    },
    "seek_investment": {
        "label": "Seek Investment",
        "description": "Increase available cash, but decision-making becomes slightly slower."
    },
    "expand_too_fast": {
        "label": "Expand Too Fast",
        "description": "Increase burn rate and tech debt, while weakening team balance and scalability."
    },
    "ignore_regulation": {
        "label": "Ignore Regulation",
        "description": "Increase regulatory risk."
    },
    "do_nothing": {
        "label": "Do Nothing",
        "description": "Keep the startup state unchanged."
    },
}


def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))


def get_allowed_decisions():
    return [
        {
            "key": key,
            "label": value["label"],
            "description": value["description"],
        }
        for key, value in ALLOWED_DECISIONS.items()
    ]


def apply_decision(state, decision: str):
    if decision not in ALLOWED_DECISIONS:
        raise ValueError(f"Invalid decision: {decision}")

    updated = deepcopy(state)

    if decision == "reduce_costs":
        updated.burn_rate *= 0.85
        updated.adaptability = clamp(updated.adaptability + 0.05)

    elif decision == "increase_marketing":
        updated.burn_rate *= 1.15
        updated.traction = clamp(updated.traction + 0.10)
        updated.pmf_score = clamp(updated.pmf_score + 0.05)

    elif decision == "hire_team":
        updated.burn_rate *= 1.20
        updated.team_strength = clamp(updated.team_strength + 0.10)
        updated.decision_delay = max(0, updated.decision_delay - 1)

    elif decision == "improve_product":
        updated.burn_rate *= 1.10
        updated.pmf_score = clamp(updated.pmf_score + 0.12)
        updated.retention_rate = clamp(updated.retention_rate + 0.08)
        updated.tech_debt = clamp(updated.tech_debt - 0.05)

    elif decision == "refactor_technology":
        updated.burn_rate *= 1.05
        updated.tech_debt = clamp(updated.tech_debt - 0.15)
        updated.scalability = clamp(updated.scalability + 0.10)

    elif decision == "delay_decision":
        updated.decision_delay += 2
        updated.pmf_score = clamp(updated.pmf_score - 0.05)
        updated.traction = clamp(updated.traction - 0.05)

    elif decision == "seek_investment":
        updated.cash *= 1.40
        updated.decision_delay += 1

    elif decision == "expand_too_fast":
        updated.burn_rate *= 1.30
        updated.tech_debt = clamp(updated.tech_debt + 0.10)
        updated.team_strength = clamp(updated.team_strength - 0.05)
        updated.scalability = clamp(updated.scalability - 0.05)

    elif decision == "ignore_regulation":
        updated.regulatory_risk = clamp(updated.regulatory_risk + 0.20)

    elif decision == "do_nothing":
        pass

    return updated