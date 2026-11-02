import streamlit as st
from bd_connector import obtener_especialidades
from control_de_la_sesion import ir_a


def mostrar_especialidad():

    # Intenta obtener las especialidades desde la BD
    try:
        especialidades = obtener_especialidades()
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        especialidades = []

    if not especialidades:
        st.warning(
            "⚠️ No se encontraron especialidades en la base de datos."
        )
        if st.button("← Volver al Triaje"):
            ir_a(3)
    else:
        idx = 0
        sug = st.session_state.get("especialidad", None)

        if sug and sug in especialidades:
            idx = especialidades.index(sug)
            st.info(f"💡 Especialidad preseleccionada: **{sug}**")

        elegida = st.selectbox(
            "Selecciona o confirma la especialidad:",
            especialidades,
            index=idx,
        )

        col1, col2 = st.columns(2)
        if col1.button("← Volver"):
            ir_a(3)
        if col2.button(
            "Ver Horarios Disponibles →",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.especialidad = elegida
            ir_a(5)