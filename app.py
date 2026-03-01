import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE (Header Fisso e Layout Professionale)
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

# 3. GENERAZIONE DATI (Database Unificato per tutte le sezioni)
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    def create_mock_watch(brand, model, ref, is_target=False, year=None):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        prod_year = year if year else random.randint(2018, 2026)
        
        # Trend Logic: Power reserve increases over time
        base_reserve = 42 if prod_year <= 2020 else (72 if prod_year >= 2024 else 60)
        reserve = int(base_reserve + random.randint(-5, 8))
        
        # Dimension Logic for Design Matrix
        if cat == "Diver": diam, thick = random.choice([41, 42, 43]), random.choice([13, 14, 15])
        elif cat == "Dress": diam, thick = random.choice([36, 38, 39]), random.choice([8, 9, 10])
        else: diam, thick = random.choice([39, 40, 41]), random.choice([11, 12, 13])

        materials = ["Steel", "Titanium Grade 5", "Ceramic", "Gold"]
        mat = random.choices(materials, weights=[0.6, 0.2, 0.15, 0.05])[0]

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": int(random.randint(1500, 5000)),
            "Category": cat, "Year": int(prod_year), "Material": mat, 
            "Diameter": diam, "Thickness": thick, "Reserve": reserve, 
            "WR": random.choice([50, 100, 200, 300]), "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Comp {i}", f"REF-{1000+i}") for i in range(1, 1801)]
    st.session_state.initialized = True

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v4.5")

# --- 5. VIEW: MY WATCHES ---
if view == "My Watches":
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="watch-tile">
                    <span class="category-badge">{watch['Category']}</span>
                    <div style="font-weight:600; margin-top:10px;">{watch['Model']}</div>
                    <div style="color:#d4af37; font-weight:500;">€ {watch['Price']:,}</div>
                    <div style="font-size:0.8rem; color:#666;">Year: {watch['Year']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. VIEW: PRICING INTELLIGENCE ---
elif view == "Pricing Intelligence":
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Diameter": "mm"}
    col_f1, col_f2, col_f3 = st.columns([1.2, 1, 1.3])
    with col_f1:
        target = st.selectbox("Select Target", st.session_state.my_portfolio, format_func=lambda x: f"{x['Model']} ({x['Year']})")
    with col_f2:
        y_param = st.selectbox("Parameter", list(units.keys()))
    with col_f3:
        year_range = st.slider("Year Range", 2015, 2026, (target['Year'] - 1, target['Year'] + 1))

    df_market = pd.DataFrame(st.session_state.competitors)
    df_f = df_market[(df_market['Category'] == target['Category']) & 
                     (df_market[y_param] == target[y_param]) &
                     (df_market['Year'].between(year_range[0], year_range[1]))].copy()

    if not df_f.empty:
        avg_p = df_f['Price'].mean()
        diff = ((target['Price'] - avg_p) / avg_p) * 100
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Category", target['Category'])
        k2.metric("Target Year", target['Year'])
        k3.metric("Competitors", len(df_f))
        k4.metric("Avg Market", f"€ {avg_p:,.0f}")
        k5.metric("Your Price", f"€ {target['Price']:,}", f"{diff:+.1f}% vs avg", delta_color="inverse")
        
        st.write("---")
        fig = px.scatter(pd.concat([df_f, pd.DataFrame([target])]), x="Price", y=y_param, color="Type",
                         color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
                         size_max=20, template="plotly_white", height=450)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No matches found for this filter combination.")

# --- 7. VIEW: DESIGN INTELLIGENCE ---
elif view == "Design Intelligence":
    col_h1, col_h2 = st.columns([1.3, 2])
    with col_h1:
        design_year_range = st.slider("Production Year Filter", 2015, 2026, (2018, 2024))
    with col_h2:
        selected_cat = st.selectbox("Market Segment Filter", ["All Categories", "Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"])

    df_all = pd.DataFrame(st.session_state.competitors)
    df_f_design = df_all[df_all['Year'].between(design_year_range[0], design_year_range[1])].copy()
    if selected_cat != "All Categories":
        df_f_design = df_f_design[df_f_design['Category'] == selected_cat]

    if not df_f_design.empty:
        matrix_df = df_f_design.groupby(['Diameter', 'Thickness']).size().reset_index(name='count')
        pivot_table = matrix_df.pivot(index='Thickness', columns='Diameter', values='count').fillna(0)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index,
            colorscale=[[0, '#27ae60'], [0.1, '#f1c40f'], [0.5, '#e67e22'], [1.0, '#c0392b']],
            text=pivot_table.values, texttemplate="%{text}", textfont={"size": 14, "color": "white"}
        ))
        fig.update_layout(xaxis_title="Diameter (mm)", yaxis_title="Thickness (mm)", template="plotly_white", height=500, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")
        st.write("### 🔍 Cell Inspector")
        c1, c2 = st.columns(2)
        with c1: sel_diam = st.selectbox("Select Diameter", sorted(df_f_design['Diameter'].unique()))
        with c2: sel_thick = st.selectbox("Select Thickness", sorted(df_f_design['Thickness'].unique()))
        
        cell_list = df_f_design[(df_f_design['Diameter'] == sel_diam) & (df_f_design['Thickness'] == sel_thick)]
        with st.expander(f"Analysis: {len(cell_list)} models found", expanded=True):
            st.dataframe(cell_list[["Brand", "Model", "Year", "Price", "Category"]], use_container_width=True, hide_index=True)

# --- 8. VIEW: MARKET INTELLIGENCE ---
elif view == "Market Intelligence":
    df_all = pd.DataFrame(st.session_state.competitors)
    
    col_f1, _ = st.columns([1, 2])
    with col_f1:
        selected_market_cat = st.selectbox("Market Segment Filter", ["All Categories", "Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"], key="mkt_cat")
    
    df_market_filtered = df_all.copy()
    if selected_market_cat != "All Categories":
        df_market_filtered = df_market_filtered[df_market_filtered['Category'] == selected_market_cat]
    
    yearly_trends = df_market_filtered.groupby('Year')['Reserve'].mean().reset_index()
    
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
        target_watch = next((w for w in st.session_state.my_portfolio if w['Category'] == selected_market_cat), st.session_state.my_portfolio[0])
        max_year = yearly_trends['Year'].max() if not yearly_trends.empty else 2026
        current_mkt_avg = yearly_trends[yearly_trends['Year'] == max_year]['Reserve'].values[0] if not yearly_trends.empty else 72
        
        if target_watch['Reserve'] < current_mkt_avg:
            gap = ((current_mkt_avg - target_watch['Reserve']) / current_mkt_avg) * 100
            st.error(f"**Obsolescence Alert**: {target_watch['Model']} ({target_watch['Reserve']}h) is **{gap:.1f}% lower** than the {selected_market_cat} {max_year} standard ({current_mkt_avg:.0f}h).")
        else:
            st.success(f"**Competitive Edge**: {target_watch['Model']} specs are above the {selected_market_cat} average.")

        mat_ratio = len(df_market_filtered[(df_market_filtered['Year'] >= 2024) & (df_market_filtered['Material'] == "Titanium Grade 5")]) / len(df_market_filtered[df_market_filtered['Year'] >= 2024]) if len(df_market_filtered[df_market_filtered['Year'] >= 2024]) > 0 else 0
        st.markdown(f'<div class="insight-card"><b>Material Trend ({selected_market_cat})</b>: <b>Titanium Grade 5</b> adoption is at <b>{mat_ratio*100:.1f}%</b>.<br><i>Strategy: High urgency for case material diversification.</i></div>', unsafe_allow_html=True)
        st.info(f"**R&D Goal**: Align upcoming {selected_market_cat} models to the {current_mkt_avg:.0f}h reserve threshold.")
