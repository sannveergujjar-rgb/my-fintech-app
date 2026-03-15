import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai

# 1. SETUP & STYLING (Same as before)
st.set_page_config(page_title="Credit Risk AI Analyzer", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #ffffff; }
    .main-header { text-align: center; color: #003366; font-size: 48px; font-weight: 800; padding: 20px; }
    .result-box { background: #f8f9fa; padding: 25px; border-radius: 12px; border: 1px solid #dee2e6; color: black; }
    </style>
    """, unsafe_allow_html=True)

# 2. LOGIN LOGIC (Shortened for brevity)
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.image("https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=800", use_container_width=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user == "admin" and pw == "finance123": 
                st.session_state['auth'] = True
                st.rerun()
else:
    st.markdown("<h1 class='main-header'>Credit Risk AI Analyzer</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Individual Analysis", "Portfolio View", "AI Research"])

    # --- TAB 1: INDIVIDUAL (Previously shared) ---
    with tab1:
        st.write("Perform single application analysis here.")

    # --- TAB 2: PORTFOLIO VIEW (FIXED) ---
    with tab2:
        st.subheader("📊 Bulk Portfolio Assessment")
        uploaded_file = st.file_uploader("Upload Applicant Excel File", type=["xlsx", "csv"])

        if uploaded_file:
            # READ DATA
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Loaded {len(df)} records successfully.")
                
                # PREVIEW TABLE
                st.write("### Data Preview")
                st.dataframe(df, use_container_width=True)

                # ANALYSIS LOGIC (Simulating AI Risk Scoring for the Table)
                # We assume the excel has columns: 'Revenue', 'CIBIL', 'DTI'
                if all(col in df.columns for col in ['Revenue', 'CIBIL']):
                    df['Risk Score'] = (df['CIBIL'] / 900 * 50) + (df['Revenue'].clip(0, 10) * 5)
                    df['Risk Category'] = df['Risk Score'].apply(lambda x: 'Low' if x > 75 else ('Medium' if x > 55 else 'High'))
                    
                    # CHARTS & GRAPHS
                    col_left, col_right = st.columns(2)
                    
                    with col_left:
                        st.write("### Risk Distribution")
                        fig_pie = px.pie(df, names='Risk Category', color='Risk Category',
                                        color_discrete_map={'Low':'#2eb82e', 'Medium':'#ffd11a', 'High':'#ff4d4d'})
                        st.plotly_chart(fig_pie, use_container_width=True)

                    with col_right:
                        st.write("### Revenue vs CIBIL Analysis")
                        fig_scatter = px.scatter(df, x="CIBIL", y="Revenue", color="Risk Category",
                                               hover_name=df.columns[0])
                        st.plotly_chart(fig_scatter, use_container_width=True)

                    # FINAL ANALYSIS BOX
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write("### 🤖 Portfolio AI Summary")
                    high_risk_count = len(df[df['Risk Category'] == 'High'])
                    st.write(f"The portfolio contains **{len(df)}** total applications.")
                    st.write(f"⚠️ **Alert:** Found **{high_risk_count}** High-Risk applications requiring immediate manual audit.")
                    st.write("The average CIBIL across the portfolio is **{:.0f}**.".format(df['CIBIL'].mean()))
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Please ensure your Excel has 'CIBIL' and 'Revenue' columns to generate graphs.")

            except Exception as e:
                st.error(f"Error processing file: {e}")

    with tab3:
        st.write("Ask AI any banking questions.")
