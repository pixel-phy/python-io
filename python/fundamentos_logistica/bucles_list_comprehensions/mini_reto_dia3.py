"""Mini reto día 3: 
    Usando una sola list comprehension con la lista de diccionarios dada, obtemer los IDs de pedidos
    urgentes donde:

    Urgente = (peso > 0) o (zona == "rural")"""

pedidos = [
    {"id": 101, "peso": 45.0, "zona": "urbana"},
    {"id": 102, "peso": 68.5, "zona": "rural"},
    {"id": 103, "peso": 23.0, "zona": "urbana"},
    {"id": 104, "peso": 52.0, "zona": "rural"},
    {"id": 105, "peso": 31.0, "zona": "urbana"},
    {"id": 106, "peso": 15.5, "zona": "rural"}
]

urgente = [clave["id"] for clave in pedidos if clave["peso"] > 30 or clave["zona"] == "rural"]

print(f"Pedidos urgentes: {urgente}")
