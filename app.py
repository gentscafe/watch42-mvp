import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="watch42 | Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. STILE UI (CSS Custom per Header Globale e Riduzione Spazi)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Header Fisso */
    .global-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background-color: white;
        display: flex;
        align-items: center;
        padding: 0 20px;
        border-bottom: 1px solid #eee;
        z-index: 999999;
    }
    
    .logo-text {
        font-weight: 700;
        font-size: 1.4rem;
        color: #1a1a1a;
        letter-spacing: -0.5px;
    }
    .logo-accent { color: #d4af37; }

    /* RIMOZIONE SPAZI BIANCHI STREAMLIT */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }

    /* Cards UI */
    .watch-tile {
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        margin-bottom: 10px; min-height: 180px;
    }
    .watch-title { font-size: 1.05rem; font-weight: 600; color: #111; margin-top: 10px; }
    .watch-price { font-size: 1.15rem; font-weight: 500; color: #d4af37; margin-top: 5px; }
    .category-badge { 
        background-color: #f3f4f6; color: #374151; padding: 2px 8px; 
        border-radius: 4px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    }
    </style>
    
    <div class="global-header">
        <div class="logo-text">watch<span class="logo-accent">42</span></div>
    </div>
    """, unsafe_allow_html=True)

# 3. GENERAZIONE DATI STATICI
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        price = random.randint(1200, 3500) if is_target else random.randint(800, 4500)
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Material": "Steel", "Diameter": random.choice([38.0, 39.0, 40.0, 41.0, 42.0]),
            "Thickness": random.choice([10.5, 12.0, 13.5, 14.5]),
            "WR": random.choice([50, 100, 200, 300]), 
            "Reserve": random.choice([42, 70, 80]),
            "Freq": random.choice([21600, 28800]), 
            "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [
        create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True)
        for i in range(1, 6)
    ]
    
    st.session_state.competitors = [
        create_mock_watch(f"Brand {random.randint(1,20)}", f"Competitor Model {i}", f"REF-{1000+i}") 
        for i in range(1, 251)
    ]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigazione")
    view = st.radio("Sezioni", ["My Watches", "Pricing Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v1.9")

# 5. VIEW: MY WATCHES
if view == "My Watches":
    st.header("My Brand Portfolio")
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="watch-tile">
                    <span class="category-badge">{watch['Category']}</span>
                    <div class="watch-title">{watch['Model']}</div>
                    <div class="watch-price">€ {watch['Price']:,}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Specifiche"):
                st.write(f"**Ref:** {watch['Ref']}")
                st.write(f"**Riserva:** {watch['Reserve']}h")

# 6. VIEW: PRICING INTELLIGENCE (Compact Mode)
elif view == "Pricing Intelligence":
    # Rimosso il titolo h1 per guadagnare spazio
    
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Freq": "vph", "Diameter": "mm"}
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        target = st.selectbox("Seleziona Target", st.session_state.my_portfolio, format_func=lambda x: x['Model'])
    with col_f2:
        y_param = st.selectbox("Parametro Tecnico", list(units.keys()))

    target_cat = target['Category']
    target_value = target[y_param]
    unit_y = units[y_param]
    df_market = pd.DataFrame(st.session_state.competitors)
    
    df_filtered = df_market[
        (df_market['Category'] == target_cat) & 
        (df_market[y_param] == target_value)
    ].copy()

    if not df_filtered.empty:
        avg_p = df_filtered['Price'].mean()
        diff_pct = ((target['Price'] - avg_p) / avg_p) * 100
        
        # KPI Section
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Categoria", target_cat)
        k2.metric("Competitor", len(df_filtered))
        k3.metric("Media Mercato", f"€ {avg_p:,.0f}")
        k4.metric(label="Il Tuo Prezzo", value=f"€ {target['Price']:,}", 
                  delta=f"{diff_pct:+.1f}% vs media", delta_color="inverse")
        
        st.write("---")

        df_plot = pd.concat([df_filtered, pd.DataFrame([target])])
        fig = px.scatter(
            df_plot, x="Price", y=y_param, color="Type",
            color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
            size=df_plot['Type'].apply(lambda x: 25 if x == "Target" else 15),
            hover_name="Model",
            labels={"Price": "Prezzo (€)", y_param: f"{y_param} ({unit_y})"},
            template="plotly_white", height=500
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0), # Ridotto margine del grafico
            xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
            yaxis=dict(range=[target_value * 0.8, target_value * 1.2], ticksuffix=f" {unit_y}"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Nessun competitor trovato in categoria '{target_cat}' con {target_value} {unit_y}.")
