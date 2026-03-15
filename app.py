import streamlit as st
import pandas as pd

# MANDATORY: This must be the FIRST line of code
st.set_page_config(page_title="FinTech Risk Portal", layout="wide")

# 1. INITIALIZE LOGIN STATE
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 2. LOGIN FUNCTION
def show_login():
    st.title("🔐 FinTech Portal Login")
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Use admin / finance123")

# 3. MAIN APP LOGIC
if not st.session_state['logged_in']:
    show_login()
else:
    # Sidebar Logout
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.title("🛡️ AI Credit Risk Analyzer")
    st.write("Welcome to the Secure MSME Lending Dashboard")

    # FILE UPLOADER SECTION
    st.header("📂 Bulk Portfolio Analysis")
    uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.success("File Uploaded Successfully!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")

    st.divider()

    # MANUAL INPUT SECTION
    st.sidebar.header("Single Entry Analysis")
    biz = st.sidebar.text_input("Business Name")
    cibil = st.sidebar.slider("CIBIL Score", 300, 900, 700)
    
    if st.sidebar.button("Run AI Analysis"):
        st.subheader(f"Results for {biz}")
        if cibil > 700:
            st.success(f"CIBIL {cibil}: LOW RISK - APPROVE")
        else:
            st.error(f"CIBIL {cibil}: HIGH RISK - REJECT")
