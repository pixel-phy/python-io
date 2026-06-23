"""Ejercicio 24: El Reparador Automático de Secuencias de Almacén

En los sistemas automáticos de almacenamiento y recuperación (ASRS), los carros robotizados leen etiquetas
numéricas en los Racks. A veces, debido al polvo o al movimiento, un único dígito se vuelve ilegible
(representado por un *). Por ejemplo "12*456" en lugar de "123456".

    Si el código original fue generado con el algoritmo de Luhn y conocemos el dígito verificador final
(que está intacto), pordemos deducir matemáticamente cuál era el dígito perdido. 

- Escribe una función llamada reparar_codigo_luhn(codigo_corrupto: str) -> str. La función recibirá una 
    cadena de 7 caracteres (6 dígitos de datos, donde uno es un *, y el 7mo carácter es el dígito verificador
    real y correcto de Luhn). Tu código debe probar los dígitos del 0 al 9 en la posición del * hasta encontrar
el único que hace que el código sea válido según Luhn, devolviendo la cadena completamente reparada.

    Input de prueba: "12*4564". """

def reparar_codigo_luhn(codigo_corrupto: str) -> str:
    """
        Repara un código de Luhn que tiene un digito ilegible (*).

        Args:
            codigo_corrupto: string de 7 caracteres con un * y el digito verificador al final
        Returns:
            El código completo reparado

    """

    # Verificamos que el código tenga la longitud correcta
    if len(codigo_corrupto) != 7:
        raise ValueError ("El código debe tener exactamente 7 caracteres")

    # Guardamos el dígito verificador
    digito_verificador = int(codigo_corrupto[-1])

    # Probamos cada dígito del 0 al 9 en la posición del *
    for digito_prueba in range(10):
        # Reemplazamos el * con el dígito de prueba 
        codigo_reparado = codigo_corrupto.replace('*', str(digito_prueba))

        # Verificamos si el dígito es el válido según Luhn
        if validar_luhn(codigo_reparado):
            return codigo_reparado

    # Si no encontramos ningún dígito que funcione
    return ""

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

#Prueba
codigo_corrupto = "12*4564"
codigo_reparado = reparar_codigo_luhn(codigo_corrupto)
print(f"Código corrupto: {codigo_corrupto}")
print(f"Código reparado: {codigo_reparado}")
print(f"Validez: {validar_luhn(codigo_reparado)}")
