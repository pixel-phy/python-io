""" Algoritmo de Luhn en investigación de Operaciones

El algoritmo de Luhn es un método de suma de verificación simple que se utiliza para validar una variedad
de números de identificación. Aunque es famoso por las tarjetas de crédito, en el mundo de las operaciones y la logística
se utiliza para validar IDs de contenedores de carga, números de seguimiento de guías de despacho,
identificadores de pallets (SSCC) y códigos de flotas de transporte.

Garantizar que un identificador de un contenedor es válido antes de correr un algoritmo de ruteo de vehículos
(VPR) evita fallos catastróficos en la asignación de recursos.

El algoritmos en 4 pasos:
    1. Empezando por el penúltimo dígito y moviéndose de derecha a izquierda, se duplica el valor de cada 
    segundo dígito.
    2. Si el resultado de duplicar es mayor que 9, se suman los dígitos del resultado o se le resta 9.
    3. Se suman todos los dígitos.
    4. Si el total del módulo 10 es igual a 0, el número es válido. """

# Ejemplo de código en Python

def algoritmo_luhn(numero_tarjeta: str) -> bool:
    digitos = [int(d) for d in numero_tarjeta]
    suma = 0
    digitos_alreves = digitos[::-1]

    for i, digito in enumerate(digitos_alreves):
        if i % 2 == 1:
            digito *= 2
            if digito > 9:
                digito -= 9
        suma += digito

    return suma % 10 == 0
        
