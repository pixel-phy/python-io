"""Validador de contenedores ISO 6346 (Luhn)

Los contenedores marítimos que entran a las terminales de carga tienen un código de control. 
    Los primeros 4 caracteres son las letras y los siguientes 6 son números. Para calcular su dígito 
de control, las letras se convierten primero a números según una tabla estandarizada (A=10, B=11, Z=38, saltándose los múltiplos de 11).

    Escribe una función simplificada que reciba un string numérico de 10 dígitos (donde el último 
    es el dígito verificador) y determine si es válido usando el algoritmo de Luhn clásico de nuestro código base.

    Input de prueba: "49927398716". """

def validar_luhn(numero: str) -> bool:
    """Valida una cadena numérica completa usando el algoritmo de Luhn."""
    if not numero or not numero.isdigit():
        return False

    digitos = [int(d) for d in numero]
    verificador = digitos[-1]
    
    suma = 0
    # Bandera para duplicar las posiciones alternas
    duplicar = True  # La primera posición a la izquierda del verificador se duplica
    
    # Recorremos desde el penúltimo dígito hacia el primero
    for i in range(len(digitos) - 2, -1, -1):
        digito = digitos[i]
        if duplicar:
            digito *= 2
            if digito > 9:
                digito -= 9
        suma += digito
        duplicar = not duplicar  # Alternamos la bandera

    # Añadimos el verificador que guardamos al inicio
    suma += verificador
    
    return suma % 10 == 0

# Prueba
numero_prueba = "49927398716"
resultado = validar_luhn(numero_prueba)
print(f"Número evaluado: {numero_prueba}")
print(f"¿Es estructuralmente válido por Luhn?: {resultado}")
