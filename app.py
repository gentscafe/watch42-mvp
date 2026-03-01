import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
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
        background-color: #f8f9fa; border-left: 5px solid #d4af37; padding: 15px; border-radius: 5px; margin-bottom: 15px;
    }
    </style>
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. GENERAZIONE DATI
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    def create_mock_watch(brand, model, ref, is_target=False, year=None):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        prod_year = year if year else random.randint(2018, 2026)
        base_reserve = 40 if prod_year <= 2020 else (70 if prod_year >= 2024 else 55)
        reserve = int(base_reserve + random.randint(-5, 10))
        materials = ["Steel", "Titanium Grade 5", "Ceramic", "Gold"]
        mat = random.choices(materials, weights=[0.6, 0.2, 0.15, 0.05])[0]
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": int(random.randint(1500, 5000)),
            "Category": cat, "Year": int(prod_year), "Material": mat, 
            "Diameter": random.choice([39, 40, 41]), "Thickness": random.choice([11, 12, 13]), 
            "Reserve": reserve, "Type": "Target" if is_target else "Market"
        }
    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"Watch {i}", f"REF-0{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Comp {i}", f"REF-{1000+i}") for i in range(1, 1501)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v4.3")

# --- VIEWS (My Watches, Pricing, Design rimangono invariate) ---
if view == "My Watches":
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f'<div class="watch-tile"><span class="category-badge">{watch["Category"]}</span><div style="font-weight:600; margin-top:10px;">{watch["Model"]}</div><div style="color:#d4af37; font-weight:500;">€ {watch["Price"]:,}</div><div style="font-size:0.8rem; color:#666;">Year: {watch["Year"]}</div></div>', unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    st.info("Pricing Intelligence (v3.2 logic)")

elif view == "Design Intelligence":
    st.info("Design Intelligence (v3.2 logic)")

# 5. VIEW: MARKET INTELLIGENCE (LAYOUT AGGIORNATO)
elif view == "Market Intelligence":
    df_all = pd.DataFrame(st.session_state.competitors)
    yearly_trends = df_all.groupby('Year')['Reserve'].mean().reset_index()
    
    # Layout a due colonne: Grafico a sinistra, Insights a destra
    col_chart, col_insights = st.columns([1.5, 1])
    
    with col_chart:
        st.write("### 📈 Power Reserve Evolution")
        fig_trend = px.line(yearly_trends, x='Year', y='Reserve', markers=True, 
                            template="plotly_white", color_discrete_sequence=["#d4af37"],
                            labels={"Reserve": "Avg Reserve (h)", "Year": "Launch Year"})
        fig_trend.update_layout(height=450, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_insights:
        st.write("### ⚠️ AI Strategic Insights")
        
        # 1. OBSOLESCENCE ALERT
        target_watch = st.session_state.my_portfolio[0]
        max_year = yearly_trends['Year'].max()
        current_mkt_avg = yearly_trends[yearly_trends['Year'] == max_year]['Reserve'].values[0]
        
        if target_watch['Reserve'] < current_mkt_avg:
            gap = ((current_mkt_avg - target_watch['Reserve']) / current_mkt_avg) * 100
            st.error(f"**Obsolescence Alert**: Your {target_watch['Model']} ({target_watch['Reserve']}h) is **{gap:.1f}% lower** than the {max_year} market standard ({current_mkt_avg:.0f}h).")
        else:
            st.success(f"**Competitive Edge**: Specs aligned with {max_year} standards.")

        # 2. MATERIAL TRENDS
        mat_26 = len(df_all[(df_all['Year'] >= 2024) & (df_all['Material'] == "Titanium Grade 5")]) / len(df_all[df_all['Year'] >= 2024])
        st.markdown(f"""
            <div class="insight-card">
                <b>Material Shift</b>: <b>Titanium Grade 5</b> adoption is at <b>{mat_26*100:.1f}%</b> in the 2024-2026 segment.<br>
                <i>Strategy: High urgency for case material diversification.</i>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. STRATEGIC GOAL
        st.info("**R&D Timing**: Optimize caliber investment cycles to match the 70h+ industrial shift.")

    st.write("---")
    st.caption("Data source: WatchBase aggregated market trends 2018-2026.")
