import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")

# 2. ADVANCED UI STYLING
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    
    .main-header {
        text-align: center;
        color: #003366;
        font-size: 50px;
        font-weight: 800;
        padding: 20px 0;
        border-bottom: 2px solid #f0f2f6;
    }

    /* LIVE NEWS TICKER */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: #003366;
        padding: 12px 0;
        border-radius: 8px;
        margin: 20px 0;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker-move 45s linear infinite;
        color: #ffffff;
        font-size: 19px;
    }
    @keyframes ticker-move {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .result-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dee2e6;
        min-height: 350px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API & AUTH
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- LOGIN ---
if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800", use_container_width=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access Dashboard", use_container_width=True):
            if u == "admin" and p == "finance123":
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Access Denied")
else:
    # --- DASHBOARD ---
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    
    # LIVE NEWS TICKER
    st.markdown("""
        <div class="ticker-wrap">
            <div class="ticker">
                🚀 <b>MARKET WATCH:</b> SENSEX hits record high &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                📢 <b>RBI UPDATE:</b> Repo rate remains steady at 6.5% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                📉 <b>MSME NEWS:</b> New ₹50,000 Cr credit scheme launched &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                ⚠️ <b>COMPLIANCE:</b> New KYC norms mandatory from April 2026 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                💹 <b>ECONOMY:</b> India GDP growth projected at 7.2%
            </div>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio View", "AI Assistant"])

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
            purpose = st.text_input("Loan Purpose", "Expansion")

        if st.button("Generate Comprehensive Report", use_container_width=True):
            score = (cibil/900*60) + (rev*4) + 10 
            fig = go.Figure(go.Indicator(mode="gauge+number", value=score, 
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "black", 'thickness': 0.25},
                'steps': [{'range': [0, 60], 'color': "#ff4d4d"}, {'range': [60, 80], 'color': "#ffd11a"}, {'range': [80, 100], 'color': "#2eb82e"}]}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            res1, res2 = st.columns(2)
            with res1:
                st.markdown(f'<div class="result-box"><h4>📊 Scoring Breakdown</h4><b>Score:</b> {score:.1f}/100<br><b>Status:</b> REFERRED<br><br>Detailed breakdown of financial health based on provided revenue and credit history.</div>', unsafe_allow_html=True)
            with res2:
                st.markdown('<div class="result-box"><h4>🤖 AI Insights</h4>Generating strategic advice...</div>', unsafe_allow_html=True)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Analyze business {name} with score {score} and CIBIL {cibil}. Provide 3 short recommendations.")
                    st.write(response.text)
                except: st.write("Verify GST filings and monitor cash flow.")

    with tab2:
        st.subheader("📊 Portfolio Bulk Analysis")
        up_file = st.file_uploader("Upload Applicant Excel/CSV", type=["xlsx", "csv"])
        
        if up_file:
            df = pd.read_csv(up_file) if up_file.name.endswith('.csv') else pd.read_excel(up_file)
            st.write("### Data Preview")
            st.dataframe(df, use_container_width=True)
            
            # Smart Column Mapping
            cols = {c.lower(): c for c in df.columns}
            cibil_col = next((v for k, v in cols.items() if 'cibil' in k or 'score' in k), None)
            
            if cibil_col:
                st.write("### Portfolio Risk Dashboard")
                df['Status'] = df[cibil_col].apply(lambda x: 'Low Risk' if x > 750 else ('Medium Risk' if x > 650 else 'High Risk'))
                
                pc1, pc2 = st.columns(2)
                with pc1:
                    fig_pie = px.pie(df, names='Status', color='Status', color_discrete_map={'Low Risk':'#2eb82e','Medium Risk':'#ffd11a','High Risk':'#ff4d4d'})
                    st.plotly_chart(fig_pie, use_container_width=True)
                with pc2:
                    fig_bar = px.histogram(df, x='Status', color='Status', color_discrete_map={'Low Risk':'#2eb82e','Medium Risk':'#ffd11a','High Risk':'#ff4d4d'})
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.markdown('<div class="result-box"><h4>🤖 AI Portfolio Summary</h4>Portfolio shows balanced risk. Re-evaluate high-risk segment.</div>', unsafe_allow_html=True)
            else:
                st.error("Excel must have a 'CIBIL' or 'Score' column.")

    with tab3:
        st.subheader("🤖 AI Financial Assistant")
        q = st.text_input("Ask a question:")
        if st.button("Query AI"):
            m = genai.GenerativeModel('gemini-1.5-flash')
            st.write(m.generate_content(q).text)
