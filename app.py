import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="watch42 | Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. UI STYLE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .global-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 60px;
        background-color: white; display: flex; align-items: center;
        padding: 0 20px; border-bottom: 1px solid #eee; z-index: 999999;
    }
    .logo-text { font-weight: 700; font-size: 1.4rem; color: #1a1a1a; letter-spacing: -0.5px; }
    .logo-accent { color: #d4af37; }
    .block-container { padding-top: 4rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { display: none; }
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

# 3. STATIC DATA GENERATION
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False, year=None):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        price = random.randint(1200, 3500) if is_target else random.randint(800, 4500)
        prod_year = year if year else random.randint(2018, 2024)
        
        if cat == "Diver":
            diam, thick = random.choice([41.0, 42.0, 43.0]), random.choice([13.0, 14.0, 15.0])
        elif cat == "Dress":
            diam, thick = random.choice([36.0, 38.0, 39.0]), random.choice([8.0, 9.0, 10.0])
        else:
            diam, thick = random.choice([39.0, 40.0, 41.0]), random.choice([11.0, 12.0, 13.0])

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Year": prod_year, "Diameter": diam, "Thickness": thick,
            "WR": random.choice([50, 100, 200, 300]), "Reserve": random.choice([42, 70, 80]),
            "Freq": random.choice([21600, 28800]), "Type": "Target" if is_target else "Market"
        }

    st.session_state.my_portfolio = [create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, 2019+i) for i in range(1, 6)]
    st.session_state.competitors = [create_mock_watch(f"Brand {random.randint(1,25)}", f"Model {i}", f"REF-{1000+i}") for i in range(1, 1001)]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v2.9")

# 5-6. VIEWS (Omitted for brevity, identical to v2.8)
if view == "My Watches":
    st.subheader("My Brand Portfolio")
    # ... (codice v2.8)
elif view == "Pricing Intelligence":
    st.subheader("Market Pricing Comparison")
    # ... (codice v2.8 con correzione KPI)

# 7. VIEW: DESIGN INTELLIGENCE (NUMBERS + LIST DRILL-DOWN)
elif view == "Design Intelligence":
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.subheader("Competitive Density Matrix")
    with col_h2:
        design_year_range = st.slider("Filter by Production Year", 2015, 2025, (2018, 2024))

    df_all = pd.DataFrame(st.session_state.competitors)
    df_f = df_all[df_all['Year'].between(design_year_range[0], design_year_range[1])].copy()
    
    # Raggruppamento per Heatmap
    matrix_df = df_f.groupby(['Diameter', 'Thickness']).size().reset_index(name='count')
    pivot_table = matrix_df.pivot(index='Thickness', columns='Diameter', values='count').fillna(0)

    # HEATMAP CON TESTO (NUMERI)
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index,
        colorscale=[[0, '#27ae60'], [0.1, '#f1c40f'], [0.5, '#e67e22'], [1.0, '#c0392b']],
        showscale=True, opacity=0.85,
        text=pivot_table.values, # Mostra i numeri
        texttemplate="%{text}", 
        textfont={"size": 14, "color": "white", "family": "Inter"},
        hovertemplate="Diam: %{x}mm<br>Thick: %{y}mm<br>Competitors: %{z}<extra></extra>"
    ))

    fig.update_layout(xaxis_title="Diameter (mm)", yaxis_title="Thickness (mm)",
                      template="plotly_white", height=550, margin=dict(l=0, r=0, t=20, b=0))

    st.plotly_chart(fig, use_container_width=True)

    # SEZIONE DRILL-DOWN (LISTA DETTAGLIATA)
    st.write("---")
    st.write("### 🔍 Cell Inspector")
    
    # Selezione interattiva per simulare il "clic" sulla cella
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        sel_diam = st.selectbox("Select Diameter", sorted(df_f['Diameter'].unique()))
    with c2:
        sel_thick = st.selectbox("Select Thickness", sorted(df_f['Thickness'].unique()))
    
    # Filtro dei competitor per la cella selezionata
    cell_competitors = df_f[(df_f['Diameter'] == sel_diam) & (df_f['Thickness'] == sel_thick)]
    
    with st.expander(f"View {len(cell_competitors)} Competitors in {sel_diam}mm x {sel_thick}mm", expanded=True):
        if not cell_competitors.empty:
            st.dataframe(
                cell_competitors[["Brand", "Model", "Year", "Price", "Category", "WR", "Reserve"]].sort_values("Price"),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No competitors in this specific dimension gap.")
