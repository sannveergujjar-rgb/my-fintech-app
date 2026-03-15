import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="FinVantage Pro | Credit Model", layout="wide")

# 2. SNOW BACKGROUND & HIGH CONTRAST TEXT
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8, #ffffff);
    }
    /* Black text for maximum readability */
    html, body, [class*="st-"], p, label {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 { color: #003366 !important; font-weight: bold; }
    
    .ticker-wrap {
        width: 100%; overflow: hidden; background: #003366;
        padding: 10px 0; border-radius: 5px; margin-bottom: 20px;
    }
    .ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker 40s linear infinite; color: #ffffff;
    }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
    """, unsafe_allow_html=True)

# 3. API CONFIG (Replace with your Gemini Key)
FREE_GEMINI_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- LOGIN PAGE ---
if not st.session_state['logged_in']:
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
    # --- MAIN DASHBOARD (Ticker only here) ---
    st.markdown("""<div class="ticker-wrap"><div class="ticker">
        <span style="margin-right:50px;">📢 RBI Policy: MSME Credit Support increased</span>
        <span style="margin-right:50px;">📈 SENSEX hits record high</span>
        <span style="margin-right:50px;">⚠️ New KYC Norms mandatory from April 2026</span>
    </div></div>""", unsafe_allow_html=True)

    st.sidebar.title("🛡️ Credit Score AI Analyzer ")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Research Assistant"])

    with tab1:
        st.header("🔍 Credit Risk Underwriting")
        c1, c2 = st.columns(2)
        with c1:
            biz_name = st.text_input("Business Name")
            rev = st.number_input("Annual Revenue (in ₹ Cr)", min_value=0.0, value=2.0)
            years = st.number_input("Years in Business", min_value=0, value=6)
            industry = st.selectbox("Industry Risk Type", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with c2:
            cibil = st.number_input("Credit Score (CIBIL)", min_value=300, max_value=900, value=720)
            dti = st.slider("Debt-to-Income Ratio (DTI %)", 0, 100, 35)

        if st.button("Generate Final Decision Report", use_container_width=True):
            # --- SCORING LOGIC (FROM YOUR DOC) ---
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else (15 if rev >= 0.5 else (10 if rev >= 0.1 else 5)))
            s_years = 15 if years > 10 else (12 if years >= 5 else (9 if years >= 3 else (6 if years >= 1 else 3)))
            s_dti = 25 if dti < 20 else (20 if dti <= 40 else (15 if dti <= 60 else (10 if dti <= 80 else 5)))
            s_cibil = 25 if cibil >= 750 else (20 if cibil >= 700 else (15 if cibil >= 650 else (10 if cibil >= 600 else 5)))
            ind_map = {"Low Risk": 10, "Medium Risk": 7, "High Risk": 4, "Very High Risk": 2}
            s_ind = ind_map[industry]
              # Data Table for Report
    df = pd.DataFrame({
        "Metric": ["CIBIL Contribution", "Experience Score", "Debt-to-Income Score", "Final Total"],
        "Value": [f"{cibil_score:.2f}", f"{exp_score:.2f}", f"{debt_ratio:.2f}", f"{total_score:.2f}"]
    })
    st.table(df)

            total_score = s_rev + s_years + s_dti + s_cibil + s_ind

            # --- GAUGE CHART (FIXED ARROW) ---
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Credit Health Score", 'font': {'size': 24, 'color': '#003366'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "#003366"}, # The 'Arrow/Needle' equivalent in Streamlit Gauge
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 60], 'color': '#ff4d4d'},
                        {'range': [60, 80], 'color': '#ffd11a'},
                        {'range': [80, 100], 'color': '#2eb82e'}]
                }))
            st.plotly_chart(fig, use_container_width=True)

            # --- RESULTS SECTION ---
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.subheader("📋 Official Decision")
                if total_score >= 80:
                    st.success("**DECISION: APPROVED**")
                    risk_lv = "Low Risk"
                elif total_score >= 60:
                    st.warning("**DECISION: REFERRED FOR REVIEW**")
                    risk_lv = "Medium Risk"
                else:
                    st.error("**DECISION: REJECTED**")
                    risk_lv = "High Risk"
                
                st.write(f"**Total Points:** {total_score}/100")
                st.write(f"**Risk Level:** {risk_lv}")

            with res_c2:
                st.subheader("🤖 AI Suggestions & Recommendations")
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Using the Small Business Credit Risk Model: {biz_name} scored {total_score}/100 and is {risk_lv}. Revenue {rev}Cr, Years {years}, CIBIL {cibil}, DTI {dti}%. Provide 3 specific banking recommendations."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.write("1. Tighten DTI monitoring.\n2. Verify latest GST filings.\n3. Request collateral for Medium Risk cases.")

    # Bulk Dashboard & Chat Assistant remain the same but with White Theme...
    with tab2:
        st.header("📊 Portfolio Analytics")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df)

    with tab3:
        st.header("🤖 AI Financial Assistant")
        user_q = st.chat_input("Ask me about the credit model...")
        if user_q:
            model = genai.GenerativeModel('gemini-1.5-flash')
            st.write(model.generate_content(user_q).text)
