import pandas as pd
import numpy as np


class RecoveryMonitor:
    """
    ReviveAI Agent 4

    Monitors recovery performance and generates
    business-level recovery analytics.
    """

    def __init__(self, transactions_df):
        self.df = transactions_df.copy()

    # ========================================================
    # OVERALL KPIs
    # ========================================================

    def calculate_kpis(self):

        total_transactions = len(self.df)

        total_failed_revenue = (
            self.df["transaction_amount"]
            .sum()
        )

        recovered_transactions = (
            self.df["recovered"]
            .sum()
        )

        recovered_revenue = (
            self.df["recovered_revenue"]
            .sum()
        )

        recovery_rate = (
            recovered_transactions
            / total_transactions
            * 100
        )

        revenue_recovery_rate = (
            recovered_revenue
            / total_failed_revenue
            * 100
        )

        average_transaction_value = (
            total_failed_revenue
            / total_transactions
        )

        average_recovered_value = (
            recovered_revenue
            / max(recovered_transactions, 1)
        )

        return {
            "total_transactions":
                int(total_transactions),

            "recovered_transactions":
                int(recovered_transactions),

            "failed_transactions":
                int(
                    total_transactions
                    - recovered_transactions
                ),

            "total_failed_revenue":
                round(
                    float(total_failed_revenue),
                    2
                ),

            "recovered_revenue":
                round(
                    float(recovered_revenue),
                    2
                ),

            "recovery_rate":
                round(
                    float(recovery_rate),
                    2
                ),

            "revenue_recovery_rate":
                round(
                    float(revenue_recovery_rate),
                    2
                ),

            "average_transaction_value":
                round(
                    float(average_transaction_value),
                    2
                ),

            "average_recovered_value":
                round(
                    float(average_recovered_value),
                    2
                )
        }

    # ========================================================
    # FAILURE TYPE ANALYSIS
    # ========================================================

    def analyze_failure_types(self):

        result = (
            self.df
            .groupby("failure_type")
            .agg(
                transactions=(
                    "transaction_id",
                    "count"
                ),

                failed_revenue=(
                    "transaction_amount",
                    "sum"
                ),

                recovered_transactions=(
                    "recovered",
                    "sum"
                ),

                recovered_revenue=(
                    "recovered_revenue",
                    "sum"
                )
            )
            .reset_index()
        )

        result["recovery_rate"] = (
            result["recovered_transactions"]
            / result["transactions"]
            * 100
        )

        result["revenue_recovery_rate"] = (
            result["recovered_revenue"]
            / result["failed_revenue"]
            * 100
        )

        return result.sort_values(
            "recovered_revenue",
            ascending=False
        )

    # ========================================================
    # CUSTOMER SEGMENT ANALYSIS
    # ========================================================

    def analyze_customer_segments(self):

        result = (
            self.df
            .groupby("customer_segment")
            .agg(
                customers=(
                    "transaction_id",
                    "count"
                ),

                failed_revenue=(
                    "transaction_amount",
                    "sum"
                ),

                recovered_transactions=(
                    "recovered",
                    "sum"
                ),

                recovered_revenue=(
                    "recovered_revenue",
                    "sum"
                )
            )
            .reset_index()
        )

        result["recovery_rate"] = (
            result["recovered_transactions"]
            / result["customers"]
            * 100
        )

        result["revenue_recovery_rate"] = (
            result["recovered_revenue"]
            / result["failed_revenue"]
            * 100
        )

        return result

    # ========================================================
    # STRATEGY ANALYSIS
    # ========================================================

    def analyze_strategies(self):

        if "recovery_method" not in self.df.columns:

            return pd.DataFrame()

        result = (
            self.df
            .groupby("recovery_method")
            .agg(
                transactions=(
                    "transaction_id",
                    "count"
                ),

                failed_revenue=(
                    "transaction_amount",
                    "sum"
                ),

                recovered_transactions=(
                    "recovered",
                    "sum"
                ),

                recovered_revenue=(
                    "recovered_revenue",
                    "sum"
                )
            )
            .reset_index()
        )

        result["recovery_rate"] = (
            result["recovered_transactions"]
            / result["transactions"]
            * 100
        )

        result["revenue_recovery_rate"] = (
            result["recovered_revenue"]
            / result["failed_revenue"]
            * 100
        )

        return result.sort_values(
            "recovered_revenue",
            ascending=False
        )

    # ========================================================
    # FAILURE SEVERITY ANALYSIS
    # ========================================================

    def analyze_severity(self):

        if "severity_score" not in self.df.columns:

            return pd.DataFrame()

        self.df["severity_band"] = pd.cut(
            self.df["severity_score"],
            bins=[
                -1,
                40,
                70,
                100
            ],
            labels=[
                "Low",
                "Medium",
                "High"
            ]
        )

        result = (
            self.df
            .groupby(
                "severity_band",
                observed=False
            )
            .agg(
                transactions=(
                    "transaction_id",
                    "count"
                ),

                recovered_transactions=(
                    "recovered",
                    "sum"
                ),

                recovered_revenue=(
                    "recovered_revenue",
                    "sum"
                )
            )
            .reset_index()
        )

        result["recovery_rate"] = (
            result["recovered_transactions"]
            / result["transactions"]
            * 100
        )

        return result

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    def executive_summary(self):

        kpis = self.calculate_kpis()

        failure_analysis = (
            self.analyze_failure_types()
        )

        segment_analysis = (
            self.analyze_customer_segments()
        )

        # Best failure type
        if not failure_analysis.empty:

            best_failure = (
                failure_analysis
                .iloc[0]["failure_type"]
            )

        else:

            best_failure = "N/A"

        # Best customer segment
        if not segment_analysis.empty:

            best_segment = (
                segment_analysis
                .sort_values(
                    "recovery_rate",
                    ascending=False
                )
                .iloc[0]["customer_segment"]
            )

        else:

            best_segment = "N/A"

        summary = (
            f"ReviveAI analyzed "
            f"{kpis['total_transactions']:,} "
            f"failed payment transactions. "

            f"The system recovered "
            f"{kpis['recovered_transactions']:,} "
            f"payments, achieving a "
            f"{kpis['recovery_rate']:.2f}% "
            f"transaction recovery rate. "

            f"Total recovered revenue was "
            f"₹{kpis['recovered_revenue']:,.2f}, "
            f"representing a "
            f"{kpis['revenue_recovery_rate']:.2f}% "
            f"revenue recovery rate. "

            f"The highest-revenue failure category "
            f"was {best_failure}, while the strongest "
            f"customer segment by recovery rate was "
            f"{best_segment}."
        )

        return summary


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    DATA_FILE = (
        "data/reviveai_transactions.csv"
    )

    df = pd.read_csv(
        DATA_FILE
    )

    monitor = RecoveryMonitor(df)

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    kpis = monitor.calculate_kpis()

    print("\n" + "=" * 75)
    print("REVIVEAI — RECOVERY MONITOR")
    print("=" * 75)

    print("\n📊 EXECUTIVE KPIs")
    print("-" * 75)

    print(
        f"Total Transactions     : "
        f"{kpis['total_transactions']:,}"
    )

    print(
        f"Recovered Transactions : "
        f"{kpis['recovered_transactions']:,}"
    )

    print(
        f"Failed Transactions    : "
        f"{kpis['failed_transactions']:,}"
    )

    print(
        f"Failed Revenue         : "
        f"₹{kpis['total_failed_revenue']:,.2f}"
    )

    print(
        f"Recovered Revenue      : "
        f"₹{kpis['recovered_revenue']:,.2f}"
    )

    print(
        f"Recovery Rate          : "
        f"{kpis['recovery_rate']:.2f}%"
    )

    print(
        f"Revenue Recovery Rate  : "
        f"{kpis['revenue_recovery_rate']:.2f}%"
    )

    # --------------------------------------------------------
    # Failure analysis
    # --------------------------------------------------------

    print("\n📉 FAILURE TYPE PERFORMANCE")
    print("-" * 75)

    print(
        monitor
        .analyze_failure_types()
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Customer analysis
    # --------------------------------------------------------

    print("\n👥 CUSTOMER SEGMENT PERFORMANCE")
    print("-" * 75)

    print(
        monitor
        .analyze_customer_segments()
        .to_string(index=False)
    )

    # --------------------------------------------------------
    # Strategy analysis
    # --------------------------------------------------------

    print("\n🎯 RECOVERY STRATEGY PERFORMANCE")
    print("-" * 75)

    strategy_result = (
        monitor.analyze_strategies()
    )

    if strategy_result.empty:

        print(
            "Strategy analysis will be available "
            "after pipeline decisions are stored."
        )

    else:

        print(
            strategy_result
            .to_string(index=False)
        )

    # --------------------------------------------------------
    # Executive summary
    # --------------------------------------------------------

    print("\n🧠 EXECUTIVE SUMMARY")
    print("-" * 75)

    print(
        monitor.executive_summary()
    )

    print("\n" + "=" * 75)
    print("RECOVERY MONITOR TEST COMPLETED")
    print("=" * 75)