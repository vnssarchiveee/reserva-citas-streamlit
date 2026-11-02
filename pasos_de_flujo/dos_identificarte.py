
import streamlit as st
import mysql.connector

from bd_connector import buscar_paciente, registrar_paciente
from control_de_la_sesion import ir_a, PASOS

def vista_identificacion():
    st.subheader("Identificación del Paciente")

    dni = st.text_input(
        "Ingresa tu DNI (8 dígitos) y presiona enter para continuar:",
        max_chars=8,
        value=st.session_state.dni
    )

    if dni and not (dni.isdigit() and len(dni) == 8):
        st.warning("El DNI debe contener exactamente 8 dígitos numéricos.")

    elif dni:
        try:
            paciente = buscar_paciente(dni)

        except mysql.connector.Error as e:
            st.error(f"Error al conectar con MySQL: {e}")
            st.stop()

        if paciente:
            st.session_state.dni = dni
            st.session_state.paciente = paciente

            st.success(
                f"Ficha encontrada: **{paciente['nombres']} "
                f"{paciente['apellidos']}**"
            )

            col1, col2 = st.columns(2)

            if col1.button("← Volver"):
                ir_a(0)

            if col2.button(
                "Confirmar e Ir a Elección de Cita →",
                type="primary",
                use_container_width=True
            ):
                ir_a(2)

        else:
            st.info(
                "El DNI no se encuentra registrado en el sistema. "
                "Crea tu ficha de paciente a continuación:"
            )

            with st.form("alta_paciente"):
                nombres = st.text_input("Nombres")
                apellidos = st.text_input("Apellidos")
                edad = st.number_input(
                    "Edad",
                    min_value=0,
                    max_value=120,
                    step=1,
                    value=25
                )
                alergias = st.text_input(
                    "Alergias (opcional)",
                    value="Ninguna"
                )

                guardar = st.form_submit_button(
                    "Crear Ficha y Continuar",
                    type="primary"
                )

            if guardar:
                if not nombres.strip() or not apellidos.strip():
                    st.error("Por favor completa tus nombres y apellidos.")

                else:
                    try:
                        registrar_paciente(
                            dni,
                            nombres.strip(),
                            apellidos.strip(),
                            int(edad),
                            alergias.strip()
                        )

                        st.session_state.dni = dni
                        st.session_state.paciente = buscar_paciente(dni)

                        st.success("¡Ficha creada exitosamente!")
                        ir_a(2)

                    except mysql.connector.Error as e:
                        st.error(f"Error al registrar el paciente: {e}")

    if not dni or not st.session_state.paciente:
        if st.button("← Volver", key="volver_identificacion"):
            ir_a(0)
