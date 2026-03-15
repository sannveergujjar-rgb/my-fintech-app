import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. Dynamic Live Background & Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #f0f4f8, #ffffff);
    }
    html, body, [class*="st-"], p, label {
        color: #000000 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 {
        color: #003366 !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Config (Replace with your actual key!)
FREE_GEMINI_KEY = "AIzaSyDJpB4Awjomr8NEJnHEbVbEA72sASmw0T4"
genai.configure(api_key=FREE_GEMINI_KEY)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # --- PAGE 1: LOGIN (User Friendly) ---
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>Banker Login</h1>", unsafe_allow_html=True)
        # Added login image
        st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=500", use_container_width=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Access Portal", use_container_width=True):
            if user == "admin" and pw == "finance123":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- PAGE 2: MAIN INTERFACE ---
    # Global corporate Navy Blue Ticker
    st.markdown("""<div style="width:100%; overflow:hidden; background:#003366; padding:10px 0; border-radius:5px; margin-bottom:20px;">
        <div style="display:inline-block; white-space:nowrap; animation:ticker 40s linear infinite; color:#ffffff;">
            <span style="margin-right:50px; font-weight:bold;">📢 RBI maintains Repo Rate at 6.5%</span>
            <span style="margin-right:50px; font-weight:bold;">📈 SENSEX hits record high</span>
            <span style="margin-right:50px; font-weight:bold;">⚠️ New KYC Norms mandatory from April 2026</span>
        </div></div>
        <style>@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }</style>
        """, unsafe_allow_html=True)

    st.sidebar.title("🛡️ Credit Risk AI Analyzer")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Bulk Dashboard", "AI Research Assistant"])

    with tab1:
        st.header("🔍 Credit Risk Underwriting")
        col_inp1, col_inp2 = st.columns(2)
        
        with col_inp1:
            biz_name = st.text_input("Business Name")
            rev = st.number_input("Annual Revenue (₹ Cr)", value=2.0)
            years = st.number_input("Years in Business", value=6)
            industry = st.selectbox("Industry Risk Type", ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"])
        with col_inp2:
            cibil = st.number_input("Credit Score (CIBIL)", min_value=300, max_value=900, value=720)
            dti = st.slider("Debt-to-Income Ratio (%)", 0, 100, 35)
            loan_goal = st.text_input("Loan Purpose", placeholder="e.g. Expansion")

        if st.button("Generate Final Decision Report", use_container_width=True):
            # Scoring Logic based on your document
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else 15)
            s_years = 15 if years > 10 else 12
            s_dti = 25 if dti < 20 else 20
            s_cibil = 25 if cibil >= 750 else 20
            
            ind_map = {"Low Risk": 10, "Medium Risk": 7, "High Risk": 4, "Very High Risk": 2}
            s_ind = ind_map[industry]

            total_score = s_rev + s_years + s_dti + s_cibil + s_ind

            # --- GAUGE CHART (FIXED ARROW) ---
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Credit Health Score", 'font': {'size': 24, 'color': '#003366'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "#003366", 'thickness': 0.3}, # This acts as the needle
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 60], 'color': '#ff4d4d'},
                        {'range': [60, 80], 'color': '#ffd11a'},
                        {'range': [80, 100], 'color': '#2eb82e'}]
                }))
            st.plotly_chart(fig, use_container_width=True)

            st.divider()
            
            # --- RESULTS SECTION (Style from image_2.png) ---
            st.markdown(f"## Analysis for: {biz_name}")
            
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.subheader("📊 Score, Result & Decision")
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
                st.subheader("💡 Suggestions & Recommendations")
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # Prompt using your document information
                    prompt = f"Using the MSME Credit Risk model, analyze a business named {biz_name} that scored {total_score}/100 (which is {risk_lv}). The CIBIL is {cibil}, DTI {dti}%, and Revenue {rev}Cr. Provide 3 specific and formal banking recommendations regarding this loan."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.write("1. Tighten DTI monitoring.\n2. Verify latest GST filings.\n3. Monitor debt-to-equity ratio.")

    with tab2:
        st.header("📊 Portfolio Dashboard")
        uploaded_file = st.file_uploader("Upload Excel/CSV", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.head())
            if "CIBIL" in df.columns:
                fig2 = px.histogram(df, x="CIBIL", title="Portfolio Credit Health")
                st.plotly_chart(fig2)

    with tab3:
        st.header("🤖 AI Research Assistant")
        # --- FIXED AI ASSISTANT FUNCTIONALITY ---
        st.info("Ask about credit policies, NPA management, or risk ratios.")
        user_query_fixed = st.text_input("Ask a question...")
        
        if st.button("Ask AI"):
            # Prevent Argument error by checking if query is empty
            if not user_query_fixed.strip():
                st.warning("Please type a question before asking.")
            else:
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_query_fixed)
                    st.write("### AI Response:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
