import streamlit as st
import pandas as pd
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Fears Visual", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE - TOTAL ATLAS DESIGN (v6.0)
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
    
    /* Sidebar Buttons */
    .stButton > button {
        border: none !important; background-color: transparent !important; color: #64748B !important;
        text-align: left !important; padding: 12px 20px !important; font-weight: 500 !important;
        border-radius: 12px !important; transition: all 0.2s !important;
    }
    .stButton > button:hover { background-color: #F8FAFC !important; color: #1E293B !important; }

    /* Visual Card Design */
    .watch-card {
        background-color: white; border-radius: 16px; border: 1px solid #E2E8F0;
        overflow: hidden; transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 25px;
    }
    .watch-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px -10px rgba(0,0,0,0.1); }
    
    .image-container {
        width: 100%; height: 200px; background-color: #F8FAFC;
        display: flex; align-items: center; justify-content: center;
        border-bottom: 1px solid #F1F5F9;
    }
    .image-container img { max-width: 100%; max-height: 180px; object-fit: contain; }

    .card-content { padding: 18px; }
    .category-badge { 
        background-color: #F1F5F9; color: #475569; padding: 4px 10px; 
        border-radius: 6px; font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
    }
    .watch-title { font-weight: 600; color: #1E293B; margin: 10px 0 5px 0; font-size: 0.95rem; height: 40px; overflow: hidden; }
    .watch-price { color: #d4af37; font-weight: 700; font-size: 1.1rem; }
    .watch-specs { font-size: 0.75rem; color: #94A3B8; margin-top: 8px; border-top: 1px solid #F1F5F9; padding-top: 8px; }

    .block-container { padding-top: 6rem !important; }
    [data-testid="stHeader"] { display: none; }
    </style>
    <div class="global-header"><div class="logo-text">watch<span class="logo-accent">42</span></div></div>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE CON IMMAGINI
# Nota: Sostituisci gli URL 'https://via.placeholder.com/...' con i link reali delle immagini Fears
fears_catalog = [
    {"Model": "Brunswick 38 Copper", "Cat": "Casual", "Price": 4150, "Img": "https://via.placeholder.com/300x200?text=Brunswick+38+Copper", "Spec": "38mm | Hand-wound"},
    {"Model": "Brunswick 40 Silver", "Cat": "Casual", "Price": 4450, "Img": "https://via.placeholder.com/300x200?text=Brunswick+40+Silver", "Spec": "40mm | Automatic"},
    {"Model": "Archival 1930 Small Seconds", "Cat": "Dress", "Price": 4200, "Img": "https://via.placeholder.com/300x200?text=Archival+1930", "Spec": "22mm | Vintage Calibre"},
    {"Model": "Brunswick PT Platinum", "Cat": "Luxury", "Price": 33000, "Img": "https://via.placeholder.com/300x200?text=Brunswick+Platinum", "Spec": "38mm | Platinum Case"},
    {"Model": "Fears Garrick", "Cat": "High-End", "Price": 19500, "Img": "https://via.placeholder.com/300x200?text=Fears+Garrick", "Spec": "42mm | Free-sprung Balance"},
    {"Model": "Brunswick 40 Aurora", "Cat": "Casual", "Price": 4600, "Img": "https://via.placeholder.com/300x200?text=Aurora+Edition", "Spec": "40mm | Mother of Pearl Dial"},
    {"Model": "Brunswick 38 White Rose", "Cat": "Casual", "Price": 4150, "Img": "https://via.placeholder.com/300x200?text=White+Rose", "Spec": "38mm | Enamel Dial"},
    {"Model": "Brunswick 40 Mallard Green", "Cat": "Casual", "Price": 4450, "Img": "https://via.placeholder.com/300x200?text=Mallard+Green", "Spec": "40mm | Automatic"},
    # ... aggiungi gli altri 12 seguendo questo schema
]

# Popolamento automatico per i restanti per arrivare a 20 (placeholder)
while len(fears_catalog) < 20:
    fears_catalog.append({"Model": f"Fears Edition {len(fears_catalog)+1}", "Cat": "Heritage", "Price": 4000, "Img": "https://via.placeholder.com/300x200?text=Fears+Heritage", "Spec": "Limited Edition"})

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if 'v' not in st.session_state: st.session_state.v = "Dashboard"
    def set_v(n): st.session_state.v = n
    pages = [("Dashboard", "📊"), ("Pricing", "💰"), ("Market", "📈")]
    for n, icon in pages:
        st.button(f"{icon} {n}", key=f"n_{n}", use_container_width=True, on_click=set_v, args=(n,))
    st.write("---")
    st.caption("Fears Visual Suite v6.0")

# 5. DASHBOARD VIEW
if st.session_state.v == "Dashboard":
    st.markdown("### Fears Visual Collection")
    
    # Grid Layout a 4 colonne
    cols = st.columns(4)
    for i, w in enumerate(fears_catalog):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="watch-card">
                    <div class="image-container">
                        <img src="{w['Img']}" alt="{w['Model']}">
                    </div>
                    <div class="card-content">
                        <span class="category-badge">{w['Cat']}</span>
                        <div class="watch-title">{w['Model']}</div>
                        <div class="watch-price">€ {w['Price']:,}</div>
                        <div class="watch-specs">{w['Spec']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
