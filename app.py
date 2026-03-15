import streamlit as st
import pandas as pd

# 1. SIMPLE LOGIN SYSTEM
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    st.title("🔐 FinTech Portal Login")
    user = st.text_input("Username (MBA Student)")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "finance123": # You can change these
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Credentials")

# 2. MAIN APP INTERFACE
if st.session_state['logged_in']:
    st.set_page_config(page_title="MSME AI Analyzer", layout="wide")
    if st.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.title("🛡️ AI Credit Risk Analyzer")
    
    # FEATURE: FILE UPLOAD
    st.header("📂 Bulk Portfolio Analysis")
    uploaded_file = st.file_uploader("Upload Business Data (Excel/CSV)", type=["csv", "xlsx"])
    
    if uploaded_file:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.write("### Data Preview", data.head())
        # Add MBA Logic: Calculate Average CIBIL for the file
        if 'CIBIL' in data.columns:
            st.info(f"Average Portfolio CIBIL: {data['CIBIL'].mean():.2f}")
    
    st.divider()

    # SIDEBAR: MANUAL INPUT
    st.sidebar.header("Manual Single Entry")
    biz_name = st.sidebar.text_input("Business Name")
    revenue = st.sidebar.number_input("Annual Revenue (₹ Lakhs)", value=50)
    years = st.sidebar.slider("Years in Business", 0, 30, 5)
    cibil = st.sidebar.slider("CIBIL Score", 300, 900, 750)

    if st.sidebar.button("Analyze Risk"):
        # Logic: (CIBIL 40% + Exp 30% + Revenue 30%)
        score = ((cibil-300)/600*40) + (min(years/10*30, 30)) + 30
        st.subheader(f"Results for {biz_name}")
        if score > 70:
            st.success(f"Score: {score:.1f} - APPROVED (Low Risk)")
        else:
            st.error(f"Score: {score:.1f} - REJECTED (High Risk)")

else:
    login()
