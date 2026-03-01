import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Collection", layout="wide", initial_sidebar_state="expanded")

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

    /* Card Design con Placeholder Uniforme */
    .watch-card {
        background-color: white; border-radius: 16px; border: 1px solid #E2E8F0;
        overflow: hidden; transition: transform 0.2s; margin-bottom: 25px;
    }
    .watch-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    
    .image-container {
        width: 100%; height: 180px; background-color: #fcfcfc;
        display: flex; align-items: center; justify-content: center;
        border-bottom: 1px solid #F1F5F9;
    }
    .image-container img { max-width: 80%; max-height: 140px; opacity: 0.8; }

    .card-content { padding: 16px; }
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    }
    .watch-title { font-weight: 600; color: #1E293B; margin: 10px 0 5px 0; font-size: 0.9rem; height: 38px; overflow: hidden; }
    .watch-price { color: #d4af37; font-weight: 700; font-size: 1.1rem; }
    .watch-specs { font-size: 0.7rem; color: #94A3B8; margin-top: 8px; border-top: 1px solid #F1F5F9; padding-top: 8px; }

    .block-container { padding-top: 6rem !important; }
    [data-testid="stHeader"] { display: none; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE - 20 MODELLI FEARS REALI
# Utilizziamo lo stesso placeholder per tutti i modelli
PLACEHOLDER_URL = "https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?q=80&w=300&auto=format&fit=crop"

fears_catalog = [
    {"Model": "Brunswick 38 Copper", "Cat": "Casual", "Price": 4150, "Spec": "38mm | Cal. 7001 Hand-wound"},
    {"Model": "Brunswick 40 Silver", "Cat": "Casual", "Price": 4450, "Spec": "40mm | La Joux-Perret Auto"},
    {"Model": "Archival 1930 Small Seconds", "Cat": "Dress", "Price": 4200, "Spec": "22mm | NOS Zenith Calibre"},
    {"Model": "Brunswick PT Platinum", "Cat": "Luxury", "Price": 33000, "Spec": "38mm | Platinum 950 Case"},
    {"Model": "Fears Garrick", "Cat": "High-End", "Price": 19500, "Spec": "42mm | Garrick UT-G04"},
    {"Model": "Brunswick 40 Aurora", "Cat": "Casual", "Price": 4600, "Spec": "40mm | MOP Dial"},
    {"Model": "Brunswick 38 White Rose", "Cat": "Casual", "Price": 4150, "Spec": "38mm | Pure White Dial"},
    {"Model": "Brunswick 40 Mallard Green", "Cat": "Casual", "Price": 4450, "Spec": "40mm | British Racing Green"},
    {"Model": "Brunswick 38 Blue Danubian", "Cat": "Casual", "Price": 4150, "Spec": "38mm | Sunray Blue"},
    {"Model": "Archival 1930 Topper Edition", "Cat": "Dress", "Price": 4500, "Spec": "22mm | Limited Edition"},
    {"Model": "Brunswick 38 Champagne", "Cat": "Casual", "Price": 3950, "Spec": "38mm | Hand-wound Heritage"},
    {"Model": "Brunswick 38 Midas Gold", "Cat": "Luxury", "Price": 15500, "Spec": "38mm | 18ct Yellow Gold"},
    {"Model": "Brunswick 38 Jubilee Edition", "Cat": "Casual", "Price": 4300, "Spec": "38mm | Royal Purple Dial"},
    {"Model": "Archival 1930 Boutique", "Cat": "Dress", "Price": 4200, "Spec": "22mm | Boutique Exclusive"},
    {"Model": "Brunswick 40 Blue", "Cat": "Casual", "Price": 4450, "Spec": "40mm | Automatic Sport-Chic"},
    {"Model": "Brunswick 38 Salmon", "Cat": "Casual", "Price": 3850, "Spec": "38mm | Vertical Brushed Salmon"},
    {"Model": "Brunswick 40 Black", "Cat": "Casual", "Price": 4450, "Spec": "40mm | Onyx Black Gloss"},
    {"Model": "Brunswick 38 Silver", "Cat": "Casual", "Price": 3950, "Spec": "38mm | Classic Heritage"},
    {"Model": "Brunswick 40 Topper Edition", "Cat": "Casual", "Price": 4700, "Spec": "40mm | Lumicast® Numerals"},
    {"Model": "Brunswick 40 Pinkish Salmon", "Cat": "Casual", "Price": 4450, "Spec": "40mm | Edition 2024"}
]

# 4. SIDEBAR
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'v' not in st.session_state: st.session_state.v = "Dashboard"
    def set_v(n): st.session_state.v = n
    pages = [("Dashboard", "📊"), ("Pricing", "💰"), ("Market", "📈")]
    for n, icon in pages:
        st.button(f"{icon} {n}", key=f"n_{n}", use_container_width=True, on_click=set_v, args=(n,))
    st.write("---")
    st.caption("Fears Analytics v6.1")

# 5. DASHBOARD VIEW
if st.session_state.v == "Dashboard":
    st.markdown("### Fears Collection Overview")
    cols = st.columns(4)
    for i, w in enumerate(fears_catalog):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="watch-card">
                    <div class="image-container">
                        <img src="{PLACEHOLDER_URL}" alt="Fears Watch">
                    </div>
                    <div class="card-content">
                        <span class="category-badge">{w['Cat']}</span>
                        <div class="watch-title">{w['Model']}</div>
                        <div class="watch-price">€ {w['Price']:,}</div>
                        <div class="watch-specs">{w['Spec']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
