import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI # New Integration

st.set_page_config(page_title="FinTech AI Hub", layout="wide")

# 1. Login Logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 FinTech Portal Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "finance123":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Credentials")
else:
    # --- SIDEBAR API CONFIG ---
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.sidebar.divider()
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

    st.title("🛡️ MSME AI Credit Risk System")
    tab1, tab2 = st.tabs(["Individual Analysis", "Bulk Portfolio Dashboard"])

    with tab1:
        st.header("Manual Loan Underwriting")
        col1, col2 = st.columns(2)
        with col1:
            biz_name = st.text_input("Business Name")
            revenue = st.number_input("Annual Revenue (₹ Lakhs)", value=50)
            debt = st.number_input("Total Debt (₹ Lakhs)", value=10)
        with col2:
            years = st.slider("Years in Business", 0, 30, 5)
            cibil = st.slider("CIBIL Score", 300, 900, 750)
        
        if st.button("Generate ChatGPT Assessment"):
            if not api_key:
                st.error("Please enter your API Key in the sidebar first!")
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    # The Prompt for ChatGPT
                    prompt = f"Analyze this Indian MSME loan: Business {biz_name}, Revenue ₹{revenue}L, Debt ₹{debt}L, {years} years old, CIBIL {cibil}. Write a 3-sentence professional credit memo recommending Approval or Rejection based on risk."
                    
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    st.subheader("🤖 ChatGPT Credit Memo")
                    st.write(response.choices[0].message.content)
                    st.success("Analysis Complete")
                except Exception as e:
                    st.error(f"AI Error: {e}")

    with tab2:
        st.header("Portfolio Analytics")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.head())
            if "CIBIL" in df.columns:
                fig = px.histogram(df, x="CIBIL", title="Portfolio Credit Health")
                st.plotly_chart(fig)
