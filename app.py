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
        # Trend: Reserve standard moves from ~42h (2018) to ~72h (2026)
        base_reserve = 42 if prod_year <= 2020 else (72 if prod_year >= 2024 else 60)
        reserve = int(base_reserve + random.randint(-5, 8))
        materials = ["Steel", "Titanium Grade 5", "Ceramic", "Gold"]
        mat = random.choices(materials, weights=[0.6, 0.2, 0.15, 0.05])[0]
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": int(random.randint(1500, 5000)),
            "Category": cat, "Year": int(prod_year), "Material": mat, 
            "Diameter": random.choice([39, 40, 41]), "Thickness": random.choice([11, 12, 13]), 
            "Reserve": reserve, "Type": "Target" if is_target else "Market"
        }
    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"Watch {i}", f"REF-0{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Comp {i}", f"REF-{1000+i}") for i in range(1, 2001)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v4.4")

# --- VIEWS (My Watches, Pricing, Design rimangono invariate) ---
if view == "My Watches":
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f'<div class="watch-tile"><span class="category-badge">{watch["Category"]}</span><div style="font-weight:600; margin-top:10px;">{watch["Model"]}</div><div style="color:#d4af37; font-weight:500;">€ {watch["Price"]:,}</div><div style="font-size:0.8rem; color:#666;">Year: {watch["Year"]}</div></div>', unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    st.info("Pricing Intelligence (v3.2 logic active)")

elif view == "Design Intelligence":
    st.info("Design Intelligence (v3.2 logic active)")

# 5. VIEW: MARKET INTELLIGENCE (WITH CATEGORY FILTER)
elif view == "Market Intelligence":
    df_all = pd.DataFrame(st.session_state.competitors)
    
    # Filtro Categoria per Analisi di Mercato
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        selected_market_cat = st.selectbox("Market Segment Filter", ["All Categories", "Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"])
    
    # Applichiamo il filtro ai dati
    df_market_filtered = df_all.copy()
    if selected_market_cat != "All Categories":
        df_market_filtered = df_market_filtered[df_market_filtered['Category'] == selected_market_cat]
    
    yearly_trends = df_market_filtered.groupby('Year')['Reserve'].mean().reset_index()
    
    # Layout a due colonne
    col_chart, col_insights = st.columns([1.5, 1])
    
    with col_chart:
        st.write(f"### 📈 {selected_market_cat} Evolution")
        fig_trend = px.line(yearly_trends, x='Year', y='Reserve', markers=True, 
                            template="plotly_white", color_discrete_sequence=["#d4af37"],
                            labels={"Reserve": "Avg Power Reserve (h)", "Year": "Launch Year"})
        fig_trend.update_layout(height=450, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_insights:
        st.write("### ⚠️ AI Strategic Insights")
        
        # 1. OBSOLESCENCE ALERT DINAMICO
        # Troviamo il primo orologio del portfolio che corrisponde alla categoria (o il primo in assoluto)
        target_watch = next((w for w in st.session_state.my_portfolio if w['Category'] == selected_market_cat), st.session_state.my_portfolio[0])
        
        max_year = yearly_trends['Year'].max() if not yearly_trends.empty else 2026
        current_mkt_avg = yearly_trends[yearly_trends['Year'] == max_year]['Reserve'].values[0] if not yearly_trends.empty else 72
        
        if target_watch['Reserve'] < current_mkt_avg:
            gap = ((current_mkt_avg - target_watch['Reserve']) / current_mkt_avg) * 100
            st.error(f"**Obsolescence Alert**: {target_watch['Model']} ({target_watch['Reserve']}h) is **{gap:.1f}% lower** than the {selected_market_cat} {max_year} standard ({current_mkt_avg:.0f}h).")
        else:
            st.success(f"**Competitive Edge**: {target_watch['Model']} specs are above the {selected_market_cat} average.")

        # 2. MATERIAL TRENDS
        mat_ratio = len(df_market_filtered[(df_market_filtered['Year'] >= 2024) & (df_market_filtered['Material'] == "Titanium Grade 5")]) / len(df_market_filtered[df_market_filtered['Year'] >= 2024]) if len(df_market_filtered[df_market_filtered['Year'] >= 2024]) > 0 else 0
        st.markdown(f"""
            <div class="insight-card">
                <b>Material Trend ({selected_market_cat})</b>: <b>Titanium Grade 5</b> is present in <b>{mat_ratio*100:.1f}%</b> of recent launches.<br>
                <i>Strategy: High urgency for case material diversification in this segment.</i>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. R&D OBJECTIVE
        st.info(f"**R&D Goal**: Align upcoming {selected_market_cat} models to the {current_mkt_avg:.0f}h reserve threshold.")

    st.write("---")
    st.caption(f"Data source: watch42 aggregated {selected_market_cat} trends 2018-2026.")
