import re
import unicodedata
import streamlit as st
from google import genai

def obtener_cliente_ia():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error cliente Gemini: {e}")
    return None

def normalizar_texto(texto):
    """Elimina tildes, mayúsculas, comillas, asteriscos y puntos finales."""
    texto = texto.lower().strip()
    texto = re.sub(r'[*"\'.]', '', texto)
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def recomendar_especialidad_ia(sintomas, lista_especialidades):
    cliente = obtener_cliente_ia()
    
    if not sintomas.strip() or not cliente or not lista_especialidades:
        return "Medicina General" if "Medicina General" in lista_especialidades else lista_especialidades[0]

    prompt = f"""
    Eres un asistente de triaje médico.
    El paciente dice: "{sintomas}"

    Especialidades disponibles: {', '.join(lista_especialidades)}

    Mapeo de intenciones habituales:
    - Comer bien, dietas, bajar/subir de peso, nutrición -> Nutrición
    - Dolor de cabeza, fiebre, malestar general -> Medicina General
    - Ansiedad, estrés, salud mental -> Psicología
    - Niños, bebés -> Pediatría
    - Oído, nariz, garganta -> Otorrinolaringología

    Responde ÚNICAMENTE con el nombre exacto de la especialidad correspondiente de la lista.
    """

    # Lista de nombres de modelos para intentar en orden
    modelos_candidatos = [
        'gemini-2.5-flash',
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-2.0-flash'
    ]

    sugerencia_raw = None

    for modelo in modelos_candidatos:
        try:
            response = cliente.models.generate_content(
                model=modelo,
                contents=prompt,
            )
            if response and response.text:
                sugerencia_raw = response.text.strip()
                break  # Si el modelo responde con éxito, sale del bucle
        except Exception:
            continue  # Si el modelo devuelve 404 u otro error, intenta el siguiente silenciosamente

    if sugerencia_raw:
        sugerencia_norm = normalizar_texto(sugerencia_raw)
        
        # Comparación flexible ignorando mayúsculas, tildes y símbolos
        for esp in lista_especialidades:
            if normalizar_texto(esp) == sugerencia_norm or normalizar_texto(esp) in sugerencia_norm:
                return esp

    return "Medicina General" if "Medicina General" in lista_especialidades else lista_especialidades[0]
