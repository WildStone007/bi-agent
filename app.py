import streamlit as st
import matplotlib.pyplot as plt
from utils import load_data, process_query, generate_insights

st.set_page_config(page_title="BI Agent", layout="wide")

st.title("🤖 Business Intelligence Agent")
st.success("System Ready ✅")

st.write("Ask questions like: 'Energy sector pipeline this quarter'")

# Load data
deals, work_orders = load_data()

query = st.text_input("Enter your query:")

if query:
    df, total_value, count = process_query(query, deals, work_orders)
    result = generate_insights(df, total_value, count)

    st.markdown(result)

    # ---- KPI CARDS ---- #
    if not df.empty:
        col1, col2, col3 = st.columns(3)

        avg = total_value / count if count > 0 else 0

        col1.metric("Total Deals", count)
        col2.metric("Pipeline Value", f"{total_value}")
        col3.metric("Avg Deal Size", f"{round(avg, 2)}")

    # ---- CHART ---- #
    if not df.empty and 'deal_value' in df.columns:
        st.subheader("📊 Deal Value Distribution")

        fig, ax = plt.subplots()
        df['deal_value'].plot(kind='bar', ax=ax)
        ax.set_ylabel("Deal Value")
        ax.set_xlabel("Deals")

        st.pyplot(fig)

    # ---- TREND INSIGHT ---- #
    if not df.empty:
        st.subheader("📈 Insight")

        if count > 3:
            st.info("Trend: Strong pipeline with consistent deal flow")
        elif count > 1:
            st.info("Trend: Moderate activity in selected segment")
        else:
            st.info("Trend: Low activity — potential growth area")

    # ---- DATA VIEW ---- #
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(df.head(100))

# Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.write("AI-powered BI assistant using CSV data.")