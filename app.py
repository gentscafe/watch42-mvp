import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - ATLAS ENTERPRISE (v5.3 Cleaned)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #F4F7FA !important; 
    }
    .stApp { background-color: #F4F7FA; }

    /* Fixed Header */
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background-color: white; display: flex; align-items: center;
        padding: 0 40px; border-bottom: 1px solid #E2E8F0; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.5rem; color: #1a1a1a; letter-spacing: -1px; }
    .logo-accent { color: #d4af37; }

    /* Modern Sidebar */
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0 !important; }

    /* Atlass Cards */
    .atlass-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .card-label { color: #64748B; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-value { color: #1E293B; font-size: 1.8rem; font-weight: 700; margin: 4px 0; }
    
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    }
    .price-tag { color: #d4af37; font-weight: 600; font-size: 1.1rem; }

    /* Layout Spacing */
    .block-container { padding-top: 6rem !important; padding-right: 3rem !important; padding-left: 3rem !important; }
    [data-testid="stHeader"] { display: none; }
    
    /* Insight Alert */
    .insight-box {
        background-color: #FEF9C3; border-left: 4px solid #d4af37; padding: 16px; border-radius: 8px; margin-top: 10px;
    }
    </style>
    
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE
if 'initialized' not in st.session_state:
    random.seed(42)
    def create_watch(brand, model, is_target=False, year=None):
        cat = random.choice(["Diver", "Dress", "GMT", "Chronograph", "Casual"])
        yr = int(year if year else random.randint(2019, 2026))
        res = int((42 if yr <= 2020 else (72 if yr >= 2024 else 60)) + random.randint(-5, 8))
        if cat == "Diver": d, t = random.choice([41, 42, 43]), random.choice([13, 14, 15])
        elif cat == "Dress": d, t = random.choice([36, 38, 39]), random.choice([8, 9, 10])
        else: d, t = random.choice([39, 40, 41]), random.choice([11, 12, 13])
        return {
            "Brand": brand, "Model": model, "Category": cat, "Year": yr,
            "Diameter": d, "Thickness": t, "Reserve": res,
            "Price": int(random.randint(1800, 5500)), "Type": "Target" if is_target else "Market",
            "Material": random.choices(["Steel", "Titanium Grade 5"], weights=[0.8, 0.2])[0]
        }
    st.session_state.my_portfolio = [create_watch("MY BRAND", f"Watch Alpha {i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_watch(f"Brand {random.randint(1,25)}", f"Comp {i}") for i in range(1, 1500)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.markdown("### Navigation")
    view = st.radio("Reports", ["Dashboard", "Pricing Intelligence", "Design Grid", "Market Trends"], label_visibility="collapsed")
    st.write("---")
    st.caption("Intelligence SaaS v5.3")

df_all = pd.DataFrame(st.session_state.competitors)

# --- VIEWS ---

if view == "Dashboard":
    st.markdown("### Portfolio Overview")
    cols = st.columns(5)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f'<div class="atlass-card"><span class="category-badge">{w["Category"]}</span><div style="font-weight:600; margin-top:12px; color:#1E293B;">{w["Model"]}</div><div class="price-tag">€ {w["Price"]:,}</div><div style="font-size:0.75rem; color:#94A3B8; margin-top:4px;">Year: {w['Year']}</div></div>', unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1: st.markdown("### Pricing Intelligence")
    with col_t2: target = st.selectbox("Target Watch", st.session_state.my_portfolio, format_func=lambda x: f"{x['Model']} ({x['Year']})")
    
    df_f = df_all[(df_all['Category'] == target['Category']) & (df_all['Year'].between(target['Year']-1, target['Year']+1))]
    avg_p = df_f['Price'].mean() if not df_f.empty else 0
    diff = ((target['Price'] - avg_p) / avg_p) * 100 if avg_p > 0 else 0
    
    m1, m2, m3, m4 = st.columns(4)
    for m, (label, val, delta) in zip([m1, m2, m3, m4], [("Category", target['Category'], None), ("Competitors", len(df_f), None), ("Market Average", f"€ {avg_p:,.0f}", None), ("Price Gap", f"€ {target['Price']:,}", f"{diff:+.1f}%")]):
        with m:
            delta_html = f'<div style="color:{"#10B981" if diff < 0 else "#EF4444"}; font-size:0.85rem; font-weight:600;">{delta} vs avg</div>' if delta else ""
            st.markdown(f'<div class="atlass-card"><div class="card-label">{label}</div><div class="card-value">{val}</div>{delta_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="atlass-card">', unsafe_allow_html=True)
    fig_p = px.scatter(df_f, x="Price", y="Reserve", color_discrete_sequence=["#CBD5E0"], opacity=0.4)
    fig_p.add_trace(go.Scatter(x=[target['Price']], y=[target['Reserve']], mode='markers', marker=dict(color='#d4af37', size=15, line=dict(width=2, color='white'))))
    fig_p.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=20, b=0), height=400, showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif view == "Design Grid":
    st.markdown("### Design Intelligence Matrix")
    c1, c2 = st.columns([1, 2])
    with c1: sel_cat = st.selectbox("Category", ["All Categories"] + list(df_all['Category'].unique()))
    with c2: years = st.slider("Production Period", 2019, 2026, (2020, 2024))

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
        st.markdown(f'<div class="atlass-card" style="height:495px;"><div class="card-label">Strategic Insights</div><div class="card-value">{len(df_f_design)} Models</div><hr style="border:0; border-top:1px solid #E2E8F0; margin:20px 0;"><div style="font-size:0.9rem; color:#475569;"><b>White Space Detected:</b><br>Low competition in dimensions favored by collectors for the {sel_cat} segment.</div></div>', unsafe_allow_html=True)

# --- VIEW 4: MARKET TRENDS (BARRA BIANCA RIMOSSA) ---
elif view == "Market Trends":
    st.markdown("### Market Intelligence & Trends")
    
    # Filtro posizionato direttamente senza contenitori Markdown vuoti sotto
    trend_cat = st.selectbox("Market Segment", ["All Categories"] + list(df_all['Category'].unique()))
    
    df_t = df_all.copy() if trend_cat == "All Categories" else df_all[df_all['Category'] == trend_cat]
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
                    <div style="color:#10B981; font-size:0.8rem;">Accelerating trend in recent launches</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
