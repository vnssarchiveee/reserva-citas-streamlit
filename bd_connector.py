import streamlit as st
import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=int(st.secrets["mysql"]["port"])
        
    )

def buscar_paciente(dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pacientes WHERE dni = %s", (dni,))
    paciente = cursor.fetchone()
    cursor.close()
    conexion.close()
    return paciente

def registrar_paciente(dni, nombres, apellidos, edad, alergias="Ninguna"):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = "INSERT INTO pacientes (dni, nombres, apellidos, edad, alergias) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (dni, nombres, apellidos, edad, alergias))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_especialidades():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT DISTINCT especialidad FROM horarios ORDER BY especialidad ASC")
    especialidades = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    conexion.close()
    return especialidades

def obtener_horarios_disponibles(especialidad, fecha):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT MIN(id) AS id, doctor, TIME(fecha_hora) AS hora, fecha_hora 
        FROM horarios 
        WHERE especialidad = %s 
          AND DATE(fecha_hora) = %s 
          AND estado = 'Disponible'
        GROUP BY doctor, fecha_hora
        ORDER BY fecha_hora ASC
    """
    cursor.execute(sql, (especialidad, fecha))
    horarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return horarios

def confirmar_reserva_cita(paciente_dni, horario_id, sintomas=""):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        sql_cita = "INSERT INTO citas (paciente_dni, horario_id, sintomas) VALUES (%s, %s, %s)"
        cursor.execute(sql_cita, (paciente_dni, horario_id, sintomas))
        
        sql_horario = "UPDATE horarios SET estado = 'Ocupado' WHERE id = %s AND estado = 'Disponible'"
        cursor.execute(sql_horario, (horario_id,))
        if cursor.rowcount == 0:
            conexion.rollback()
            return False
            
        conexion.commit()
        exito = True
    except Exception as e:
        conexion.rollback()
        print(f"Error al procesar la reserva: {e}")
        exito = False
    finally:
        cursor.close()
        conexion.close()
        
    return exito

