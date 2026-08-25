import os
import random
import numpy as np
import pandas as pd

# Reproducibility
random.seed(42)
np.random.seed(42)

# Number of transactions
N_TRANSACTIONS = 5000

# Output directory
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "reviveai_transactions.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# Customer / transaction values
# -----------------------------

payment_methods = [
    "credit_card",
    "debit_card",
    "upi",
    "net_banking",
    "wallet"
]

failure_types = [
    "card_declined",
    "insufficient_funds",
    "expired_card",
    "gateway_error",
    "authentication_failed",
    "network_error"
]

customer_segments = [
    "premium",
    "regular",
    "new",
    "at_risk"
]

recovery_methods = [
    "smart_retry",
    "customer_outreach",
    "alternative_payment",
    "payment_plan",
    "discount_offer",
    "human_escalation"
]

records = []

for i in range(N_TRANSACTIONS):

    transaction_id = f"TXN{i + 100001:06d}"
    customer_id = f"CUST{random.randint(10000, 19999)}"

    amount = round(
        np.random.lognormal(mean=7.0, sigma=0.65),
        2
    )

    amount = min(max(amount, 100), 100000)

    payment_method = random.choice(payment_methods)
    failure_type = random.choice(failure_types)
    customer_segment = random.choices(
        customer_segments,
        weights=[0.15, 0.55, 0.20, 0.10]
    )[0]

    previous_failures = np.random.poisson(1.2)
    previous_failures = min(previous_failures, 8)

    customer_lifetime_value = round(
        np.random.lognormal(mean=9.0, sigma=0.8),
        2
    )

    customer_lifetime_value = min(
        max(customer_lifetime_value, 500),
        500000
    )

    days_since_last_purchase = random.randint(1, 365)

    retry_count = random.randint(0, 4)

    account_age_days = random.randint(30, 2000)

    website_visits_last_30_days = np.random.poisson(4)

    cart_additions_last_30_days = np.random.poisson(1)

    # --------------------------------
    # Recovery probability construction
    # --------------------------------

    recovery_score = 0.50

    # Failure-specific effects
    if failure_type in ["gateway_error", "network_error"]:
        recovery_score += 0.20

    elif failure_type == "expired_card":
        recovery_score += 0.05

    elif failure_type == "authentication_failed":
        recovery_score -= 0.05

    elif failure_type == "insufficient_funds":
        recovery_score -= 0.10

    elif failure_type == "card_declined":
        recovery_score -= 0.08

    # Customer segment effects
    if customer_segment == "premium":
        recovery_score += 0.15

    elif customer_segment == "at_risk":
        recovery_score -= 0.15

    elif customer_segment == "new":
        recovery_score += 0.03

    # Previous failures
    recovery_score -= previous_failures * 0.035

    # Recent activity
    recovery_score += min(website_visits_last_30_days * 0.015, 0.15)

    recovery_score += min(cart_additions_last_30_days * 0.025, 0.10)

    # Retry fatigue
    recovery_score -= retry_count * 0.04

    # Customer value
    if customer_lifetime_value > 100000:
        recovery_score += 0.08

    elif customer_lifetime_value < 2000:
        recovery_score -= 0.04

    # Transaction amount
    if amount > 50000:
        recovery_score -= 0.05

    # Keep score within valid probability range
    recovery_probability = np.clip(
        recovery_score,
        0.05,
        0.95
    )

    # --------------------------------
    # Generate recovery outcome
    # --------------------------------

    recovered = np.random.binomial(
        1,
        recovery_probability
    )

    recovered_revenue = (
        amount if recovered == 1 else 0
    )

    # --------------------------------
    # Choose recovery method
    # --------------------------------

    if failure_type in ["gateway_error", "network_error"]:
        recovery_method = "smart_retry"

    elif failure_type == "expired_card":
        recovery_method = "alternative_payment"

    elif failure_type == "insufficient_funds":
        recovery_method = random.choice(
            ["payment_plan", "customer_outreach"]
        )

    elif failure_type == "authentication_failed":
        recovery_method = "customer_outreach"

    elif customer_segment == "premium":
        recovery_method = "customer_outreach"

    elif recovery_probability < 0.30:
        recovery_method = "human_escalation"

    else:
        recovery_method = random.choice(
            [
                "smart_retry",
                "customer_outreach",
                "alternative_payment"
            ]
        )

    # --------------------------------
    # Failure severity
    # --------------------------------

    severity_score = 50

    severity_score += previous_failures * 5
    severity_score += retry_count * 4

    if amount > 50000:
        severity_score += 10

    if customer_segment == "premium":
        severity_score += 5

    severity_score = int(
        np.clip(severity_score, 0, 100)
    )

    # --------------------------------
    # Record
    # --------------------------------

    records.append({
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_amount": amount,
        "payment_method": payment_method,
        "failure_type": failure_type,
        "customer_segment": customer_segment,
        "previous_failures": previous_failures,
        "customer_lifetime_value": customer_lifetime_value,
        "days_since_last_purchase": days_since_last_purchase,
        "retry_count": retry_count,
        "account_age_days": account_age_days,
        "website_visits_last_30_days": website_visits_last_30_days,
        "cart_additions_last_30_days": cart_additions_last_30_days,
        "recovery_probability": round(
            recovery_probability,
            3
        ),
        "recovered": recovered,
        "recovered_revenue": round(
            recovered_revenue,
            2
        ),
        "recovery_method": recovery_method,
        "severity_score": severity_score
    })


# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(records)

# Save CSV
df.to_csv(
    OUTPUT_FILE,
    index=False
)

# -----------------------------
# Display summary
# -----------------------------

print("=" * 60)
print("REVIVEAI DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Total transactions : {len(df):,}")
print(f"Recovered payments : {df['recovered'].sum():,}")
print(
    f"Recovery rate      : "
    f"{df['recovered'].mean() * 100:.2f}%"
)

print(
    f"Total failed value : "
    f"₹{df['transaction_amount'].sum():,.2f}"
)

print(
    f"Recovered revenue  : "
    f"₹{df['recovered_revenue'].sum():,.2f}"
)

print("\nFailure Types:")
print(
    df["failure_type"]
    .value_counts()
    .to_string()
)

print("\nCustomer Segments:")
print(
    df["customer_segment"]
    .value_counts()
    .to_string()
)

print("\nDataset saved to:")
print(OUTPUT_FILE)

print("=" * 60)