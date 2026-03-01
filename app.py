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
        background-color: #f8f9fa; border-left: 5px solid #d4af37; padding: 15px; border-radius: 5px; margin-bottom: 10px;
    }
    </style>
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. GENERAZIONE DATI (Database Unificato)
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
        weights = [0.8, 0.05, 0.1, 0.05] if prod_year <= 2021 else [0.6, 0.2, 0.15, 0.05]
        mat = random.choices(materials, weights=weights)[0]

        if cat == "Diver":
            diam, thick = random.choice([41.0, 42.0, 43.0]), random.choice([13.0, 14.0, 15.0])
        elif cat == "Dress":
            diam, thick = random.choice([36.0, 37.0, 38.0, 39.0]), random.choice([8.0, 9.0, 10.0])
        else:
            diam, thick = random.choice([39.0, 40.0, 41.0]), random.choice([11.0, 12.0, 13.0])

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": int(random.randint(1500, 5000)),
            "Category": cat, "Year": int(prod_year), "Material": mat, 
            "Diameter": diam, "Thickness": thick, "Reserve": reserve, 
            "WR": random.choice([50, 100, 200, 300]), "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Comp {i}", f"REF-{1000+i}") for i in range(1, 1501)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence", "Market Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v4.2")

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
        k2.metric("Year", target['Year'])
        k3.metric("Competitors", len(df_f))
        k4.metric("Avg Market", f"€ {avg_p:,.0f}")
        k5.metric("Your Price", f"€ {target['Price']:,}", f"{diff:+.1f}% vs avg", delta_color="inverse")
        
        st.write("---")
        fig = px.scatter(pd.concat([df_f, pd.DataFrame([target])]), x="Price", y=y_param, color="Type",
                         color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
                         size_max=20, template="plotly_white", height=450)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No matches found.")

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
    st.write("### 📈 Tech Evolution Tracker")
    trend_param = st.selectbox("Monitor Industrial Standard", ["Reserve", "Price", "Thickness"])
    yearly_trends = df_all.groupby('Year')[trend_param].mean().reset_index()
    
    fig_trend = px.line(yearly_trends, x='Year', y=trend_param, markers=True, template="plotly_white", color_discrete_sequence=["#d4af37"])
    st.plotly_chart(fig_trend, use_container_width=True)

    st.write("---")
    st.write("### ⚠️ AI Strategic Insights")
    col_ins1, col_ins2 = st.columns(2)
    
    with col_ins1:
        st.write("**Obsolescence Alert**")
        target_watch = st.session_state.my_portfolio[0]
        # FIX: Cerchiamo l'anno massimo disponibile invece di forzare il 2026
        max_year = yearly_trends['Year'].max()
        current_mkt_avg = yearly_trends[yearly_trends['Year'] == max_year][trend_param].values[0]
        
        if target_watch[trend_param] < current_mkt_avg:
            gap = ((current_mkt_avg - target_watch[trend_param]) / current_mkt_avg) * 100
            st.error(f"**Action Required**: Your {target_watch['Model']} ({target_watch[trend_param]}h) is **{gap:.1f}% lower** than the {max_year} market standard ({current_mkt_avg:.0f}h).")
        else:
            st.success(f"**Competitive Edge**: Your specs are aligned with {max_year} standards.")

    with col_ins2:
        st.write("**Material Trends**")
        mat_21 = len(df_all[(df_all['Year'] <= 2021) & (df_all['Material'] == "Titanium Grade 5")]) / len(df_all[df_all['Year'] <= 2021]) if len(df_all[df_all['Year'] <= 2021]) > 0 else 0
        mat_26 = len(df_all[(df_all['Year'] >= 2024) & (df_all['Material'] == "Titanium Grade 5")]) / len(df_all[df_all['Year'] >= 2024]) if len(df_all[df_all['Year'] >= 2024]) > 0 else 0
        growth = (mat_26 - mat_21) * 100
        st.markdown(f'<div class="insight-card"><b>Material Shift</b>: Detected <b>+{growth:.1f}%</b> increase in <b>Titanium Grade 5</b>.<br><i>Strategy: Consider case upgrade for 2027 collection.</i></div>', unsafe_allow_html=True)
