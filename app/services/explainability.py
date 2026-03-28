from app.services.ml_model import model, feature_columns, prepare_features


def explain_decision_tree(data):
    X, feature_map = prepare_features(data)

    node_indicator = model.decision_path(X)
    leaf_id = model.apply(X)[0]

    feature = model.tree_.feature
    threshold = model.tree_.threshold

    reasons = []

    node_index = node_indicator.indices[
        node_indicator.indptr[0] : node_indicator.indptr[1]
    ]

    for node_id in node_index:
        if leaf_id == node_id:
            continue

        feature_idx = feature[node_id]
        if feature_idx == -2:
            continue

        feature_name = feature_columns[feature_idx]
        threshold_value = threshold[node_id]
        actual_value = feature_map[feature_name]

        if actual_value <= threshold_value:
            rule_text = (
                f"{feature_name} = {round(actual_value, 4)} <= {round(threshold_value, 4)}"
            )
        else:
            rule_text = (
                f"{feature_name} = {round(actual_value, 4)} > {round(threshold_value, 4)}"
            )

        reasons.append(rule_text)

    return reasons


def summarize_hybrid_result(rule_result, ai_result, agreement):
    if agreement:
        if ai_result["label"] == "FAILURE":
            return "Both rule-based and AI models indicate a high likelihood of startup failure."
        return "Both rule-based and AI models indicate a favorable startup situation."

    if rule_result["risk_level"] == "HIGH" and ai_result["label"] == "SUCCESS":
        return "Rule-based analysis is stricter than the AI model. This startup has warning signs but the AI model still predicts success."

    if rule_result["risk_level"] in ["LOW", "MEDIUM"] and ai_result["label"] == "FAILURE":
        return "The AI model detected failure patterns not fully captured by the rule-based engine."

    return "The rule-based and AI analyses disagree. The startup may require further review."


def get_final_decision(rule_result, ai_result):
    if rule_result["risk_level"] == "HIGH" or ai_result["label"] == "FAILURE":
        return "AT RISK"
    if rule_result["risk_level"] == "MEDIUM":
        return "MODERATE RISK"
    return "SAFE"