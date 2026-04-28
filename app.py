import streamlit as st
from utils import load_data, process_query, generate_insights

st.set_page_config(page_title="BI Agent", layout="wide")

st.title("🤖 Business Intelligence Agent")
st.write("Ask questions like: 'Energy sector pipeline this quarter'")

# Load data
deals, work_orders = load_data()

query = st.text_input("Enter your query:")

if query:
    df, total_value, count = process_query(query, deals, work_orders)
    result = generate_insights(df, total_value, count)

    st.markdown(result)

    # Show filtered data
    with st.expander("🔍 View Filtered Data"):
        st.dataframe(df.head(100))

# Sidebar info
st.sidebar.title("ℹ️ Info")
st.sidebar.write("This app simulates Monday.com BI using CSV data.")