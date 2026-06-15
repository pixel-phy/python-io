"""Ejercicio 01:
    Define una función asignar_vehiculo_por_peso(peso) que:
    - Reciba un número (peso en kg).
    - Devuelva un string con el vehículo según:
        • < 5 kg -> "Moto"
        • 5 a 20 kg -> "Furgoneta"
        • > 20 kg -> "Camión"
    - Incluye validación para pesos negativos o no numéricos """

def asignar_vehiculo_por_peso(peso: float):
    try:
        peso_float = float(peso)

        if peso_float < 0:
            return "Peso debe ser un número mayor que cero."
        elif peso_float < 5:
            return "Moto"
        elif peso_float <= 20:
            return "Furgoneta"
        return "Camión"
    except ValueError as e:
        return f"Error: el valor ingresado no es un número válido. Detalle: {e}"

print(asignar_vehiculo_por_peso(3))
print(asignar_vehiculo_por_peso(20))
print(asignar_vehiculo_por_peso(25))
print(asignar_vehiculo_por_peso(-5))
print(asignar_vehiculo_por_peso("hola"))
