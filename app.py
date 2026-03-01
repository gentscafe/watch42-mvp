import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Heritage", layout="wide", initial_sidebar_state="expanded")

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
        background-color: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px;
    }
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

# 3. DATA ENGINE - DEFINIZIONE REALE FEARS
# Forziamo il caricamento ignorando il vecchio session_state se i modelli non sono corretti
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

# Sovrascriviamo sempre il portfolio per garantire che i nomi siano corretti
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
            "Reserve": int(42 + (yr-2019)*5), "Price": random.randint(3000, 25000),
            "Material": random.choices(["Steel", "Titanium Grade 5"], weights=[0.8, 0.2])[0]
        })

# 4. CUSTOM SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'page_view' not in st.session_state: st.session_state.page_view = "Dashboard"
    
    def set_p(n): st.session_state.page_view = n
    
    pages = [("Dashboard", "📊"), ("Pricing Intelligence", "💰"), ("Design Grid", "📐"), ("Market Trends", "📈")]
    for n, icon in pages:
        st.button(f"{icon} {n}", key=f"btn_{n}", use_container_width=True, on_click=set_p, args=(n,))
    st.write("---")
    st.caption("Fears Analytics v5.9")

view = st.session_state.page_view
df_all = pd.DataFrame(st.session_state.competitors)

# --- VIEWS ---
if view == "Dashboard":
    st.markdown("### Fears Collection (20 Models)")
    cols = st.columns(4)
    for i, w in enumerate(st.session_state.my_portfolio):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="atlass-card">
                    <span class="category-badge">{w['Category']}</span>
                    <div style="font-weight:600; margin-top:10px; color:#1E293B; height:45px; overflow:hidden;">{w['Model']}</div>
                    <div class="price-tag">€ {w['Price']:,}</div>
                    <div style="font-size:0.7rem; color:#94A3B8; margin-top:5px;">{w['Diameter']}mm | {w['Year']} Edition</div>
                </div>
            """, unsafe_allow_html=True)

elif view == "Pricing Intelligence":
    # (Resto del codice Pricing... senza errori di Key)
    st.markdown("### Pricing Analysis")
    target = st.selectbox("Select Fears Model", st.session_state.my_portfolio, format_func=lambda x: x['Model'])
    # ... (logica pricing v5.8)
