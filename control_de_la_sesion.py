import streamlit as st
PASOS = [
    "Bienvenida",
    "Identificación",
    "Tipo de Cita",
    "Triaje / Evaluación",
    "Especialidad",
    "Horarios",
    "Confirmación y Ticket",
]
DEFAULTS = {
    "paso": 0,
    "modo": "Normal",
    "dni": "",
    "paciente": None,
    "sintomas": "",
    "sugerencia": "",
    "especialidad": None,
    "horario": None,
    "ticket": None,
    "puntaje_urgencia": 0,
    "fecha_str": "",
}

def inicializar_session():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)

def ir_a(paso):
    st.session_state.paso = paso
    st.rerun()

def reiniciar():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.rerun()



