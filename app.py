import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. ADVANCED UI STYLING
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    
    /* Centered Main Heading */
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 50px;
        font-weight: 800;
        padding: 20px 0px;
        margin-bottom: 10px;
    }

    /* Sub-header for Login */
    .sub-header {
        text-align: center;
        color: #444;
        font-size: 22px;
        margin-bottom: 30px;
    }

    /* High Readability Content */
    html, body, [class*="st-"], p, label {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px;
    }

    /* EXACT Result Box Style from Screenshots */
    .result-box {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        min-height: 260px;
    }

    /* News Ticker - Navy Blue */
    .ticker-wrap {
        width: 100%; overflow: hidden; background: #003366;
        padding: 12px 0; border-radius: 10px; margin-bottom: 30px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker 45s linear infinite; color: #ffffff; font-size: 19px;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. AI CONFIGURATION
# Replace with your actual Gemini API Key
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=GEMINI_API_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- PHASE 1: LOGIN WINDOW ---
if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Secure Institutional Access</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        # High-Quality Login Image
        st.image("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800&q=80", use_container_width=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login to Dashboard", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Username or Password")
else:
    # --- PHASE 2: AUTHORIZED DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    
    st.markdown("""<div class="ticker-wrap"><div class="ticker">
        <span style="margin-right:70px;">📈 MSME Sector: Credit growth projected at 12.5% for 2026</span>
        <span style="margin-right:70px;">📢 RBI Alert: New provisioning norms for unsecured loans</span>
        <span style="margin-right:70px;">🚀 Tech Alert: AI-driven credit scoring reduces NPA by 15%</span>
    </div></div>""", unsafe_allow_html=True)

    st.sidebar.title("System Controls")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    t1, t2, t3 = st.tabs(["Individual Analysis", "Portfolio Dashboard", "AI Assistant"])

    with t1:
        st.subheader("🔍 New Loan Evaluation")
        c1, c2 = st.columns(2)
        with c1:
            biz_name = st.text_input("Business Name", value="Sharma Global Ventures")
            rev = st.number_input("Annual Revenue (₹ Cr)", value=2.0)
            years = st.number_input("Years in Business", value=6)
            industry = st.selectbox("Industry Risk", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with c2:
            cibil = st.number_input("CIBIL Score", min_value=300, max_value=900, value=720)
            dti = st.slider("Debt-to-Income (%)", 0, 100, 35
