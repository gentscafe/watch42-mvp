# 6. VIEW: PRICING INTELLIGENCE (Vertical Benchmarking Version)
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

    # Logica di Filtro: Isolo i competitor con lo stesso valore tecnico del target
    target_value = target[y_param]
    df_market_all = pd.DataFrame(st.session_state.competitors)
    
    # Filtriamo i competitor che hanno esattamente lo stesso valore del target sul parametro Y
    df_filtered_market = df_market_all[df_market_all[y_param] == target_value].copy()
    
    # Uniamo il target per la visualizzazione
    df_target = pd.DataFrame([target])
    df_plot = pd.concat([df_filtered_market, df_target])

    unit_y = units[y_param]
    
    st.subheader(f"Analisi Prezzi per {y_param}: {target_value} {unit_y}")
    
    if len(df_filtered_market) > 0:
        fig = px.scatter(
            df_plot, x="Price", y=y_param, color="Type",
            color_discrete_map={"Market": "#CBD5E0", "Target": "#D4AF37"},
            size=df_plot['Type'].apply(lambda x: 25 if x == "Target" else 15),
            hover_name="Model",
            labels={"Price": "Prezzo (€)", y_param: f"{y_param} ({unit_y})"},
            template="plotly_white", height=500
        )

        # Forziamo l'asse Y a restare fisso sul valore del target per enfatizzare la linea orizzontale
        fig.update_layout(
            xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
            yaxis=dict(range=[target_value * 0.9, target_value * 1.1], ticksuffix=f" {unit_y}"),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insight automatico
        avg_market_price = df_filtered_market['Price'].mean()
        diff = target['Price'] - avg_market_price
        pos_text = "sopra" if diff > 0 else "sotto"
        
        st.success(f"""
            **Market Insight:** Per orologi con **{target_value} {unit_y}** di {y_param}, 
            il prezzo medio di mercato è di **€ {avg_market_price:,.0f}**. 
            Il tuo modello è posizionato **{pos_text}** alla media di **€ {abs(diff):,.0f}**.
        """)
    else:
        st.warning(f"Non ci sono competitor nel database con esattamente {target_value} {unit_y} di {y_param}. Prova a cambiare parametro o target.")
