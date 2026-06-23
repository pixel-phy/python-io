"""Ejercicio 27: Cross-Docking Blindado con Conservación de Flujo 
    A un centro de distribución (Cross-Docking) llegan tarimas de proveedores externos. El manifiesto 
    de entrada viene en strings formato: "ID_GS1-128,CANTIDAD".

    1. Primero debes parsear el código GS!-128 (extrayendo el GTIN, lote y cantidad) y verificar que sea válido
    (pasando también la prueba del dígito de control EAN-13).

     2. Los artículos válidos se transfieren directamente a los camiones de salida.

     3. Debe sumar la cantidad total que ingresó de forma válida y compararla contra el mannifiesto de salida
     (una lista simple de enteros). Evalúa si se cumple la restricción de conservación de flujo en el andén
    (Entradas Válidas = Salidas).

    Input de prueba:
    manifiesto_entrada = [
    "(01)97501055311224(10)LOTE2026(30)100",  # Válido (EAN-13 termina en 4)
    "(01)97501055311220(10)LOTE2026(30)150"   # Corrupto (EAN-13 termina en 0)
    ]
    manifiesto_salida = [60, 40] """

import re

def validar_ean13(gtin: str) -> bool:
    """Valida un código GTIN de 13 dígitos usando el algoritmo internacional EAN-13."""
    if len(gtin) != 13 or not gtin.isdigit():
        return False
        
    digito_control = int(gtin[-1])
    digitos = [int(d) for d in gtin[:-1]]
    
    # AJUSTE DE ÍNDICES: 
    # Índices pares (0,2,4...) -> Posiciones físicas IMPARES (Peso 1)
    # Índices impares (1,3,5...) -> Posiciones físicas PARES (Peso 3)
    suma_pos_impares_fisicas = sum(digitos[i] for i in range(0, 12, 2)) 
    suma_pos_pares_fisicas = sum(digitos[i] for i in range(1, 12, 2))   
    
    # El factor multiplicador por 3 se asocia a las posiciones pares físicas
    calculado = (10 - ((suma_pos_impares_fisicas + (suma_pos_pares_fisicas * 3)) % 10)) % 10
    
    return calculado == digito_control

def parsear_gs1_128(codigo: str) -> dict:
    """
    Parsea un código GS1-128 y extrae GTIN (01), lote (10) y cantidad (30).
    Retorna un diccionario con los datos o None si el formato es inválido.
    """
    # Patrón para extraer los campos GS1-128
    # (01)GTIN(10)LOTE(30)CANTIDAD
    patron = r"\(01\)(\d{13})\(10\)([^()]+)\(30\)(\d+)"
    
    match = re.search(patron, codigo)
    if not match:
        return None
    
    gtin = match.group(1)
    lote = match.group(2)
    cantidad = int(match.group(3))
    
    return {
        "gtin": gtin,
        "lote": lote,
        "cantidad": cantidad,
        "codigo_completo": codigo
    }


def procesar_cross_docking(manifiesto_entrada, manifiesto_salida):
    """
    Procesa el cross-docking verificando la conservación de flujo.
    
    Args:
        manifiesto_entrada: Lista de strings con códigos GS1-128
        manifiesto_salida: Lista de enteros con cantidades de salida
    
    Returns:
        dict: {
            'entradas_validas': Lista de dicts con datos de entradas válidas,
            'total_entradas_validas': int,
            'total_salidas': int,
            'conservacion_flujo': bool
        }
    """
    entradas_validas = []
    total_entradas = 0
    
    for codigo in manifiesto_entrada:
        # Parsear el código GS1-128
        datos = parsear_gs1_128(codigo)
        
        if datos is None:
            continue
        
        # Validar GTIN con EAN-13
        if not validar_ean13(datos["gtin"]):
            continue
        
        # Si es válido, agregar a la lista
        entradas_validas.append(datos)
        total_entradas += datos["cantidad"]
    
    # Calcular total de salidas
    total_salidas = sum(manifiesto_salida)
    
    # Verificar conservación de flujo
    conservacion_flujo = (total_entradas == total_salidas)
    
    return {
        "entradas_validas": entradas_validas,
        "total_entradas_validas": total_entradas,
        "total_salidas": total_salidas,
        "conservacion_flujo": conservacion_flujo
    }


# Prueba con el input proporcionado
if __name__ == "__main__":
    manifiesto_entrada = [
        "(01)97501055311224(10)LOTE2026(30)100",  # Válido (EAN-13 termina en 4)
        "(01)97501055311220(10)LOTE2026(30)150"   # Corrupto (EAN-13 termina en 0)
    ]
    manifiesto_salida = [60, 40]
    
    resultado = procesar_cross_docking(manifiesto_entrada, manifiesto_salida)
    
    print("Resultados: ")
    print(f"Entradas válidas procesadas: {len(resultado['entradas_validas'])}")
    for entrada in resultado['entradas_validas']:
        print(f"  - GTIN: {entrada['gtin']}, Lote: {entrada['lote']}, Cantidad: {entrada['cantidad']}")
    
    print(f"\nTotal entradas válidas: {resultado['total_entradas_validas']}")
    print(f"Total salidas: {resultado['total_salidas']}")
    print(f"Conservación de flujo: {resultado['conservacion_flujo']}")
