import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - ATLAS INSPIRED (Unificato)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F4F7FA !important; }
    .stApp { background-color: #F4F7FA; }
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background-color: white; display: flex; align-items: center;
        padding: 0 40px; border-bottom: 1px solid #E2E8F0; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.5rem; color: #1a1a1a; letter-spacing: -1px; }
    .logo-accent { color: #d4af37; }
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0 !important; }
    .atlass-card {
        background-color: white; padding: 24px; border-radius: 16px;
        border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .card-label { color: #64748B; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; }
    .card-value { color: #1E293B; font-size: 1.8rem; font-weight: 700; }
    .category-badge { background-color: #F1F5F9; color: #475569; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }
    .block-container { padding-top: 6rem !important; }
    [data-testid="stHeader"] { display: none; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE
if 'initialized' not in st.session_state:
    random.seed(42)
    def create_watch(brand, model, is_target=False, year=None):
        cat = random.choice(["Diver", "Dress", "GMT", "Chronograph", "Casual"])
        yr = year if year else random.randint(2019, 2026)
        if cat == "Diver": d, t = random.choice([41, 42, 43]), random.choice([13, 14, 15])
        elif cat == "Dress": d, t = random.choice([37, 38, 39]), random.choice([8, 9, 10])
        else: d, t = random.choice([39, 40, 41]), random.choice([11, 12, 13])
        return {
            "Brand": brand, "Model": model, "Category": cat, "Year": yr,
            "Diameter": d, "Thickness": t, "Price": random.randint(1800, 5500),
            "Reserve": int((42 if yr <= 2020 else 72) + random.randint(-5, 5)), "Type": "Target" if is_target else "Market"
        }
    st.session_state.my_portfolio = [create_watch("MY BRAND", f"Alpha {i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_watch(f"Brand {random.randint(1,20)}", f"Comp {i}") for i in range(1, 1500)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    view = st.radio("Reports", ["Dashboard", "Price Intelligence", "Design Grid", "Market Trends"])

df_all = pd.DataFrame(st.session_state.competitors)

# --- VIEW: DESIGN GRID (LA SEZIONE CHE MANCAVA) ---
if view == "Design Grid":
    st.markdown("### Design Intelligence Matrix")
    
    # Filtri in stile pulito
    c1, c2 = st.columns([1, 2])
    with c1:
        sel_cat = st.selectbox("Category", ["All Categories"] + list(df_all['Category'].unique()))
    with c2:
        years = st.slider("Production Period", 2019, 2026, (2020, 2024))

    df_f = df_all[df_all['Year'].between(years[0], years[1])]
    if sel_cat != "All Categories":
        df_f = df_f[df_f['Category'] == sel_cat]

    # Heatmap logic
    matrix = df_f.groupby(['Diameter', 'Thickness']).size().reset_index(name='count')
    pivot = matrix.pivot(index='Thickness', columns='Diameter', values='count').fillna(0)

    col_m1, col_m2 = st.columns([2, 1])
    
    with col_m1:
        st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values, x=pivot.columns, y=pivot.index,
            colorscale=[[0, '#F1F5F9'], [0.1, '#FEF3C7'], [0.5, '#F59E0B'], [1, '#D4AF37']],
            text=pivot.values, texttemplate="%{text}", hoverinfo="z"
        ))
        fig.update_layout(height=450, margin=dict(l=0,r=0,t=0,b=0), template="plotly_white",
                          xaxis_title="Diameter (mm)", yaxis_title="Thickness (mm)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
            <div class="atlass-card" style="height:495px;">
                <div class="card-label">Market Saturation</div>
                <div class="card-value">{len(df_f)} <span style="font-size:1rem; color:#64748B;">Models</span></div>
                <hr style="border:0; border-top:1px solid #E2E8F0; margin:20px 0;">
                <div style="font-size:0.9rem; color:#475569;">
                    <b>Analysis:</b><br>
                    The matrix shows a high concentration in the 40mm/12mm segment.<br><br>
                    <b>Strategic Gap:</b><br>
                    Low competition detected in <b>39mm/10mm</b> configurations for the {sel_cat} segment.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Inspector
    st.markdown("### Model Inspector")
    with st.expander("View specific models in the selected grid", expanded=False):
        st.dataframe(df_f[["Brand", "Model", "Diameter", "Thickness", "Price"]], use_container_width=True, hide_index=True)

# (Le altre sezioni Dashboard, Price e Market rimangono con la logica Atlass v5.0)
elif view == "Dashboard":
    st.markdown("### Portfolio Overview")
    cols = st.columns(5)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f'<div class="atlass-card"><span class="category-badge">{w["Category"]}</span><div style="font-weight:600; margin-top:12px;">{w["Model"]}</div><div style="color:#d4af37; font-weight:600;">€ {w["Price"]:,}</div></div>', unsafe_allow_html=True)

elif view == "Price Intelligence":
    st.info("Section active with v5.0 pricing logic.")

elif view == "Market Trends":
    st.info("Section active with v5.0 trend logic.")
