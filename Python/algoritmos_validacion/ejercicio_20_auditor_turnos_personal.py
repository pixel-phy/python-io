"""Ejercicio 20: Auditor de turnos de personal (Restricciones Acopladas)

En el problema de Programación de Horarios de Tripulación, las restricciones laborales son muy estrictas.
    Para que un horario de un trabajador sea válido para el Solver, debe cumplir tres resctricciones al 
mismo tiempo:
    1. Máximo de horas por turno: No puede trabajar más de 480 minutos (8 horas) por turno.
        2. Descanso mínimo: Debe tener al menos 660 minutos (11 horas) de descanso entre el fin 
    de un turno y el inicio del siguiente.
    3. No negatividad y orden: El tiempo de fin de turno debe ser estrictamente mayor al tiempo de inicio.

    Escribe una función que reciba una lista de turnos (donde cada turno es un diccionario {'inicio': min, 
                                                                                             'fin': min})
    ordenados cronológicamente. La función debe auditar por completo la agenda del empleado y retornar un reporte
    formateado (puede ser un diccionario listo para JSON) especificando si la agenda es factible para el 
    Solver o detallar exactamente qué restricciones se rompieron y en qué índices de turnos ocurrió 

    Input de prueba: turnos_empleado = [
    {'inicio':480, 'fin':900}
    {'inicio':1440, 'fin':2000}
    {'inicio':2300, 'fin':2800}
    ]"""

def auditar_horario(turnos:list)-> dict:
    """
    Audita un horario de empleado verificando todas las restricciones laborales.
    
    Args:
        turnos (list): Lista de diccionarios con 'inicio' y 'fin' en minutos
    
    Returns:
        dict: Reporte detallado del auditoría
    """
    # Inicializar reporte
    reporte = {
        "factible": True,
        "turnos_analizados": len(turnos),
        "restricciones_violadas": [],
        "detalles_turnos": []
    }
    
    # Si no hay turnos, consideramos factible
    if not turnos:
        reporte["factible"] = True
        reporte["mensaje"] = "No hay turnos que auditar"
        return reporte
    
    # Validar cada turno individualmente
    for i, turno in enumerate(turnos):
        inicio = turno['inicio']
        fin = turno['fin']
        violaciones_turno = []
        
        # Restricción 3: No negatividad y orden (fin > inicio)
        if fin <= inicio:
            violaciones_turno.append({
                "tipo": "orden_y_no_negatividad",
                "descripcion": f"El fin del turno ({fin}) debe ser mayor al inicio ({inicio})",
                "turno_indice": i
            })
            reporte["factible"] = False
        
        # Restricción 1: Máximo de horas por turno (480 minutos = 8 horas)
        duracion = fin - inicio
        if duracion > 480:
            violaciones_turno.append({
                "tipo": "maximo_horas",
                "descripcion": f"El turno dura {duracion} minutos, excede el máximo de 480 minutos",
                "turno_indice": i,
                "duracion": duracion,
                "limite": 480,
                "exceso": duracion - 480
            })
            reporte["factible"] = False
        
        # Guardar detalles del turno
        detalle_turno = {
            "indice": i,
            "inicio": inicio,
            "fin": fin,
            "duracion": duracion,
            "es_valido": len(violaciones_turno) == 0
        }
        
        if violaciones_turno:
            detalle_turno["violaciones"] = violaciones_turno
            reporte["restricciones_violadas"].extend(violaciones_turno)
        
        reporte["detalles_turnos"].append(detalle_turno)
    
    # Restricción 2: Descanso mínimo entre turnos (660 minutos = 11 horas)
    for i in range(len(turnos) - 1):
        turno_actual = turnos[i]
        turno_siguiente = turnos[i + 1]
        
        fin_actual = turno_actual['fin']
        inicio_siguiente = turno_siguiente['inicio']
        descanso = inicio_siguiente - fin_actual
        
        if descanso < 660:
            violacion_descanso = {
                "tipo": "descanso_minimo",
                "descripcion": f"Descanso de {descanso} minutos entre turno {i} y {i+1}, mínimo requerido 660 minutos",
                "turno_indice": i,
                "turno_siguiente_indice": i + 1,
                "descanso_actual": descanso,
                "descanso_requerido": 660,
                "deficit": 660 - descanso
            }
            reporte["restricciones_violadas"].append(violacion_descanso)
            reporte["factible"] = False
    
    # Agregar resumen ejecutivo
    if reporte["factible"]:
        reporte["mensaje"] = "Todas las restricciones se cumplen"
    else:
        total_violaciones = len(reporte["restricciones_violadas"])
        reporte["mensaje"] = f"Se encontraron {total_violaciones} violaciones"
    
    return reporte


# Función auxiliar para formatear minutos a horas
def minutos_a_horas(minutos):
    horas = minutos // 60
    minutos_rest = minutos % 60
    return f"{horas}:{minutos_rest:02d}"


# Prueba con el input proporcionado
turnos_empleado = [
    {'inicio': 480, 'fin': 900},    # 8:00 - 15:00
    {'inicio': 1440, 'fin': 2000},  # 24:00 - 33:20
    {'inicio': 2300, 'fin': 2800}   # 38:20 - 46:40
]

resultado = auditar_horario(turnos_empleado)

# Mostrar reporte formateado
print("\nReporte de auditoría:")
print(f"{resultado['mensaje']}")
print(f"Turnos analizados: {resultado['turnos_analizados']}")
print()

# Detalles por turno
print("Detalles por turno:")

for detalle in resultado['detalles_turnos']:
    inicio = minutos_a_horas(detalle['inicio'])
    fin = minutos_a_horas(detalle['fin'])
    estado = "Válido" if detalle['es_valido'] else "Inválido"
    print(f"Turno {detalle['indice']}: {inicio} → {fin} ({detalle['duracion']} min) - {estado}")
    
    if not detalle['es_valido']:
        for violacion in detalle.get('violaciones', []):
            print(f"{violacion['descripcion']}")

print()

# Violaciones encontradas
if resultado['restricciones_violadas']:
    print("Violaciones encontradas:")

    for i, violacion in enumerate(resultado['restricciones_violadas'], 1):
        print(f"{i}. {violacion['descripcion']}")
else:
    print("No se encontraron violaciones")
    print("   - Todos los turnos respetan el máximo de 8 horas")
    print("   - Todos los descansos entre turnos son de al menos 11 horas")
    print("   - Todos los turnos tienen fin > inicio")


