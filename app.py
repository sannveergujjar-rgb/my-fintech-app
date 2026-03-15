import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai # Free Google AI

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
    st.sidebar.info("Get a free key from Google AI Studio")
    free_api_key = st.sidebar.text_input("Enter Free Gemini API Key", type="password")

    st.title("🛡️ MSME AI Credit Risk System")
    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Financial Assistant"])

    # --- TAB 1: MANUAL ENTRY ---
    with tab1:
        st.header("Single Loan Underwriting")
        biz_name = st.text_input("Business Name")
        cibil = st.slider("CIBIL Score", 300, 900, 750)
        if st.button("Quick Score"):
            if cibil > 700: st.success(f"Score: {cibil} - Strong")
            else: st.error(f"Score: {cibil} - Weak")

    # --- TAB 2: BULK DASHBOARD ---
    with tab2:
        st.header("Portfolio Analytics")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.head())
            if "CIBIL" in df.columns:
                st.plotly_chart(px.histogram(df, x="CIBIL", title="Credit Health"))

    # --- TAB 3: FREE AI ASSISTANT ---
    with tab3:
        st.header("🤖 Free AI Financial Consultant")
        st.write("Ask the AI about credit policies, NPA management, or risk ratios.")
        user_query = st.text_input("Ask a question (e.g., 'What are the 5 Cs of Credit?')")
        
        if st.button("Ask AI"):
            if not free_api_key:
                st.warning("Please enter your free Gemini API key in the sidebar.")
            else:
                try:
                    genai.configure(api_key=free_api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_query)
                    st.write("### AI Response:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
