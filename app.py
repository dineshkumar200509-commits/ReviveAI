import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# REVIVEAI — AI PAYMENT RECOVERY INTELLIGENCE
# DASHBOARD V2
# ============================================================

st.set_page_config(
    page_title="ReviveAI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 1.5rem 0 1rem 0;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 18px;
    color: #64748b;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

.audit-box {
    padding: 18px;
    border-radius: 12px;
    background-color: #f1f5f9;
    border: 1px solid #e2e8f0;
    margin-bottom: 10px;
}

.strategy-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA FILES
# ============================================================

TRANSACTION_FILE = "data/reviveai_transactions.csv"
AI_RESULTS_FILE = "data/reviveai_ai_results.csv"


# ============================================================
# LOAD DATA
# ============================================================

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
# SIDEBAR
# ============================================================

st.sidebar.title("💳 ReviveAI")

st.sidebar.caption(
    "AI Payment Recovery Control Center"
)

st.sidebar.divider()

st.sidebar.subheader("🔎 Filters")


# Failure filter

failure_options = sorted(
    ai_results["failure_type"]
    .dropna()
    .unique()
    .tolist()
)

selected_failures = st.sidebar.multiselect(
    "Failure Type",
    failure_options,
    default=failure_options
)


# Customer segment filter

segment_options = sorted(
    ai_results["customer_segment"]
    .dropna()
    .unique()
    .tolist()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segment_options,
    default=segment_options
)


# Risk filter

risk_options = sorted(
    ai_results["risk_level"]
    .dropna()
    .unique()
    .tolist()
)

selected_risks = st.sidebar.multiselect(
    "Risk Level",
    risk_options,
    default=risk_options
)


# AI strategy filter

strategy_options = sorted(
    ai_results["ai_strategy"]
    .dropna()
    .unique()
    .tolist()
)

selected_strategies = st.sidebar.multiselect(
    "AI Strategy",
    strategy_options,
    default=strategy_options
)


st.sidebar.divider()

st.sidebar.caption(
    "ReviveAI V2 • AI Recovery Intelligence"
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = ai_results[
    ai_results["failure_type"].isin(
        selected_failures
    )
    &
    ai_results["customer_segment"].isin(
        selected_segments
    )
    &
    ai_results["risk_level"].isin(
        selected_risks
    )
    &
    ai_results["ai_strategy"].isin(
        selected_strategies
    )
].copy()


# ============================================================
# EMPTY FILTER CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "No transactions match the selected filters."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">💳 ReviveAI</div>
        <div class="hero-subtitle">
            AI-Powered Payment Recovery Intelligence Platform
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Analyze failed payments, predict recovery probability, "
    "optimize recovery strategies, and generate personalized "
    "customer communication."
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_analyzed = len(filtered)

recovered_transactions = int(
    filtered["actual_recovered"].sum()
)

unrecovered_transactions = (
    total_analyzed
    - recovered_transactions
)

historical_recovered_revenue = (
    filtered["actual_recovered_revenue"].sum()
)

total_transaction_value = (
    filtered["transaction_amount"].sum()
)

historical_recovery_rate = (
    recovered_transactions
    / max(total_analyzed, 1)
    * 100
)

historical_revenue_recovery_rate = (
    historical_recovered_revenue
    / max(total_transaction_value, 1)
    * 100
)

ai_expected_revenue = (
    filtered["expected_revenue"].sum()
)

ai_expected_net_value = (
    filtered["expected_net_value"].sum()
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📊 Executive Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Transactions Analyzed",
        f"{total_analyzed:,}"
    )


with col2:

    st.metric(
        "Historical Recovery",
        f"{historical_recovery_rate:.2f}%"
    )


with col3:

    st.metric(
        "Historical Recovered Revenue",
        f"₹{historical_recovered_revenue / 100000:.2f} L"
    )


with col4:

    st.metric(
        "AI Expected Opportunity",
        f"₹{ai_expected_revenue / 100000:.2f} L"
    )


# ============================================================
# SECOND KPI ROW
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
        f"{unrecovered_transactions:,}"
    )


with col3:

    st.metric(
        "Revenue Recovery Rate",
        f"{historical_revenue_recovery_rate:.2f}%"
    )


with col4:

    st.metric(
        "AI Expected Net Value",
        f"₹{ai_expected_net_value / 100000:.2f} L"
    )


# ============================================================
# IMPORTANT BUSINESS NOTE
# ============================================================

st.info(
    "💡 Historical recovered revenue represents actual recorded "
    "recovery. AI Expected Opportunity represents model-estimated "
    "recoverable revenue and should not be interpreted as already recovered."
)


# ============================================================
# RECOVERY PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">📈 Recovery Performance</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Recovery outcome
# ------------------------------------------------------------

with col1:

    outcome_data = pd.DataFrame({
        "Outcome": [
            "Recovered",
            "Not Recovered"
        ],

        "Transactions": [
            recovered_transactions,
            unrecovered_transactions
        ]
    })

    fig = px.pie(
        outcome_data,
        names="Outcome",
        values="Transactions",
        hole=0.5,
        title="Historical Payment Recovery"
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
        filtered["failure_type"]
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
        title="Failure Type Distribution",
        text="count"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# AI STRATEGY INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">🎯 AI Strategy Intelligence</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Strategy distribution
# ------------------------------------------------------------

with col1:

    strategy_data = (
        filtered["ai_strategy"]
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
# Customer segment
# ------------------------------------------------------------

with col2:

    segment_data = (
        filtered
        .groupby("customer_segment")
        .agg(
            transactions=(
                "transaction_id",
                "count"
            ),

            recovered=(
                "actual_recovered",
                "sum"
            )
        )
        .reset_index()
    )

    segment_data["recovery_rate"] = (
        segment_data["recovered"]
        / segment_data["transactions"]
        * 100
    )

    fig = px.bar(
        segment_data,
        x="customer_segment",
        y="recovery_rate",
        title="Historical Recovery Rate by Customer Segment",
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
# FINANCIAL OPPORTUNITY
# ============================================================

st.markdown(
    '<div class="section-title">💰 Financial Opportunity</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    financial_data = pd.DataFrame({
        "Metric": [
            "Historical Recovered Revenue",
            "AI Expected Recovery Revenue",
            "AI Expected Net Value"
        ],

        "Revenue": [
            historical_recovered_revenue,
            ai_expected_revenue,
            ai_expected_net_value
        ]
    })

    fig = px.bar(
        financial_data,
        x="Metric",
        y="Revenue",
        title="Historical Recovery vs AI Opportunity",
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
        filtered
        .groupby("failure_type")
        .agg(
            transactions=(
                "transaction_id",
                "count"
            ),

            recovered=(
                "actual_recovered",
                "sum"
            )
        )
        .reset_index()
    )

    failure_recovery["recovery_rate"] = (
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
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Model Performance</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Selected Model",
        "Logistic Regression"
    )


with col2:

    st.metric(
        "Accuracy",
        "66.10%"
    )


with col3:

    st.metric(
        "ROC-AUC",
        "69.53%"
    )


with col4:

    st.metric(
        "Training Records",
        "4,000"
    )


st.caption(
    "Benchmark values from the ReviveAI recovery model evaluation."
)


# ============================================================
# AI DECISION AUDIT TRAIL
# ============================================================

st.markdown(
    '<div class="section-title">🧠 AI Decision Audit Trail</div>',
    unsafe_allow_html=True
)

st.write(
    "ReviveAI processes each transaction through multiple "
    "decision stages before producing a recovery action."
)


audit_col1, audit_col2, audit_col3 = st.columns(3)


with audit_col1:

    st.markdown(
        """
        <div class="audit-box">
        <h4>🔍 Agent 1 — Failure Analyzer</h4>
        <b>Input:</b> Failed transaction<br><br>
        Classifies failure type, calculates severity,
        assesses risk and determines initial handling.
        </div>
        """,
        unsafe_allow_html=True
    )


with audit_col2:

    st.markdown(
        """
        <div class="audit-box">
        <h4>🧠 Agent 2 — Recovery Strategist</h4>
        <b>Input:</b> Enriched failure profile<br><br>
        Predicts recovery probability and selects
        the strategy with the highest expected value.
        </div>
        """,
        unsafe_allow_html=True
    )


with audit_col3:

    st.markdown(
        """
        <div class="audit-box">
        <h4>✉️ Agent 3 — Communication Generator</h4>
        <b>Input:</b> Recovery strategy<br><br>
        Generates customer-facing communication
        adapted to the failure and customer segment.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRANSACTION INVESTIGATOR
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔎 AI Transaction Investigator</div>',
    unsafe_allow_html=True
)

st.write(
    "Select any transaction to inspect the complete AI decision trail."
)


transaction_ids = (
    filtered["transaction_id"]
    .tolist()
)


selected_id = st.selectbox(
    "Transaction",
    transaction_ids
)


selected = filtered[
    filtered["transaction_id"]
    == selected_id
].iloc[0]


# ============================================================
# TRANSACTION KPIs
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
# AGENT 1 DETAILS
# ============================================================

st.markdown("#### 🔍 Agent 1 — Failure Analysis")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.write(
        f"**Failure Type:** "
        f"{selected['failure_type']}"
    )


with col2:

    st.write(
        f"**Category:** "
        f"{selected['failure_category']}"
    )


with col3:

    st.write(
        f"**Severity:** "
        f"{selected['severity_score']}"
    )


with col4:

    st.write(
        f"**Risk:** "
        f"{selected['risk_level']}"
    )


# ============================================================
# AGENT 2 DETAILS
# ============================================================

st.markdown("#### 🧠 Agent 2 — Recovery Decision")

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        <div class="strategy-box">
        <b>Recommended Strategy</b><br>
        {selected['ai_strategy']}
        <br><br>
        <b>Priority</b><br>
        {selected['priority']}
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="strategy-box">
        <b>Decision Reason</b><br>
        {selected['strategy_reason']}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AGENT 3 COMMUNICATION
# ============================================================

st.markdown("#### ✉️ Agent 3 — Customer Communication")

st.write(
    f"**Generation Method:** "
    f"{selected['generation_method']}"
)

st.write(
    f"**Tone:** "
    f"{selected['message_tone']}"
)

st.text_input(
    "Subject",
    value=str(
        selected["message_subject"]
    )
)

st.text_area(
    "Generated Customer Message",
    value=str(
        selected["message_body"]
    ),
    height=240
)


# ============================================================
# HISTORICAL OUTCOME
# ============================================================

st.markdown("#### 📊 Historical Outcome")

col1, col2 = st.columns(2)


with col1:

    actual_status = (
        "Recovered"
        if selected["actual_recovered"] == 1
        else "Not Recovered"
    )

    st.metric(
        "Actual Outcome",
        actual_status
    )


with col2:

    st.metric(
        "Actual Recovered Revenue",
        f"₹{selected['actual_recovered_revenue']:,.2f}"
    )


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander(
    "📋 View Filtered Transaction Data"
):

    display_columns = [
        "transaction_id",
        "failure_type",
        "customer_segment",
        "risk_level",
        "recovery_probability",
        "ai_strategy",
        "expected_revenue",
        "expected_net_value",
        "actual_recovered"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in filtered.columns
    ]

    st.dataframe(
        filtered[available_columns],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ReviveAI • AI-Powered Payment Recovery Intelligence • Dashboard V2"
)