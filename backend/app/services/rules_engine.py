def apply_rules(df, pred_class, probability):

    # Rule-based overrides
    if df["amt"].iloc[0] > 100000:
        return "Fraud (Rule: High Amount)"

    if probability > 0.85:
        return "Fraud (Rule: High Risk Score)"

    return "Fraud" if pred_class==1 else "Not Fraud"