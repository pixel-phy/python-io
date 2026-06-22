"""Checksum Básico (Suma de Verificación Algorítmica)

    Un Checksum básico suma los valores numéricos de un conjunto de datos (una cadena, un vector de inventario o 
    un mensaje de telemetría) y aplica una operación matemática (generalmente un módulo) para reducir toda esa 
    información a un único número o carácter de tamaño fijo.

    En el transporte de datos masivos para modelos de optimización estocástica o de colas, los servidores envían
    millones de matrices de coeficientes por segundo. Si un solo número cambia debido a la latencia de la red 
    (por ejemplo, que un costo de transporte cambie de $1.02 a $7.02), el Solver de IO arrojará una solución óptima
    completamente errónea para el negocio. El checksum actúa como la primera línea de defensa para validar que 
    el paquete de datos llegó intacto. 

    Variantes comunes en la industria:
    1. Suma modular básica: Sumar todos los bytes o digitos y aplicar un módulo.
    2. Complemento a 1 o 2: Usado en cabeceras de red, donde se suman los valores y se invierten los bits 
    para facilitar una verificación ultrarrápida a nivel de hardware.
    """

# Ejemplo

def checksum_basico(datos: str) -> int:
    # Convierte cada carácter en su valor ASCII y los suma
    suma_total = sum(ord(caracter) for caracter in datos)
    # Reduce el resultado a un rango de 0 a 255 (1 byte de tamaño)
    return suma_total % 256
