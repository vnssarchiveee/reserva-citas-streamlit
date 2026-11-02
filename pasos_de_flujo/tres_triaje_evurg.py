import streamlit as st
import mysql.connector
from control_de_la_sesion import ir_a

def elegir_opciones():
        pac = st.session_state.paciente
        st.subheader("Selección de Modalidad de Cita")
        st.info(f"👤 **Paciente activo:** {pac['nombres']} {pac['apellidos']} (DNI: {pac['dni']})")
        
        st.write("Selecciona el tipo de atención que necesitas:")
        
        modo_sel = st.radio(
            "Opción de atención:",
            ["📅 Reserva de Cita Normal (Asistida por IA)", "🚨 Evaluador de Cita Urgente"],
            index=0 if st.session_state.modo == "Normal" else 1
        )
        
        col1, col2 = st.columns(2)
        if col1.button("← Volver"):
            ir_a(1)
        if col2.button("Continuar a Evaluación →", type="primary", use_container_width=True):
            st.session_state.modo = "Urgencia" if "Urgente" in modo_sel else "Normal"
            ir_a(3)