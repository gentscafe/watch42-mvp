import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="HoroIntel | Competitive Intelligence", layout="wide")

# 2. STILE UI (Executive White)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #fcfcfc; }
    .watch-tile {
        background-color: white; padding: 20px; border-radius: 10px;
        border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        margin-bottom: 10px;
    }
    .watch-title { font-size: 1.1rem; font-weight: 600; color: #111; }
    .watch-ref { font-size: 0.8rem; color: #888; font-family: monospace; }
    .watch-price { font-size: 1.2rem; font-weight: 500; color: #d4af37; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. GENERAZIONE DATI STATICI (Sempre uguali)
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False):
        cat = random.choice(["Diver", "Dress", "GMT", "Chronograph"])
        price = random.randint(1200, 3500) if is_target else random.randint(800, 4500)
        # Rendiamo i valori tecnici più "standard" per favorire i match nel benchmarking
        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Material": "Steel", "Diameter": random.choice([39.0, 40.0, 41.0]),
            "Thickness": random.choice([10.5, 12.0, 13.5, 14.5]),
            "WR": random.choice([100, 200, 300]), "Reserve": random.choice([42, 70, 80]),
            "Freq": random.choice([21600, 28800]), "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [
        create_mock_watch("MY BRAND", "Aethelgard I", "MB-01", True),
        create_mock_watch("MY BRAND", "Nebula Chrono", "MB-02", True),
        create_mock_watch("MY BRAND", "Deep Horizon", "MB-03", True),
        create_mock_watch("MY BRAND", "Urban Ghost", "MB-04", True),
        create_mock_watch("MY BRAND", "Vertex GMT", "MB-05", True),
    ]
    
    st.session_state.competitors = [
        create_mock_watch(f"Brand {i}", f"Legacy {10+i}", f"REF-{1000+i}") 
        for i in range(1, 101) # Aumentati a 100 per avere più probabilità di match
    ]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.title("HORO INTEL")
    st.write("---")
    view = st.radio("Sezione", ["My Watches", "Pricing Intelligence"])
    st.write("---")
    st.caption("v1.1 Stable")

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
                    <div class="watch-price">€ {watch['Price']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Edit Specs"):
                st.text_input("Model Name", watch['Model'], key=f"m_{i}")
                st.number_input("Price (€)", value=float(watch['Price']), key=f"p_{i}")
                st.number_input("Thickness (mm)", value=float(watch['Thickness']), key=f"t_{i}")
                st.number_input("Reserve (h)", value=int(watch['Reserve']), key=f"r_{i}")
                st.info("Visual only mode")

# 6. VIEW: PRICING INTELLIGENCE (Vertical Benchmarking)
elif view == "Pricing Intelligence":
    st.header("Dynamic Pricing Matrix")
    
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Freq": "vph", "Diameter": "mm"}
    
    col_a, col_b = st.columns(2)
    with col_a:
        target = st.selectbox("Seleziona Target (MY BRAND)", 
                             st.session_state.my_portfolio, 
                             format_func=lambda x: f"{x['Model']}")
    with col_b:
        y_param = st.selectbox("Parametro Tecnico di Confronto", list(units.keys()))

    # Logica di Filtro
    target_value = target[y_param]
    unit_y = units[y_param]
    df_market_all = pd.DataFrame(st.session_state.competitors)
    
    # Filtro competitor con stesso valore
    df_filtered_market = df_market_all[df_market_all[y_param] == target_value].copy()
    df_plot = pd.concat([df_filtered_market, pd.DataFrame([target])])

    st.subheader(f"Confronto Prezzi per {y_param}: {target_value} {unit_y}")
    
    if not df_filtered_market.empty:
        fig = px.scatter(
            df_plot, x="Price", y=y_param, color="Type",
            color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
            size=df_plot['Type'].apply(lambda x: 25 if x == "Target" else 15),
            hover_name="Model",
            labels={"Price": "Prezzo (€)", y_param: f"{y_param} ({unit_y})"},
            template="plotly_white", height=450
        )

        fig.update_layout(
            xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
            yaxis=dict(range=[target_value * 0.8, target_value * 1.2], ticksuffix=f" {unit_y}"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight
        avg_p = df_filtered_market['Price'].mean()
        diff = target['Price'] - avg_p
        st.success(f"**Market Insight:** La media di mercato per questa specifica è **€ {avg_p:,.0f}**. Il tuo prezzo è {'sopra' if diff > 0 else 'sotto'} di **€ {abs(diff):,.0f}**.")
    else:
        st.warning(f"Nessun competitor trovato con {target_value} {unit_y}. Prova un altro parametro.")
