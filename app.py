import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="watch42 | Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background-color: white; display: flex; align-items: center;
        padding: 0 20px; border-bottom: 1px solid #eee; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.4rem; color: #1a1a1a; letter-spacing: -0.5px; }
    .logo-accent { color: #d4af37; }
    .block-container { padding-top: 4rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { display: none; }
    .watch-tile {
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        margin-bottom: 10px; min-height: 180px;
    }
    .category-badge { 
        background-color: #f3f4f6; color: #374151; padding: 2px 8px; 
        border-radius: 4px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    }
    .insight-card {
        background-color: #f8f9fa; border-left: 5px solid #d4af37; padding: 15px; border-radius: 5px; margin-bottom: 10px;
    }
    </style>
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. STATIC DATA GENERATION (Enhanced for Trends)
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False, year=None):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        prod_year = year if year else random.randint(2018, 2026) # Extended to 2026
        
        # Trend Logic: Power reserve increases over time
        base_reserve = 40 if prod_year <= 2020 else (70 if prod_year >= 2024 else 55)
        reserve = base_reserve + random.randint(-5, 10)
        
        # Material Trend: Titanium adoption increases
        materials = ["Steel", "Titanium Grade 5", "Ceramic", "Gold"]
        weights = [0.8, 0.05, 0.1, 0.05] if prod_year <= 2021 else [0.6, 0.2, 0.15, 0.05]
        mat = random.choices(materials, weights=weights)[0]

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": random.randint(1500, 5000),
            "Category": cat, "Year": prod_year, "Material": mat, 
            "Diameter": random.choice([39, 40, 41, 42]), "Thickness": random.choice([11, 12, 13]),
            "Reserve": reserve, "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Model {i}", f"REF-{1000+i}") for i in range(1, 1501)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v4.0")

# --- VIEWS 1-3 (Omitted for brevity, functionally identical to v3.2) ---
if view == "My Watches":
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f'<div class="watch-tile"><span class="category-badge">{watch["Category"]}</span><div style="font-weight:600; margin-top:10px;">{watch["Model"]}</div><div style="color:#d4af37; font-weight:500;">€ {watch["Price"]:,}</div><div style="font-size:0.8rem; color:#666;">Year: {watch["Year"]}</div></div>', unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    st.info("Pricing Intelligence active (v3.2 logic)")

elif view == "Design Intelligence":
    st.info("Design Intelligence active (v3.2 logic)")

# 5. NEW VIEW: MARKET INTELLIGENCE (Strategic Control Tower)
elif view == "Market Intelligence":
    st.caption("Strategic monitor for industrial technical evolution and shifting collector preferences.")
    
    df_all = pd.DataFrame(st.session_state.competitors)
    
    # 📉 1. TECH EVOLUTION TRACKER
    st.write("### 📈 Tech Evolution Tracker")
    trend_param = st.selectbox("Monitor Industrial Standard Shift", ["Reserve", "Price", "Thickness"])
    
    # Calculate yearly averages
    yearly_trends = df_all.groupby('Year')[trend_param].mean().reset_index()
    
    fig_trend = px.line(yearly_trends, x='Year', y=trend_param, 
                        title=f"Market Average {trend_param} (2018-2026)",
                        markers=True, template="plotly_white", color_discrete_sequence=["#d4af37"])
    
    fig_trend.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_trend, use_container_width=True)

    # ⚠️ 2. AI STRATEGIC INSIGHTS
    st.write("---")
    st.write("### ⚠️ AI Strategic Insights")
    
    col_ins1, col_ins2 = st.columns(2)
    
    # OBSOLESCENCE ALERT
    with col_ins1:
        st.write("**Obsolescence Alert**")
        target_watch = st.session_state.my_portfolio[0] # Example target
        current_mkt_avg = yearly_trends[yearly_trends['Year'] == 2026][trend_param].values[0]
        
        if target_watch[trend_param] < current_mkt_avg:
            gap = ((current_mkt_avg - target_watch[trend_param]) / current_mkt_avg) * 100
            st.error(f"**Action Required**: Your {target_watch['Model']} caliber ({target_watch[trend_param]}h) is **{gap:.1f}% lower** than the 2026 market standard ({current_mkt_avg:.0f}h).")
        else:
            st.success(f"**Competitive Edge**: Your technical specs are aligned with 2026 standards.")

    # MATERIAL TRENDS
    with col_ins2:
        st.write("**Material Adoption Trends**")
        # Calculate Titanium Grade 5 growth
        mat_21 = len(df_all[(df_all['Year'] <= 2021) & (df_all['Material'] == "Titanium Grade 5")]) / len(df_all[df_all['Year'] <= 2021])
        mat_26 = len(df_all[(df_all['Year'] >= 2024) & (df_all['Material'] == "Titanium Grade 5")]) / len(df_all[df_all['Year'] >= 2024])
        growth = (mat_26 - mat_21) * 100
        
        st.markdown(f"""
            <div class="insight-card">
                <b>Material Shift</b>: Detected a <b>+{growth:.1f}% increase</b> in <b>Titanium Grade 5</b> usage among competitors.<br>
                <i>Strategy: Consider a case material upgrade for upcoming 2027 collection.</i>
            </div>
        """, unsafe_allow_html=True)

    # 🎯 3. RISK MITIGATION OBJECTIVES
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**R&D Timing**: Optimize investment cycles for new calibers to maintain technological appeal.")
    with c2:
        st.info("**Price Sustainability**: Technical proof to justify premium pricing based on industrial luxury standards.")
    with c3:
        st.info("**Competitive Advantage**: Anticipate common features (e.g., antimagnetism) before they saturate the segment.")
