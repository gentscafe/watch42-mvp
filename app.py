# 6. VIEW: PRICING INTELLIGENCE (Versione con Unità di Misura)
elif view == "Pricing Intelligence":
    st.header("Dynamic Pricing Matrix")
    
    # Mappa delle unità di misura per rendere tutto dinamico
    units = {
        "Reserve": "h",
        "Thickness": "mm",
        "WR": "m",
        "Freq": "vph",
        "Diameter": "mm"
    }
    
    col_a, col_b = st.columns(2)
    with col_a:
        target = st.selectbox("Seleziona Target (MY BRAND)", 
                             st.session_state.my_portfolio, 
                             format_func=lambda x: f"{x['Model']} ({x['Ref']})")
    with col_b:
        y_param = st.selectbox("Parametro Tecnico (Asse Y)", 
                              list(units.keys()))

    # Merge dei dati
    df_market = pd.DataFrame(st.session_state.competitors)
    df_target = pd.DataFrame([target])
    df_all = pd.concat([df_market, df_target])

    # Creazione Plotly Scatter con etichette asse e hover migliorati
    unit_y = units[y_param]
    
    fig = px.scatter(
        df_all, 
        x="Price", 
        y=y_param, 
        color="Type",
        color_discrete_map={"Market": "#E2E8F0", "Target": "#D4AF37"},
        size=df_all['Type'].apply(lambda x: 20 if x == "Target" else 10),
        hover_name="Model",
        labels={
            "Price": "Prezzo di Listino (€)",
            y_param: f"{y_param} ({unit_y})"
        },
        hover_data={
            "Brand": True,
            "Price": ":.2f", # Formato valuta
            y_param: True,
            "Type": False
        },
        template="plotly_white",
        height=650
    )

    # Raffinamento estetico del layout
    fig.update_layout(
        xaxis=dict(ticksuffix=" €", gridcolor="#f0f0f0"),
        yaxis=dict(ticksuffix=f" {unit_y}", gridcolor="#f0f0f0"),
        showlegend=False,
        font=dict(family="Inter, sans-serif", size=12)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
        <div style="background-color: #fffbeb; padding: 15px; border-radius: 8px; border: 1px solid #fef3c7;">
            <p style="margin:0; color: #92400e; font-size: 0.9rem;">
                <strong>Analisi di Posizionamento:</strong> Il modello <strong>{target['Model']}</strong> viene confrontato 
                sulla base del prezzo (€) rispetto alla sua <strong>{y_param}</strong> ({unit_y}). 
                I competitor in grigio rappresentano il benchmark di mercato.
            </p>
        </div>
    """, unsafe_allow_html=True)
