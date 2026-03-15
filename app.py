import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="MSME Credit Risk AI", layout="centered")

st.title("🛡️ AI Credit Risk Analyzer")
st.subheader("MBA Finance Project: MSME Lending Model")

# Sidebar for Inputs
st.sidebar.header("Business Details")
biz_name = st.sidebar.text_input("Business Name", "Example Traders")
revenue = st.sidebar.number_input("Annual Revenue (₹ Lakhs)", min_value=1, value=50)
years = st.sidebar.slider("Years in Business", 0, 30, 5)
cibil = st.sidebar.slider("CIBIL Score", 300, 900, 750)
existing_debt = st.sidebar.number_input("Existing Debt (₹ Lakhs)", min_value=0, value=10)

# The "AI" Scoring Logic (Weighted Model)
# CIBIL: 40%, Revenue-to-Debt: 30%, Experience: 30%
if st.sidebar.button("Analyze Risk"):
    # Normalized Scores
    cibil_score = (cibil - 300) / 600 * 40
    exp_score = min((years / 10) * 30, 30)
    debt_ratio = (1 - (existing_debt / revenue)) * 30 if revenue > existing_debt else 0
    
    total_score = cibil_score + exp_score + debt_ratio
    
    # Display Results
    st.write(f"### Analysis for: {biz_name}")
    
    if total_score > 75:
        st.success(f"**Score: {total_score:.2f}/100 - LOW RISK**")
        st.write("✅ **Recommendation:** Approve Loan at Prime Interest Rate (8-10%).")
    elif total_score > 50:
        st.warning(f"**Score: {total_score:.2f}/100 - MEDIUM RISK**")
        st.write("⚠️ **Recommendation:** Refer to Credit Officer. Suggest 12% Interest + Collateral.")
    else:
        st.error(f"**Score: {total_score:.2f}/100 - HIGH RISK**")
        st.write("❌ **Recommendation:** Reject Application. High probability of default.")

    # Data Table for Report
    df = pd.DataFrame({
        "Metric": ["CIBIL Contribution", "Experience Score", "Debt-to-Income Score", "Final Total"],
        "Value": [f"{cibil_score:.2f}", f"{exp_score:.2f}", f"{debt_ratio:.2f}", f"{total_score:.2f}"]
    })
    st.table(df)
else:
    st.info("Enter business details in the sidebar and click 'Analyze Risk' to start.")
