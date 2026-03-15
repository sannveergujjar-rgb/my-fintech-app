import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="CreditIQ | Credit Model", layout="wide")

# 2. SNOW BACKGROUND & TEXT STYLING
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #f0f4f8, #ffffff); }
    html, body, [class*="st-"], p, label { color: #000000 !important; font-size: 18px; }
    h1, h2, h3 { color: #003366 !important; font-weight: bold; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #003366; padding: 10px 0; border-radius: 5px; margin-bottom: 20px; }
    .ticker { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; color: #ffffff; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. API CONFIG (Ensure this key is correct!)
FREE_GEMINI_KEY = "AIzaSyDJpB4Awjomr8NEJnHEbVbEA72sASmw0T4"
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # --- LOGIN PAGE ---
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Banker Login</h1>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Access Portal", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- DASHBOARD ---
    st.markdown("""<div class="ticker-wrap"><div class="ticker">
        <span style="margin-right:50px;">📢 RBI Policy: MSME Credit Support increased</span>
        <span style="margin-right:50px;">📈 SENSEX hits record high</span>
        <span style="margin-right:50px;">⚠️ New KYC Norms mandatory from April 2026</span>
    </div></div>""", unsafe_allow_html=True)

    st.sidebar.title("🛡️ FinVantage Pro")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Research Assistant"])

    with tab1:
        st.header("🔍 Credit Risk Underwriting")
        c1, c2 = st.columns(2)
        with c1:
            biz_name = st.text_input("Business Name", value="Test Corp")
            rev = st.number_input("Annual Revenue (₹ Cr)", value=2.0)
            years = st.number_input("Years in Business", value=6)
            industry = st.selectbox("Industry Risk", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with c2:
            cibil = st.number_input("CIBIL Score", value=720)
            dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 35)

        if st.button("Generate Report"):
            # Logic calculation
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else 15)
            s_years = 15 if years > 10 else 12
            s_dti = 25 if dti < 20 else 20
            s_cibil = 25 if cibil >= 750 else 20
            score = s_rev + s_years + s_dti + s_cibil + 7 

            # --- GAUGE WITH VISIBLE NEEDLE ---
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "black"},
                    'bar': {'color': "black", 'thickness': 0.25}, # THIS IS YOUR "ARROW"
                    'steps': [
                        {'range': [0, 60], 'color': "#ff4d4d"},
                        {'range': [60, 80], 'color': "#ffd11a"},
                        {'range': [80, 100], 'color': "#2eb82e"}]
                }))
            st.plotly_chart(fig, use_container_width=True)

            # --- RESULTS ---
            st.subheader(f"Final Decision: {'APPROVED' if score >= 80 else 'REVIEW'}")
            
            # AI RECOMMENDATIONS
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                resp = model.generate_content(f"Provide 3 loan recommendations for {biz_name} with score {score}/100.")
                st.info(resp.text)
            except Exception as e:
                st.warning("AI Assistant busy. Suggestion: Verify collateral and cash flow.")

    with tab2:
        st.write("Upload file to see dashboard.")
        st.file_uploader("Upload Excel")

    with tab3:
        st.header("🤖 AI Assistant")
        q = st.chat_input("Ask me anything...")
        if q:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                st.write(model.generate_content(q).text)
            except:
                st.error("Check your API Key.")
