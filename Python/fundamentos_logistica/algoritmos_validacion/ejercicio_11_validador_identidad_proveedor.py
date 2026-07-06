"""Ejercicio 11: Validador de identidad de proveedor (Gestión de compras)

    En un modelo de selección de Proveedores y contratos, nuestra empresa solo tiene permitido
    comprar productos a un pool específico de proveedores autorizados cuyos códigos de empresa
    de 5 dígitos en el EAN-13 son: ["12345", "67890", "55555"]. Además, el producto debe venir
    de México (prefijo 750).

    - Escribir una función que reciba un código de barras. Debe validar: 1) Que sea un EAN-13
    válido numérciamente. 2) Que pertenezca al prefijo de país 750. 3) Que corresponda a uno 
    de los 3 proveedores autorizados (extrae los 5 dígitos que siguen al prefijo del país).
    - Input de prueba: "7501234567897". """

def validar_proveedor_autorizado(codigo: str) -> dict:
    """Valida la procedencia y validez de un SKU según la norma GS1 EAN-13.

    Optimizado para búsquedas en tiempo constante O(1).
    """
    # Inicializamos la estructura de forma consistente
    resultado = {
        'codigo': codigo,
        'valido': False,
        'errores': [],
        'detalles': {}
    }

    # 1. Validaciones de formato básicas
    if not codigo or len(codigo) != 13:
        resultado['errores'].append(f"Longitud incorrecta: {len(codigo)} (debe ser 13)")
        return resultado

    if not codigo.isdigit():
        resultado['errores'].append("Contiene caracteres no numéricos")
        return resultado

    # 2. Validación matemática del dígito verificador
    digitos = [int(c) for c in codigo]
    suma = sum(digitos[i] * (3 if i % 2 else 1) for i in range(12))
    digito_esperado = (10 - (suma % 10)) % 10
    digito_recibido = digitos[12]

    if digito_recibido != digito_esperado:
        resultado['errores'].append(f"Dígito verificador inválido: esperado {digito_esperado}, recibido {digito_recibido}")
        return resultado

    resultado['detalles']['digito_verificador_valido'] = True

    # 3. Extracción de la jerarquía GS1
    prefijo_pais = codigo[0:3]
    codigo_proveedor = codigo[3:8]
    codigo_producto = codigo[8:12]
    digito_verificador = codigo[12]

    resultado['detalles']['prefijo_pais'] = prefijo_pais
    resultado['detalles']['codigo_proveedor'] = codigo_proveedor
    resultado['detalles']['codigo_producto'] = codigo_producto
    resultado['detalles']['digito_verificador'] = digito_verificador

    # 4. Control de procedencia geográfica (México = 750)
    PAIS_MEXICO = "750"
    if prefijo_pais != PAIS_MEXICO:
        resultado['errores'].append(f"País no autorizado: {prefijo_pais} (solo se permite {PAIS_MEXICO})")
        return resultado

    resultado['detalles']['pais_valido'] = True
    resultado['detalles']['pais'] = 'México'

    # 5. Control de pool corporativo (Optimizado usando un set)
    PROVEEDORES_AUTORIZADOS = {"12345", "67890", "55555"}

    if codigo_proveedor not in PROVEEDORES_AUTORIZADOS:
        resultado['errores'].append(
            f"Proveedor no autorizado: {codigo_proveedor} "
            f"(autorizados: {', '.join(PROVEEDORES_AUTORIZADOS)})"
        )
        return resultado

    # Corrección de asignaciones seguras
    resultado['detalles']['proveedor_valido'] = True
    resultado['detalles']['proveedor_autorizado'] = codigo_proveedor

    # Cierre exitoso del pipeline
    resultado['valido'] = True
    resultado['detalles']['mensaje'] = "Producto válido: Origen México y proveedor autorizado."

    return resultado

# Prueba
codigo_prueba = "7501234567897"
res = validar_proveedor_autorizado(codigo_prueba)

import json
print(json.dumps(res, indent=4, ensure_ascii=False))
