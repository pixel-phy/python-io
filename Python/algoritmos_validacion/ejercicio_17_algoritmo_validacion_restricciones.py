"""Validación de Restricciones

En Investigación de Operaciones, un modelo de optimización lineal o entera se compone de una función 
objetivo y un conjunto de restricciones (inecuaciones o ecuaciones matemáticas).

    Antes de mandar una matriz de coeficientes a un Solver comercial (PuLP), es una pésima práctica dejar 
que el Solver falle o determine que el problema es infactible sin saber por qué. La vlidación de restricciones
en la capa de datos consiste en evaluar si una solución propuesta (o los datos actuales de la operación) violan
los limites físicos, operativos o legales del sistema antes de correr el algoritmo de optimización. """

# Código de implementación general
def validar_restricciones_carga(pesos: list, volumenes: list, capacidad_max_peso: float, capacidad_max_vol: float) -> dict:
    reporte = {"factible": True, "violaciones": []}
    
    # Restricción 1: No negatividad
    if any(p < 0 for p in pesos) or any(v < 0 for v in volumenes):
        reporte["factible"] = False
        reporte["violaciones"].append("Violación de No Negatividad: Existen valores de peso o volumen negativos.")
    
    # Restricción 2: Capacidad de Peso
    peso_total = sum(pesos)
    if peso_total > capacidad_max_peso:
        reporte["factible"] = False
        exceso = peso_total - capacidad_max_peso
        reporte["violaciones"].append(f"Violación de Capacidad de Peso: Exceso de {exceso} kg.")
        
    # Restricción 3: Capacidad de Volumen
    volumen_total = sum(volumenes)
    if volumen_total > capacidad_max_vol:
        reporte["factible"] = False
        exceso_vol = volumen_total - capacidad_max_vol
        reporte["violaciones"].append(f"Violación de Capacidad de Volumen: Exceso de {exceso_vol} m³.")
        
    return reporte
