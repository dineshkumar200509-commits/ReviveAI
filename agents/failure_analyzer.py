import pandas as pd


class FailureAnalyzer:
    """
    ReviveAI Agent 1

    Analyzes failed payment transactions and produces:
    - Failure category
    - Severity score
    - Customer risk level
    - Recommended initial handling
    """

    def __init__(self):
        self.failure_rules = {
            "gateway_error": {
                "category": "technical",
                "base_severity": 35,
                "handling": "smart_retry"
            },
            "network_error": {
                "category": "technical",
                "base_severity": 30,
                "handling": "smart_retry"
            },
            "card_declined": {
                "category": "payment_decline",
                "base_severity": 60,
                "handling": "alternative_payment"
            },
            "insufficient_funds": {
                "category": "funding_issue",
                "base_severity": 65,
                "handling": "payment_plan"
            },
            "expired_card": {
                "category": "payment_method_issue",
                "base_severity": 55,
                "handling": "customer_outreach"
            },
            "authentication_failed": {
                "category": "authentication_issue",
                "base_severity": 70,
                "handling": "customer_outreach"
            }
        }

    def analyze_transaction(self, transaction):
        """
        Analyze one failed payment transaction.
        """

        failure_type = transaction["failure_type"]

        rule = self.failure_rules.get(
            failure_type,
            {
                "category": "unknown",
                "base_severity": 70,
                "handling": "human_escalation"
            }
        )

        severity = rule["base_severity"]

        # Previous failures increase severity
        previous_failures = int(
            transaction["previous_failures"]
        )

        severity += previous_failures * 4

        # Multiple retries indicate increased difficulty
        retry_count = int(
            transaction["retry_count"]
        )

        severity += retry_count * 3

        # High-value transactions receive greater attention
        transaction_amount = float(
            transaction["transaction_amount"]
        )

        if transaction_amount >= 50000:
            severity += 15

        elif transaction_amount >= 20000:
            severity += 8

        # Premium customers receive higher priority
        customer_segment = transaction["customer_segment"]

        if customer_segment == "premium":
            severity += 5

        severity = min(max(severity, 0), 100)

        # --------------------------------
        # Customer risk calculation
        # --------------------------------

        risk_score = 0

        risk_score += previous_failures * 10
        risk_score += retry_count * 8

        if customer_segment == "at_risk":
            risk_score += 30

        elif customer_segment == "premium":
            risk_score -= 10

        if transaction_amount >= 50000:
            risk_score += 10

        risk_score = min(max(risk_score, 0), 100)

        if risk_score >= 70:
            risk_level = "HIGH"

        elif risk_score >= 40:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        # --------------------------------
        # Priority calculation
        # --------------------------------

        priority_score = (
            severity * 0.6
            + risk_score * 0.4
        )

        if priority_score >= 70:
            priority = "URGENT"

        elif priority_score >= 45:
            priority = "HIGH"

        elif priority_score >= 25:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        # --------------------------------
        # Final recommendation
        # --------------------------------

        handling = rule["handling"]

        # Very high-risk cases go to humans
        if risk_level == "HIGH" and severity >= 75:
            handling = "human_escalation"

        result = {
            "transaction_id": transaction["transaction_id"],
            "failure_type": failure_type,
            "failure_category": rule["category"],
            "severity_score": round(severity, 2),
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "priority": priority,
            "recommended_handling": handling
        }

        return result

    def analyze_dataframe(self, df):
        """
        Analyze every transaction in a DataFrame.
        """

        results = []

        for _, transaction in df.iterrows():
            results.append(
                self.analyze_transaction(transaction)
            )

        analysis_df = pd.DataFrame(results)

        return analysis_df


# --------------------------------------------
# Standalone test
# --------------------------------------------

if __name__ == "__main__":

    DATA_FILE = "data/reviveai_transactions.csv"

    df = pd.read_csv(DATA_FILE)

    analyzer = FailureAnalyzer()

    # Analyze first 10 transactions
    results = analyzer.analyze_dataframe(
        df.head(10)
    )

    print("\n" + "=" * 70)
    print("REVIVEAI — FAILURE ANALYZER TEST")
    print("=" * 70)

    print(
        results.to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETED")
    print("=" * 70)