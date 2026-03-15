import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="FinVantage Pro | White Edition", layout="wide")

# 2. SNOW BACKGROUND & ENHANCED TEXT STYLING
st.markdown("""
    <style>
    /* White Snow Moving Background */
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8, #ffffff);
        background-attachment: fixed;
    }
    
    /* Global Text Enhancement */
    html, body, [class*="st-"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 18px;
        color: #1a1a1a !important; /* Deep black/grey for readability */
    }

    h1, h2, h3 {
        color: #003366 !important; /* Corporate Navy Blue */
        font-weight: 700 !important;
    }

    /* News Ticker Styling */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: #003366;
        padding: 12px 0;
        margin-bottom: 25px;
        border-radius: 5px;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 40s linear infinite;
        color: #ffffff;
        font-size: 20px;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .news-item { margin-right: 60px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 3. HARDCODED API KEY (Replace with your actual key)
FREE_GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- PAGE 1: LOGIN (No Ticker) ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500", use_container_width=True)
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
    # --- PAGE 2: MAIN INTERFACE (Ticker Appears Here) ---
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker">
                <span class="news-item">❄️ RBI Policy Update: Snow-Lending Rates Reduced by 15bps</span>
                <span class="news-item">📈 Market Alert: SENSEX Hits Record High as MSME Credit Demand Surges</span>
                <span class="news-item">⚠️ Compliance: New KYC norms mandatory from April 2026</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.title("🛡️ FinVantage Pro")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    
    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Research Assistant"])

    with tab1:
        st.header("🔍 Credit Risk Underwriting")
        c1, c2 = st.columns(2)
        with c1:
            biz_name = st.text_input("Business Name", placeholder="e.g. Sharma Exports")
            rev = st.number_input("Annual Revenue (INR Lakhs)", value=50)
            years = st.number_input("Years in Business", value=3)
        with c2:
            cibil = st.slider("CIBIL Score", 300, 900, 720)
            debt = st.number_input("Total Debt (INR Lakhs)", value=5)
            goal = st.text_input("Loan Purpose", placeholder="e.g. Expansion")

        if st.button("Generate Final Decision Report", use_container_width=True):
            # Scoring Logic
            risk_score = ((cibil-300)/600*50) + (min(years/10*25, 25)) + (max(0, (1 - debt/rev)*25))
            
            st.divider()
            st.markdown(f"## 📋 Report: {biz_name}")
            
            # Visual Score Gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_score,
                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#003366"},
                         'steps': [{'range': [0, 40], 'color': "#ff4d4d"},
                                   {'range': [40, 75], 'color': "#ffd11a"},
                                   {'range': [75, 100], 'color': "#2eb82e"}]}))
            st.plotly_chart(fig, use_container_width=True)
            

            # Results & Recommendations Section
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.subheader("📊 Result & Score")
                if risk_score > 75:
                    st.success("**DECISION: APPROVED**")
                    status = "Low Risk"
                elif risk_score > 45:
                    st.warning("**DECISION: CONDITIONAL APPROVAL**")
                    status = "Moderate Risk"
                else:
                    st.error("**DECISION: REJECTED**")
                    status = "High Risk"
                st.write(f"**Final Credit Score:** {risk_score:.2f}/100")
                st.write(f"**Risk Category:** {status}")

            with res_col2:
                st.subheader("💡 Suggestions & Recommendations")
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Analyze: Business {biz_name}, CIBIL {cibil}, Score {risk_score}. Provide 3 short expert recommendations for a bank manager regarding this loan."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.write("1. Check collateral value.\n2. Verify GST filings.\n3. Monitor debt-to-equity ratio.")

    with tab2:
        st.header("📊 Portfolio Dashboard")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.style.highlight_max(axis=0))
            if "CIBIL" in df.columns:
                fig2 = px.histogram(df, x="CIBIL", nbins=20, title="Portfolio CIBIL Distribution", template="plotly_white")
                st.plotly_chart(fig2)
                

    with tab3:
        st.header("🤖 AI Financial Assistant")
        user_q = st.chat_input("Ask about banking norms or your portfolio...")
        if user_q:
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.write(model.generate_content(user_q).text)
