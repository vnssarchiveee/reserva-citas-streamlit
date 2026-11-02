from datetime import datetime, timedelta
from bd_connector import obtener_conexion

# Plantilla base de horarios por día
PATRON_HORARIOS = [
    ('Dr. Carlos Mendoza', 'Medicina General', '08:00:00', 'Regular'),
    ('Dr. Carlos Mendoza', 'Medicina General', '09:00:00', 'Prioritaria'),
    ('Dr. Carlos Mendoza', 'Medicina General', '10:30:00', 'Regular'),
    ('Dr. Carlos Mendoza', 'Medicina General', '11:30:00', 'Prioritaria'),
    ('Dr. Carlos Mendoza', 'Medicina General', '15:00:00', 'Regular'),
    ('Lic. Mariana Flores', 'Nutrición', '09:00:00', 'Regular'),
    ('Lic. Mariana Flores', 'Nutrición', '11:00:00', 'Prioritaria'),
    ('Lic. Mariana Flores', 'Nutrición', '14:00:00', 'Regular'),
    ('Mg. Javier Paredes', 'Psicología', '10:00:00', 'Regular'),
    ('Mg. Javier Paredes', 'Psicología', '12:00:00', 'Prioritaria'),
    ('Mg. Javier Paredes', 'Psicología', '16:00:00', 'Regular'),
    ('Dra. Ana Rodríguez', 'Otorrinolaringología', '08:30:00', 'Regular'),
    ('Dra. Ana Rodríguez', 'Otorrinolaringología', '10:00:00', 'Prioritaria'),
    ('Dra. Ana Rodríguez', 'Otorrinolaringología', '11:30:00', 'Regular'),
    ('Q.F. Andrea Espinoza', 'Farmacia', '09:00:00', 'Regular'),
    ('Q.F. Andrea Espinoza', 'Farmacia', '09:30:00', 'Prioritaria'),
    ('Q.F. Andrea Espinoza', 'Farmacia', '15:30:00', 'Regular'),
    ('Dr. Roberto Silva', 'Pediatría', '08:00:00', 'Prioritaria'),
    ('Dr. Roberto Silva', 'Pediatría', '10:00:00', 'Regular'),
]

def poblar_anio():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    fecha_inicio = datetime(2026, 11, 1)
    fecha_fin = datetime(2026, 12, 31)
    
    registros = 0
    fecha_actual = fecha_inicio
    
    while fecha_actual <= fecha_fin:
        # Excluye domingos (weekday 6)
        if fecha_actual.weekday() != 6:
            fecha_str = fecha_actual.strftime('%Y-%m-%d')
            for doc, esp, hora, prio in PATRON_HORARIOS:
                fecha_hora = f"{fecha_str} {hora}"
                query = """
                    INSERT INTO horarios (doctor, especialidad, fecha_hora, estado, prioridad)
                    VALUES (%s, %s, %s, 'Disponible', %s)
                """
                cursor.execute(query, (doc, esp, fecha_hora, prio))
                registros += 1
        fecha_actual += timedelta(days=1)
        
    conn.commit()
    cursor.close()
    conn.close()
    #print(f"✅ ¡Completado! Se registraron {registros} horarios.")

if __name__ == "__main__":
    poblar_anio()