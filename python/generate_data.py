import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

BASE_DIR = "data/raw"
os.makedirs(BASE_DIR, exist_ok=True)

# -----------------------
# CRM - Customers
# -----------------------
n_customers = 1200

customers = []
for i in range(n_customers):
    customer_id = f"CUST_{i:05d}"
    external_id = f"EXT_{random.randint(1, 900):05d}"  # gera duplicidade
    email = f"user{external_id.lower()}@email.com"
    state = random.choice(["SP", "RJ", "MG", "CE", "BA", None])
    segment = random.choice(["low", "mid", "high", None])
    signup_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 400))
    last_update = signup_date + timedelta(days=random.randint(-30, 200))  # datas ruins

    customers.append([
        customer_id,
        external_id,
        email,
        state,
        segment,
        signup_date.date(),
        last_update.date()
    ])

customers_df = pd.DataFrame(
    customers,
    columns=[
        "customer_id",
        "external_id",
        "email",
        "state",
        "segment",
        "signup_date",
        "last_update"
    ]
)

customers_df.to_csv(f"{BASE_DIR}/customers_crm_raw.csv", index=False)

# -----------------------
# Transactions
# -----------------------
transactions = []
for i in range(8000):
    transaction_id = f"TX_{i:07d}"
    customer_id = random.choice(customers_df["customer_id"])
    amount = round(random.uniform(-20, 500), 2)  # valores negativos
    date = datetime(2023, 6, 1) + timedelta(days=random.randint(0, 200))

    transactions.append([
        transaction_id,
        customer_id,
        amount,
        date.date()
    ])

transactions_df = pd.DataFrame(
    transactions,
    columns=["transaction_id", "customer_id", "amount", "transaction_date"]
)

transactions_df.to_csv(f"{BASE_DIR}/transactions_raw.csv", index=False)

# -----------------------
# Campaigns
# -----------------------
campaigns_df = pd.DataFrame([
    ["CMP_01", "Cashback Reactivation", "2023-08-01", "2023-08-31"],
    ["CMP_02", "Loyalty Points", "2023-09-01", "2023-09-30"]
], columns=["campaign_id", "campaign_name", "start_date", "end_date"])

campaigns_df.to_csv(f"{BASE_DIR}/campaigns_raw.csv", index=False)

# -----------------------
# Campaign Activations
# -----------------------
activations = []
for _, row in customers_df.sample(600).iterrows():
    activations.append([
        row["customer_id"],
        random.choice(["CMP_01", "CMP_02"]),
        datetime(2023, 8, 1) + timedelta(days=random.randint(0, 30))
    ])

activations_df = pd.DataFrame(
    activations,
    columns=["customer_id", "campaign_id", "activation_date"]
)

# duplicidade proposital
activations_df = pd.concat([activations_df, activations_df.sample(50)])

activations_df.to_csv(f"{BASE_DIR}/campaign_activations_raw.csv", index=False)

print("✅ Dados sintéticos gerados com sucesso em data/raw")
