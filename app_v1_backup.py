import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# REVIVEAI — AI PAYMENT RECOVERY INTELLIGENCE
# ============================================================

st.set_page_config(
    page_title="ReviveAI",
    page_icon="💳",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

TRANSACTION_FILE = (
    "data/reviveai_transactions.csv"
)

AI_RESULTS_FILE = (
    "data/reviveai_ai_results.csv"
)


@st.cache_data
def load_data():

    transactions = pd.read_csv(
        TRANSACTION_FILE
    )

    ai_results = pd.read_csv(
        AI_RESULTS_FILE
    )

    return transactions, ai_results


try:

    transactions, ai_results = load_data()

except Exception as error:

    st.error(
        f"Unable to load ReviveAI data: {error}"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("💳 ReviveAI")

st.subheader(
    "AI-Powered Payment Recovery Intelligence"
)

st.caption(
    "Analyze failed payments • Predict recovery • "
    "Optimize recovery strategy • Generate customer communication"
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_transactions = len(
    transactions
)

recovered_transactions = int(
    transactions["recovered"].sum()
)

failed_transactions = (
    total_transactions
    - recovered_transactions
)

failed_revenue = (
    transactions["transaction_amount"]
    .sum()
)

recovered_revenue = (
    transactions["recovered_revenue"]
    .sum()
)

recovery_rate = (
    recovered_transactions
    / total_transactions
    * 100
)

revenue_recovery_rate = (
    recovered_revenue
    / failed_revenue
    * 100
)

expected_revenue = (
    ai_results["expected_revenue"]
    .sum()
)

expected_net_value = (
    ai_results["expected_net_value"]
    .sum()
)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("### 📊 Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Failed Transactions",
        f"{total_transactions:,}"
    )

with col2:

    st.metric(
        "Recovery Rate",
        f"{recovery_rate:.2f}%"
    )

with col3:

    st.metric(
        "Recovered Revenue",
        f"₹{recovered_revenue / 100000:.2f} L"
    )

with col4:

    st.metric(
        "AI Expected Revenue",
        f"₹{expected_revenue / 100000:.2f} L"
    )


st.divider()


# ============================================================
# SECONDARY KPIs
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Recovered Payments",
        f"{recovered_transactions:,}"
    )

with col2:

    st.metric(
        "Unrecovered Payments",
        f"{failed_transactions:,}"
    )

with col3:

    st.metric(
        "Revenue Recovery Rate",
        f"{revenue_recovery_rate:.2f}%"
    )

with col4:

    st.metric(
        "AI Expected Net Value",
        f"₹{expected_net_value / 100000:.2f} L"
    )


# ============================================================
# CHART ROW 1
# ============================================================

st.markdown("### 📈 Recovery Performance")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Recovery outcome
# ------------------------------------------------------------

with col1:

    recovered_data = pd.DataFrame({
        "Outcome": [
            "Recovered",
            "Not Recovered"
        ],

        "Transactions": [
            recovered_transactions,
            failed_transactions
        ]
    })

    fig = px.pie(
        recovered_data,
        names="Outcome",
        values="Transactions",
        title="Payment Recovery Outcome",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Failure types
# ------------------------------------------------------------

with col2:

    failure_data = (
        transactions[
            "failure_type"
        ]
        .value_counts()
        .reset_index()
    )

    failure_data.columns = [
        "failure_type",
        "count"
    ]

    fig = px.bar(
        failure_data,
        x="failure_type",
        y="count",
        title="Failed Payment Types"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CHART ROW 2
# ============================================================

st.markdown("### 🎯 AI Strategy Intelligence")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# AI strategy distribution
# ------------------------------------------------------------

with col1:

    strategy_data = (
        ai_results[
            "ai_strategy"
        ]
        .value_counts()
        .reset_index()
    )

    strategy_data.columns = [
        "strategy",
        "count"
    ]

    fig = px.bar(
        strategy_data,
        x="strategy",
        y="count",
        title="AI Recommended Recovery Strategies",
        text="count"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Customer segment recovery
# ------------------------------------------------------------

with col2:

    segment_data = (
        transactions
        .groupby("customer_segment")
        .agg(
            transactions=(
                "transaction_id",
                "count"
            ),

            recovered=(
                "recovered",
                "sum"
            )
        )
        .reset_index()
    )

    segment_data[
        "recovery_rate"
    ] = (
        segment_data["recovered"]
        / segment_data["transactions"]
        * 100
    )

    fig = px.bar(
        segment_data,
        x="customer_segment",
        y="recovery_rate",
        title="Recovery Rate by Customer Segment",
        text="recovery_rate"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AI FINANCIAL IMPACT
# ============================================================

st.markdown("### 💰 AI Financial Impact")

col1, col2 = st.columns(2)

with col1:

    financial_data = pd.DataFrame({
        "Metric": [
            "Historical Recovered Revenue",
            "AI Expected Recovery Revenue",
            "AI Expected Net Value"
        ],

        "Revenue": [
            recovered_revenue,
            expected_revenue,
            expected_net_value
        ]
    })

    fig = px.bar(
        financial_data,
        x="Metric",
        y="Revenue",
        title="Historical vs AI Financial Opportunity",
        text="Revenue"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    failure_recovery = (
        transactions
        .groupby("failure_type")
        .agg(
            transactions=(
                "transaction_id",
                "count"
            ),

            recovered=(
                "recovered",
                "sum"
            )
        )
        .reset_index()
    )

    failure_recovery[
        "recovery_rate"
    ] = (
        failure_recovery["recovered"]
        / failure_recovery["transactions"]
        * 100
    )

    fig = px.bar(
        failure_recovery,
        x="failure_type",
        y="recovery_rate",
        title="Recovery Rate by Failure Type",
        text="recovery_rate"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TRANSACTION INVESTIGATOR
# ============================================================

st.divider()

st.markdown(
    "### 🔎 AI Transaction Investigator"
)

st.write(
    "Select a failed transaction to inspect the complete "
    "ReviveAI decision trail."
)


transaction_ids = (
    ai_results[
        "transaction_id"
    ]
    .tolist()
)


selected_id = st.selectbox(
    "Select Transaction",
    transaction_ids
)


selected = ai_results[
    ai_results["transaction_id"]
    == selected_id
].iloc[0]


# ============================================================
# TRANSACTION DETAILS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Transaction Amount",
        f"₹{selected['transaction_amount']:,.2f}"
    )

with col2:

    st.metric(
        "Recovery Probability",
        f"{selected['recovery_probability'] * 100:.1f}%"
    )

with col3:

    st.metric(
        "Expected Revenue",
        f"₹{selected['expected_revenue']:,.2f}"
    )

with col4:

    st.metric(
        "Expected Net Value",
        f"₹{selected['expected_net_value']:,.2f}"
    )


# ============================================================
# DECISION TRAIL
# ============================================================

st.markdown("#### 🧠 AI Decision Trail")

col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**Failure Type:** "
        f"{selected['failure_type']}"
    )

    st.write(
        f"**Failure Category:** "
        f"{selected['failure_category']}"
    )

    st.write(
        f"**Severity Score:** "
        f"{selected['severity_score']}"
    )

    st.write(
        f"**Risk Level:** "
        f"{selected['risk_level']}"
    )

    st.write(
        f"**Priority:** "
        f"{selected['priority']}"
    )


with col2:

    st.write(
        f"**AI Strategy:** "
        f"{selected['ai_strategy']}"
    )

    st.write(
        f"**Strategy Reason:** "
        f"{selected['strategy_reason']}"
    )

    st.write(
        f"**Generation Method:** "
        f"{selected['generation_method']}"
    )


# ============================================================
# COMMUNICATION PREVIEW
# ============================================================

st.markdown("#### ✉️ Customer Communication Preview")

st.info(
    f"**Subject:** {selected['message_subject']}"
)

st.text_area(
    "Generated Message",
    selected["message_body"],
    height=220
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ReviveAI • AI-Powered Payment Recovery Intelligence"
)