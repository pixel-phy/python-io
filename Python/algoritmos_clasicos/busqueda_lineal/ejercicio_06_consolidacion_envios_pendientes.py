"""Ejercicio 5: Consolidación de envíos pendientes
Un centro logístico tiene una lista de envíos pendientes (cada uno con ID, destino y peso). Se debe buscar linealmente 
todos los envíos hacia un destino dado y calcular el peso total consolidado para optimizar
el uso de camiones. Devuelve (cantidad_envio, peso_total). """

def consolidar_envios(envios: dict, destino: str):
    cantidad = 0
    peso_total = 0

    # Se recorren todos los envíos
    for envio in envios:
        if envio["destino"] == destino:
            cantidad += 1
            peso_total += envio["peso"]

    return (cantidad, peso_total)

# Prueba
envios = [
    {"id": 101, "destino": "Norte", "peso": 150},
    {"id": 102, "destino": "Sur", "peso": 200},
    {"id": 103, "destino": "Norte", "peso": 75},
    {"id": 104, "destino": "Este", "peso": 300},
    {"id": 105, "destino": "Norte", "peso": 50}
]

print(consolidar_envios(envios, "Norte"))
print(consolidar_envios(envios, "Oeste"))
