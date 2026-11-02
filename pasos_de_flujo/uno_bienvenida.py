
import streamlit as st
from control_de_la_sesion import ir_a

def mostrar():
    st.subheader("Bienvenido a la Plataforma de Reserva")
    st.write(
            "Reserve su cita médica de forma rápida y sencilla sin hacer filas. "
            "Le guiaremos paso a paso para identificar su expediente, evaluar sus síntomas y seleccionar su turno."
        )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Iniciar Reserva →", type="primary", use_container_width=True):
        ir_a(1)