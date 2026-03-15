import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai

# 1. APP CONFIGURATION
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. PROFESSIONAL UI STYLING (CSS)
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 50px;
        font-weight: 800;
        padding-top: 20px;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 20px;
        margin-bottom: 30px;
    }
    .result-box {
        background-color: #f9f9f9;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ddd;
        min-height: 250px;
        color: #000 !important;
    }
    .ticker-wrap {
        width: 100%; background: #003366; color: white;
        padding: 10px; border-radius: 10px; margin-bottom: 25px;
        overflow: hidden; white-space: nowrap;
    }
    .ticker {
        display: inline-block;
        animation: ticker 40s linear infinite;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. API SETUP
# PLEASE ADD YOUR KEY HERE
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- LOGIN PAGE ---
if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Secure Banker Portal</p>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800", use_container_width=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- MAIN DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="ticker-wrap"><div class="ticker">📢 Market Alert: RBI keeps repo rates steady at 6.5% | 📈 MSME Loan demand rises by 15% | ⚠️ Update KYC for all High-Risk accounts</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Help"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Business Name", "Global Tech")
            rev = st.number_input("Annual Revenue (₹ Cr)", 2.5)
            years = st.number_input("Years in Business", 5)
            ind = st.selectbox("Industry Risk", ["Low Risk", "Medium Risk", "High Risk"])
        with c2:
            cibil = st.number_input("CIBIL Score", 720)
            dti = st.slider("DTI Ratio (%)", 0, 100, 30)
            st.text_input("Loan Purpose", "Expansion")

        if st.button("Generate AI Credit Report", use_container_width=True):
            # LOGIC
            score = 75  # Default for visual check
            # Exact Factor scoring
            s1 = 25 if rev > 5 else 15
            s2 = 25 if cibil > 750 else 15
            score = s1 + s2 + 35 

            # GAUGE CHART (SHARP ARROW)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "black", 'thickness': 0.2}, # SHARP NEEDLE
                    'steps': [
                        {'range': [0, 60], 'color': "red"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}]
                }))
            fig.update_layout(height=300, margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

            # RESULT BOXES
            st.markdown(f"### Assessment for {name}")
            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f'<div class="result-box"><h4>📊 Result</h4><b>Score:</b> {score}/100<br><b>Decision:</b> REFERRED</div>', unsafe_allow_html=True)
            with res2:
                st.markdown('<div class="result-box"><h4>🤖 AI Suggestion</h4>Check GST filings and verify collateral status.</div>', unsafe_allow_html=True)

    with tab2:
        st.file_uploader("Upload Portfolio")
    
    with tab3:
        st.text_input("Ask AI")
