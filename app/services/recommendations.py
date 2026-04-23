def get_risk_level(global_risk):
    if global_risk >= 0.70:
        return "High Risk"
    elif global_risk >= 0.45:
        return "Medium Risk"
    else:
        return "Low Risk"


def get_key_weaknesses(data, derived):
    weaknesses = []

    if derived["runway"] < 6:
        weaknesses.append({"icon": "💰", "label": "Low Cash Reserves", "variable": "runway"})
    if derived["financial_stress"] > 0.6:
        weaknesses.append({"icon": "🔥", "label": "High Financial Stress", "variable": "financial_stress"})

    if data.pmf_score < 0.5:
        weaknesses.append({"icon": "📉", "label": "Poor Product-Market Fit", "variable": "pmf_score"})
    if derived["market_fit"] < 0.4:
        weaknesses.append({"icon": "🎯", "label": "Weak Market Fit Score", "variable": "market_fit"})
    if derived["growth_rate"] < 0.3:
        weaknesses.append({"icon": "📊", "label": "Low Growth Rate", "variable": "growth_rate"})
    if data.retention_rate < 0.4:
        weaknesses.append({"icon": "🔄", "label": "Low User Retention", "variable": "retention_rate"})
    if data.traction < 0.3:
        weaknesses.append({"icon": "📈", "label": "Insufficient Market Traction", "variable": "traction"})

    if data.adaptability < 0.4:
        weaknesses.append({"icon": "🔀", "label": "Low Adaptability", "variable": "adaptability"})
    if data.decision_delay > 5:
        weaknesses.append({"icon": "⏱️", "label": "Slow Decision-Making", "variable": "decision_delay"})
    if derived["decision_quality"] < 0.4:
        weaknesses.append({"icon": "🧠", "label": "Poor Decision Quality", "variable": "decision_quality"})
    if derived["timing_score"] < 0.4:
        weaknesses.append({"icon": "⏰", "label": "Bad Market Timing", "variable": "timing_score"})

    if data.team_strength < 0.5:
        weaknesses.append({"icon": "👥", "label": "Team Leadership Issues", "variable": "team_strength"})
    if derived["execution_capability"] < 0.4:
        weaknesses.append({"icon": "⚡️", "label": "Weak Execution Capability", "variable": "execution_capability"})
    if derived["governance_score"] < 0.4:
        weaknesses.append({"icon": "🏛", "label": "Poor Governance", "variable": "governance_score"})

    if data.tech_debt > 0.6:
        weaknesses.append({"icon": "⚙️", "label": "High Technical Debt", "variable": "tech_debt"})
    if derived["reliability"] < 0.4:
        weaknesses.append({"icon": "🛡", "label": "Low System Reliability", "variable": "reliability"})
    if derived["maintenance_cost"] > 0.6:
        weaknesses.append({"icon": "🔧", "label": "High Maintenance Cost", "variable": "maintenance_cost"})
    if data.scalability < 0.4:
        weaknesses.append({"icon": "📡", "label": "Poor Scalability", "variable": "scalability"})

    if data.regulatory_risk > 0.6:
        weaknesses.append({"icon": "⚖️", "label": "High Regulatory Risk", "variable": "regulatory_risk"})
    if derived["shock_probability"] > 0.6:
        weaknesses.append({"icon": "🌪", "label": "High Shock Probability", "variable": "shock_probability"})
    if derived["compliance_cost"] > 0.6:
        weaknesses.append({"icon": "📋", "label": "High Compliance Cost", "variable": "compliance_cost"})
    if data.external_shock > 0.6:
        weaknesses.append({"icon": "💥", "label": "High External Shock Exposure", "variable": "external_shock"})

    return weaknesses


def get_recommendation_cards(data, derived):
    cards = []

    high_actions = []
    if derived["runway"] < 3:
        high_actions.append("Secure Emergency Funding immediately")
    if derived["financial_stress"] > 0.8:
        high_actions.append("Reduce operational costs drastically")
    if data.pmf_score < 0.3:
        high_actions.append("Pivot to Find Market Fit")
    if derived["market_fit"] < 0.3:
        high_actions.append("Redefine your target customer segment")
    if data.team_strength < 0.3:
        high_actions.append("Address Leadership Gaps urgently")
    if derived["decision_quality"] < 0.3:
        high_actions.append("Restructure decision-making processes")
    if data.retention_rate < 0.2:
        high_actions.append("Fix critical user experience issues")
    if high_actions:
        cards.append({"title": "Urgent Action Needed", "priority": "HIGH", "color": "red", "actions": high_actions})

    medium_actions = []
    if data.burn_rate > data.cash * 0.15:
        medium_actions.append("Cut Unnecessary Costs")
    if data.traction < 0.4:
        medium_actions.append("Optimize Marketing Spend")
    if derived["runway"] < 9:
        medium_actions.append("Extend Runway Period")
    if derived["growth_rate"] < 0.4:
        medium_actions.append("Accelerate Revenue Growth Strategies")
    if derived["financial_stress"] > 0.5:
        medium_actions.append("Improve Cash Flow Management")
    if medium_actions:
        cards.append({"title": "Improve Financial Efficiency", "priority": "MEDIUM", "color": "orange", "actions": medium_actions})

    team_actions = []
    if data.team_strength < 0.5:
        team_actions.append("Provide Leadership Training")
    if derived["governance_score"] < 0.4:
        team_actions.append("Strengthen Team Collaboration")
    if derived["execution_capability"] < 0.4:
        team_actions.append("Hire Experienced Advisors")
    if data.decision_delay > 5:
        team_actions.append("Implement Faster Decision Frameworks")
    if derived["timing_score"] < 0.4:
        team_actions.append("Improve Strategic Timing Awareness")
    if team_actions:
        cards.append({"title": "Enhance Team Skills", "priority": "MEDIUM", "color": "blue", "actions": team_actions})

    tech_actions = []
    if data.tech_debt > 0.5:
        tech_actions.append("Schedule Technical Debt Reduction Sprints")
    if derived["reliability"] < 0.5:
        tech_actions.append("Improve System Reliability and Stability")
    if derived["maintenance_cost"] > 0.5:
        tech_actions.append("Optimize Maintenance Processes")
    if data.scalability < 0.4:
        tech_actions.append("Redesign Scalable Architecture")
    if tech_actions:
        cards.append({"title": "Improve Technical Performance", "priority": "LOW", "color": "purple", "actions": tech_actions})

    external_actions = []
    if data.regulatory_risk > 0.6:
        external_actions.append("Consult Legal and Compliance Experts")
    if derived["compliance_cost"] > 0.6:
        external_actions.append("Reduce Compliance Cost Exposure")
    if derived["shock_probability"] > 0.6:
        external_actions.append("Build Business Continuity Plans")
    if data.external_shock > 0.6:
        external_actions.append("Diversify Revenue Streams")
    if external_actions:
        cards.append({"title": "Manage External Risks", "priority": "LOW", "color": "gray", "actions": external_actions})

    if not cards:
        cards.append({
            "title": "Keep Up the Good Work",
            "priority": "LOW",
            "color": "green",
            "actions": [
                "Continue monitoring your KPIs regularly",
                "Focus on scaling your growth channels",
                "Maintain financial discipline",
            ],
        })

    return cards



def get_strategic_summary(data, derived, global_risk):
    issues = []
    if derived["runway"] < 6:
        issues.append("securing funding")
    if derived["market_fit"] < 0.4 or data.pmf_score < 0.5:
        issues.append("finding market fit")
    if derived["financial_stress"] > 0.5:
        issues.append("optimizing costs")
    if data.team_strength < 0.5 or derived["governance_score"] < 0.4:
        issues.append("strengthening your team")
    if derived["reliability"] < 0.4 or data.tech_debt > 0.6:
        issues.append("reducing technical debt")
    if derived["shock_probability"] > 0.6 or data.regulatory_risk > 0.6:
        issues.append("managing external risks")

    if not issues:
        return "Your startup shows strong fundamentals. Focus on scaling efficiently while maintaining operational excellence."

    if len(issues) == 1:
        return f"Focus on {issues[0]} to improve your startup's chances of success and ensure sustainable long-term growth."

    main = ", ".join(issues[:-1])
    last = issues[-1]
    return f"Focus on {main} and {last} for sustainable growth."


def generate_recommendation_report(data, derived, risk_scores):
    global_risk = risk_scores["global_risk"]
    return {
        "risk_level": get_risk_level(global_risk),
        "risk_score": global_risk,
        "key_weaknesses": get_key_weaknesses(data, derived),
        "recommendation_cards": get_recommendation_cards(data, derived),
        "strategic_summary": get_strategic_summary(data, derived, global_risk),
    }