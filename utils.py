def process_query(query, deals, work_orders):
    query = query.lower().strip()

    df = deals.copy()

    # ---- VALID KEYWORDS ---- #
    keywords = ["energy", "won", "lost", "quarter"]

    if not any(word in query for word in keywords):
        return pd.DataFrame(), 0, 0

    # ---- FILTERS ---- #

    # Sector filter
    if "energy" in query and 'sector' in df.columns:
        df = df[df['sector'].astype(str).str.contains("energy", case=False, na=False)]

    # Status filter
    if "won" in query and 'status' in df.columns:
        df = df[df['status'].astype(str).str.contains("won", case=False, na=False)]

    if "lost" in query and 'status' in df.columns:
        df = df[df['status'].astype(str).str.contains("lost", case=False, na=False)]

    # ---- QUARTER HANDLING ---- #

    if "quarter" in query:

        # Case 1: ONLY "quarter"
        if query.strip() == "quarter":
            for col in df.columns:
                if "date" in col and pd.api.types.is_datetime64_any_dtype(df[col]):
                    df['quarter'] = df[col].dt.to_period('Q').astype(str)
            return df, 0, len(df)

        # Case 2: filter current quarter
        else:
            current_q = (datetime.now().month - 1) // 3 + 1

            for col in df.columns:
                if "date" in col and pd.api.types.is_datetime64_any_dtype(df[col]):
                    df = df[df[col].dt.quarter == current_q]

    # ---- METRICS ---- #

    value_col = None
    for col in df.columns:
        if "value" in col or "amount" in col:
            value_col = col
            break

    total_value = df[value_col].sum() if value_col and not df.empty else 0
    count = len(df)

    return df, total_value, count