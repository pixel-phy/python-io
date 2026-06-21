"""Ejercicio 3: Búsqueda de rutas alternativas en transporte
Una empresa de logística tiene una lista de rutas disponibles entre ciudades.
Cada ruta es una tupla: (origen, destino, tiempo_horas). Dada una ciudad origen y una destino,
encuentra todas las rutas directas posibles (búsqueda lineal) y devuelve una lista con los tiempos."""

def buscar_rutas(rutas: tuple, origen: str, destino: str):
    tiempos = []
    # Recorremos todas las rutas
    for ruta in rutas:
    # ruta es una tupla: (origen, destino, tiempo)
        if ruta[0] == origen and ruta[1] == destino:
            tiempos.append(ruta[2]) # Agregamos el tiempo
    return tiempos

# Prueba:
rutas = [
    ("Madrid", "Barcelona", 2.5),
    ("Madrid", "Valencia", 1.8),
    ("Barcelona", "Madrid", 2.5),
    ("Madrid", "Barcelona", 2.2),
    ("Valencia", "Sevilla", 4.0)
]
print(buscar_rutas(rutas, "Madrid", "Barcelona"))
print(buscar_rutas(rutas, "Madrid", "Paris"))
