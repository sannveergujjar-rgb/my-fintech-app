import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai

# 1. APP CONFIGURATION
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. PROFESSIONAL UI STYLING
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 50px;
        font-weight: 800;
        padding: 20px 0px;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        min-height: 400px;
        color: #000 !important;
        margin-bottom: 20px;
    }
    .ticker-wrap {
        width: 100%; background: #003366; color: white;
        padding: 12px; border-radius: 10px; margin-bottom: 25px;
        overflow: hidden; white-space: nowrap;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; font-size: 18px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. API SETUP
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- LOGIN SCREEN ---
if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800", use_container_width=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login to Dashboard", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    st.markdown('<div class="ticker-wrap"><div class="ticker">🚀 MSME Credit Demand is up by 18% | 📉 Repo Rate remains at 6.5% | ⚠️ New RBI Guidelines for digital lending mandatory from 2026</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio View", "AI Assistant"])

    with tab1:
        st.subheader("📋 Loan Application Assessment")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Business Name", "Sharma Enterprises")
            rev = st.number_input("Annual Revenue (₹ Cr)", 2.5)
            years = st.number_input("Years in Business", 5)
        with c2:
            cibil = st.number_input("CIBIL Score", 720)
            dti = st.slider("DTI Ratio (%)", 0, 100, 30)
            purpose = st.text_input("Loan Purpose", "Machinery Purchase")

        if st.button("Generate Comprehensive Report", use_container_width=True):
            # LOGIC CALCULATION
            s_rev = 30 if rev > 5 else 20
            s_years = 20 if years > 5 else 15
            s_cibil = 30 if cibil > 750 else 20
            s_dti = 20 if dti < 40 else 10
            score = s_rev + s_years + s_cibil + s_dti

            # GAUGE CHART (SHARP ARROW)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "black"},
                    'bar': {'color': "#1a1a1a", 'thickness': 0.25}, # BLACK NEEDLE
                    'steps': [
                        {'range': [0, 60], 'color': "#ff4d4d"},
                        {'range': [60, 80], 'color': "#ffd11a"},
                        {'range': [80, 100], 'color': "#2eb82e"}]
                }))
            fig.update_layout(height=350, margin=dict(t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)

            

            # EXPANDED RESULT STYLE
            st.markdown(f"### 📄 Detailed Credit Report: {name}")
            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f"""<div class="result-box">
                    <h4>📊 Quantitative Scoring Analysis</h4>
                    <hr>
                    <b>Final Credit Score:</b> {score}/100<br>
                    <b>Loan Decision:</b> {'APPROVED' if score >= 80 else 'REFERRED'}<br><br>
                    <b>Scoring Pillars:</b><br>
                    <ul>
                        <li>Revenue Health: {s_rev}/30</li>
                        <li>Business Vintage: {s_years}/20</li>
                        <li>Credit History (CIBIL): {s_cibil}/30</li>
                        <li>Debt Burden (DTI): {s_dti}/20</li>
                    </ul>
                    <b>Financial Summary:</b> The business shows stable cash flow over {years} years. 
                    The DTI of {dti}% suggests manageable debt levels.
                </div>""", unsafe_allow_html=True)

            with res2:
                st.markdown('<div class="result-box"><h4>🤖 AI Underwriting Insights</h4><hr>', unsafe_allow_html=True)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    p = f"Act as a bank credit manager. For business {name} with score {score}/100 and CIBIL {cibil}, provide a detailed analysis including risk factors, mitigating circumstances, and 3 specific loan conditions."
                    st.write(model.generate_content(p).text)
                except:
                    st.write("• Verify secondary income sources.<br>• Request 12-month GST 3B filings.<br>• Monitor working capital cycles closely.")
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.info("Upload Portfolio Excel to analyze multiple businesses.")
        st.file_uploader("Upload File")
    
    with tab3:
        st.subheader("Ask AI Assistant")
        q = st.text_input("Question:")
        if st.button("Query"):
            if q:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    st.write(model.generate_content(q).text)
                except: st.error("Check API Key.")
