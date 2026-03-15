import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. THEME & ALIGNMENT STYLING
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    
    /* Center and Style the Main Heading */
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 45px;
        font-weight: 800;
        padding: 20px 0px;
        border-bottom: 2px solid #f0f2f6;
        margin-bottom: 30px;
    }

    /* High Readability Text */
    html, body, [class*="st-"], p, label {
        color: #000000 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 18px;
    }

    /* Professional Result Box */
    .result-box {
        background-color: #fcfcfc;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #eef2f7;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
        min-height: 250px;
    }

    /* News Ticker */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: #003366;
        padding: 12px 0; border-radius: 8px; margin-bottom: 25px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker 45s linear infinite; color: #ffffff; font-size: 19px;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. API CONFIG (Replace with your Gemini Key)
FREE_GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- LOGIN SCREEN ---
if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        # High-Quality Fintech Image
        st.image("https://images.unsplash.com/photo-1560472355-536de3962603?w=800&q=80", use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Secure Banker Access</h3>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login to Dashboard", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- DASHBOARD HEADER ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    
    st.markdown("""<div class="ticker-wrap"><div class="ticker">
        <span style="margin-right:60px;">🚀 MSME Lending Cap increased by Govt</span>
        <span style="margin-right:60px;">📉 Inflation dips to 4.2% - Positive for Borrowers</span>
        <span style="margin-right:60px;">🛑 Alert: RBI updates NPA reporting guidelines</span>
    </div></div>""", unsafe_allow_html=True)

    st.sidebar.title("🛡️ System Controls")
    st.sidebar.button("Log Out", on_click=lambda: st.session_state.update({"logged_in": False}))

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio Dashboard", "AI Research Assistant"])

    with tab1:
        st.subheader("📋 New Loan Application Underwriting")
        c1, c2 = st.columns(2)
        with c1:
            biz_name = st.text_input("Business Name", value="Global Tech Solutions")
            rev = st.number_input("Annual Revenue (₹ Cr)", value=1.5)
            years = st.number_input("Years in Business", value=5)
            industry = st.selectbox("Industry Risk Category", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with c2:
            cibil = st.number_input("CIBIL Score", value=740, min_value=300, max_value=900)
            dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 25)
            purpose = st.text_input("Loan Purpose", value="Working Capital")

        if st.button("Analyze Creditworthiness", use_container_width=True):
            # CALCULATE POINTS BASED ON YOUR DOCUMENT
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else 15)
            s_years = 15 if years > 10 else (12 if years >= 5 else 9)
            s_dti = 25 if dti < 20 else (20 if dti <= 40 else 15)
            s_cibil = 25 if cibil >= 750 else (20 if cibil >= 700 else 15)
            ind_val = {"Low Risk": 10, "Medium Risk": 7, "High Risk": 4, "Very High Risk": 2}[industry]
            
            total_score = s_rev + s_years + s_dti + s_cibil + ind_val

            # --- GAUGE CHART WITH SHARP NEEDLE ---
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=total_score,
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "black", 'tickwidth': 2},
                    'bar': {'color': "#1a1a1a", 'thickness': 0.25}, # BLACK SHARP ARROW
                    'steps': [
                        {'range': [0, 60], 'color': "#ff6666"},
                        {'range': [60, 80], 'color': "#ffcc00"},
                        {'range': [80, 100], 'color': "#00cc66"}]
                }))
            st.plotly_chart(fig, use_container_width=True)
            

            # --- REPORT BOXES (IMAGE STYLE) ---
            st.markdown(f"### Assessment Report: {biz_name}")
            res_c1, res_c2 = st.columns(2)
            
            with res_c1:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("📊 Score & Status")
                if total_score >= 80:
                    st.success("**FINAL DECISION: APPROVED**")
                    risk_txt = "Low Risk"
                elif total_score >= 60:
                    st.warning("**FINAL DECISION: REFERRED**")
                    risk_txt = "Medium Risk"
                else:
                    st.error("**FINAL DECISION: REJECTED**")
                    risk_txt = "High Risk"
                st.write(f"**Calculated Score:** {total_score}/100")
                st.write(f"**Classification:** {risk_txt}")
                st.markdown('</div>', unsafe_allow_html=True)

            with res_c2:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.subheader("🤖 AI Suggestions")
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Act as a Senior Credit Officer. Analyze: {biz_name}, Score {total_score}, CIBIL {cibil}, DTI {dti}%. Provide 3 bulleted strategic recommendations."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.write("• Verify tax audit reports.\n• Monitor Debt-Service Coverage Ratio.\n• Check for existing defaults.")
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.header("📈 Portfolio Performance")
        st.info("Upload Excel/CSV to analyze bulk applications.")
        st.file_uploader("Select Financial Dataset")

    with tab3:
        st.header("🤖 Financial AI Assistant")
        q = st.text_input("Enter your query (e.g., 'What are Basel III norms?')")
        if st.button("Search AI Database"):
            if q:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.write(model.generate_content(q).text)
                except:
                    st.error("AI service error. Check API Key.")
