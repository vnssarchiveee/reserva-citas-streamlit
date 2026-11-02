import streamlit as st
from google import genai
from bd_connector import obtener_especialidades

def obtener_cliente_ia():
    try:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception:
        return None
client = obtener_cliente_ia()

def recomendar_especialidad_ia(sintomas, lista_especialidades):
    if not sintomas.strip() or not client:
        return "Medicina General" if "Medicina General" in lista_especialidades else lista_especialidades[0]
        
    prompt = f"""
    Eres un asistente médico de triaje. 
    El paciente describe sus síntomas: "{sintomas}"
    
    De esta lista exacta de especialidades disponibles en el centro médico: {lista_especialidades}
    Responde ÚNICAMENTE con el nombre exacto de la especialidad más adecuada de la lista.
    No agregues introducciones, ni explicaciones, ni puntos finales. Solo el nombre de la especialidad.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        sugerencia = response.text.strip()
        if sugerencia in lista_especialidades:
            return sugerencia
    except Exception:
        pass
        
    return "Medicina General" if "Medicina General" in lista_especialidades else lista_especialidades[0]