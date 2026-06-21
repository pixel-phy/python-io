"""Ejercicio 04: Filtro de Sanitización de Datos para Modelos de Ruteo

Nos entregan un archivo log corrupto (simulado en una lista de strings) con 10.000 solicitudes de despacho
de carga para un modelo de optimización lineal de flota. Algunas solicitudes tienen IDs de contenedores mal 
digitados (fallan Luhn) y otras tienen caracteres basura. Si metes datos corruptos al solucionador (Solver),
el costo computacional se disparará o el modelo será infactible.
    - Escirbir una función de alta eficiencia que filtr una lista de IDs, descarte los inválidos, limpie 
    los caracteres no numéricos y devuelva una lista de IDs limpios listos para el Solver, junto con un 
    reporte de eficiencia (cuántos se descartaron).
    - Input de prueba: ["4000001232", "4000X01232", "73500000000000017", "9999999999"] """

def validar_luhn_optimizada(cadena_numerica: str) -> bool:
    """Valida una cadena puramente numérica con Luhn clásico.
    
    Optimizado: Asume que el string ya viene limpio para ahorrar tiempo de CPU.
    """
    suma = 0
    # Usamos un flag booleano alternante para evitar la creación de listas
    multiplicar_por_dos = False
    
    # Recorremos al revés usando el iterador nativo de Python
    for char in reversed(cadena_numerica):
        digito = int(char)
        if multiplicar_por_dos:
            doble = digito * 2
            suma += doble - 9 if doble > 9 else doble
        else:
            suma += digito
        multiplicar_por_dos = not multiplicar_por_dos
        
    return suma % 10 == 0


def filtrar_ids_ruteo(batch: list[str]) -> tuple[list[str], dict]:
    """Procesa, sanitiza y audita masivamente IDs de entrada para el Solver."""
    total_procesados = len(batch)
    if total_procesados == 0:
        return [], {"error": "Batch vacío"}

    ids_validos = []
    corruptos = 0
    invalidos_luhn = 0
    sanitizados = 0

    for id_raw in batch:
        # 1. Extracción de dígitos en un solo paso
        id_limpio = "".join(char for char in id_raw if char.isdigit())
        
        if not id_limpio:
            corruptos += 1
            continue
            
        if len(id_limpio) != len(id_raw):
            sanitizados += 1

        # 2. Validación directa (la función ya recibe el string limpio)
        if validar_luhn_optimizada(id_limpio):
            ids_validos.append(id_limpio)
        else:
            invalidos_luhn += 1

    # Métricas de rendimiento logístico
    total_validos = len(ids_validos)
    tasa_aceptacion = (total_validos / total_procesados) * 100
    
    reporte = {
        "total_procesados": total_procesados,
        "ids_validos": total_validos,
        "descartados": total_procesados - total_validos,
        "tasa_aceptacion": f"{tasa_aceptacion:.2f}%",
        "detalle_descartes": {
            "completamente_corruptos": corruptos,
            "fallaron_luhn": invalidos_luhn,
            "modificados_y_salvados": sanitizados
        },
        "calidad_fuente_datos": "ALTA" if tasa_aceptacion > 70 else "MEDIA" if tasa_aceptacion > 40 else "BAJA"
    }

    return ids_validos, reporte

batch_prueba = [
    "4000001232",          # Válido
    "4000X01232",          # Corrupto (tiene X)
    "73500000000000017",   # Válido (SSCC)
    "9999999999"           # Inválido (no pasa Luhn)
]

ids_limpios, reporte = filtrar_ids_ruteo(batch_prueba)

print("IDs válidos encontrados:")
for idx, id_valido in enumerate(ids_limpios, 1):
    print(f"  {idx}. {id_valido}")

print("\nREPORTE DE EFICIENCIA:")
for key, value in reporte.items():
    if key == "detalle_descartes":
        print(f"  {key}:")
        for sub_key, sub_value in value.items():
            print(f"    {sub_key}: {sub_value}")
    else:
        print(f"  {key}: {value}")
