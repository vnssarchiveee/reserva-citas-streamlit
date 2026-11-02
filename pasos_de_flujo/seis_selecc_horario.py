import streamlit as st
from datetime import datetime, date
from bd_connector import obtener_horarios_disponibles
from control_de_la_sesion import ir_a

def mostrar_horarios():
    st.subheader(f"Horarios Disponibles para {st.session_state.especialidad}")

    fecha_elegida = st.date_input("Selecciona la fecha:", min_value=datetime.now().date())
    horarios = obtener_horarios_disponibles(st.session_state.especialidad, fecha_elegida)

    if not horarios:
        st.warning("No hay turnos disponibles para esta especialidad en la fecha seleccionada.")
    else:
        for h in horarios:
            c1, c2 = st.columns([3, 1])
            
            nombre_doc = h['doctor'] if h['doctor'].startswith("Dr") else f"Dr/a. {h['doctor']}"
            
            c1.markdown(
                f"👨‍⚕️ **{nombre_doc}**  \n"
                f"📅 {fecha_elegida:%d/%m/%Y} · 🕐 Hora: {h['hora']}"
            )
            if c2.button("Elegir Turno", key=f"h_{h['id']}", type="primary"):
                st.session_state.horario = h
                st.session_state.fecha_str = f"{fecha_elegida:%d/%m/%Y}"
                ir_a(6)
            st.divider()

    if st.button("← Volver"):
        ir_a(4)