import streamlit as st
from datetime import datetime, date
from bd_connector import obtener_horarios_disponibles,confirmar_reserva_cita
from control_de_la_sesion import ir_a, reiniciar


def mostrar_confirmacion():
    p, h = st.session_state.paciente, st.session_state.horario

    if st.session_state.ticket:
        t = st.session_state.ticket
        st.success("¡Cita reservada con éxito!")
        
        with st.container(border=True):
            st.markdown("### 🎫 Ticket Digital de Confirmación")
            st.write(f"**Paciente:** {t['paciente']}")
            st.write(f"**DNI:** {t['dni']}")
            st.write(f"**Especialidad:** {t['especialidad']}")
            st.write(f"**Médico:** {t['doctor']}")
            st.write(f"**Fecha:** {t['fecha']}")
            st.write(f"**Hora:** {t['hora']}")
            if t['sintomas']:
                st.write(f"**Motivo:** {t['sintomas']}")
                
        st.caption("Presenta tu DNI al llegar a admisión.")
        
        if st.button("🔄 Reservar otra cita", type="primary", use_container_width=True):
            reiniciar()

    else:
        st.subheader("Confirma los Datos de tu Cita")
        nombre_doc = h['doctor'] if h['doctor'].startswith("Dr") else f"Dr/a. {h['doctor']}"
        
        with st.container(border=True):
            st.write(f"**Paciente:** {p['nombres']} {p['apellidos']} (DNI: {p['dni']})")
            st.write(f"**Especialidad:** {st.session_state.especialidad}")
            st.write(f"**Médico:** {nombre_doc}")
            st.write(f"**Fecha:** {st.session_state.get('fecha_str', '')}")
            st.write(f"**Hora:** {h['hora']}")
            if st.session_state.sintomas:
                st.write(f"**Síntomas:** {st.session_state.sintomas}")

        col1, col2 = st.columns(2)
        if col1.button("← Elegir otro turno"):
            ir_a(5)
            
        if col2.button("Confirmar Cita", type="primary", use_container_width=True):
            ok = confirmar_reserva_cita(
                p["dni"], h["id"], st.session_state.sintomas
            )

            if ok:
                st.session_state.ticket = {
                    "paciente": f"{p['nombres']} {p['apellidos']}",
                    "dni": p["dni"],
                    "especialidad": st.session_state.especialidad,
                    "doctor": nombre_doc,
                    "fecha": st.session_state.get('fecha_str', ''),
                    "hora": str(h["hora"]),
                    "sintomas": st.session_state.sintomas,
                }
                st.rerun()
            else:
                st.error("El horario seleccionado ya no está disponible. Por favor elige otro.")