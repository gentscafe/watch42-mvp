import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - TOTAL ATLAS DESIGN (v5.6)
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
        background-color: white; padding: 24px; border-radius: 16px; border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;
    }
    .card-label { color: #64748B; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-value { color: #1E293B; font-size: 1.8rem; font-weight: 700; margin: 4px 0; }
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    }
    .price-tag { color: #d4af37; font-weight: 600; font-size: 1.1rem; }
    .block-container { padding-top: 6rem !important; padding-right: 3rem !important; padding-left: 3rem !important; }
    [data-testid="stHeader"] { display: none; }
    .insight-box { background-color: #FEF9C3; border-left: 4px solid #d4af37; padding: 16px; border-radius: 8px; margin-top: 10px; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE - FEARS REAL DATA
if 'initialized' not in st.session_state:
    # Portfolio Reale Fears
    st.session_state.my_portfolio = [
        {"Brand": "Fears", "Model": "Brunswick 38 Copper", "Category": "Casual", "Year": 2024, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 4150, "Material": "Steel"},
        {"Brand": "Fears", "Model": "Brunswick 40 Silver", "Category": "Casual", "Year": 2025, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450, "Material": "Steel"},
        {"Brand": "Fears", "Model": "Archival 1930", "Category": "Dress", "Year": 2021, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "Price": 3950, "Material": "Steel"},
        {"Brand": "Fears", "Model": "Fears Garrick", "Category": "High-End", "Year": 2022, "Diameter": 42, "Thickness": 10.0, "Reserve": 45, "Price": 19500, "Material": "904L Steel"},
        {"Brand": "Fears", "Model": "Brunswick PT", "Category": "Luxury", "Year": 2024, "Diameter": 38, "Thickness": 12.1, "Reserve": 50, "Price": 33000, "Material": "Platinum"}
    ]
    
    # Generatore Competitor (Market Data)
    random.seed(42)
    st.session_state.competitors = []
    for i in range(1000):
        cat = random.choice(["Casual", "Dress", "High-End", "Luxury"])
        yr = random.randint(2020, 2026)
        # Logica di mercato: la riserva sta salendo verso i 72h
        res = int(42 + (yr-2020)*5 + random.randint(-5, 5))
        st.session_state.competitors.append({
            "Brand": f"Brand {random.randint(1,50)}", "Model": f"Comp {i}", "Category": cat, "Year": yr,
            "Diameter": random.choice([38, 39, 40, 41, 42]), "Thickness": random.uniform(9, 14), 
            "Reserve": res, "Price": random.randint(2000, 35000)
        })
    st.session_state.initialized = True

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'current_page' not in st.session_state: st.session_state.current_page = "Dashboard"
    def set_page(name): st.session_state.current_page = name
    pages = [("Dashboard", "📊"), ("Pricing Intelligence", "💰"), ("Design Grid", "📐"), ("Market Trends", "📈")]
    for name, icon in pages:
        st.button(f"{icon} {name}", key=f"btn_{name}", use_container_width=True, on_click=set_page, args=(name,))
    st.write("---")
    st.caption("Fears Intelligence v5.6")

df_all = pd.DataFrame(st.session_state.competitors)
view = st.session_state.current_page

# --- VIEWS ---
if view == "Dashboard":
    st.markdown("### Fears Collection Overview")
    cols = st.columns(5)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="atlass-card">
                    <span class="category-badge">{w['Category']}</span>
                    <div style="font-weight:600; margin-top:12px; color:#1E293B; height:40px;">{w['Model']}</div>
                    <div class="price-tag">€ {w['Price']:,}</div>
                    <div style="font-size:0.75rem; color:#94A3B8; margin-top:4px;">{w['Material']} | {w['Diameter']}mm</div>
                </div>
            """, unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1: st.markdown("### Fears Pricing Analysis")
    with col_t2: target = st.selectbox("Seleziona Modello Fears", st.session_state.my_portfolio, format_func=lambda x: f"{x['Model']} ({x['Year']})")
    
    df_f = df_all[(df_all['Category'] == target['Category'])]
    avg_p = df_f['Price'].mean() if not df_f.empty else 0
    diff = ((target['Price'] - avg_p) / avg_p) * 100 if avg_p > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    for m, (label, val, delta) in zip([m1, m2, m3, m4], [("Segmento", target['Category'], None), ("Benchmark Items", len(df_f), None), ("Media Mercato", f"€ {avg_p:,.0f}", None), ("Posizionamento", f"€ {target['Price']:,}", f"{diff:+.1f}%")]):
        with m:
            delta_html = f'<div style="color:{"#10B981" if diff < 0 else "#EF4444"}; font-size:0.85rem; font-weight:600;">{delta} vs avg</div>' if delta else ""
            st.markdown(f'<div class="atlass-card"><div class="card-label">{label}</div><div class="card-value">{val}</div>{delta_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
    fig_p = px.scatter(df_f, x="Price", y="Reserve", color_discrete_sequence=["#CBD5E0"], opacity=0.4, labels={"Price": "Prezzo (€)", "Reserve": "Riserva di Carica (h)"})
    fig_p.add_trace(go.Scatter(x=[target['Price']], y=[target['Reserve']], mode='markers+text', name=target['Model'], text=[target['Model']], textposition="top center", marker=dict(color='#d4af37', size=15, line=dict(width=2, color='white'))))
    fig_p.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=20, b=0), height=450, showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "Design Grid":
    st.markdown("### Fears Design Matrix (Form vs Thinness)")
    c1, c2 = st.columns([1, 2])
    with c1: sel_cat = st.selectbox("Categoria", ["All"] + list(df_all['Category'].unique()))
    with c2: years = st.slider("Periodo di Analisi", 2020, 2026, (2022, 2025))
    df_f_design = df_all[df_all['Year'].between(years[0], years[1])]
    if sel_cat != "All": df_f_design = df_f_design[df_f_design['Category'] == sel_cat]
    
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
        fig_h = px.density_heatmap(df_f_design, x="Diameter", y="Thickness", nbinsx=10, nbinsy=10, color_continuous_scale=[[0, '#F1F5F9'], [1, '#D4AF37']])
        fig_h.update_layout(height=450, margin=dict(l=0,r=0,t=0,b=0), template="plotly_white")
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="atlass-card" style="height:495px;"><div class="card-label">Strategic Insights</div><div class="card-value">Fears Sweet Spot</div><hr style="border:0; border-top:1px solid #E2E8F0; margin:20px 0;"><div style="font-size:0.9rem; color:#475569;">I modelli Fears come l\'<b>Archival</b> (8.5mm) si posizionano in un\'area di mercato "ultra-slim" quasi priva di competitor nel segmento sotto i 4000€.</div></div>', unsafe_allow_html=True)

elif view == "Market Trends":
    st.markdown("### Fears vs Market Evolution")
    trend_cat = st.selectbox("Settore", ["All"] + list(df_all['Category'].unique()))
    df_t = df_all if trend_cat == "All" else df_all[df_all['Category'] == trend_cat]
    trends = df_t.groupby('Year')['Reserve'].mean().reset_index()
    
    c_left, c_right = st.columns([1.6, 1])
    with c_left:
        st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Trend Riserva di Carica (Mercato)</div>', unsafe_allow_html=True)
        fig_line = px.line(trends, x='Year', y='Reserve', markers=True, color_discrete_sequence=["#d4af37"])
        for w in st.session_state.my_portfolio:
            if trend_cat == "All" or w['Category'] == trend_cat:
                fig_line.add_trace(go.Scatter(x=[w['Year']], y=[w['Reserve']], mode='markers+text', name=w['Model'], text=[w['Model']], textposition="bottom right", marker=dict(size=10)))
        fig_line.update_layout(template="plotly_white", height=400, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c_right:
        st.markdown(f"""
            <div class="atlass-card" style="height:488px;">
                <div class="card-label">Fears Intelligence Report</div>
                <div class="insight-box">
                    <b>Analisi Calibro</b><br>
                    Il Brunswick 40 con 68h di riserva è perfettamente allineato al trend 2026.<br>
                    <i>Consiglio: Upgrade dei calibri manuali (50h) per mantenere il vantaggio competitivo.</i>
                </div>
            </div>
        """, unsafe_allow_html=True)
