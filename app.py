# 6. VIEW: PRICING INTELLIGENCE (Layout con KPI in alto)
elif view == "Pricing Intelligence":
    st.header("Dynamic Pricing Matrix")
    
    units = {"Reserve": "h", "Thickness": "mm", "WR": "m", "Freq": "vph", "Diameter": "mm"}
    
    col_a, col_b = st.columns(2)
    with col_a:
        target = st.selectbox("Seleziona Target (MY BRAND)", 
                             st.session_state.my_portfolio, 
                             format_func=lambda x: f"{x['Model']}")
    with col_b:
        y_param = st.selectbox("Parametro Tecnico", list(units.keys()))

    # Logica di Filtro
    target_cat = target['Category']
    target_value = target[y_param]
    unit_y = units[y_param]
    df_market = pd.DataFrame(st.session_state.competitors)
    
    df_filtered = df_market[
        (df_market['Category'] == target_cat) & 
        (df_market[y_param] == target_value)
    ].copy()

    # --- NUOVA SEZIONE KPI (SOPRA IL GRAFICO) ---
    st.write("---")
    if not df_filtered.empty:
        avg_p = df_filtered['Price'].mean()
        # Calcolo Price Positioning Index (PPI)
        ppi = ((target['Price'] - avg_p) / avg_p) * 100
        
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Competitor Diretti", len(df_filtered))
        kpi2.metric("Prezzo Medio Mercato", f"€ {avg_p:,.0f}")
        kpi3.metric("Il tuo Prezzo", f"€ {target['Price']:,}")
        kpi4.metric("Positioning Index (PPI)", f"{ppi:+.1f}%", 
                    delta=f"{ppi:+.1f}% vs media", delta_color="inverse")
        
        st.write("---") # Separatore prima del grafico

        # --- GRAFICO ---
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
            xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
            yaxis=dict(range=[target_value * 0.8, target_value * 1.2], ticksuffix=f" {unit_y}"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Nessun competitor in categoria '{target_cat}' trovato con {target_value} {unit_y}.")
