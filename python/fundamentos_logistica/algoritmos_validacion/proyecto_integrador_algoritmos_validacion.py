"""Proyecto integrador: Sistema de Control de tráfico Marítimo y Despacho Portuario (Hub Logístico Intermodal)

    En los puertos automatizados de contenedores, la gestión de la terminal es un problema crítico
    de optimización conocido como BAP (Berth Allocation Problem - Problema de asignación de muelles). 
    Los barcos portacontenedores llegan a la costa y el sistema debe validar su identidad, verificar
    que tengan ventanas de tiempo aprobadas para atracar, y asegurar que la carga y descargar de contenedores 
    no sature la capacidad de almacenamiento temporal del muelle, respetando la conservación de flujos de salida 
    ferroviaria.

    Si los datos de un buque vienen alterados o violan restricciones, el puerto puede sufrir un cuello
    de botella, generando multas millonarias por demoras.

    Eres el ingeniero de Optiimización Principal de un puerto intermodal de contenedores. El sistema central
    recibe un lote de datos en formato crudo de los buques que solicitan autorización para atracar e 
    iniciar operaciones hoy. Tu misión es programar el motor de auditoría y filtrado que procesará este lote
    antes de enviarlo al Solver de asignación de grúas.

    El flujo del programa debe implementar de forma estricta los siguientes módulos:

    [Datos Crudos] ➔ 1. Validación de ID (Damm) ➔ 2. Ventana de Tiempo ➔ 3. Conservación de Flujo (Grúas) ➔ [Solver]

    Requerimientos técnicos del Pipeline

    1. Fase 1: Control de Identidad Marítima (Algoritmo de Damm):
    - Cada buque tiene un identificador de viaje de 5 dígitos en texto. El 5to dígito es el verificador. 
    - Debes validar el ID usando el algoritmo de Damm. Si el ID es inválido, el buque se rechaza inmediatamente
    por "Fallo de Seguridad e Integridad de Identificador".

    2. Fase 2: Ventana de tiempo de Atraque (Intervalos Cerrados):
    - El puerto opera en minutos indexados desde las 00:00 horas (0 a 1440 minutos).
    - Cada busque válido debe evaluar si su hora_llegada estimada cae dentro de la ventana de tiempo reservada
    (inicio_ventana, fin_ventana). Si llega fuera de tiempo, se rechaza por "infactibilidad de Horario de Atraque".

    3. Fase 3: Conservación de Flujo Operativo de Carga (Equilibrio de Redes):
    - Para evitar la saturación del muelle, los buques deben cumplir con una política estricta de balance de inventario:
    la cantidad de contenedores que el buque descarga en el muelle (unidades_entrantes) sumada al inventario inicial
    el andén, debe ser desalojada exactamente por los trenes de carga asignados (unidades_salientes).
    - Restricción matemática: unidades__entrantes - unidades_salientes = 0 (asumiendo balance neutro en andén para transbordo directo).
    Si hay un residuo diferente de cero, el buque se congela por "Infactibilidad de Conservación de Flujo en Terminal".

    4. Fase 4: Consolidación y Reporte Ejecutivo:

    - Al final, debes agrupar los barcos aceptados, calcular el total de contenedores que ingresarán al puerto de forma 
    segura y emitir la decisión final: si al menos un buque fue aceptado y ningún dato interrumpió el flujo crítico, 
    la jornada portuaria se declara "APROBADA PARA OPTIMIZACIÓN".

    Dataset de Prueba:

    buques_en_espera = [
    {
        "buque_id": "57240",          # ID Válido en Damm
        "hora_llegada": 500,          # Llega a las 8:20 AM
        "ventana": (480, 600),        # Ventana aprobada
        "descarga_contenedores": 120, 
        "despacho_trenes": [60, 60]   # Suma 120 (Flujo Conservado)
    },
    {
        "buque_id": "52740",          # ID Inválido en Damm (Transposición)
        "hora_llegada": 550, 
        "ventana": (500, 700),
        "descarga_contenedores": 200,
        "despacho_trenes": [200]
    },
    {
        "buque_id": "36742",          # ID Válido en Damm
        "hora_llegada": 900,          # Llega a las 3:00 PM
        "ventana": (600, 800),        # Ventana cerraba a la 1:20 PM -> ¡Alerta!
        "descarga_contenedores": 150,
        "despacho_trenes": [150]
    },
    {
        "buque_id": "42300",          # ID Válido en Damm
        "hora_llegada": 1100,         
        "ventana": (1000, 1200),      
        "descarga_contenedores": 300, 
        "despacho_trenes": [150, 100] # Suma 250 -> ¡Alerta! Faltan 50 por despachar
    }
]
    Diseñar el script completo en Python que resuelva este ecosistema industrial. Estructura las 
    funciones auxiliares de validación, el bucle Principal de filtrado secuencial y una función 
    de impresión de reporte con un formato profesional legible"""

def algoritmo_damm(id_verificar: str) -> bool:
    """
    Implementación del algoritmo de Damm para validación de dígito verificador.
    Tabla de operación Damm para base 10.
    """
    # Tabla de Damm (matriz de transición)
    tabla_damm = [
        [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
        [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
        [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
        [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
        [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
        [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
        [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
        [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
        [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
        [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
    ]
    
    # Convertir a dígitos y aplicar algoritmo
    digitos = [int(c) for c in id_verificar.strip()]
    interim = 0
    for digito in digitos:
        interim = tabla_damm[interim][digito]
    
    # El resultado debe ser 0 para ID válido
    return interim == 0

def validar_id(id_buque: str) -> bool:
    """
    Valida que el ID tenga exactamente 5 dígitos y sea válido según Damm.
    """
    if not id_buque or len(id_buque) != 5:
        return False
    if not id_buque.isdigit():
        return False
    return algoritmo_damm(id_buque)


def validar_ventana_tiempo(hora_llegada: int, inicio_ventana: int, fin_ventana: int) -> bool:
    """
    Valida que la hora de llegada esté dentro de la ventana de tiempo (intervalo cerrado).
    El puerto opera de 0 a 1440 minutos.
    """
    if hora_llegada < 0 or hora_llegada > 1440:
        return False
    if inicio_ventana < 0 or fin_ventana > 1440:
        return False
    if inicio_ventana > fin_ventana:
        return False
    
    return inicio_ventana <= hora_llegada <= fin_ventana

def validar_conservacion_flujo(descarga_contenedores: int, despacho_trenes: list) -> bool:
    """
    Valida la conservación de flujo: descarga = suma de despacho en trenes.
    """
    if not despacho_trenes or any(t < 0 for t in despacho_trenes):
        return False
    
    total_salida = sum(despacho_trenes)
    return descarga_contenedores == total_salida


def formatear_tiempo(minutos: int) -> str:
    """
    Convierte minutos a formato HH:MM para reportes legibles.
    """
    horas = minutos // 60
    minutos_rest = minutos % 60
    return f"{horas:02d}:{minutos_rest:02d}"

def imprimir_reporte(buques_aceptados: list, buques_rechazados: list, total_contenedores: int) -> None:
    """
    Imprime el reporte ejecutivo en formato profesional.
    """
    print("\n")
    print(" Reporte Ejecutivo: Sistema de Control de Tráfico marítimo ".center(80))
    
    # Resumen general
    print("\nResumen de procesamiento:")
    print(f"    Buques Aceptados: {len(buques_aceptados)}")
    print(f"    Buques Rechazados: {len(buques_rechazados)}")
    print(f"    Total Contenedores en Flujo Seguro: {total_contenedores:,}")
    
    # Detalle de buques aceptados
    if buques_aceptados:
        print("\n   Buques aceptados para Optimización:")
        print(f"{'ID':<10} {'Llegada':<15} {'Ventana':<20} {'Descarga':<12} {'Trenes':<15}")
        for buque in buques_aceptados:
            llegada = formatear_tiempo(buque["hora_llegada"])
            ventana = f"{formatear_tiempo(buque['ventana'][0])} - {formatear_tiempo(buque['ventana'][1])}"
            trenes = " + ".join([str(t) for t in buque["despacho_trenes"]])
            print(f"{buque['buque_id']:<10} {llegada:<15} {ventana:<20} {buque['descarga_contenedores']:<12} {trenes:<15}")
    
    # Detalle de buques rechazados
    if buques_rechazados:
        print("\nBuques rechazados:")

        for i, (buque, razon) in enumerate(buques_rechazados, 1):
            print(f"   {i}. ID {buque['buque_id']} → {razon}")
    
    # Decisión final
    print("\n")
    if buques_aceptados and not any(b[1] for b in buques_rechazados):
        print(" Decisión Final: Jornada portuaria aprobada para optimización".center(80))
    elif buques_aceptados:
        print("Decisión Final: Aprobada parcialmente - Revisiones en curso".center(80))
    else:
        print("Decisión Final: Jornada Rechazada - No hay buques válidos".center(80))

def procesar_lote(buques_en_espera: list) -> tuple:
    """
    Pipeline principal de procesamiento con filtrado secuencial.
    
    Returns:
        tuple: (buques_aceptados, buques_rechazados, total_contenedores)
    """
    buques_aceptados = []
    buques_rechazados = []
    
    print("\n Procesamiento Lotes de Buques...")
    
    for idx, buque in enumerate(buques_en_espera, 1):
        print(f"\n  Procesamiento de Buque #{idx} - ID: {buque['buque_id']}")
        
        # FASE 1: Validación de ID (Damm)
        if not validar_id(buque["buque_id"]):
            razon = "Fallo de Seguridad e Integridad de Identificador"
            buques_rechazados.append((buque, razon))
            print(f"Rechazado: {razon}")
            continue
        
        print(f"    ID validado correctamente")
        
        # FASE 2: Ventana de Tiempo
        inicio, fin = buque["ventana"]
        if not validar_ventana_tiempo(buque["hora_llegada"], inicio, fin):
            razon = "Infactibilidad de Horario de Atraque"
            buques_rechazados.append((buque, razon))
            print(f"    Rechazado: {razon} (Llega: {formatear_tiempo(buque['hora_llegada'])}, Ventana: {formatear_tiempo(inicio)}-{formatear_tiempo(fin)})")
            continue
        
        print(f"    Ventana de tiempo aprobada")
        
        # FASE 3: Conservación de Flujo
        if not validar_conservacion_flujo(buque["descarga_contenedores"], buque["despacho_trenes"]):
            razon = "Infactibilidad de Conservación de Flujo en Terminal"
            buques_rechazados.append((buque, razon))
            total_trenes = sum(buque["despacho_trenes"])
            print(f" Rechazado: {razon} (Descarga: {buque['descarga_contenedores']}, Trenes: {total_trenes})")
            continue
        
        print(f"    Flujo conservado correctamente")
        
        # BUQUE ACEPTADO
        buques_aceptados.append(buque)
        print(f"Buque aceptado para optimización")

    # Calcular total de contenedores
    total_contenedores = sum(b["descarga_contenedores"] for b in buques_aceptados)
    
    return buques_aceptados, buques_rechazados, total_contenedores


# DATASET DE PRUEBA
buques_en_espera = [
    {
        "buque_id": "57240",          # ID Válido en Damm
        "hora_llegada": 500,          # Llega a las 8:20 AM
        "ventana": (480, 600),        # Ventana aprobada
        "descarga_contenedores": 120, 
        "despacho_trenes": [60, 60]   # Suma 120 (Flujo Conservado)
    },
    {
        "buque_id": "52740",          # ID Inválido en Damm (Transposición)
        "hora_llegada": 550, 
        "ventana": (500, 700),
        "descarga_contenedores": 200,
        "despacho_trenes": [200]
    },
    {
        "buque_id": "36742",          # ID Válido en Damm
        "hora_llegada": 900,          # Llega a las 3:00 PM
        "ventana": (600, 800),        # Ventana cerraba a la 1:20 PM -> ¡Alerta!
        "descarga_contenedores": 150,
        "despacho_trenes": [150]
    },
    {
        "buque_id": "42300",          # ID Válido en Damm
        "hora_llegada": 1100,         
        "ventana": (1000, 1200),      
        "descarga_contenedores": 300, 
        "despacho_trenes": [150, 100] # Suma 250 -> ¡Alerta! Faltan 50 por despachar
    }
]


def main():
    """
    Función principal que ejecuta el sistema completo.
    """
    print(" SISTEMA DE CONTROL DE TRÁFICO MARÍTIMO Y DESPACHO PORTUARIO".center(80))
    
    # Ejecutar pipeline de procesamiento
    buques_aceptados, buques_rechazados, total_contenedores = procesar_lote(buques_en_espera)
    
    # Generar reporte ejecutivo
    imprimir_reporte(buques_aceptados, buques_rechazados, total_contenedores)
    
    return buques_aceptados, buques_rechazados, total_contenedores


if __name__ == "__main__":
    main()
