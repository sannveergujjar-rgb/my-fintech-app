import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. MANDATORY PAGE CONFIG
st.set_page_config(page_title="AI Credit Risk Portal", layout="wide")

# 2. DYNAMIC LIVE BACKGROUND & STYLING
# This CSS adds a professional gradient animation to the background
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-title {
        color: white;
        text-shadow: 2px 2px 4px #000000;
        text-align: center;
    }
    </style>
    """, unsafe_allow_ Harris=True)

# 3. TOP BANNER IMAGE
# We use a high-quality relevant image from a public URL
st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80&w=1000", 
         caption="FinTech Underwriting & Risk Management Interface", use_container_width=True)

# 4. HARDCODED API KEY & LOGIN
# REPLACE 'YOUR_GEMINI_API_KEY_HERE' with your actual key from Google AI Studio
FREE_GEMINI_KEY = "AIzaSyDJpB4Awjomr8NEJnHEbVbEA72sASmw0T4" 
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 class='main-title'>🔐 FinTech Portal Login</h1>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "finance123":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Credentials")
else:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.markdown("<h1 class='main-title'>🛡️ MSME AI Credit Risk System</h1>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Chat Assistant"])

    # --- TAB 1: INDIVIDUAL ANALYSIS ---
    with tab1:
        st.header("Single Loan Underwriting")
        biz = st.text_input("Business Name")
        cibil = st.slider("CIBIL Score", 300, 900, 750)
        if st.button("Generate Result"):
            if cibil > 700: st.success("APPROVED")
            else: st.error("REJECTED")

    # --- TAB 2: BULK DASHBOARD ---
    with tab2:
        st.header("Portfolio Analytics")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.plotly_chart(px.histogram(df, x="CIBIL", title="Portfolio Health"))

    # --- TAB 3: AI CHAT ASSISTANT (AUTOMATED KEY) ---
    with tab3:
        st.header("🤖 Financial AI Assistant")
        user_query = st.chat_input("Ask me anything about this portfolio or credit risk...")
        
        if user_query:
            with st.chat_message("user"):
                st.write(user_query)
            
            with st.chat_message("assistant"):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_query)
                    st.write(response.text)
                except Exception as e:
                    st.error("AI is currently unavailable. Please check the API key.")
