import pandas as pd

from agents.failure_analyzer import FailureAnalyzer
from agents.recovery_strategist import RecoveryStrategist
from agents.communication_agent import CommunicationAgent


class ReviveAIPipeline:
    """
    ReviveAI master orchestration pipeline.

    Flow:

    Transaction
        ↓
    Failure Analyzer
        ↓
    Recovery Strategist
        ↓
    Communication Agent
        ↓
    Final Recovery Recommendation
    """

    def __init__(self):

        print("\nInitializing ReviveAI agents...")

        self.failure_analyzer = FailureAnalyzer()

        self.recovery_strategist = RecoveryStrategist()

        self.communication_agent = CommunicationAgent()

        print("All agents initialized successfully.")

    # ========================================================
    # PROCESS ONE TRANSACTION
    # ========================================================

    def process_transaction(self, transaction):

        # ----------------------------------------------------
        # AGENT 1 — FAILURE ANALYSIS
        # ----------------------------------------------------

        failure_analysis = (
            self.failure_analyzer
            .analyze_transaction(transaction)
        )

        # ----------------------------------------------------
        # AGENT 2 — RECOVERY STRATEGY
        # ----------------------------------------------------

        recovery_strategy = (
            self.recovery_strategist
            .analyze_transaction(
                transaction,
                failure_analysis
            )
        )

        # ----------------------------------------------------
        # AGENT 3 — COMMUNICATION
        # ----------------------------------------------------

        communication = (
            self.communication_agent
            .generate_message(
                transaction,
                recovery_strategy
            )
        )

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return {
            "transaction": transaction.to_dict(),

            "failure_analysis":
                failure_analysis,

            "recovery_strategy":
                recovery_strategy,

            "communication":
                communication
        }

    # ========================================================
    # PROCESS MULTIPLE TRANSACTIONS
    # ========================================================

    def process_dataframe(
        self,
        df,
        limit=None
    ):

        if limit is not None:
            df = df.head(limit)

        results = []

        for _, transaction in df.iterrows():

            try:

                result = self.process_transaction(
                    transaction
                )

                results.append(result)

            except Exception as error:

                print(
                    f"Error processing "
                    f"{transaction.get('transaction_id', 'unknown')}: "
                    f"{error}"
                )

        return results


# ============================================================
# TEST PIPELINE
# ============================================================

if __name__ == "__main__":

    DATA_FILE = (
        "data/reviveai_transactions.csv"
    )

    print("\n" + "=" * 80)
    print("REVIVEAI — END-TO-END PIPELINE TEST")
    print("=" * 80)

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    df = pd.read_csv(
        DATA_FILE
    )

    print(
        f"\nLoaded {len(df):,} transactions."
    )

    # --------------------------------------------------------
    # Initialize pipeline
    # --------------------------------------------------------

    pipeline = ReviveAIPipeline()

    # --------------------------------------------------------
    # Process one transaction
    # --------------------------------------------------------

    transaction = df.iloc[0]

    result = pipeline.process_transaction(
        transaction
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n" + "=" * 80)
    print("FINAL AI DECISION")
    print("=" * 80)

    print(
        f"\nTransaction ID:"
        f"\n{transaction['transaction_id']}"
    )

    print(
        f"\nAmount:"
        f"\n₹{transaction['transaction_amount']:,.2f}"
    )

    # --------------------------------------------------------
    # Agent 1
    # --------------------------------------------------------

    failure = result[
        "failure_analysis"
    ]

    print("\n" + "-" * 80)
    print("🔍 AGENT 1 — FAILURE ANALYZER")
    print("-" * 80)

    print(
        f"Failure Type      : "
        f"{failure['failure_type']}"
    )

    print(
        f"Failure Category  : "
        f"{failure['failure_category']}"
    )

    print(
        f"Severity Score    : "
        f"{failure['severity_score']}"
    )

    print(
        f"Risk Level        : "
        f"{failure['risk_level']}"
    )

    print(
        f"Priority          : "
        f"{failure['priority']}"
    )

    print(
        f"Initial Handling  : "
        f"{failure['recommended_handling']}"
    )

    # --------------------------------------------------------
    # Agent 2
    # --------------------------------------------------------

    strategy = result[
        "recovery_strategy"
    ]

    print("\n" + "-" * 80)
    print("🧠 AGENT 2 — RECOVERY STRATEGIST")
    print("-" * 80)

    print(
        f"Recovery Probability : "
        f"{strategy['recovery_probability'] * 100:.2f}%"
    )

    print(
        f"Best Strategy        : "
        f"{strategy['best_strategy']}"
    )

    print(
        f"Expected Revenue     : "
        f"₹{strategy['expected_revenue']:,.2f}"
    )

    print(
        f"Strategy Cost        : "
        f"₹{strategy['strategy_cost']:,.2f}"
    )

    print(
        f"Expected Net Value   : "
        f"₹{strategy['expected_net_value']:,.2f}"
    )

    print(
        f"Recovery Priority    : "
        f"{strategy['priority']}"
    )

    print(
        f"Decision Reason      : "
        f"{strategy['strategy_reason']}"
    )

    # --------------------------------------------------------
    # Agent 3
    # --------------------------------------------------------

    communication = result[
        "communication"
    ]

    print("\n" + "-" * 80)
    print("✉️ AGENT 3 — COMMUNICATION GENERATOR")
    print("-" * 80)

    print(
        f"Generation Method : "
        f"{communication['generation_method']}"
    )

    print(
        f"Tone              : "
        f"{communication['tone']}"
    )

    print(
        f"\nSubject:\n"
        f"{communication['subject']}"
    )

    print(
        f"\nMessage:\n"
        f"{communication['body']}"
    )

    print("\n" + "=" * 80)
    print("REVIVEAI PIPELINE TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)