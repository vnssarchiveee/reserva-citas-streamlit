import streamlit as st
from control_de_la_sesion import ir_a
from bd_connector import buscar_paciente, registrar_paciente, obtener_especialidades
from ia_gemini_helper import recomendar_especialidad_ia

especialidades = obtener_especialidades()
def caso_normal():
             st.subheader("🤖 Triaje Asistido por Inteligencia Artificial")
             st.write("Describe los síntomas o el malestar que presentas:")
             
             texto = st.text_area(
                 "Descripción de síntomas:",
                 value=st.session_state.sintomas,
                 placeholder="Ejemplo: Tengo dolor constante de cabeza, congestión nasal y mareos leves..."
             )
     
             if st.button("🤖 Analizar síntomas con IA", type="primary", use_container_width=True):
                 if not texto.strip():
                     st.warning("Escribe tus síntomas antes de analizar.")
                 else:
                     with st.spinner("Analizando con Google Gemini..."):
                         st.session_state.sintomas = texto.strip()
                         st.session_state.sugerencia = recomendar_especialidad_ia(texto, especialidades)
                         st.session_state.especialidad = st.session_state.sugerencia
     
             if st.session_state.sugerencia:
                 st.success(f"Especialidad recomendada por IA: **{st.session_state.sugerencia}**")
     
             col1, col2 = st.columns(2)
             if col1.button("← Volver"):
                 ir_a(2)
             if col2.button("Continuar a Especialidad →", type="primary", use_container_width=True):
                 ir_a(4)
     

def caso_urgente():
        st.subheader("🚨 Evaluador de Gravedad y Urgencia")
        st.write("Responde las siguientes preguntas para evaluar tu nivel de urgencia:")
        
        dolor = st.slider("1. Nivel de dolor actual (1 al 10):", min_value=1, max_value=10, value=1)
        duracion = st.radio(
            "2. ¿Hace cuánto iniciaron los síntomas principales?",
            ["Hace más de una semana", "Entre 2 y 7 días", "En las últimas 24 horas"]
        )
        
        st.write("3. Marca si presentas síntomas adicionales:")
        s_respiratorio = st.checkbox("Dificultad severa para respirar (+25 pts)")
        s_fiebre = st.checkbox("Fiebre alta persistente superior a 38.5 °C (+20 pts)")
        s_trauma = st.checkbox("Incapacidad para moverse o traumatismo reciente (+20 pts)")
        
        pts = dolor * 4
        if duracion == "En las últimas 24 horas": pts += 20
        elif duracion == "Entre 2 y 7 días": pts += 10
        if s_respiratorio: pts += 25
        if s_fiebre: pts += 20
        if s_trauma: pts += 20
        
        st.session_state.puntaje_urgencia = pts
        st.session_state.sintomas = f"Caso de Urgencia (Triaje: {pts} pts)"
        
        # CASO 1: URGENCIA ALTA (> 70 pts)
        if pts > 70:
            st.error(f"🚨 **CASO URGENTE DETECTADO** ({pts} / 125 pts)")
            st.info("Su puntaje requiere atención prioritaria de emergencia.")

            col1, col2 = st.columns(2)
            if col1.button("← Volver"):
                ir_a(2)
            if col2.button("Continuar a Especialidad →", type="primary", use_container_width=True):
                ir_a(4)

        # CASO 2: PRIORIDAD BAJA O MODERADA (<= 70 pts)
        else:
            st.warning(f"ℹ️ **Nivel de prioridad bajo/moderado ({pts} / 125 pts)**")
            st.info(
                "Su estado no requiere atención de emergencia inmediata. "
                "Por favor, solicite una **Cita Normal** para ser atendido en consultorio por un especialista."
            )

            col1, col2 = st.columns(2)
            if col1.button("← Volver"):
                ir_a(2)
            if col2.button("📅 Ir a Cita Normal", type="primary", use_container_width=True):
                st.session_state.modo = "Normal"  # Cambia a modo Cita Normal
                ir_a(2)                           # Redirige de vuelta a Selección de Modalidad

def mostrar_triaje():
    if st.session_state.modo == "Normal":
        caso_normal()
    else:
         caso_urgente()