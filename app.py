import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SETUP & STYLE
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .main-header { text-align: center; color: #003366; font-size: 48px; font-weight: 800; padding: 20px; border-bottom: 2px solid #eee; }
    .result-box { background: #f8f9fa; padding: 25px; border-radius: 12px; border: 1px solid #dee2e6; color: black; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. API & AUTH
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

if 'auth' not in st.session_state: st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800", use_container_width=True)
        u, p = st.text_input("User"), st.text_input("Pass", type="password")
        if st.button("Login", use_container_width=True):
            if u == "admin" and p == "finance123":
                st.session_state['auth'] = True
                st.rerun()
else:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio View", "AI Research Assistant"])

    # --- TAB 1: INDIVIDUAL ANALYSIS (UNTOUCHED) ---
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
            s_rev = 30 if rev > 5 else 20
            s_years = 20 if years > 5 else 15
            s_cibil = 30 if cibil > 750 else 20
            s_dti = 20 if dti < 40 else 10
            score = s_rev + s_years + s_cibil + s_dti

            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "black", 'thickness': 0.25},
                    'steps': [{'range': [0, 60], 'color': "red"}, {'range': [60, 80], 'color': "orange"}, {'range': [80, 100], 'color': "green"}]
                }))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f'<div class="result-box"><h4>📊 Result</h4>Score: {score}/100<br>Decision: {"APPROVED" if score >= 80 else "REFERRED"}</div>', unsafe_allow_html=True)
            with res2:
                st.markdown('<div class="result-box"><h4>🤖 AI Insights</h4>Verify GST and bank statements.</div>', unsafe_allow_html=True)

    # --- TAB 2: PORTFOLIO VIEW (REWRITTEN & IMPROVISED) ---
    with tab2:
        st.subheader("📈 Bulk Portfolio Credit Risk Analysis")
        up_file = st.file_uploader("Upload Excel File", type=["xlsx", "csv"])

        if up_file:
            try:
                # Load data
                df = pd.read_csv(up_file) if up_file.name.endswith('.csv') else pd.read_excel(up_file)
                
                # Show Table
                st.write("### 📂 Uploaded Applicant Data")
                st.dataframe(df, use_container_width=True)

                # Find key columns automatically (Case-insensitive search)
                cols = {c.lower(): c for c in df.columns}
                cibil_col = next((v for k, v in cols.items() if 'cibil' in k or 'score' in k), None)
                rev_col = next((v for k, v in cols.items() if 'rev' in k or 'turnover' in k), None)

                if cibil_col and rev_col:
                    # Calculate Risk for each row
                    df['Calculated Score'] = (df[cibil_col] / 900 * 60) + (df[rev_col].clip(0,10) * 4)
                    df['Risk Status'] = df['Calculated Score'].apply(lambda x: 'Low' if x > 70 else ('Medium' if x > 50 else 'High'))

                    # CHARTS SECTION
                    st.write("### 📊 Risk Intelligence Dashboard")
                    g1, g2 = st.columns(2)
                    
                    with g1:
                        fig_pie = px.pie(df, names='Risk Status', title="Overall Portfolio Risk Mix",
                                        color='Risk Status', color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with g2:
                        fig_bar = px.bar(df, x=df.columns[0], y='Calculated Score', color='Risk Status',
                                        title="Applicant Wise Credit Scores")
                        st.plotly_chart(fig_bar, use_container_width=True)

                    # ANALYSIS SUMMARY BOX
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write("### 🤖 AI Portfolio Analysis")
                    st.write(f"• **Total Applicants Analyzed:** {len(df)}")
                    st.write(f"• **Average Credit Score:** {df['Calculated Score'].mean():.1f}/100")
                    st.write(f"• **High Risk Alerts:** {len(df[df['Risk Status']=='High'])} files require immediate rejection or higher collateral.")
                    st.write("• **Observation:** The portfolio shows a concentration in " + df['Risk Status'].mode()[0] + " risk assets.")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("❌ Column Missing: Please ensure your file has 'CIBIL' and 'Revenue' columns.")
            
            except Exception as e:
                st.error(f"Error: {e}")

    # --- TAB 3: AI RESEARCH ---
    with tab3:
        st.subheader("🤖 AI Research Assistant")
        q = st.text_input("Ask any financial question...")
        if st.button("Analyze"):
            if q:
                try:
                    m = genai.GenerativeModel('gemini-1.5-flash')
                    st.write(m.generate_content(q).text)
                except: st.error("API Error")
