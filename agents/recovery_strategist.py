import os
import joblib
import pandas as pd


class RecoveryStrategist:
    """
    ReviveAI Agent 2

    Uses the trained ML model to:
    1. Predict recovery probability.
    2. Estimate expected recovered revenue.
    3. Evaluate possible recovery strategies.
    4. Select the best strategy.
    5. Assign a recovery priority.
    """

    def __init__(
        self,
        model_path="models/recovery_prediction_model.joblib"
    ):

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Recovery model not found: {model_path}"
            )

        self.model = joblib.load(model_path)

    # ========================================================
    # STRATEGY DEFINITIONS
    # ========================================================

    def get_strategy_profiles(self, transaction):

        failure_type = transaction["failure_type"]
        customer_segment = transaction["customer_segment"]

        strategies = {
            "smart_retry": {
                "base_probability": 0.72,
                "cost": 5,
                "reason": "Retry the payment using optimized timing."
            },

            "customer_outreach": {
                "base_probability": 0.62,
                "cost": 15,
                "reason": "Send personalized payment recovery communication."
            },

            "alternative_payment": {
                "base_probability": 0.68,
                "cost": 10,
                "reason": "Ask the customer to use another payment method."
            },

            "payment_plan": {
                "base_probability": 0.55,
                "cost": 25,
                "reason": "Offer a structured payment option."
            },

            "discount_offer": {
                "base_probability": 0.50,
                "cost": 0,
                "reason": "Offer a targeted incentive to complete payment."
            },

            "human_escalation": {
                "base_probability": 0.48,
                "cost": 75,
                "reason": "Escalate the case to a human recovery specialist."
            }
        }

        # -----------------------------------------------
        # Context-aware adjustments
        # -----------------------------------------------

        if failure_type in [
            "gateway_error",
            "network_error"
        ]:
            strategies["smart_retry"]["base_probability"] += 0.15

        if failure_type == "expired_card":
            strategies["alternative_payment"][
                "base_probability"
            ] += 0.15

        if failure_type == "insufficient_funds":
            strategies["payment_plan"][
                "base_probability"
            ] += 0.12

        if failure_type == "authentication_failed":
            strategies["customer_outreach"][
                "base_probability"
            ] += 0.12

        if customer_segment == "premium":
            strategies["customer_outreach"][
                "base_probability"
            ] += 0.08

        if customer_segment == "at_risk":
            strategies["customer_outreach"][
                "base_probability"
            ] += 0.05

        # Keep all probabilities valid
        for strategy in strategies:

            strategies[strategy]["base_probability"] = min(
                strategies[strategy]["base_probability"],
                0.95
            )

        return strategies

    # ========================================================
    # BUILD MODEL INPUT
    # ========================================================

    def prepare_features(
        self,
        transaction,
        severity_score
    ):

        data = pd.DataFrame([{
            "transaction_amount":
                transaction["transaction_amount"],

            "payment_method":
                transaction["payment_method"],

            "failure_type":
                transaction["failure_type"],

            "customer_segment":
                transaction["customer_segment"],

            "previous_failures":
                transaction["previous_failures"],

            "customer_lifetime_value":
                transaction["customer_lifetime_value"],

            "days_since_last_purchase":
                transaction["days_since_last_purchase"],

            "retry_count":
                transaction["retry_count"],

            "account_age_days":
                transaction["account_age_days"],

            "website_visits_last_30_days":
                transaction["website_visits_last_30_days"],

            "cart_additions_last_30_days":
                transaction["cart_additions_last_30_days"],

            "severity_score":
                severity_score,

            "failure_retry_burden":
                transaction["previous_failures"]
                + transaction["retry_count"],

            "customer_engagement_score":
                transaction["website_visits_last_30_days"] * 0.6
                + transaction["cart_additions_last_30_days"] * 1.5,

            "customer_value_per_day":
                transaction["customer_lifetime_value"]
                / (
                    transaction["account_age_days"] + 1
                ),

            "high_value_customer":
                int(
                    transaction["customer_lifetime_value"]
                    >= 100000
                ),

            "high_value_transaction":
                int(
                    transaction["transaction_amount"]
                    >= 50000
                )
        }])

        return data

    # ========================================================
    # MAIN DECISION ENGINE
    # ========================================================

    def analyze_transaction(
        self,
        transaction,
        failure_analysis
    ):

        severity_score = failure_analysis[
            "severity_score"
        ]

        # -----------------------------------------------
        # ML prediction
        # -----------------------------------------------

        features = self.prepare_features(
            transaction,
            severity_score
        )

        recovery_probability = self.model.predict_proba(
            features
        )[0][1]

        recovery_probability = round(
            float(recovery_probability),
            4
        )

        transaction_amount = float(
            transaction["transaction_amount"]
        )

        # -----------------------------------------------
        # Strategy evaluation
        # -----------------------------------------------

        strategies = self.get_strategy_profiles(
            transaction
        )

        strategy_results = []

        for name, profile in strategies.items():

            probability = profile[
                "base_probability"
            ]

            # Blend global ML prediction with
            # strategy-specific probability.
            adjusted_probability = (
                recovery_probability * 0.60
                + probability * 0.40
            )

            adjusted_probability = min(
                max(adjusted_probability, 0.05),
                0.95
            )

            expected_revenue = (
                transaction_amount
                * adjusted_probability
            )

            expected_net_value = (
                expected_revenue
                - profile["cost"]
            )

            strategy_results.append({
                "strategy": name,
                "probability": round(
                    adjusted_probability,
                    4
                ),
                "expected_revenue": round(
                    expected_revenue,
                    2
                ),
                "cost": profile["cost"],
                "expected_net_value": round(
                    expected_net_value,
                    2
                ),
                "reason": profile["reason"]
            })

        # -----------------------------------------------
        # Select best strategy
        # -----------------------------------------------

        strategy_results.sort(
            key=lambda x: x["expected_net_value"],
            reverse=True
        )

        best_strategy = strategy_results[0]

        # -----------------------------------------------
        # Recovery priority
        # -----------------------------------------------

        expected_value = best_strategy[
            "expected_net_value"
        ]

        if expected_value >= 50000:
            priority = "CRITICAL"

        elif expected_value >= 20000:
            priority = "HIGH"

        elif expected_value >= 5000:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        # -----------------------------------------------
        # Final output
        # -----------------------------------------------

        return {
            "transaction_id":
                transaction["transaction_id"],

            "recovery_probability":
                recovery_probability,

            "best_strategy":
                best_strategy["strategy"],

            "expected_revenue":
                best_strategy["expected_revenue"],

            "strategy_cost":
                best_strategy["cost"],

            "expected_net_value":
                best_strategy["expected_net_value"],

            "priority":
                priority,

            "strategy_reason":
                best_strategy["reason"],

            "all_strategy_results":
                strategy_results
        }


# ============================================================
# TEST AGENT 2
# ============================================================

if __name__ == "__main__":

    from failure_analyzer import FailureAnalyzer

    DATA_FILE = "data/reviveai_transactions.csv"

    df = pd.read_csv(DATA_FILE)

    failure_analyzer = FailureAnalyzer()

    strategist = RecoveryStrategist()

    print("\n" + "=" * 75)
    print("REVIVEAI — RECOVERY STRATEGIST TEST")
    print("=" * 75)

    for index in range(5):

        transaction = df.iloc[index]

        failure_result = (
            failure_analyzer
            .analyze_transaction(transaction)
        )

        recovery_result = (
            strategist
            .analyze_transaction(
                transaction,
                failure_result
            )
        )

        print("\n" + "-" * 75)

        print(
            f"Transaction       : "
            f"{transaction['transaction_id']}"
        )

        print(
            f"Amount            : "
            f"₹{transaction['transaction_amount']:,.2f}"
        )

        print(
            f"Failure           : "
            f"{transaction['failure_type']}"
        )

        print(
            f"Customer segment  : "
            f"{transaction['customer_segment']}"
        )

        print(
            f"Recovery chance   : "
            f"{recovery_result['recovery_probability'] * 100:.2f}%"
        )

        print(
            f"Best strategy     : "
            f"{recovery_result['best_strategy']}"
        )

        print(
            f"Expected revenue  : "
            f"₹{recovery_result['expected_revenue']:,.2f}"
        )

        print(
            f"Strategy cost     : "
            f"₹{recovery_result['strategy_cost']:,.2f}"
        )

        print(
            f"Expected net value: "
            f"₹{recovery_result['expected_net_value']:,.2f}"
        )

        print(
            f"Priority          : "
            f"{recovery_result['priority']}"
        )

        print(
            f"Reason            : "
            f"{recovery_result['strategy_reason']}"
        )

    print("\n" + "=" * 75)
    print("RECOVERY STRATEGIST TEST COMPLETED")
    print("=" * 75)