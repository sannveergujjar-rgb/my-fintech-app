import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="FinVantage AI | Credit Risk", layout="wide")

# 2. PROFESSIONAL GLASS-DARK THEME & NEWS ANIMATION
st.markdown("""
    <style>
    /* Professional Dark Gradient Background */
    .stApp {
        background: radial-gradient(circle at 24.1% 44.7%, rgb(12, 12, 35) 0%, rgb(0, 0, 0) 90%);
        color: #FFFFFF;
    }
    
    /* User-Friendly Login Box */
    .login-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* News Ticker Styling */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: rgba(0, 200, 255, 0.1);
        padding: 10px 0;
        border-bottom: 1px solid #00c8ff;
        margin-bottom: 20px;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 30s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .news-item { font-weight: bold; color: #00c8ff; margin-right: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 3. NEWS TICKER POPUP (Just like Bloomberg/MoneyControl)
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="news-item">📢 RBI maintains Repo Rate at 6.5%</span>
            <span class="news-item">📈 MSME Lending grows by 14% this quarter</span>
            <span class="news-item">⚠️ High Alert: New Cyber-frauds reported in Digital Lending</span>
            <span class="news-item">💼 Government announces new Credit Guarantee Scheme for Tech Startups</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. HARDCODED API KEY (Replace with your actual key)
FREE_GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=FREE_GEMINI_KEY)

# 5. USER-FRIENDLY LOGIN WINDOW
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Portal Access</h2>", unsafe_allow_html=True)
        user = st.text_input("Administrator ID")
        pw = st.text_input("Secure Password", type="password")
        if st.button("Authorize Access", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Denied: Check Credentials")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- AUTHENTICATED INTERFACE ---
    st.sidebar.title("🛡️ FinVantage Pro")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    
    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Research Assistant"])

    with tab1:
        st.header("🔍 Smart Underwriting")
        
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                biz_name = st.text_input("Business Name")
                rev = st.number_input("Annual Revenue (INR Lakhs)", value=50)
                years = st.number_input("Years in Business", value=2)
            with c2:
                cibil = st.slider("CIBIL Score", 300, 900, 700)
                debt = st.number_input("Total Debt (INR Lakhs)", value=10)

        if st.button("Generate Comprehensive AI Report", use_container_width=True):
            # Scoring Logic
            risk_score = ((cibil-300)/600*50) + (min(years/10*25, 25)) + (max(0, (1 - debt/rev)*25))
            
            # Risk Gauge Graph
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                title = {'text': "Credit Health Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#00c8ff"},
                    'steps' : [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}]}))
            st.plotly_chart(fig)

            # AI Interpretation
            st.subheader("🤖 AI Risk Assessment")
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                query = f"Act as a bank manager. Analyze: {biz_name}, CIBIL {cibil}, Debt-to-Revenue {(debt/rev)*100:.1f}%. Give 2 pros, 2 cons, and a final decision."
                response = model.generate_content(query)
                st.write(response.text)
            except:
                st.write("AI Assistant temporarily offline. Scoring suggests: " + ("APPROVED" if risk_score > 65 else "REFERRED"))

    with tab2:
        st.header("📊 Portfolio Visualization")
        # Same dashboard as before but with Dark Theme charts
        uploaded_file = st.file_uploader("Upload Portfolio", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            fig = px.scatter(df, x="CIBIL", y="Loan_Amount", color="Industry", size="Loan_Amount", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("💬 AI Assistant")
        user_q = st.chat_input("Ask about NPA policies...")
        if user_q:
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.write(model.generate_content(user_q).text)
