"""Dígitos Verificadores (Data Integrity)

Un dígito verificador (o checksum) es un mecanismo de redundancia que se añade al final de una cadena numérica
para detectar errores en su transcripción o transmisión. A diferencia de las funciones hash criptográficas
(como MD5 o SHA-256) que buscan seguridad y ocultamiento, los dígitos verificadores se diseñan para detectar 
los errores típicos cometidos por seres humano (errores de dedo, fatiga lectura veloz).

    Los dos errores humanos más comunes en bases de datos operativas son:
    1. Errores de sustitución: Digitar un número por otro (ej. Escribir 123 en lugar de 128). Ocurre el 85%
    de las veces.
    2. Errores de transposición: Intercambiar dos caracteres adyacentes (ej. escribir 132 en lugar de 123).
    Ocurre del 10% al 15% de las veces."""

# El algoritmo de Luhn

def calcular_luhn(codigo_base: str) -> int:
    """Calcula el digito verificador de Luhn para una cadena numérica."""

    suma = 0
    # Alternamos enpezando desde la derecha (el dígito a calcular será la pos 0)
    duplicar = True

    for car in reversed(codigo_base):
        digito = int(car)
        if duplicar:
            digito *= 2
            if digito > 9:
                digito -=9
        suma += digito
        duplicar = not duplicar

    return (10 - (suma % 10)) % 10
