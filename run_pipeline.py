import pandas as pd

from pipeline import ReviveAIPipeline


# ============================================================
# REVIVEAI — BATCH AI DECISION ENGINE
# ============================================================

INPUT_FILE = (
    "data/reviveai_transactions.csv"
)

OUTPUT_FILE = (
    "data/reviveai_ai_results.csv"
)


print("\n" + "=" * 80)
print("REVIVEAI — BATCH AI DECISION ENGINE")
print("=" * 80)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print(
    f"\nLoaded {len(df):,} transactions."
)


# ============================================================
# 2. INITIALIZE PIPELINE
# ============================================================

pipeline = ReviveAIPipeline()


# ============================================================
# 3. PROCESS ALL TRANSACTIONS
# ============================================================

print(
    "\nProcessing transactions..."
)

results = []

for index, transaction in df.iterrows():

    try:

        result = pipeline.process_transaction(
            transaction
        )

        failure = result[
            "failure_analysis"
        ]

        strategy = result[
            "recovery_strategy"
        ]

        communication = result[
            "communication"
        ]

        results.append({

            # -------------------------------
            # Transaction
            # -------------------------------

            "transaction_id":
                transaction["transaction_id"],

            "transaction_amount":
                transaction["transaction_amount"],

            "payment_method":
                transaction["payment_method"],

            "failure_type":
                transaction["failure_type"],

            "customer_segment":
                transaction["customer_segment"],

            # -------------------------------
            # Agent 1
            # -------------------------------

            "failure_category":
                failure["failure_category"],

            "severity_score":
                failure["severity_score"],

            "risk_score":
                failure["risk_score"],

            "risk_level":
                failure["risk_level"],

            "priority":
                failure["priority"],

            "initial_handling":
                failure["recommended_handling"],

            # -------------------------------
            # Agent 2
            # -------------------------------

            "recovery_probability":
                strategy["recovery_probability"],

            "ai_strategy":
                strategy["best_strategy"],

            "expected_revenue":
                strategy["expected_revenue"],

            "strategy_cost":
                strategy["strategy_cost"],

            "expected_net_value":
                strategy["expected_net_value"],

            "strategy_reason":
                strategy["strategy_reason"],

            # -------------------------------
            # Agent 3
            # -------------------------------

            "message_subject":
                communication["subject"],

            "message_body":
                communication["body"],

            "message_tone":
                communication["tone"],

            "generation_method":
                communication["generation_method"],

            # -------------------------------
            # Historical outcome
            # -------------------------------

            "actual_recovered":
                transaction["recovered"],

            "actual_recovered_revenue":
                transaction["recovered_revenue"]

        })

    except Exception as error:

        print(
            f"Error processing "
            f"{transaction['transaction_id']}: "
            f"{error}"
        )


# ============================================================
# 4. CREATE RESULTS DATAFRAME
# ============================================================

results_df = pd.DataFrame(
    results
)


# ============================================================
# 5. SAVE RESULTS
# ============================================================

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 6. SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("AI PIPELINE COMPLETED")
print("=" * 80)

print(
    f"\nTransactions processed : "
    f"{len(results_df):,}"
)

print(
    f"Output file            : "
    f"{OUTPUT_FILE}"
)


# ============================================================
# STRATEGY DISTRIBUTION
# ============================================================

print("\nAI RECOMMENDED STRATEGIES")
print("-" * 80)

strategy_counts = (
    results_df["ai_strategy"]
    .value_counts()
)

print(
    strategy_counts.to_string()
)


# ============================================================
# EXPECTED REVENUE
# ============================================================

total_expected_revenue = (
    results_df["expected_revenue"]
    .sum()
)

total_expected_net_value = (
    results_df["expected_net_value"]
    .sum()
)

print("\nAI FINANCIAL IMPACT")
print("-" * 80)

print(
    f"Expected Recovery Revenue : "
    f"₹{total_expected_revenue:,.2f}"
)

print(
    f"Expected Net Value        : "
    f"₹{total_expected_net_value:,.2f}"
)


print("\n" + "=" * 80)
print("REVIVEAI AI RESULTS SAVED SUCCESSFULLY")
print("=" * 80)