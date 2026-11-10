import streamlit as st
from control_de_la_sesion import ir_a
from bd_connector import buscar_paciente, registrar_paciente, obtener_especialidades
from ia_gemini_helper import recomendar_especialidad_ia


def caso_normal():
             especialidades = obtener_especialidades()
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
    st.subheader("🚨 Evaluador de Urgencia")
    st.write(
        "Responde las siguientes preguntas (escala del 1 al 5) para evaluar tu nivel de urgencia:"
    )

    # Control del estado para ocultar el resultado hasta presionar el botón
    if "evaluado" not in st.session_state:
        st.session_state.evaluado = False

    # Formulario de preguntas
    dolor = st.slider(
        "1. ¿Qué tan fuerte es su dolor o molestia ahora?",
        min_value=1,
        max_value=5,
        value=1,
        help="1 = Casi no lo siento | 5 = Es muy fuerte",
    )

    actividades = st.slider(
        "2. ¿Qué tanto le impide hacer sus actividades diarias (trabajar, estudiar, dormir, comer)?",
        min_value=1,
        max_value=5,
        value=1,
        help="1 = Nada | 5 = No puedo hacer nada",
    )

    empeoramiento = st.slider(
        "3. ¿Qué tan rápido han empeorado sus síntomas desde que empezaron?",
        min_value=1,
        max_value=5,
        value=1,
        help="1 = Siguen igual | 5 = Empeoran cada hora",
    )

    preocupacion = st.slider(
        "4. ¿Qué tanto le preocupa su estado de salud en este momento?",
        min_value=1,
        max_value=5,
        value=1,
        help="1 = Nada | 5 = Muchísimo",
    )

    st.write("")

    # Botones principales antes de evaluar
    col1, col2 = st.columns(2)
    if col1.button("← Volver"):
        st.session_state.evaluado = False
        ir_a(2)

    if col2.button(
        "🔍 Ver resultado", type="primary", use_container_width=True
    ):
        st.session_state.evaluado = True

    # Solo se muestra el resultado si la persona presiona "Ver resultado"
    if st.session_state.evaluado:
        pts = dolor + actividades + empeoramiento + preocupacion
        st.markdown("---")

        # CASO 1: CONSULTA NORMAL (4 a 8 pts)
        if 4 <= pts <= 8:
            nivel = "Consulta normal"
            st.session_state.puntaje_urgencia = pts
            st.session_state.sintomas = (
                f"Caso de Urgencia (Triaje: {pts} pts - {nivel})"
            )

            st.info(
                f"ℹ️ **Resultado de Evaluación: {nivel} ({pts}/20 pts)**\n\n"
                "Su estado no requiere atención de emergencia inmediata. Se agendará una cita en la fecha disponible."
            )

            if st.button(
                "📅 Ir a Cita Normal", type="primary", use_container_width=True
            ):
                st.session_state.modo = "Normal"
                st.session_state.evaluado = False
                ir_a(2)

        # CASO 2: URGENCIA LEVE (9 a 14 pts)
        elif 9 <= pts <= 14:
            nivel = "Urgencia leve"
            st.session_state.puntaje_urgencia = pts
            st.session_state.sintomas = (
                f"Caso de Urgencia (Triaje: {pts} pts - {nivel})"
            )

            st.warning(
                f"⚠️ **Resultado de Evaluación: {nivel} ({pts}/20 pts)**\n\n"
                "Se requiere una cita prioritaria en los próximos días."
            )

            if st.button(
                "Continuar a Especialidad →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.evaluado = False
                ir_a(4)

        # CASO 3: URGENCIA ALTA (15 a 20 pts)
        else:
            nivel = "Urgencia alta"
            st.session_state.puntaje_urgencia = pts
            st.session_state.sintomas = (
                f"Caso de Urgencia (Triaje: {pts} pts - {nivel})"
            )

            st.error(
                f"🚨 **Resultado de Evaluación: {nivel} ({pts}/20 pts)**\n\n"
                "Atención requerida el mismo día o en el primer horario libre."
            )

            if st.button(
                "Continuar a Especialidad →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.evaluado = False
                ir_a(4)

def mostrar_triaje():
    if st.session_state.modo == "Normal":
        caso_normal()
    else:
        caso_urgente()
