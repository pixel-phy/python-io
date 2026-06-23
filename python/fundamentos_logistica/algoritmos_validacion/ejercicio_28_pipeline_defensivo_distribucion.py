"""Ejercicio 28: El Pipeline Defensivo de Distribución Urbana (VRP)

Un ruteador automático va a asignar un lote de entregas a un chofer. Los datos crudos llegan como una lista 
de diccionarios con formato de texto:

    entregas_crudas = [
    {"orden": "1234561", "peso": "250", "ventana": "480,600", "llegada_estimada": "500"},
    {"orden": "1235461", "peso": "400", "ventana": "540,700", "llegada_estimada": "560"},
    {"orden": "6543210", "peso": "150", "ventana": "600,800", "llegada_estimada": "750"}
]
    Debemos diseñar un pipeline completo que procese estos datos siguiendo este estricto orden de filtrado:

    1. Filtro 1 (Integridad de datos): Valida el número de "orden" usando el algoritmo de 
    Verhoeff. Si el ID es inválido, descartar la entrega por completo y regístrarla como "Error de Datos".

    2. Filtro 2 (Restricción de Ventana de Tiempo): Para las órdenes con ID válido,
    verifica si la "llegada_estimada" cumple con la Restricción de la "ventana" (inicio <= llegada_estimada <= fin).
    si no la cumple, márcala como "Infactible por Horario".

    3. Filtro 3 (Restricción de Capacidad Global): Suma el peso de las órdenes que pasaron ambos filtros anteriores.
    El camión tiene una capacidad máxima de 500 kg. Si la suma excede los 500 kg, el lote completo se declara "Infactible
    por peso total para la Ruta".

    Retornar un reporte integrado (puede ser un diccionario) estructurado donde se identifique qué órdenes fallaron
    por datos, cuáles por horario, cuáles son totalmente válidas, el peso total final aceptado y si la ruta es finalmente
    aprobada o rechazada para el Solver. """

def verhoeff_validate(numero: str) -> bool:
    """
    Valida un número usando el algoritmo de Verhoeff.
    Retorna True si es válido, False en caso contrario.
    """
    # Tablas del algoritmo Verhoeff
    d = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
        [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
        [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
        [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
        [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
        [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ]
    
    p = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
        [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
        [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
        [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
        [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
    ]
    
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
    
    # Verificar que sea solo dígitos
    if not numero.isdigit():
        return False
    
    # Algoritmo de Verhoeff
    c = 0
    digitos = [int(d) for d in reversed(numero)]
    
    for i, digito in enumerate(digitos):
        c = d[c][p[i % 8][digito]]
    
    return c == 0


def procesar_pipeline_distribucion(entregas_crudas):
    """
    Procesa el pipeline completo de distribución urbana.
    
    Args:
        entregas_crudas: Lista de diccionarios con los datos de entregas
    
    Returns:
        dict: Reporte estructurado con todos los resultados
    """
    CAPACIDAD_MAXIMA = 500
    
    # Inicializar resultados
    reporte = {
        "ordenes_rechazadas_datos": [],
        "ordenes_rechazadas_horario": [],
        "ordenes_validas": [],
        "detalle_ordenes_validas": [],
        "peso_total_aceptado": 0,
        "ruta_aprobada": False,
        "resumen_ejecucion": {
            "total_ordenes": len(entregas_crudas),
            "filtro1_pasaron": 0,
            "filtro2_pasaron": 0,
            "filtro3_pasaron": 0,
            "rechazadas_datos": 0,
            "rechazadas_horario": 0,
            "rechazadas_peso": 0
        }
    }
    
    # Variables para el pipeline
    ordenes_filtro1 = []  # Ordenes que pasan el filtro 1 (ID válido)
    peso_acumulado = 0
    
    print("\n")
    print("Iniciando Pipeline de Distribución")
    
    # Filtro 1:
    print("\nValidación de integridad de datos (Verhoeff)")
    
    for entrega in entregas_crudas:
        orden = entrega.get("orden", "")
        peso = entrega.get("peso", "0")
        ventana = entrega.get("ventana", "")
        llegada = entrega.get("llegada_estimada", "")
        
        print(f"\nProcesando orden: {orden}")
        
        # Validar formato básico
        if not orden or not peso or not ventana or not llegada:
            print(f"  Datos incompletos - orden: {orden}")
            reporte["ordenes_rechazadas_datos"].append({
                "orden": orden,
                "motivo": "Datos incompletos"
            })
            reporte["resumen_ejecucion"]["rechazadas_datos"] += 1
            continue
        
        # Validar con Verhoeff
        if not verhoeff_validate(orden):
            print(f"  ID inválido (Verhoeff) - {orden}")
            reporte["ordenes_rechazadas_datos"].append({
                "orden": orden,
                "motivo": "ID inválido (Verhoeff)"
            })
            reporte["resumen_ejecucion"]["rechazadas_datos"] += 1
            continue
        
        # Si pasa el filtro 1, guardar para el siguiente filtro
        print(f"  ID válido")
        ordenes_filtro1.append(entrega)
        reporte["resumen_ejecucion"]["filtro1_pasaron"] += 1
    
    # Filtro 2
    print("\nValidación de ventana de tiempo")
    
    ordenes_filtro2 = []  # Ordenes que pasan el filtro 2 (horario válido)
    
    for entrega in ordenes_filtro1:
        orden = entrega.get("orden", "")
        ventana_str = entrega.get("ventana", "")
        llegada_str = entrega.get("llegada_estimada", "")
        
        print(f"\nProcesando orden: {orden}")
        print(f"  Ventana: {ventana_str}, Llegada estimada: {llegada_str}")
        
        try:
            # Parsear ventana: "inicio,fin"
            partes = ventana_str.split(",")
            if len(partes) != 2:
                raise ValueError("Formato de ventana inválido")
            
            inicio = int(partes[0].strip())
            fin = int(partes[1].strip())
            llegada = int(llegada_str.strip())
            
            # Verificar restricción de ventana
            if inicio <= llegada <= fin:
                print(f"  Cumple ventana: {inicio} <= {llegada} <= {fin}")
                ordenes_filtro2.append(entrega)
                reporte["resumen_ejecucion"]["filtro2_pasaron"] += 1
            else:
                print(f"  Fuera de ventana: {inicio} <= {llegada} <= {fin} - NO CUMPLE")
                reporte["ordenes_rechazadas_horario"].append({
                    "orden": orden,
                    "motivo": f"Llegada {llegada} fuera de ventana [{inicio}, {fin}]"
                })
                reporte["resumen_ejecucion"]["rechazadas_horario"] += 1
                
        except (ValueError, AttributeError) as e:
            print(f"  Error al parsear datos: {e}")
            reporte["ordenes_rechazadas_horario"].append({
                "orden": orden,
                "motivo": f"Error en datos de tiempo: {str(e)}"
            })
            reporte["resumen_ejecucion"]["rechazadas_horario"] += 1
    
    # Filtro 3
    print("\nValidación de capacidad global")
    
    peso_acumulado = 0
    ordenes_filtro3 = []  # Ordenes que pasan el filtro 3 (capacidad)
    
    for entrega in ordenes_filtro2:
        orden = entrega.get("orden", "")
        peso_str = entrega.get("peso", "0")
        
        print(f"\nProcesando orden: {orden}")
        print(f"  Peso declarado: {peso_str} kg")
        
        try:
            peso = int(peso_str)
            if peso < 0:
                raise ValueError("El peso no puede ser negativo")
            
            # Verificar capacidad acumulada
            if peso_acumulado + peso <= CAPACIDAD_MAXIMA:
                peso_acumulado += peso
                ordenes_filtro3.append(entrega)
                print(f"    Peso acumulado: {peso_acumulado}/{CAPACIDAD_MAXIMA} kg")
            else:
                print(f"    Excede capacidad: {peso_acumulado} + {peso} = {peso_acumulado + peso} > {CAPACIDAD_MAXIMA}")
                reporte["ordenes_rechazadas_horario"].append({
                    "orden": orden,
                    "motivo": f"Excede capacidad: {peso_acumulado} + {peso} > {CAPACIDAD_MAXIMA}"
                })
                reporte["resumen_ejecucion"]["rechazadas_peso"] += 1
                
        except (ValueError, AttributeError) as e:
            print(f"    Error en peso: {e}")
            reporte["ordenes_rechazadas_horario"].append({
                "orden": orden,
                "motivo": f"Error en datos de peso: {str(e)}"
            })
            reporte["resumen_ejecucion"]["rechazadas_peso"] += 1
    
    # Reporte final
    
    # Actualizar reporte con órdenes válidas
    for entrega in ordenes_filtro3:
        reporte["ordenes_validas"].append(entrega.get("orden", ""))
        reporte["detalle_ordenes_validas"].append({
            "orden": entrega.get("orden", ""),
            "peso": entrega.get("peso", "0"),
            "ventana": entrega.get("ventana", ""),
            "llegada_estimada": entrega.get("llegada_estimada", "")
        })
    
    reporte["peso_total_aceptado"] = peso_acumulado
    reporte["ruta_aprobada"] = (
        len(reporte["ordenes_rechazadas_datos"]) == 0 and
        len(reporte["ordenes_rechazadas_horario"]) == 0 and
        peso_acumulado <= CAPACIDAD_MAXIMA and
        len(ordenes_filtro3) > 0  # Al menos una orden válida
    )
    
    reporte["resumen_ejecucion"]["filtro3_pasaron"] = len(ordenes_filtro3)
    
    return reporte


def imprimir_reporte(reporte):
    """
    Imprime el reporte de manera formateada y legible.
    """
    print("\n")
    print("Reporte final")
    
    print("\nResumen: ")
    print(f"  Total órdenes procesadas: {reporte['resumen_ejecucion']['total_ordenes']}")
    print(f"  Filtro 1 (Datos válidos): {reporte['resumen_ejecucion']['filtro1_pasaron']}")
    print(f"  Filtro 2 (Horario válido): {reporte['resumen_ejecucion']['filtro2_pasaron']}")
    print(f"  Filtro 3 (Capacidad): {reporte['resumen_ejecucion']['filtro3_pasaron']}")
    print(f"  Rechazadas por datos: {reporte['resumen_ejecucion']['rechazadas_datos']}")
    print(f"  Rechazadas por horario: {reporte['resumen_ejecucion']['rechazadas_horario']}")
    
    print("\nÓrdenes rechazadas: ")
    
    if reporte["ordenes_rechazadas_datos"]:
        print("\n  [ERROR DE DATOS]")
        for item in reporte["ordenes_rechazadas_datos"]:
            print(f"    • Orden {item['orden']}: {item['motivo']}")
    else:
        print("  No hay órdenes rechazadas por datos")
    
    if reporte["ordenes_rechazadas_horario"]:
        print("\n  [INFACTIBLE POR HORARIO]")
        for item in reporte["ordenes_rechazadas_horario"]:
            print(f"    • Orden {item['orden']}: {item['motivo']}")
    else:
        print("  No hay órdenes rechazadas por horario ")
    
    print("\nÓrdenes válidas:")
    if reporte["ordenes_validas"]:
        for orden in reporte["ordenes_validas"]:
            print(f"    • Orden {orden}")
    else:
        print("    No hay órdenes válidas")
    
    print("\nPeso total aceptado:")
    print(f"    {reporte['peso_total_aceptado']} kg")
    
    print("\nDecisión final de la ruta:")
    if reporte["ruta_aprobada"]:
        print(" APROBADA - La ruta es factible para el Solver")
    else:
        print(" RECHAZADA - La ruta NO es factible para el Solver")
        if not reporte["ordenes_validas"]:
            print("    Motivo: No hay órdenes válidas")
        elif reporte["peso_total_aceptado"] > 500:
            print(f"    Motivo: Peso excede capacidad máxima (500 kg)")

# prueba

if __name__ == "__main__":
    entregas_crudas = [
        {"orden": "1234561", "peso": "250", "ventana": "480,600", "llegada_estimada": "500"},
        {"orden": "1235461", "peso": "400", "ventana": "540,700", "llegada_estimada": "560"},
        {"orden": "6543210", "peso": "150", "ventana": "600,800", "llegada_estimada": "750"}
    ]
    
    # Procesar el pipeline
    reporte = procesar_pipeline_distribucion(entregas_crudas)
    
    # Imprimir reporte formateado
    imprimir_reporte(reporte)
