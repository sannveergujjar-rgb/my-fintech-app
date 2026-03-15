import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. UI STYLING
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .main-header { text-align: center; color: #003366; font-size: 50px; font-weight: 800; padding: 20px 0; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #003366; padding: 12px 0; border-radius: 8px; margin: 20px 0; }
    .ticker { display: inline-block; white-space: nowrap; animation: ticker-move 45s linear infinite; color: #ffffff; font-size: 19px; }
    @keyframes ticker-move { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .result-box { background-color: #f8f9fa; padding: 25px; border-radius: 12px; border: 1px solid #dee2e6; min-height: 400px; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 3. API CONFIG
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- LOGIN SCREEN ---
if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1556742044-3c52d6e88c62?w=800", use_container_width=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login to Dashboard", use_container_width=True):
            if u == "admin" and p == "finance123":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Invalid Credentials")
else:
    # --- DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    st.markdown('<div class="ticker-wrap"><div class="ticker">🚀 Repo Rate: 6.5% | 📢 RBI Alert: New MSME Norms | 💹 Projected GDP Growth: 7.2% | 📉 Market Watch: SENSEX Hits New High</div></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio View", "AI Assistant"])

    with tab1:
        st.subheader("📋 New Loan Assessment")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Business Name", "Sharma Enterprises")
            rev = st.number_input("Annual Revenue (₹ Cr)", 2.5)
            years = st.number_input("Years in Business", 5)
        with c2:
            cibil = st.number_input("CIBIL Score", 720)
            dti = st.slider("DTI Ratio (%)", 0, 100, 35)
            purpose = st.text_input("Loan Purpose", "Expansion")

        if st.button("Generate Detailed Report", use_container_width=True):
            # DYNAMIC SCORING
            s_rev = 25 if rev > 5 else (20 if rev >= 1 else 15)
            s_years = 15 if years >= 5 else 10
            s_cibil = 30 if cibil >= 750 else (20 if cibil >= 700 else 10)
            s_dti = 30 if dti < 30 else (20 if dti < 50 else 10)
            score = s_rev + s_years + s_cibil + s_dti

            # DYNAMIC STATUS LOGIC
            if score >= 85: status, color = "APPROVED", "#2eb82e"
            elif score >= 65: status, color = "#ffd11a", "#ffd11a" # Referred color
            else: status, color = "REJECTED", "#ff4d4d"

            fig = go.Figure(go.Indicator(mode="gauge+number", value=score, 
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "black", 'thickness': 0.25},
                'steps': [{'range': [0, 60], 'color': "#ff4d4d"}, {'range': [60, 85], 'color': "#ffd11a"}, {'range': [85, 100], 'color': "#2eb82e"}]}))
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

            

            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f"""<div class="result-box">
                    <h4>📊 Quantitative Analysis</h4>
                    <b>Credit Score:</b> {score}/100<br>
                    <b>Decision:</b> <span style="color:{color}; font-weight:bold;">{status if status != '#ffd11a' else 'REFERRED'}</span>
                    <hr>
                    <li>Revenue Pillar: {s_rev}/25</li>
                    <li>Experience Pillar: {s_years}/15</li>
                    <li>Credit History: {s_cibil}/30</li>
                    <li>Debt Burden: {s_dti}/30</li>
                </div>""", unsafe_allow_html=True)
            with res2:
                st.markdown('<div class="result-box"><h4>🤖 AI Qualitative Insights</h4>', unsafe_allow_html=True)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = f"Analyze business {name} with a credit score of {score}/100 and CIBIL of {cibil}. Provide 3 short, professional banking suggestions."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except: st.write("• Verify GST filings.<br>• Monitor cash flow.<br>• Collateral may be required.")
                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("📊 Portfolio Analysis")
        up_file = st.file_uploader("Upload Applicant Excel", type=["xlsx", "csv"])
        if up_file:
            df = pd.read_csv(up_file) if up_file.name.endswith('.csv') else pd.read_excel(up_file)
            st.dataframe(df, use_container_width=True)
            
            cols = {c.lower(): c for c in df.columns}
            c_col = next((v for k, v in cols.items() if 'cibil' in k or 'score' in k), None)
            if c_col:
                df['Status'] = df[c_col].apply(lambda x: 'Low Risk' if x > 750 else ('Medium Risk' if x > 650 else 'High Risk'))
                fig_pie = px.pie(df, names='Status', color='Status', color_discrete_map={'Low Risk':'#2eb82e','Medium Risk':'#ffd11a','High Risk':'#ff4d4d'})
                st.plotly_chart(fig_pie, use_container_width=True)

    with tab3:
        st.subheader("🤖 AI Assistant")
        q = st.text_input("Enter Question:")
        if st.button("Query AI"):
            m = genai.GenerativeModel('gemini-1.5-flash')
            st.write(m.generate_content(q).text)
