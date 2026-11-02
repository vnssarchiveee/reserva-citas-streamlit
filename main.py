import streamlit as st
from datetime import datetime, date
from ia_gemini_helper import obtener_cliente_ia,recomendar_especialidad_ia
from bd_connector import obtener_conexion, buscar_paciente, registrar_paciente, obtener_especialidades,obtener_horarios_disponibles,confirmar_reserva_cita
from control_de_la_sesion import PASOS, DEFAULTS, ir_a, reiniciar, inicializar_session
from pasos_de_flujo import uno_bienvenida, dos_identificarte, tres_triaje_evurg, cuatro_, cinco_seleccion_especialidad, seis_selecc_horario, siete_confirmar_cita

inicializar_session()

# INTERFAZ Y FLUJO PASO A PASO
st.set_page_config(page_title="Centro Médico - Citas", page_icon="🩺", layout="centered")

paso = st.session_state.paso
st.title("🏥 Centro Médico - Gestión de Citas")
st.progress((paso + 1) / len(PASOS))
st.caption(f"Paso {paso + 1} de {len(PASOS)}: **{PASOS[paso]}**")
st.divider()

#  BIENVENIDA
if paso == 0:
    uno_bienvenida.mostrar()
# IDENTIFICACIÓN Y CREACIÓN DE FICHA 
elif paso == 1:
    dos_identificarte.vista_identificacion()
# SELECCIÓN DE MODALIDAD DE CITA 
elif paso == 2:
    tres_triaje_evurg.elegir_opciones()
# TRIAJE CON IA O EVALUACIÓN DE URGENCIA 
elif paso == 3:
    cuatro_.mostrar_triaje()
# SELECCIÓN DE ESPECIALIDAD 
elif paso == 4:
    cinco_seleccion_especialidad.mostrar_especialidad()
# SELECCIÓN DE HORARIOS 
elif paso == 5:
    seis_selecc_horario.mostrar_horarios()
# CONFIRMACIÓN Y TICKET DIGITAL 
elif paso == 6:
    siete_confirmar_cita.mostrar_confirmacion()

# activar el entorno: Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned.\Scripts\Activate.ps1
# streamlit run main.py