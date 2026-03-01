import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="HoroIntel | Stable Prototype", layout="wide")

# 2. STILE UI (Executive White)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .watch-tile {
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .watch-title { font-size: 1.1rem; font-weight: 600; color: #111; }
    .watch-price { font-size: 1.2rem; font-weight: 500; color: #d4af37; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. GENERAZIONE DATI STATICI (Bloccata con Seed)
# Usiamo un seed fisso così i dati "casuali" sono in realtà sempre gli stessi ad ogni avvio
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False):
        cat = random.choice(["Diver", "Dress", "GMT", "Chronograph"])
        price = random.randint(1200, 3500) if is_target else random.randint(800, 4500)
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Material": "Steel", "Diameter": random.choice([39.0, 40.0, 41.0]),
            "Thickness": round(random.uniform(10.5, 14.5), 1),
            "WR": random.choice([100, 200, 300]), "Reserve": random.choice([42, 70, 80]),
            "Freq": random.choice([21600, 28800]), "Type": "Target" if is_target else "Market"
        }

    # Creazione una tantum dei 5 modelli MY BRAND
    st.session_state.my_portfolio = [
        create_mock_watch("MY BRAND", "Aethelgard I", "MB-01", True),
        create_mock_watch("MY BRAND", "Nebula Chrono", "MB-02", True),
        create_mock_watch("MY BRAND", "Deep Horizon", "MB-03", True),
        create_mock_watch("MY BRAND", "Urban Ghost", "MB-04", True),
        create_mock_watch("MY BRAND", "Vertex GMT", "MB-05", True),
    ]
    
    # Creazione una tantum dei 25 Competitor
    st.session_state.competitors = [
        create_mock_watch(f"Brand {i}", f"Legacy {10+i}", f"REF-{1000+i}") 
        for i in range(1, 26)
    ]
    st.session_state.initialized = True

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("HORO INTEL")
    view = st.radio("Sezione", ["My Watches", "Pricing Intelligence"])

# 5. VIEW: MY WATCHES
if view == "My Watches":
    st.header("My Brand Portfolio")
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="watch-tile">
                    <div class="watch-title">{watch['Model']}</div>
                    <div class="watch-ref">{watch['Ref']}</div>
                    <div class="watch-price">€{watch['Price']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Specs"):
                # Campi editabili (non salvano nel db per ora)
                st.text_input("Model Name", watch['Model'], key=f"m_{i}")
                st.number_input("Price (€)", value=watch['Price'], key=f"p_{i}")
                st.number_input("Thickness (mm)", value=watch['Thickness'], key=f"t_{i}")
                st.number_input("Reserve (h)", value=watch['Reserve'], key=f"r_{i}")
                st.info("Visual Only: changes won't persist.")

# 6. VIEW: PRICING INTELLIGENCE
elif view == "Pricing Intelligence":
    st.header("Dynamic Pricing Matrix")
    
    col_a, col_b = st.columns(2)
    with col_a:
        target = st.selectbox("Seleziona Target", st.session_state.my_portfolio, format_func=lambda x: x['Model'])
    with col_b:
        y_param = st.selectbox("Parametro Y", ["Reserve", "Thickness", "WR", "Diameter"])

    # Merge dei dati per il grafico
    df_all = pd.concat([pd.DataFrame(st.session_state.competitors), pd.DataFrame([target])])

    fig = px.scatter(
        df_all, x="Price", y=y_param, color="Type",
        color_discrete_map={"Market": "#E2E8F0", "Target": "#D4AF37"},
        size=df_all['Type'].apply(lambda x: 18 if x == "Target" else 9),
        hover_name="Model", template="plotly_white", height=600
    )
    st.plotly_chart(fig, use_container_width=True)
