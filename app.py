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
        
        # Coherent Design Logic for Heatmap clustering
        if cat == "Diver":
            diam, thick = random.choice([41.0, 42.0, 43.0]), random.uniform(13.0, 15.5)
        elif cat == "Dress":
            diam, thick = random.choice([36.0, 37.0, 38.0, 39.0]), random.uniform(8.0, 10.5)
        else:
            diam, thick = random.choice([39.0, 40.0, 41.0]), random.uniform(11.0, 13.5)

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Year": prod_year, "Diameter": round(diam, 1), "Thickness": round(thick, 1),
            "WR": random.choice([50, 100, 200, 300]), "Reserve": random.choice([42, 70, 80]),
            "Freq": random.choice([21600, 28800]), "Type": "Target" if is_target else "Market"
        }

    my_years = [2020, 2021, 2022, 2023, 2024]
    st.session_state.my_portfolio = [
        create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, my_years[i-1])
        for i in range(1, 6)
    ]
    
    st.session_state.competitors = [
        create_mock_watch(f"Brand {random.randint(1,25)}", f"Model {i}", f"REF-{1000+i}") 
        for i in range(1, 601)
    ]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v2.6")

# 5. VIEW: MY WATCHES (Same as v2.5)
if view == "My Watches":
    cols = st.columns(5)
    for i, watch in enumerate(st.session_state.my_portfolio):
        with cols[i]:
            st.markdown(f"""
                <div class="watch-tile">
                    <span class="category-badge">{watch['Category']}</span>
                    <div class="watch-title">{watch['Model']}</div>
                    <div class="watch-price">€ {watch['Price']:,}</div>
                    <div style="font-size:0.8rem; color:#666;">Year: {watch['Year']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("Specifications"):
                st.write(f"Size: {watch['Diameter']}mm x {watch['Thickness']}mm")

# 6. VIEW: PRICING INTELLIGENCE (Same as v2.5)
elif view == "Pricing Intelligence":
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Freq": "vph", "Diameter": "mm"}
    col_f1, col_f2, col_f3 = st.columns([1.2, 1, 1.3])
    with col_f1:
        target = st.selectbox("Select Target Watch", st.session_state.my_portfolio, 
                             format_func=lambda x: f"{x['Model']} — {x['Category']} ({x['Year']})")
    with col_f2:
        y_param = st.selectbox("Technical Parameter", list(units.keys()))
    with col_f3:
        t_year = target['Year']
        year_range = st.slider("Production Year Range", 2015, 2025, (t_year - 1, t_year + 1), key="price_slider")

    df_market = pd.DataFrame(st.session_state.competitors)
    df_filtered = df_market[(df_market['Category'] == target['Category']) & 
                            (df_market[y_param] == target[y_param]) &
                            (df_market['Year'].between(year_range[0], year_range[1]))].copy()

    if not df_filtered.empty:
        avg_p = df_filtered['Price'].mean()
        diff_pct = ((target['Price'] - avg_p) / avg_p) * 100
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Category", target['Category']), k2.metric("Target Year", target['Year'])
        k3.metric("Competitors", len(df_filtered)), k4.metric("Avg Price", f"€ {avg_p:,.0f}")
        k5.metric("Your Price", f"€ {target['Price']:,}", f"{diff_pct:+.1f}% vs avg", delta_color="inverse")
        st.write("---")
        df_plot = pd.concat([df_filtered, pd.DataFrame([target])])
        fig = px.scatter(df_plot, x="Price", y=y_param, color="Type",
                         color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
                         size=df_plot['Type'].apply(lambda x: 25 if x == "Target" else 15),
                         labels={"Price": "Price (€)", y_param: f"{y_param} ({units[y_param]})"},
                         template="plotly_white", height=480)
        fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# 7. VIEW: DESIGN INTELLIGENCE (Heatmap + Scatter Overlay)
elif view == "Design Intelligence":
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.subheader("White Space Heatmap")
    with col_h2:
        design_year_range = st.slider("Filter by Production Year", 2015, 2025, (2018, 2024), key="design_slider")

    df_all = pd.DataFrame(st.session_state.competitors)
    # Filter data for heatmap based on year
    df_filtered_design = df_all[df_all['Year'].between(design_year_range[0], design_year_range[1])].copy()
    
    # Calculate density for the heatmap background
    heatmap_df = df_filtered_design.groupby(['Diameter', 'Thickness']).size().reset_index(name='count')
    pivot_table = heatmap_df.pivot(index='Thickness', columns='Diameter', values='count').fillna(0)

    # SEMAPHORE COLORS: Green (Gap) to Red (Crowded)
    custom_colorscale = [[0, '#27ae60'], [0.1, '#f1c40f'], [0.5, '#e67e22'], [1.0, '#c0392b']]

    # 1. Base Heatmap Layer
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index,
        colorscale=custom_colorscale, showscale=True, opacity=0.8,
        hovertemplate="Diam: %{x}mm<br>Thick: %{y}mm<br>Density: %{z}<extra></extra>"
    ))

    # 2. Scatter Overlay (The "Competitor Dots")
    fig.add_trace(go.Scatter(
        x=df_filtered_design['Diameter'], y=df_filtered_design['Thickness'],
        mode='markers', marker=dict(color='white', size=4, opacity=0.4, line=dict(width=0.5, color='black')),
        name='Competitors', hoverinfo='text',
        text=[f"{row['Brand']} {row['Model']} ({row['Year']})" for _, row in df_filtered_design.iterrows()]
    ))

    fig.update_layout(
        xaxis_title="Case Diameter (mm)", yaxis_title="Case Thickness (mm)",
        template="plotly_white", height=600, margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="#f0f0f0")
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    st.info(f"Showing **{len(df_filtered_design)}** models from **{design_year_range[0]}** to **{design_year_range[1]}**. Hover over white dots to identify brands.")
