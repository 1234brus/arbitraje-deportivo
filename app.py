import streamlit as st
from cuotas_api import obtener_cuotas
from arbitraje import detectar_arbitraje

st.set_page_config(page_title="Arbitraje Deportivo", layout="wide")
st.title("🎯 Buscador de Arbitraje en Apuestas")

monto = st.number_input("💰 Monto total a apostar (S/.)", min_value=10.0, value=100.0, step=10.0)

if st.button("🔍 Buscar arbitrajes"):
    with st.spinner("Consultando API..."):
        eventos = obtener_cuotas()
        encontrados = 0

        for evento in eventos:
            home = evento.get("home_team", "Equipo A")
            away = evento.get("away_team", "Equipo B")
            nombre_evento = f"{home} vs {away}"
            mejores_cuotas = {}
            detalle_casas = {}

            for bookie in evento.get("bookmakers", []):
                casa = bookie.get("title", bookie.get("key", "Casa desconocida"))
                mercados = bookie.get("markets", [])
                if not mercados:
                    continue
                h2h = mercados[0].get("outcomes", [])
                for outcome in h2h:
                    nombre = outcome["name"]
                    cuota = outcome["price"]
                    if nombre not in mejores_cuotas or cuota > mejores_cuotas[nombre]:
                        mejores_cuotas[nombre] = cuota
                        detalle_casas[nombre] = casa

            if len(mejores_cuotas) >= 2:
                resultado = detectar_arbitraje(mejores_cuotas, monto)
                if resultado:
                    encontrados += 1
                    st.markdown(f"### 📌 {nombre_evento}")
                    
                    st.write("🏦 **Mejores cuotas por resultado:**")
                    for opcion in mejores_cuotas:
                        st.write(f"- {opcion}: {mejores_cuotas[opcion]} en *{detalle_casas[opcion]}*")
                    
                    st.write("📊 **Apuestas sugeridas:**")
                    st.json(resultado["apuestas"])
                    st.success(f"💸 Ganancia estimada: S/. {resultado['ganancia']} ({resultado['porcentaje_arbitraje']}% de arbitraje)")
                    st.divider()

        if encontrados == 0:
            st.warning("No se encontraron oportunidades de arbitraje en este momento.")

