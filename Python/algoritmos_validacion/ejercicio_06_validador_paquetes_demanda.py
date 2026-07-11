"""Ejercicio 06: Validador de Paquetes de Demanda (Módulo 100)

    Queremos diseñar el sistema de mensajería para un modelo de control de inventarios. 
    Cada tienda envía un reporte nocturno de stock con el formato "TIENDA01_SKU405_CANT250".
    El sistema añade al final un guión y un checksum de dos digitos calculador con el módulo 
    100 de la suma de los valores numéricos ASCII de los caracteres.
    - Escribe una función que valide si el paquete de datos mantiene su integridad.
    - Input prueba: "TIENDA01_SKU405_CANT250-84". (Aísla el string del chesum final "84" y 
    valida si la suma de los caracteres del mensaje base módulo 100 da exactamente 84). """

def validador_paquete(paquete: str) -> bool:
    """Valida la integridad de un paquete de datos mediante Checksum módulo 100.
        Optimizado para evitar bucles manuales y blindado contra errores de casteo.
        """
    #1. Separar el mensaje del checksum de forma segura
    partes = paquete.rsplit('-', 1)
    if len(partes) != 2:
        return False

    mensaje, checksum_str = partes

    # 2. Validar de forma defensiva que el checksum sea numértico
    try:
        checksum_esperado = int(checksum_str)
    except ValueError:
        return False # El checksum no es un entero válido.

    # 3. Cálculo de los valores ASCII optimizado a nivel de C nativo
    # Se utuiliza un generador dentro de sum() para evitar alojar listas en memoria
    checksum_calculado = sum(ord(caracter) for caracter in mensaje) % 100

    # 4. Comparación lógica
    return checksum_calculado == checksum_esperado

# Prueba:
paquete_prueba = "TIENDA01_SKU405_CANT250-84"
resultado = validador_paquete(paquete_prueba)

print(f"Paquete: {paquete_prueba}")
print(f"Validez: {resultado}")

paquete_ruido = "TIENDA01_SKU405_CANT250-XX"
print(f"Validez: {not validador_paquete(paquete_ruido)}")
