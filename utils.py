import pandas as pd
from datetime import datetime


def load_data():
    try:
        deals = pd.read_csv("deals.csv")
    except Exception:
        deals = pd.DataFrame()

    try:
        work_orders = pd.read_csv("work_orders.csv")
    except Exception:
        work_orders = pd.DataFrame()

    # Normalize column names
    deals.columns = deals.columns.str.lower().str.strip()
    work_orders.columns = work_orders.columns.str.lower().str.strip()

    # Fill missing values
    deals.fillna("Unknown", inplace=True)
    work_orders.fillna("Unknown", inplace=True)

    # Convert date columns safely
    for col in deals.columns:
        if "date" in col:
            deals[col] = pd.to_datetime(deals[col], errors='coerce')

    for col in work_orders.columns:
        if "date" in col:
            work_orders[col] = pd.to_datetime(work_orders[col], errors='coerce')

    return deals, work_orders


def process_query(query, deals, work_orders):
    query = query.lower().strip()

    df = deals.copy()

    # VALID KEYWORDS
    keywords = ["energy", "won", "lost", "quarter"]

    if not any(word in query for word in keywords):
        return pd.DataFrame(), 0, 0

    # Sector filter
    if "energy" in query and 'sector' in df.columns:
        df = df[df['sector'].astype(str).str.contains("energy", case=False, na=False)]

    # Status filter
    if "won" in query and 'status' in df.columns:
        df = df[df['status'].astype(str).str.contains("won", case=False, na=False)]

    if "lost" in query and 'status' in df.columns:
        df = df[df['status'].astype(str).str.contains("lost", case=False, na=False)]

    # Quarter handling
    if "quarter" in query:

        if query.strip() == "quarter":
            for col in df.columns:
                if "date" in col and pd.api.types.is_datetime64_any_dtype(df[col]):
                    df['quarter'] = df[col].dt.to_period('Q').astype(str)
            return df, 0, len(df)

        else:
            current_q = (datetime.now().month - 1) // 3 + 1

            for col in df.columns:
                if "date" in col and pd.api.types.is_datetime64_any_dtype(df[col]):
                    df = df[df[col].dt.quarter == current_q]

    # Metrics
    value_col = None
    for col in df.columns:
        if "value" in col or "amount" in col:
            value_col = col
            break

    total_value = df[value_col].sum() if value_col and not df.empty else 0
    count = len(df)

    return df, total_value, count


def generate_insights(df, total_value, count):

    if 'quarter' in df.columns and total_value == 0:
        summary = df['quarter'].value_counts().to_string()
        return f"""
### 📊 Deals by Quarter

{summary}
"""

    if df.empty:
        return "🤖 Please ask a meaningful business query like 'energy deals this quarter' or 'won deals'."

    avg = total_value / count if count > 0 else 0

    return f"""
### 📊 Business Insights

- Total Deals: {count}
- Total Pipeline Value: {round(total_value, 2)}
- Average Deal Size: {round(avg, 2)}

### 📌 Observations
- Data processed successfully
- Results may include incomplete records

### ⚠️ Data Quality Note
Some fields may contain missing or inconsistent values.
"""