import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SYSTEM CONFIGURATION
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. BRANDING & UI ARCHITECTURE (CSS)
st.markdown("""
    <style>
    /* Clean Professional Background */
    .stApp { background: #ffffff; }
    
    /* Centered Title Styling */
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 48px;
        font-weight: 800;
        padding: 25px 0px;
        border-bottom: 3px solid #f0f2f6;
        margin-bottom: 35px;
    }

    /* Standardized Typography */
    html, body, [class*="st-"], p, label {
        color: #1a1a1a !important;
        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
        font-size: 17px;
    }

    /* Result Box: Matches your exact style request */
    .result-box {
        background-color: #fcfcfc;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        min-height: 280px;
        margin-top: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.03);
    }

    /* News Ticker */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: #003366;
        padding: 12px 0; border-radius: 8px; margin-bottom: 30px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker 50s linear infinite; color: #ffffff; font-size: 18px;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. AI INITIALIZATION
# Replace with your actual Gemini API Key
GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_KEY)

# Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- UI LOGIC: LOGIN ---
if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    l1, l2, l3 = st.columns([1, 1.6, 1])
    with l2:
        # Premium Login Image (Security Focused)
        st.image("https://images.unsplash.com/photo-1563986768609-322da13575f3?q=80&w=1000", use_container_width=True)
        st.markdown("<h3 style='text-align: center;'>Banker Secure Access</h3>", unsafe_allow_html=True)
        user = st.text_input("Administrator ID")
        pw = st.text_input("Access Token", type="password")
        if st.button("Authorize & Enter", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")
else:
    # --- UI LOGIC: DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    
    # Live News Ticker (Appears only after login)
    st.markdown("""<div class="ticker-wrap"><div class="ticker">
        <span style="margin-right:70px;">📊 RBI Update: Policy rates unchanged - Positive for MSME growth</span>
        <span style="margin-right:70px;">📉 Sector News: Tech services show 12% increase in credit demand</span>
        <span style="margin-right:70px;">⚠️ Regulatory Alert: New Basel IV risk-weighting norms finalized</span>
    </div></div>""", unsafe_allow_html=True)

    st.sidebar.title("System Portfolio")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    t1, t2, t3 = st.tabs(["Individual Analysis", "Bulk Portfolio", "AI Research Assistant"])

    with t1:
        st.subheader("📋 Application Details")
        col_a, col_b = st.columns(2)
        with col_a:
            biz_name = st.text_input("Business Legal Name", value="Sharma Global Ltd")
            rev = st.number_input("Annual Revenue (₹ Cr)", min_value=0.0, value=2.5)
            years = st.number_input("Business Vintage (Years)", min_value=0, value=7)
            industry = st.selectbox("Industry Segment Risk", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with col_b:
            cibil = st.number_input("CIBIL/FICO Score", min_value=300, max_value=900, value=745)
            dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 22)
            purpose = st.text_input("Funding Purpose", value="Working Capital Expansion")

        if st.button("Generate Credit Report", use_container_width=True):
            # QUANTITATIVE SCORING ENGINE (Based on your Document)
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else 15)
            s_years = 15 if years > 10 else (12 if years >= 5 else 9)
            s_dti = 25 if dti < 20 else (20 if dti <= 40 else 15)
