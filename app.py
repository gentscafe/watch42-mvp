import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(page_title="HoroIntel | Auto-Intelligence", layout="wide")

# 2. STILE UI
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
    .watch-price { font-size: 1.2rem; font-weight: 500; color: #d4af37; margin-top: 8px; }
    .category-badge { 
        background-color: #f3f4f6; color: #374151; padding: 2px 8px; 
        border-radius: 4px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    }
    </style>
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
        create_mock_watch("MY BRAND", "Aethelgard I", "MB-01", True),
        create_mock_watch("MY BRAND", "Nebula Chrono", "MB-02", True),
        create_mock_watch("MY BRAND", "Deep Horizon", "MB-03", True),
        create_mock_watch("MY BRAND", "Urban Ghost", "MB-04", True),
        create_mock_watch("MY BRAND", "Vertex GMT", "MB-05", True),
    ]
    
    st.session_state.competitors = [
        create_mock_watch(f"Brand {i}", f"Legacy {10+i}", f"REF-{1000+i}") 
        for i in range(1, 201) # 200 competitor per assicurare massa critica
    ]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.title("HORO INTEL")
    st.write("---")
    view = st.radio("Sezione", ["My Watches", "Pricing Intelligence"])

# 5. VIEW: MY WATCHES
if view == "My Watches":
    st.header("My Brand Portfolio")
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="watch-tile">
                    <span class="category-badge">{watch['Category']}</span>
                    <div class="watch-title" style="margin-top:8px;">{watch['Model']}</div>
                    <div class="watch-price">€ {watch['Price']:,}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Dettagli"):
                st.write(f"Ref: {watch['Ref']}")
                st.write(f"Movimento: {watch['Reserve']}h / {watch['Freq']}vph")

# 6. VIEW: PRICING INTELLIGENCE (Auto-Filtering Logic)
elif view == "Pricing Intelligence":
    st.header("Dynamic Pricing Matrix")
    
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Freq": "vph", "Diameter": "mm"}
    
    col_a, col_b = st.columns(2)
    with col_a:
        # 1. L'utente sceglie il target
        target = st.selectbox("Seleziona Target (MY BRAND)", 
                             st.session_state.my_portfolio, 
                             format_func=lambda x: f"{x['Model']}")
    
    # 2. SISTEMA IMPOSTA AUTOMATICAMENTE LA CATEGORIA
    target_cat = target['Category']
    
    with col_b:
        y_param = st.selectbox("Parametro Tecnico", list(units.keys()))

    # Visualizziamo il filtro automatico (disabilitato per l'utente perché è automatico)
    st.markdown(f"Filtro Mercato Attivo: **Categoria {target_cat}**")

    # LOGICA DI FILTRO
    target_value = target[y_param]
    unit_y = units[y_param]
    df_market = pd.DataFrame(st.session_state.competitors)
    
    # Filtriamo per CATEGORIA e VALORE TECNICO
    df_filtered = df_market[
        (df_market['Category'] == target_cat) & 
        (df_market[y_param] == target_value)
    ].copy()
    
    df_plot = pd.concat([df_filtered, pd.DataFrame([target])])

    

    if not df_filtered.empty:
        fig = px.scatter(
            df_plot, x="Price", y=y_param, color="Type",
            color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
            size=df_plot['Type'].apply(lambda x: 25 if x == "Target" else 15),
            hover_name="Model",
            labels={"Price": "Prezzo (€)", y_param: f"{y_param} ({unit_y})"},
            template="plotly_white", height=500
        )
        fig.update_layout(
            xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
            yaxis=dict(range=[target_value * 0.9, target_value * 1.1], ticksuffix=f" {unit_y}"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiche veloci
        st.metric("Competitor diretti trovati", len(df_filtered), 
                  f"Media Prezzo: € {df_filtered['Price'].mean():,.0f}")
    else:
        st.warning(f"Nessun competitor in categoria '{target_cat}' ha lo stesso valore di {y_param} ({target_value} {unit_y}).")
