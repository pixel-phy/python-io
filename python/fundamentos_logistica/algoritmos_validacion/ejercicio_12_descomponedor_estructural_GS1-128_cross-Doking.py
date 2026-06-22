"""Ejercicio 12: Descomponedor Estructural GS1-128 para Cross-Docking

    En logística avanzada, el código GS1-128 utiliza "identificadores de Aplicación" (IA) entre paréntesis
    para meter múltiples datos en una soba barra. Por ejemplo, el código: "(01)97501234567897(10)LOT-ABC(30)150"
    significa:
        - (01) = identificador del código de proeucto (GTIN de 14 digitos fijos: 97501234567897).
        - (10) = Identificador del número de lote (longitud variable hasta encontrar el siguiente IA, aquí es LOT-ABC).
        - (30) = Identificador de la cantidad de unidades en el pallet (aquí es 150).

    Para alimentar un modelo de Cross-Docking (clasificación inmediata de mercancía de camión de entrada a camión de 
    salida sin pasar por almacén), necestias extraer estos componentes en microsegundos de CPU.

        - Escribe una función optimizada que parsee este string específico, extraiga el GTIM de 14 digitos, verifique
        que los últimos 13 digitos del GTIN cumplan con la regla de validación EAN-13 (ignora el primer digito del GTIN
        de 14, ya que es una variable de empaque), extraiga el lote y la cantidad de unidades como un entero. Retorna
        un diccionarios con los datos limpios.

        Input de prueba: "(01)97501055311220(10)LOTE2026(30)250". """

import json

# Tu función idéntica, solo corregí un pequeñísimo typo en el docstring ("pasear" -> "parsear")
def parsear_gs1_128(codigo: str) -> dict:
    """Parsea un código GS1-128 y extrae GTIN, lote y cantidad."""
    resultado = {'valido': False, 'errores': [], 'datos': {}}

    if not codigo or not codigo.startswith('('):
        resultado['errores'].append("Formato inválido: debe comenzar con '('")
        return resultado

    i, componentes, longitud = 0, {}, len(codigo)

    while i < longitud:
        if codigo[i] == '(':
            if i + 3 >= longitud or codigo[i+3] != ')':
                resultado['errores'].append(f"IA incompleto en posición {i}")
                return resultado
            ia = codigo[i+1:i+3]
            i += 4
            inicio_valor = i
            while i < longitud and codigo[i] != '(':
                i += 1
            componentes[ia] = codigo[inicio_valor:i]
        else:
            resultado['errores'].append(f"Caracter inesperado '{codigo[i]}' en posición {i}")
            return resultado
    
    if '01' not in componentes or '10' not in componentes or '30' not in componentes:
        resultado['errores'].append("Faltan componentes requeridos (01, 10 o 30)")
        return resultado
    
    gtin = componentes['01']
    if len(gtin) != 14 or not gtin.isdigit():
        resultado['errores'].append("GTIN inválido (debe tener 14 dígitos numéricos)")
        return resultado
    
    ean13 = gtin[1:]  
    ean13_digitos = [int(c) for c in ean13]
    suma = sum(ean13_digitos[i] * (3 if i % 2 else 1) for i in range(12))
    digito_esperado = (10 - suma % 10) % 10
    
    if ean13_digitos[12] != digito_esperado:
        resultado['errores'].append(f"EAN-13 inválido: los últimos 13 dígitos ({ean13}) no pasan validación")
        return resultado
    
    cantidad_str = componentes['30']
    if not cantidad_str.isdigit() or int(cantidad_str) <= 0:
        resultado['errores'].append("Cantidad debe ser un entero mayor a 0")
        return resultado
    
    lote = componentes['10']
    if not lote or lote.strip() == '':
        resultado['errores'].append("Lote no puede estar vacío")
        return resultado
    
    resultado['valido'] = True
    resultado['datos'] = {
        'gtin': gtin,
        'ean13': ean13,
        'lote': lote,
        'cantidad': int(cantidad_str)
    }
    return resultado

# Prueba 

codigo_pallet = "(01)97501055311224(10)LOTE2026(30)250"

respuesta_servidor = parsear_gs1_128(codigo_pallet)

# Lo imprimimos en formato estandarizado JSON para que veas la belleza de salida
print(json.dumps(respuesta_servidor, indent=4, ensure_ascii=False))
