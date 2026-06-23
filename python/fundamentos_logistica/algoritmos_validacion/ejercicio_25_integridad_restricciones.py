""" Ejercicios Integradores: 

Construir algoritmos capaces de procesasr una carga de datos cruda, aplicar filtros de integridad (checksums) 
para descartar ruido de transcripción, y posteriormente someter los datos limpios a las inecuaciones 
de restricciones operativas del modelo.

    ¿Por qué se utiliza en OR?
    Si pasamos datos corruptos al Solver, corremos dos grandes riesgos:
1. Infactibilidad Fantasma: El solver dice que el problema no tiene solución porque un ID mal 
escrito alteró un parámetro clave, cuando en realidad la operación física sí es viable.
2. Suboptimización Ciega: El Solver encuentra una "solución óptima" basada en un número de factura o 
peso equivocado, lo que lleva a tomar decisiones erróneas en el mundo real (como evitar un camión medio vacío).

Al integrar ambos mundos en un solo pipeline, garantizamos que el Solver reciba únicamente datos 
matemáticamente limpios y operativamente factibles. """

def validar_luhn(numero: str) -> bool:
    """Función de soporte (Día 5)"""
    if not numero or not numero.isdigit(): return False
    digitos = [int(d) for d in numero]
    suma, duplicar = 0, False
    for i in range(len(digitos) - 1, -1, -1):
        d = digitos[i]
        if duplicar:
            d *= 2
            if d > 9: d -= 9
        suma += d
        duplicar = not duplicar
    return suma % 10 == 0

def pipeline_logistico_integrado(ordenes_crudas: list[str], capacidad_max: float) -> dict:
    reporte = {"ordenes_validas": [], "ordenes_corruptas": [], "factible_para_solver": True, "detalles": ""}
    peso_acumulado = 0.0
    
    for registro in ordenes_crudas:
        partes = registro.split(",")
        id_orden, peso_str = partes[0].strip(), partes[1].strip()
        
        # Paso 1: Filtro de Integridad de Datos (Día 5)
        if not validar_luhn(id_orden):
            reporte["ordenes_corruptas"].append(registro)
            continue
            
        # Paso 2: Evaluación Operativa (Día 4)
        peso = float(peso_str)
        peso_acumulado += peso
        reporte["ordenes_validas"].append({"id": id_orden, "peso": peso})
        
    # Paso 3: Validación de Restricción Global (Día 4)
    if peso_acumulado > capacidad_max:
        reporte["factible_para_solver"] = False
        reporte["detalles"] = f"Infactible: El peso total ({peso_acumulado} kg) excede la capacidad del camión ({capacidad_max} kg)."
    else:
        reporte["detalles"] = f"Factible: {peso_acumulado} kg listos para optimización."
        
    return reporte
