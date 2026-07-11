""" Mini Reto Día 1:
Construye una variable compuesta que represente un envío completo usando:
    - int (código de envío).
    - float (peso).
    - str (destino).
    - list (historial de estados).
    - dict (metadatos: chofer, unidad).
    - tuple (coordenadas fijas de entrega). """

datos_envio = {
    "codigo": 1001,
    "peso_kg": 23.6,
    "destino": "Bogotá",
    "historial_estados": ["Despachado", "Entregado"],
    "metadatos": {"chofer": "Mario", "placa": "WKL089"},
    "coordenadas_entrega": (42.8942, -98.4323)
}

print(f"Destino: {datos_envio['destino']} | Último estado historial: {datos_envio['historial_estados'][-1]}")
