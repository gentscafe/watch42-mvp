import streamlit as st
import pandas as pd

# Tentativo di importare Plotly per il grafico
try:
    import plotly.express as px
except ImportError:
    px = None

# --- 1. CONFIGURAZIONE E DATI STATICI ---
st.set_page_config(page_title="watch42 | Dashboard", layout="wide")

USER_BRAND = "MY BRAND"

# Dati dei tuoi 10 orologi
MY_WATCHES = [
    {"ref": "MY-001", "name": "Vision Alpha", "price": 4500, "reserve": 72, "thick": 12.1, "mat": "Steel"},
    {"ref": "MY-002", "name": "Vision Beta", "price": 10500, "reserve": 48, "thick": 10.5, "mat": "Gold"},
    {"ref": "MY-003", "name": "Oceanic 300", "price": 3200, "reserve": 80, "thick": 13.8, "mat": "Steel"},
    {"ref": "MY-004", "name": "Aero GMT", "price": 6800, "reserve": 72, "thick": 11.2, "mat": "Titanium"},
    {"ref": "MY-005", "name": "Slim Master", "price": 15000, "reserve": 42, "thick": 7.9, "mat": "Platinum"},
    {"ref": "MY-006", "name": "Chronos S", "price": 8900, "reserve": 60, "thick": 14.2, "mat": "Steel"},
    {"ref": "MY-007", "name": "Night Walker", "price": 5400, "reserve": 48, "thick": 12.0, "mat": "Ceramic"},
    {"ref": "MY-008", "name": "Heritage 1950", "price": 4100, "reserve": 38, "thick": 11.5, "mat": "Steel"},
    {"ref": "MY-009", "name": "Grand Complication", "price": 45000, "reserve": 72, "thick": 13.0, "mat": "Gold"},
    {"ref": "MY-010", "name": "Urban Daily", "price": 2400, "reserve": 42, "thick": 10.8, "mat": "Steel"},
]

# Dati di mercato per il grafico
MARKET_LIST = []
for w in MY_WATCHES:
    MARKET_LIST.append({"brand": USER_BRAND, "model": w["name"], "price": w["price"], "reserve": w["reserve"], "thick": w["thick"], "status": "Il Tuo Brand"})

# Aggiungiamo competitor realistici
MARKET_LIST += [
    {"brand": "Rolex", "model": "Submariner", "price": 12500, "reserve": 70, "thick": 13.0, "status": "Competitor"},
    {"brand": "Omega", "model": "Speedmaster", "price": 7200, "reserve": 50, "thick": 13.5, "status": "Competitor"},
    {"brand": "Patek Philippe", "model": "Nautilus", "price": 65000, "reserve": 45, "thick": 8.3, "status": "Competitor"},
    {"brand": "Tudor", "model": "Black Bay", "price": 4100, "reserve": 70, "thick": 14.8, "status": "Competitor"},
    {"brand": "Cartier", "model": "Santos", "price": 7800, "reserve": 42, "thick": 9.4, "status": "Competitor"},
    {"brand": "IWC", "model": "Portugieser", "price": 8500, "reserve": 60, "thick": 12.5, "status": "Competitor"},
]
# Generiamo 50 orologi "Indie" per densità nel grafico
for i in range(50):
    MARKET_LIST.append({
        "brand": f"Indie Lab {i}", "model": f"Model {i}", 
        "price": 2000 + (i*1000), "reserve": 40 + (i%40), "thick": 8 + (i%7),
        "status": "Mercato"
    })

df_market = pd.DataFrame(MARKET_LIST)

# --- 2. SIDEBAR ---
st.sidebar.title("watch42")
st.sidebar.markdown("---")
nav = st.sidebar.radio("NAVIGAZIONE", ["⌚ My Watches", "📊 Pricing Matrix", "🗄️ Explorer"])

# --- 3. SEZIONE: MY WATCHES ---
if nav == "⌚ My Watches":
    st.header("Il Tuo Portfolio")
    st.write("Visualizzazione dei modelli attualmente in produzione.")
    
    cols = st.columns(3)
    for i, watch in enumerate(MY_WATCHES):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(watch['name'])
                st.caption(f"Ref: {watch['ref']} | {watch['mat']}")
                
                c1, c2 = st.columns(2)
                c1.metric("Prezzo", f"€{watch['price']:,}")
                c2.metric("Spessore", f"{watch['thick']}mm")
                
                st.write(f"⚙️ Riserva di Carica: **{watch['reserve']}h**")
                st.button("Vedi Dettagli", key=f"btn_{watch['ref']}", use_container_width=True)

# --- 4. SEZIONE: PRICING MATRIX ---
elif nav == "📊 Pricing Matrix":
    st.header("Analisi Posizionamento di Mercato")
    
    if px:
        # Filtri sopra il grafico
        f1, f2 = st.columns(2)
        y_choice = f1.selectbox("Parametro Tecnico (Asse Y)", ["reserve", "thick"], format_func=lambda x: "Riserva (h)" if x=="reserve" else "Spessore (mm)")
        target_watch = f2.selectbox("Evidenzia Modello", [w['name'] for w in MY_WATCHES])
        
        # Plot
        fig = px.scatter(
            df_market, x="price", y=y_choice, color="status",
            hover_name="brand", hover_data=["model"],
            color_discrete_map={"Il Tuo Brand": "#2E5BFF", "Competitor": "#EF4444", "Mercato": "#D1D5DB"},
            labels={"price": "Prezzo (€)", "reserve": "Riserva (h)", "thick": "Spessore (mm)"},
            height=600, template="plotly_white"
        )
        fig.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=1, color='White')))
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Libreria Plotly non trovata. Carica il file requirements.txt.")

# --- 5. SEZIONE: EXPLORER ---
elif nav == "🗄️ Explorer":
    st.header("Market Data Explorer")
    st.markdown("Tabella completa dei dati di mercato analizzati.")
    
    # Filtro semplice
    search = st.text_input("Cerca Brand o Modello")
    if search:
        df_display = df_market[df_market['brand'].str.contains(search, case=False) | df_market['model'].str.contains(search, case=False)]
    else:
        df_display = df_market
        
    st.dataframe(df_display, use_container_width=True, hide_index=True)
