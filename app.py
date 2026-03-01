import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - TOTAL ATLAS DESIGN
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
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    }
    .price-tag { color: #d4af37; font-weight: 600; font-size: 1.1rem; }
    .block-container { padding-top: 6rem !important; padding-right: 3rem !important; padding-left: 3rem !important; }
    [data-testid="stHeader"] { display: none; }
    .insight-box { background-color: #FEF9C3; border-left: 4px solid #d4af37; padding: 16px; border-radius: 8px; margin-top: 10px; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE - FEARS PORTFOLIO + MARKET DATA
fears_models = [
    {"Model": "Brunswick 38 Copper", "Category": "Casual", "Year": 2022, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 4150},
    {"Model": "Brunswick 40 Silver", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450},
    {"Model": "Archival 1930 Small Seconds", "Category": "Dress", "Year": 2021, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "Price": 4200},
    {"Model": "Brunswick 38 Blue Danubian", "Category": "Casual", "Year": 2023, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 4150},
    {"Model": "Brunswick PT (Platinum)", "Category": "Luxury", "Year": 2023, "Diameter": 38, "Thickness": 12.1, "Reserve": 50, "Price": 33000},
    {"Model": "Fears Garrick Collaboration", "Category": "High-End", "Year": 2022, "Diameter": 42, "Thickness": 10.0, "Reserve": 45, "Price": 19500},
    {"Model": "Brunswick 40 Pinkish Salmon", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450},
    {"Model": "Brunswick 38 White Rose", "Category": "Casual", "Year": 2022, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 4150},
    {"Model": "Archival 1930 Topper Edition", "Category": "Dress", "Year": 2022, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "Price": 4500},
    {"Model": "Brunswick 40 Aurora", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4600},
    {"Model": "Brunswick 38 Champagne", "Category": "Casual", "Year": 2021, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 3950},
    {"Model": "Brunswick 40 Mallard Green", "Category": "Casual", "Year": 2023, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450},
    {"Model": "Brunswick 38 Midas Gold", "Category": "Luxury", "Year": 2023, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 15500},
    {"Model": "Brunswick 38 Jubilee Edition", "Category": "Casual", "Year": 2022, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 4300},
    {"Model": "Archival 1930 Boutique", "Category": "Dress", "Year": 2023, "Diameter": 22, "Thickness": 8.5, "Reserve": 40, "Price": 4200},
    {"Model": "Brunswick 40 Blue", "Category": "Casual", "Year": 2023, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450},
    {"Model": "Brunswick 38 Salmon", "Category": "Casual", "Year": 2020, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 3850},
    {"Model": "Brunswick 40 Black", "Category": "Casual", "Year": 2023, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4450},
    {"Model": "Brunswick 38 Silver", "Category": "Casual", "Year": 2021, "Diameter": 38, "Thickness": 11.8, "Reserve": 50, "Price": 3950},
    {"Model": "Brunswick 40 Topper Edition", "Category": "Casual", "Year": 2024, "Diameter": 40, "Thickness": 11.9, "Reserve": 68, "Price": 4700}
]

st.session_state.my_portfolio = fears_models

if 'competitors' not in st.session_state:
    random.seed(42)
    st.session_state.competitors = []
    for i in range(1200):
        yr = random.randint(2019, 2026)
        st.session_state.competitors.append({
            "Brand": f"Brand {random.randint(1,50)}", "Model": f"M-{i}", 
            "Category": random.choice(["Casual", "Dress", "Luxury", "High-End"]), 
            "Year": yr, "Diameter": random.choice([38, 39, 40, 41, 42]), "Thickness": random.uniform(9, 14), 
            "Reserve": int(42 + (yr-2019)*5), "Price": random.randint(3000, 25000)
        })

# 4. CUSTOM SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'p_view' not in st.session_state: st.session_state.p_view = "Dashboard"
    def set_v(n): st.session_state.p_view = n
    pages = [("Dashboard", "📊"), ("Pricing Intelligence", "💰"), ("Design Grid", "📐"), ("Market Trends", "📈")]
    for n, icon in pages:
        st.button(f"{icon} {n}", key=f"btn_{n}", use_container_width=True, on_click=set_v, args=(n,))
    st.write("---")
    st.caption("Fears Analytics v6.3")

view = st.session_state.p_view
df_all = pd.DataFrame(st.session_state.competitors)

# --- 5. VIEW: DASHBOARD (Fears Catalog - No Images) ---
if view == "Dashboard":
    st.markdown("### Fears Collection Overview")
    cols = st.columns(4)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="atlass-card">
                    <span class="category-badge">{w['Category']}</span>
                    <div style="font-weight:600; margin-top:12px; color:#1E293B; height:38px; overflow:hidden; font-size:0.95rem;">{w['Model']}</div>
                    <div class="price-tag">€ {w['Price']:,}</div>
                    <div style="font-size:0.75rem; color:#94A3B8; margin-top:8px; border-top:1px solid #F1F5F9; padding-top:8px;">{w['Diameter']}mm | {w['Year']} Edition</div>
                </div>
            """, unsafe_allow_html=True)

# --- 6. VIEW: PRICING INTELLIGENCE ---
elif view == "Pricing Intelligence":
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1: st.markdown("### Pricing Analysis")
    with col_t2: target = st.selectbox("Select Model", st.session_state.my_portfolio, format_func=lambda x: x['Model'])
    
    df_f = df_all[df_all['Category'] == target['Category']]
    avg_p = df_f['Price'].mean() if not df_f.empty else 0
    diff = ((target['Price'] - avg_p) / avg_p) * 100 if avg_p > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    for m, (label, val, delta) in zip([m1, m2, m3, m4], [("Category", target['Category'], None), ("Competitors", len(df_f), None), ("Market Avg", f"€ {avg_p:,.0f}", None), ("Positioning", f"€ {target['Price']:,}", f"{diff:+.1f}%")]):
        with m:
            delta_html = f'<div style="color:{"#10B981" if diff < 0 else "#EF4444"}; font-size:0.8rem; font-weight:600;">{delta} vs avg</div>' if delta else ""
            st.markdown(f'<div class="atlass-card"><div class="card-label">{label}</div><div class="card-value" style="font-size:1.2rem;">{val}</div>{delta_html}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
    fig_p = px.scatter(df_f, x="Price", y="Reserve", color_discrete_sequence=["#CBD5E0"], opacity=0.4)
    fig_p.add_trace(go.Scatter(x=[target['Price']], y=[target['Reserve']], mode='markers+text', text=[target['Model']], textposition="top center", marker=dict(color='#d4af37', size=15, line=dict(width=2, color='white'))))
    fig_p.update_layout(template="plotly_white", height=400, margin=dict(l=0,r=0,t=20,b=0), showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. VIEW: DESIGN GRID ---
elif view == "Design Grid":
    st.markdown("### Design Intelligence Matrix")
    c1, c2 = st.columns([1, 2])
    with c1: sel_cat = st.selectbox("Category Filter", ["All Categories"] + list(df_all['Category'].unique()))
    with c2: years = st.slider("Timeline", 2019, 2026, (2020, 2024))
    
    df_f_design = df_all[df_all['Year'].between(years[0], years[1])]
    if sel_cat != "All Categories": df_f_design = df_f_design[df_f_design['Category'] == sel_cat]
    
    matrix = df_f_design.groupby(['Diameter', 'Thickness']).size().reset_index(name='count')
    pivot = matrix.pivot(index='Thickness', columns='Diameter', values='count').fillna(0)
    
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
        fig_h = go.Figure(data=go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index, colorscale=[[0, '#F1F5F9'], [1, '#D4AF37']], text=pivot.values, texttemplate="%{text}"))
        fig_h.update_layout(height=450, margin=dict(l=0,r=0,t=0,b=0), template="plotly_white", xaxis_title="Diameter (mm)", yaxis_title="Thickness (mm)")
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="atlass-card" style="height:495px;"><div class="card-label">Strategic Insights</div><div class="card-value">{len(df_f_design)} Models</div><hr style="border:0; border-top:1px solid #E2E8F0; margin:20px 0;"><div style="font-size:0.9rem; color:#475569;"><b>White Space Detected:</b><br>Low competition in dimensions below 39mm for the {sel_cat} segment.</div></div>', unsafe_allow_html=True)

# --- 8. VIEW: MARKET TRENDS ---
elif view == "Market Trends":
    st.markdown("### Market Intelligence & Trends")
    trend_cat = st.selectbox("Segment Filter", ["All Categories"] + list(df_all['Category'].unique()))
    df_t = df_all if trend_cat == "All Categories" else df_all[df_all['Category'] == trend_cat]
    trends = df_t.groupby('Year')['Reserve'].mean().reset_index()
    max_yr = int(trends['Year'].max()) if not trends.empty else 2026
    mkt_avg_2026 = trends[trends['Year'] == max_yr]['Reserve'].values[0] if not trends.empty else 72

    c_left, c_right = st.columns([1.6, 1])
    with c_left:
        st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-label">Power Reserve Evolution (Industrial Shift)</div>', unsafe_allow_html=True)
        fig_line = px.line(trends, x='Year', y='Reserve', markers=True, color_discrete_sequence=["#d4af37"])
        fig_line.update_layout(template="plotly_white", height=400, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c_right:
        st.markdown(f"""
            <div class="atlass-card" style="height:488px;">
                <div class="card-label">AI Strategy Control Tower</div>
                <div class="insight-box">
                    <b>Obsolescence Risk</b><br>
                    {max_yr} Industrial Standard: <b>{mkt_avg_2026:.0f}h</b>.<br>
                    <i>Status: Catalog requires caliber upgrade.</i>
                </div>
                <div style="margin-top:25px; padding-top:20px; border-top:1px solid #E2E8F0;">
                    <div style="color:#64748B; font-size:0.8rem; margin-bottom:10px;">MATERIAL ADOPTION</div>
                    <div style="font-size:1.1rem; font-weight:600; color:#1E293B;">Titanium Grade 5: +18.4%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
