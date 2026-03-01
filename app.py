import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - ATLAS INSPIRED
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #F4F7FA !important; 
    }
    .stApp { background-color: #F4F7FA; }

    /* Header Fisso */
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 65px;
        background-color: white; display: flex; align-items: center;
        padding: 0 40px; border-bottom: 1px solid #E2E8F0; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.5rem; color: #1a1a1a; letter-spacing: -1px; }
    .logo-accent { color: #d4af37; }

    /* Modern Sidebar */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #E2E8F0 !important;
        padding-top: 20px;
    }
    [data-testid="stSidebarNav"] { padding-top: 80px; }

    /* Modern Cards (Inspired by Atlass) */
    .atlass-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    .card-label { color: #64748B; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-value { color: #1E293B; font-size: 1.8rem; font-weight: 700; margin: 4px 0; }
    
    /* Metrics & Badges */
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.7rem; font-weight: 700;
    }
    .price-tag { color: #d4af37; font-weight: 600; font-size: 1.1rem; }

    /* Spacing adjustment */
    .block-container { padding-top: 6rem !important; padding-right: 3rem !important; padding-left: 3rem !important; }
    [data-testid="stHeader"] { display: none; }
    
    /* Alert Boxes */
    .insight-box {
        background-color: #FEF9C3; border-left: 4px solid #d4af37; padding: 16px; border-radius: 8px;
    }
    </style>
    
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. DATA PERSISTENCE
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    def create_watch(brand, model, ref, is_target=False, year=None):
        cat = random.choice(["Diver", "Dress", "GMT", "Chronograph", "Casual"])
        year = year if year else random.randint(2019, 2026)
        res = int((42 if year <= 2020 else (72 if year >= 2024 else 60)) + random.randint(-5, 8))
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": random.randint(1800, 5500),
            "Category": cat, "Year": int(year), "Diameter": random.choice([39, 40, 41]),
            "Thickness": random.choice([11, 12, 13]), "Reserve": res, "Type": "Target" if is_target else "Market"
        }
    st.session_state.my_portfolio = [create_watch("MY BRAND", f"Watch Alpha {i}", f"A-{i}", True, 2020+i) for i in range(1, 6)]
    st.session_state.competitors = [create_watch(f"Brand {random.randint(1,20)}", f"Model {i}", f"R-{i}") for i in range(1, 1000)]
    st.session_state.initialized = True

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("### Navigation")
    view = st.radio("Reports", ["Dashboard", "Price Intelligence", "Design Grid", "Market Trends"], label_visibility="collapsed")
    st.write("---")
    st.caption("Intelligence SaaS v5.0")

# --- VIEWS ---

if view == "Dashboard":
    st.markdown("### Analytics Overview")
    cols = st.columns(5)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="atlass-card">
                    <span class="category-badge">{w['Category']}</span>
                    <div style="font-weight:600; margin-top:12px; color:#1E293B;">{w['Model']}</div>
                    <div class="price-tag">€ {w['Price']:,}</div>
                    <div style="font-size:0.75rem; color:#94A3B8; margin-top:4px;">Year: {w['Year']}</div>
                </div>
            """, unsafe_allow_html=True)

elif view == "Price Intelligence":
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1: st.markdown("### Pricing Intelligence")
    with col_t2: target = st.selectbox("Target Watch", st.session_state.my_portfolio, format_func=lambda x: f"{x['Model']} ({x['Year']})")
    
    df_m = pd.DataFrame(st.session_state.competitors)
    df_f = df_m[(df_m['Category'] == target['Category']) & (df_m['Year'].between(target['Year']-1, target['Year']+1))]
    
    avg_p = df_f['Price'].mean()
    diff = ((target['Price'] - avg_p) / avg_p) * 100
    
    # Atlass-style Metrics
    m1, m2, m3, m4 = st.columns(4)
    for m, label, val, delta in zip([m1, m2, m3, m4], 
                                   ["Category", "Competitors", "Market Average", "Price Gap"],
                                   [target['Category'], len(df_f), f"€ {avg_p:,.0f}", f"€ {target['Price']:,}"],
                                   [None, None, None, f"{diff:+.1f}%"]):
        with m:
            delta_html = f'<div style="color:{"#10B981" if diff < 0 else "#EF4444"}; font-size:0.85rem; font-weight:600;">{delta} vs avg</div>' if delta else ""
            st.markdown(f"""
                <div class="atlass-card">
                    <div class="card-label">{label}</div>
                    <div class="card-value">{val}</div>
                    {delta_html}
                </div>
            """, unsafe_allow_html=True)

    fig = px.scatter(df_f, x="Price", y="Reserve", color_discrete_sequence=["#CBD5E0"], opacity=0.5)
    fig.add_trace(go.Scatter(x=[target['Price']], y=[target['Reserve']], mode='markers', 
                             marker=dict(color='#d4af37', size=15, line=dict(width=2, color='white')), name="Target"))
    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=20, b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif view == "Market Trends":
    st.markdown("### Market Intelligence Evolution")
    df_all = pd.DataFrame(st.session_state.competitors)
    trends = df_all.groupby('Year')['Reserve'].mean().reset_index()
    
    c_left, c_right = st.columns([1.6, 1])
    with c_left:
        fig_l = px.line(trends, x='Year', y='Reserve', markers=True, color_discrete_sequence=["#d4af37"])
        fig_l.update_layout(template="plotly_white", height=450)
        st.plotly_chart(fig_l, use_container_width=True)
    
    with c_right:
        st.markdown(f"""
            <div class="atlass-card" style="height:450px;">
                <div class="card-label">AI Strategic Insights</div>
                <div style="margin-top:20px;">
                    <div class="insight-box">
                        <b>Obsolescence Alert</b><br>
                        Industrial standard for 2026 is moving to <b>72h</b>. Your current average is 22% below the curve.
                    </div>
                    <br>
                    <div style="padding:10px; color:#475569; font-size:0.9rem;">
                        • <b>Titanium Shift</b>: Adoption +14%<br>
                        • <b>Price Index</b>: Luxury segment +5.2%<br>
                        • <b>R&D Suggestion</b>: Caliber update priority High.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
