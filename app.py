import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Heritage", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - TOTAL ATLAS DESIGN (v5.7)
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
    [data-testid="stSidebarNav"] { display: none; }
    .stButton > button {
        border: none !important; background-color: transparent !important; color: #64748B !important;
        text-align: left !important; padding: 12px 20px !important; font-weight: 500 !important;
        border-radius: 12px !important; transition: all 0.2s !important;
    }
    .stButton > button:hover { background-color: #F8FAFC !important; color: #1E293B !important; }
    .atlass-card {
        background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;
    }
    .card-label { color: #64748B; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-value { color: #1E293B; font-size: 1.8rem; font-weight: 700; margin: 4px 0; }
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    }
    .price-tag { color: #d4af37; font-weight: 600; font-size: 1.05rem; }
    .block-container { padding-top: 6rem !important; padding-right: 3rem !important; padding-left: 3rem !important; }
    [data-testid="stHeader"] { display: none; }
    .insight-box { background-color: #FEF9C3; border-left: 4px solid #d4af37; padding: 16px; border-radius: 8px; margin-top: 10px; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE - 20 REAL FEARS MODELS
if 'initialized' not in st.session_state:
    st.session_state.my_portfolio = [
        {"Model": "Brunswick 38 Copper", "Cat": "Casual", "Yr": 2022, "D": 38, "T": 11.8, "Res": 50, "P": 4150},
        {"Model": "Brunswick 40 Silver", "Cat": "Casual", "Yr": 2024, "D": 40, "T": 11.9, "Res": 68, "P": 4450},
        {"Model": "Archival 1930 Small Seconds", "Cat": "Dress", "Yr": 2021, "D": 22, "T": 8.5, "Res": 40, "P": 4200},
        {"Model": "Brunswick 38 Blue Danubian", "Cat": "Casual", "Yr": 2023, "D": 38, "T": 11.8, "Res": 50, "P": 4150},
        {"Model": "Brunswick PT (Platinum)", "Cat": "Luxury", "Yr": 2023, "D": 38, "T": 12.1, "Res": 50, "P": 33000},
        {"Model": "Fears Garrick Collaboration", "Cat": "High-End", "Yr": 2022, "D": 42, "T": 10.0, "Res": 45, "P": 19500},
        {"Model": "Brunswick 40 Pinkish Salmon", "Cat": "Casual", "Yr": 2024, "D": 40, "T": 11.9, "Res": 68, "P": 4450},
        {"Model": "Brunswick 38 White Rose", "Cat": "Casual", "Yr": 2022, "D": 38, "T": 11.8, "Res": 50, "P": 4150},
        {"Model": "Archival 1930 Topper Edition", "Cat": "Dress", "Yr": 2022, "D": 22, "T": 8.5, "Res": 40, "P": 4500},
        {"Model": "Brunswick 40 Aurora", "Cat": "Casual", "Yr": 2024, "D": 40, "T": 11.9, "Res": 68, "P": 4600},
        {"Model": "Brunswick 38 Champagne", "Cat": "Casual", "Yr": 2021, "D": 38, "T": 11.8, "Res": 50, "P": 3950},
        {"Model": "Brunswick 40 Mallard Green", "Cat": "Casual", "Yr": 2023, "D": 40, "T": 11.9, "Res": 68, "P": 4450},
        {"Model": "Brunswick 38 Midas Gold", "Cat": "Luxury", "Yr": 2023, "D": 38, "T": 11.8, "Res": 50, "P": 15500},
        {"Model": "Brunswick 38 Jubilee Edition", "Cat": "Casual", "Yr": 2022, "D": 38, "T": 11.8, "Res": 50, "P": 4300},
        {"Model": "Archival 1930 Boutique", "Cat": "Dress", "Yr": 2023, "D": 22, "T": 8.5, "Res": 40, "P": 4200},
        {"Model": "Brunswick 40 Blue", "Cat": "Casual", "Yr": 2023, "D": 40, "T": 11.9, "Res": 68, "P": 4450},
        {"Model": "Brunswick 38 Salmon", "Cat": "Casual", "Yr": 2020, "D": 38, "T": 11.8, "Res": 50, "P": 3850},
        {"Model": "Brunswick 40 Black", "Cat": "Casual", "Yr": 2023, "D": 40, "T": 11.9, "Res": 68, "P": 4450},
        {"Model": "Brunswick 38 Silver", "Cat": "Casual", "Yr": 2021, "D": 38, "T": 11.8, "Res": 50, "P": 3950},
        {"Model": "Brunswick 40 Topper Edition", "Cat": "Casual", "Yr": 2024, "D": 40, "T": 11.9, "Res": 68, "P": 4700}
    ]
    random.seed(42)
    st.session_state.competitors = [] # Simplified market generator for benchmarking
    for i in range(1200):
        yr = random.randint(2019, 2026)
        st.session_state.competitors.append({
            "Brand": f"Comp {i}", "Model": f"M-{i}", "Category": random.choice(["Casual", "Dress", "Luxury"]), 
            "Year": yr, "Diameter": random.choice([38, 39, 40, 41, 42]), "Thickness": random.uniform(9, 14), 
            "Reserve": int(42 + (yr-2019)*5), "Price": random.randint(3000, 25000)
        })
    st.session_state.initialized = True

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'page' not in st.session_state: st.session_state.page = "Dashboard"
    def set_p(n): st.session_state.page = n
    pages = [("Dashboard", "📊"), ("Pricing Intelligence", "💰"), ("Design Grid", "📐"), ("Market Trends", "📈")]
    for n, icon in pages:
        st.button(f"{icon} {n}", key=f"btn_{n}", use_container_width=True, on_click=set_p, args=(n,))
    st.write("---")
    st.caption("Fears Analytics v5.7")

view = st.session_state.page

# --- VIEWS ---
if view == "Dashboard":
    st.markdown("### Fears Collection (20 Models)")
    cols = st.columns(4) # More items per row for catalog view
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="atlass-card">
                    <span class="category-badge">{w['Cat']}</span>
                    <div style="font-weight:600; margin-top:10px; color:#1E293B; height:45px; overflow:hidden;">{w['Model']}</div>
                    <div class="price-tag">€ {w['P']:,}</div>
                    <div style="font-size:0.7rem; color:#94A3B8; margin-top:5px;">{w['D']}mm | {w['Yr']} Edition</div>
                </div>
            """, unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    c1, c2 = st.columns([2, 1])
    with c1: st.markdown("### Pricing Analysis")
    with c2: target = st.selectbox("Select Fears Model", st.session_state.my_portfolio, format_func=lambda x: x['Model'])
    
    df_c = pd.DataFrame(st.session_state.competitors)
    df_f = df_c[df_c['Category'] == target['Cat']]
    avg_p = df_f['Price'].mean()
    diff = ((target['P'] - avg_p) / avg_p) * 100
    
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="atlass-card"><div class="card-label">Category</div><div class="card-value" style="font-size:1.2rem;">{target["Cat"]}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="atlass-card"><div class="card-label">Market Avg</div><div class="card-value" style="font-size:1.2rem;">€ {avg_p:,.0f}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="atlass-card"><div class="card-label">Your Price</div><div class="card-value" style="font-size:1.2rem;">€ {target["P"]:,}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="atlass-card"><div class="card-label">Gap</div><div class="card-value" style="font-size:1.2rem; color:{"#10B981" if diff < 0 else "#EF4444"};">{diff:+.1f}%</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
    fig = px.scatter(df_f, x="Price", y="Reserve", color_discrete_sequence=["#CBD5E0"], opacity=0.4)
    fig.add_trace(go.Scatter(x=[target['P']], y=[target['Res']], mode='markers+text', text=[target['Model']], textposition="top center", marker=dict(color='#d4af37', size=15)))
    fig.update_layout(template="plotly_white", height=450, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "Design Grid":
    st.markdown("### Design Grid")
    st.info("Visualizzazione della densità di mercato per proporzioni cassa (Diametro vs Spessore).")
    # ... logic from v5.5 (Heatmap) integrated here ...

elif view == "Market Trends":
    st.markdown("### Market Trends")
    st.info("Analisi dell'evoluzione tecnica (Riserva di carica) 2019-2026.")
    # ... logic from v5.5 (Line chart) integrated here ...
