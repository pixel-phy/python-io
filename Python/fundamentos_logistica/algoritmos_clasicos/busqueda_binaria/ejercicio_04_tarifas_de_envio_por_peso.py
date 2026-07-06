"""Ejercicio 04: Tarifas de envío por peso
    Una empresa de logística tiene una tabla de tarifas ordenadas por peso (kg). Cada peso tiene una
    tarifa por kilo. El sistema debe encontrar la tarifa exacta para un peso específico al cotizar envíos.

    Datos: Lista de diccionarios con peso y tarifa, ordenada por peso.
    Entrada: Peso a consultar.
    Salida: Tarifa correspondiente o mensaje de "sin tarifa definida". """

def buscar_tarifa(tarifas: list[dict], peso_buscado: int):
    """Busca una tarifa por peso usando búsqueda binaria.

        Args: 
            tarifas: Lista de diccionarios {"peso": x, "tarifa": y} ordenada por peso
            peso_buscado: Peso en kg a consultar

        Returns:
            Tarifa correspondiente o None si no existe
    """

    izquierda = 0
    derecha = len(tarifas) - 1

    while izquierda <= derecha:
        medio = izquierda + (derecha - izquierda) // 2
        peso_actual = tarifas[medio]["peso"] # accedemos al valor del diccionario

        if peso_actual == peso_buscado:
            return tarifas[medio]["tarifa"]
        elif peso_actual < peso_buscado:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None

# Pruebas
tarifas = [
    {"peso": 1, "tarifa": 5.50},
    {"peso": 3, "tarifa": 4.20},
    {"peso": 5, "tarifa": 3.80},
    {"peso": 10, "tarifa": 2.90},
    {"peso": 20, "tarifa": 2.10}
]

# Caso 1: Encontrado
tarifa = buscar_tarifa(tarifas, 5)
if tarifa is not None:
    print(f"Tarifa para 5 kg: ${tarifa}")
else:
    print("No existe tarifa para 5 kg")

# Caso 2: No encontrado
tarifa = buscar_tarifa(tarifas, 7)
if tarifa is not None:
    print(f"Tarifa para 7 kg: ${tarifa}")
else:
    print("No existe tarifa para 7 kg")
