import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import time
from agents.sales_agent import get_rfp_list
from agents.master_agent import run_rfp_pipeline

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="🚀 Agentic RFP Automation",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------
# Load Logo and Apply Branding
# ----------------------------
try:
    logo = Image.open("logo.png")  # Place your logo file in the app folder
except:
    logo = None

st.markdown("<style>body{background-color: #f9f9f9;}</style>", unsafe_allow_html=True)
st.markdown("---")

col_logo, col_title = st.columns([1, 8])
with col_logo:
    if logo:
        st.image(logo, width=120)
with col_title:
    st.markdown("<h1 style='color:#2C3E50;'>Agentic RFP Automation 🤖</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#4CAF50;'>Master Agent orchestrates Sales → Technical → Pricing → Report</h4>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# Sidebar - Controls & Future Scope
# ----------------------------
with st.sidebar:
    st.header("⚙ Controls")
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    filter_score = st.slider("Minimum Spec Match % Filter", 0, 100, 50)

    st.header("💡 Future Scope")
    st.info("""
    - AI-driven dynamic pricing optimization 💰  
    - Live market data integration 📈  
    - Real-time collaboration tools 🛠  
    - Multi-RFP upload & batch processing 📂  
    - Dashboard analytics with filters 📊  
    """)

if dark_mode:
    st.markdown("<style>body{background-color: #222; color: #fff;}</style>", unsafe_allow_html=True)

# ----------------------------
# Load RFPs
# ----------------------------
rfps = get_rfp_list()
rfp_map = {r["id"]: r for r in rfps}

selected = st.selectbox(
    "📄 Choose an RFP", 
    options=list(rfp_map.keys()), 
    format_func=lambda x: f"{x} — {rfp_map[x]['title']}"
)

# ----------------------------
# Run Pipeline with Progress Bar
# ----------------------------
if st.button("Run Pipeline 🚀", type="primary"):
    with st.spinner("Running agents... 🤖"):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.005)  # Adjust for animation smoothness
            progress.progress(i + 1)
        result = run_rfp_pipeline(selected, top_n=5)

    rfp = result["rfp"]
    recs = result["recommendations"]
    pdf_bytes = result["pdf"]

    # ----------------------------
    # Dashboard Tabs
    # ----------------------------
    tabs = st.tabs(["📝 RFP Summary", "📊 Recommendations", "📈 Charts", "📥 Download", "💬 Feedback"])

    # --- Tab 1: RFP Summary ---
    with tabs[0]:
        st.subheader("📝 RFP Summary")
        st.metric(label="RFP ID", value=rfp.get("id"))
        st.metric(label="RFP Title", value=rfp.get("title"))
        st.write("**Specifications:**")
        st.json(rfp.get("specs", {}))
        st.write("**Tests Required:**", rfp.get("tests_required", []))
        st.write("**Quantity:**", rfp.get("quantity"))

    # --- Tab 2: Recommendations Table ---
    with tabs[1]:
        st.subheader("📊 Recommendations Table")
        rows = []
        for idx, r in enumerate(recs, 1):
            pricing = r.get("pricing", {})
            rows.append({
                "Rank": idx,
                "SKU": r.get("sku"),
                "Product": r.get("name"),
                "Spec Match %": r.get("score"),
                "Unit Price": pricing.get("unit_price"),
                "Test Cost": pricing.get("test_cost"),
                "Total Estimated Cost": pricing.get("total_cost")
            })
        df = pd.DataFrame(rows)

        # Filter by score
        df = df[df["Spec Match %"] >= filter_score]

        st.table(df)

        # KPI Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("🏆 Best Match", df.iloc[0]["Product"], f"{df.iloc[0]['Spec Match %']}%")
        col2.metric("💰 Lowest Price", df["Unit Price"].min(), f"${df['Unit Price'].min()}")
        col3.metric("📉 Lowest Total Cost", df["Total Estimated Cost"].min(), f"${df['Total Estimated Cost'].min()}")

    # --- Tab 3: Charts ---
    with tabs[2]:
        st.subheader("📈 Spec Match Interactive Chart")
        fig = px.bar(
            df,
            x="Product",
            y="Spec Match %",
            color="Spec Match %",
            text="Spec Match %",
            title="Top Product Matches"
        )
        fig.update_layout(xaxis_title="Product", yaxis_title="Spec Match %")
        st.plotly_chart(fig, use_container_width=True)

    # --- Tab 4: Download Report ---
    with tabs[3]:
        st.subheader("📥 Download Report")
        st.download_button(
            label="Download PDF Report 📥",
            data=pdf_bytes,
            file_name=f"{rfp.get('id')}_response.pdf",
            mime="application/pdf"
        )

    # --- Tab 5: Feedback ---
    with tabs[4]:
        st.subheader("💬 Feedback")
        feedback = st.text_area("Enter your feedback:", placeholder="Your thoughts here...")
        if st.button("Submit Feedback 📨"):
            st.success("Thanks for your feedback!")

    st.balloons()  # 🎉 Celebrate success
    st.success("✅ RFP Pipeline Completed Successfully!")
