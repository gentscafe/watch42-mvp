import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - ATLAS ZERO-GAP (v6.6)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F4F7FA !important; }
    .stApp { background-color: #F4F7FA; }
    
    /* Riduzione drastica dei margini tra i blocchi Streamlit */
    .block-container { padding-top: 5rem !important; padding-bottom: 0rem !important; }
    [data-testid="stVerticalBlock"] > div { padding-top: 0rem !important; padding-bottom: 0.5rem !important; }
    
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background-color: white; display: flex; align-items: center;
        padding: 0 40px; border-bottom: 1px solid #E2E8F0; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.4rem; color: #1a1a1a; letter-spacing: -1px; }
    .logo-accent { color: #d4af37; }
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0 !important; }
    [data-testid="stSidebarNav"] { display: none; }
    
    .stButton > button {
        border: none !important; background-color: transparent !important; color: #64748B !important;
        text-align: left !important; padding: 10px 20px !important; font-weight: 500 !important;
        border-radius: 10px !important;
    }
    .stButton > button:hover { background-color: #F8FAFC !important; color: #1E293B !important; }

    .atlass-card {
        background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02); margin-bottom: 10px;
    }
    .card-label { color: #64748B; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
    .card-value { color: #1E293B; font-size: 1.1rem; font-weight: 700; }
    
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 2px 8px; 
        border-radius: 4px; font-size: 0.6rem; font-weight: 700;
    }
    .price-tag { color: #d4af37; font-weight: 700; }
    [data-testid="stHeader"] { display: none; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE (Fears Portfolio)
fears_models = [
    {"Model": "Brunswick 38 Copper", "Category": "Casual", "Year": 2022, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "WR": 50, "Price": 4150},
    {"Model": "Brunswick 40 Silver", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "WR": 100, "Price": 4450},
    {"Model": "Archival 1930 Small Seconds", "Category": "Dress", "Year": 2021, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "WR": 0, "Price": 4200},
    {"Model": "Brunswick 38 Blue Danubian", "Category": "Casual", "Year": 2023, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "WR": 50, "Price": 4150},
    {"Model": "Brunswick PT (Platinum)", "Category": "Luxury", "Year": 2023, "Diameter": 38, "Thickness": 12.1, "Reserve": 50, "WR": 50, "Price": 33000},
    {"Model": "Fears Garrick Collaboration", "Category": "High-End", "Year": 2022, "Diameter": 42, "Thickness": 10.0, "Reserve": 45, "WR": 100, "Price": 19500},
    {"Model": "Brunswick 40 Pinkish Salmon", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "WR": 100, "Price": 4450},
    {"Model": "Brunswick 38 White Rose", "Category": "Casual", "Year": 2022, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "WR": 50, "Price": 4150},
    {"Model": "Archival 1930 Topper Edition", "Category": "Dress", "Year": 2022, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "WR": 0, "Price": 4500},
    {"Model": "Brunswick 40 Aurora", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "WR": 100, "Price": 4600}
]

if 'competitors' not in st.session_state:
    random.seed(42)
    st.session_state.competitors = [{
        "Brand": f"B-{i}", "Model": f"M-{i}", "Category": random.choice(["Casual", "Dress", "Luxury", "High-End"]), 
        "Year": random.randint(2020, 2026), "Diameter": random.choice([38, 40]), "Thickness": random.uniform(9, 13), 
        "Reserve": random.randint(40, 70), "Price": random.randint(3000, 20000), "WR": 50
    } for i in range(1000)]

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'view' not in st.session_state: st.session_state.view = "Dashboard"
    def nav(n): st.session_state.view = n
    for n, icon in [("Dashboard", "📊"), ("Pricing Intelligence", "💰"), ("Design Grid", "📐"), ("Market Trends", "📈")]:
        st.button(f"{icon} {n}", key=f"n_{n}", use_container_width=True, on_click=nav, args=(n,))

view = st.session_state.view
df_all = pd.DataFrame(st.session_state.competitors)

# --- VIEW: PRICING INTELLIGENCE (Compact Layout) ---
if view == "Pricing Intelligence":
    # Riga 1: Titolo e Filtri (Tutto sulla stessa linea per salvare spazio)
    f1, f2, f3 = st.columns([1.2, 1, 1])
    with f1: st.subheader("Pricing Analysis")
    with f2: target = st.selectbox("Model", fears_models, format_func=lambda x: x['Model'], label_visibility="collapsed")
    with f3: y_axis = st.selectbox("Axis Y", ["Reserve", "Thickness", "Diameter", "WR"], label_visibility="collapsed")
    
    df_f = df_all[df_all['Category'] == target['Category']]
    avg_p = df_f['Price'].mean()
    diff = ((target['Price'] - avg_p) / avg_p) * 100
    
    # Riga 2: KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="atlass-card"><div class="card-label">Segment</div><div class="card-value">{target["Category"]}</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="atlass-card"><div class="card-label">Market Avg</div><div class="card-value">€ {avg_p:,.0f}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="atlass-card"><div class="card-label">Your Price</div><div class="card-value">€ {target["Price"]:,}</div></div>', unsafe_allow_html=True)
    # Gap colorato direttamente nella card senza spazi extra
    color = "#10B981" if diff < 0 else "#EF4444"
    k4.markdown(f'<div class="atlass-card"><div class="card-label">Gap</div><div class="card-value" style="color:{color}">{diff:+.1f}%</div></div>', unsafe_allow_html=True)
    
    # Riga 3: Grafico (Attaccato alle card)
    st.markdown('<div class="atlass-card" style="margin-top:-5px;">', unsafe_allow_html=True)
    fig = px.scatter(df_f, x="Price", y=y_axis, color_discrete_sequence=["#CBD5E0"], opacity=0.4)
    fig.add_trace(go.Scatter(x=[target['Price']], y=[target[y_axis]], mode='markers+text', text=[target['Model']], 
                               textposition="top center", marker=dict(color='#d4af37', size=14, line=dict(width=2, color='white'))))
    fig.update_layout(template="plotly_white", height=400, margin=dict(l=0,r=0,t=10,b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "Dashboard":
    st.subheader("Fears Collection Overview")
    cols = st.columns(4)
    for i, w in enumerate(fears_models):
        with cols[i % 4]:
            st.markdown(f'<div class="atlass-card"><span class="category-badge">{w["Category"]}</span><div style="font-weight:600; margin-top:10px;">{w["Model"]}</div><div class="price-tag">€ {w["Price"]:,}</div></div>', unsafe_allow_html=True)

# (Altre sezioni seguono la stessa logica di margini ridotti)
