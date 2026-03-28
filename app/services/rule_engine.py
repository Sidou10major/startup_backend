def evaluate_rule_based(data):
    runway = data.cash / data.burn_rate
    risk_score = 0.0
    reasons = []

    # Financial
    if runway < 3:
        risk_score += 0.30
        reasons.append("Low runway (< 3 months)")
    elif runway < 6:
        risk_score += 0.15
        reasons.append("Moderate runway (< 6 months)")

    # Market
    if data.pmf_score < 0.4:
        risk_score += 0.25
        reasons.append("Weak product-market fit")

    # Strategic
    if data.decision_delay > 6:
        risk_score += 0.15
        reasons.append("High decision delay")

    # Organizational
    if data.team_strength < 0.5:
        risk_score += 0.15
        reasons.append("Weak team strength")

    # Technological
    if data.tech_debt > 0.6:
        risk_score += 0.10
        reasons.append("High technical debt")

    # External
    if data.regulatory_risk > 0.7:
        risk_score += 0.05
        reasons.append("High regulatory risk")

    if risk_score >= 0.60:
        risk_level = "HIGH"
    elif risk_score >= 0.30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "runway": round(runway, 2),
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "reasons": reasons,
    }