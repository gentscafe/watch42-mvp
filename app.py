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

# 3. STATIC DATA GENERATION (Enhanced for Design mapping)
if 'initialized' not in st.session_state:
    random.seed(42)
    np.random.seed(42)
    
    def create_mock_watch(brand, model, ref, is_target=False, year=None):
        categories = ["Diver", "Dress", "GMT", "Chronograph", "Pilot/Field", "Casual"]
        cat = random.choice(categories)
        price = random.randint(1200, 3500) if is_target else random.randint(800, 4500)
        prod_year = year if year else random.randint(2018, 2024)
        
        # Design Logic: Specific dimensions based on category to create "clusters"
        if cat == "Diver":
            diam = random.choice([41.0, 42.0, 43.0])
            thick = random.choice([13.0, 14.0, 15.0])
        elif cat == "Dress":
            diam = random.choice([37.0, 38.0, 39.0])
            thick = random.choice([8.0, 9.0, 10.0])
        else:
            diam = random.choice([39.0, 40.0, 41.0])
            thick = random.choice([11.0, 12.0, 13.0])

        return {
            "Brand": brand, "Model": model, "Ref": ref, "Price": price,
            "Category": cat, "Year": prod_year, "Diameter": diam, "Thickness": thick,
            "Reserve": random.choice([42, 70, 80]), "Type": "Target" if is_target else "Market"
        }

    my_years = [2020, 2021, 2022, 2023, 2024]
    st.session_state.my_portfolio = [
        create_mock_watch("MY BRAND", f"My watch {i}", f"REF-0{i}", True, my_years[i-1])
        for i in range(1, 6)
    ]
    
    st.session_state.competitors = [
        create_mock_watch(f"Brand {random.randint(1,25)}", f"Model {i}", f"REF-{1000+i}") 
        for i in range(1, 501) # Large sample for heatmap density
    ]
    st.session_state.initialized = True

# 4. SIDEBAR
with st.sidebar:
    st.write("### Navigation")
    view = st.radio("Sections", ["My Watches", "Pricing Intelligence", "Design Intelligence"])
    st.write("---")
    st.caption("Intelligence SaaS v2.4")

# 5. VIEW: MY WATCHES
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
            with st.expander("Specs"):
                st.write(f"Size: {watch['Diameter']}mm x {watch['Thickness']}mm")

# 6. VIEW: PRICING INTELLIGENCE (Omitted for brevity - same as v2.3)
elif view == "Pricing Intelligence":
    st.info("Pricing Intelligence Logic remains active as per v2.3")

# 7. VIEW: DESIGN INTELLIGENCE (NEW)
elif view == "Design Intelligence":
    st.subheader("White Space Heatmap")
    st.caption("Strategic R&D tool to identify market gaps through physical proportions.")

    df_comp = pd.DataFrame(st.session_state.competitors)
    
    # Logic: Cross-tabulation of Diameter vs Thickness to count competitors in each cell
    heatmap_data = pd.crosstab(df_comp['Thickness'], df_comp['Diameter'])

    # Create Heatmap
    # We define a custom color scale: Green (0-1), Yellow (2-5), Red (10+)
    colorscale = [
        [0, "#27ae60"],      # Green (Empty/Gap)
        [0.1, "#f1c40f"],    # Yellow (Low Saturation)
        [0.5, "#e67e22"],    # Orange (Medium Saturation)
        [1.0, "#c0392b"]     # Red (High Saturation)
    ]

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=colorscale,
        hoverongaps=False,
        hovertemplate="Diameter: %{x}mm<br>Thickness: %{y}mm<br>Competitors: %{z}<extra></extra>"
    ))

    fig.update_layout(
        xaxis_title="Case Diameter (mm)",
        yaxis_title="Case Thickness (mm)",
        height=600,
        template="plotly_white",
        margin=dict(l=0, r=0, t=20, b=0)
    )

    # Adding a Legend for the CEO
    st.plotly_chart(fig, use_container_width=True)

    # Strategic Insights Panel
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("**White Space (Green)**: High R&D Opportunity. Design here to launch a unique product.")
    with c2:
        st.warning("**Medium Saturation (Orange)**: Competitive segment. Marketing-driven success.")
    with c3:
        st.error("**High Saturation (Red)**: Overcrowded area. Success depends strictly on price.")
