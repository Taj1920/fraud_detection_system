def apply_rules(df, prediction, probability):

    # Rule-based overrides
    if df["amt"].iloc[0] > 100000:
        return "Fraud (Rule: High Amount)"

    if probability > 0.85:
        return "Fraud (Rule: High Risk Score)"

    return "Fraud" if prediction==1 else "Not Fraud"