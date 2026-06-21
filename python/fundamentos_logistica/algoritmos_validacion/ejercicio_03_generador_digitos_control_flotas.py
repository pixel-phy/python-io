""" Ejercicio 03: El generador de dígitos de control para flotas

Estamos integrando una nueva flota de 500 camiones cisterna a un modelo de asignación de rutas de combustible.
Los camiones tienen un ID base de 9 dígitos, pero necestias generar el décimo dígito (dígito de verificación)
usando Luhn para que el sistema de telemetría los reconozca sin errores de transmisión.
    - Escribe una función que reciba el ID base (9 dígitos) y calcule el dígito exacto que 
    debe añadirse al final para que todo el número pase la validación de Luhn.
    - input de prueba: "400000123". """

def calcular_digito_control(id_base: str) -> int:
    """Calcula el dígito de control para un ID base de 9 dígitos usando Luhn clásico.

    Garantiza la integridad de los IDs de camiones antes de su asignación en modelos VRP.
    """
    # 1. Sanitización de entrada
    id_limpio = id_base.replace(" ", "").replace("-", "")

    # 2. Validaciones estrictas de negocio
    if not id_limpio or not id_limpio.isdigit():
        raise ValueError("El ID base debe contener solo dígitos numéricos.")

    if len(id_limpio) != 9:
        raise ValueError(f"El ID base debe tener exactamente 9 dígitos. Recibido: {len(id_limpio)}")

    suma = 0
    # Al revertir una cadena de 9 dígitos para calcular el 10mo dígito:
    # El primer elemento procesado (antiguo índice 8) actúa como posición 'impar' desde la derecha
    # en el número final completo. Por ende, se multiplica por 2.
    for i, char in enumerate(reversed(id_limpio)):
        digito = int(char)
        if i % 2 == 0:
            doble = digito * 2
            if doble > 9:
                doble -= 9
            suma += doble
        else:
            suma += digito

    # Calcular cuánto falta para la siguiente decena
    return (10 - (suma % 10)) % 10

# Prueba del sistema
try:
    id_base = "400000123"
    digito = calcular_digito_control(id_base)
    id_completo = id_base + str(digito)

    print(f"ID base: {id_base}")
    print(f"Dígito calculado: {digito}")
    print(f"ID completo verificado: {id_completo}")
except ValueError as e:
    print(f"Error de datos: {e}")
