import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="FinTech AI Hub", layout="wide")

# 2. Login Logic
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
    # --- APP HEADER ---
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title("🛡️ MSME AI Credit Risk System")
    
    # --- TAB SYSTEM ---
    tab1, tab2 = st.tabs(["Individual Analysis", "Bulk Portfolio Dashboard"])

    # --- TAB 1: INDIVIDUAL ANALYSIS (Your Original Feature) ---
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
        
        if st.button("Generate AI Assessment"):
            # Calculation Logic
            score = ((cibil-300)/600*40) + (min(years/10*30, 30)) + (max(0, (1 - debt/revenue)*30))
            
            st.subheader(f"Report for {biz_name}")
            if score > 70:
                st.success(f"**Final Decision: APPROVED** (Score: {score:.1f}/100)")
                st.info("AI Assessment: Strong repayment capacity and credit history.")
            elif score > 50:
                st.warning(f"**Final Decision: REFER TO COMMITTEE** (Score: {score:.1f}/100)")
                st.info("AI Assessment: Marginal scores. Requires additional collateral.")
            else:
                st.error(f"**Final Decision: REJECTED** (Score: {score:.1f}/100)")
                st.info("AI Assessment: High risk of default due to low CIBIL/High Leverage.")

    # --- TAB 2: BULK DASHBOARD (The New Feature) ---
    with tab2:
        st.header("Portfolio Analytics")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            # Dashboard Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Cases", len(df))
            if "CIBIL" in df.columns:
                m2.metric("Avg CIBIL", f"{df['CIBIL'].mean():.0f}")
                
            # Charts
            c1, c2 = st.columns(2)
            if "CIBIL" in df.columns:
                fig = px.box(df, y="CIBIL", title="Credit Score Spread", points="all")
                c1.plotly_chart(fig, use_container_width=True)
            
            if "Industry" in df.columns:
                fig2 = px.pie(df, names="Industry", title="Portfolio Sector Mix")
                c2.plotly_chart(fig2, use_container_width=True)
                
            st.dataframe(df)
