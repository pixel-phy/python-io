"""Ejercicio 2: List Comprehension para pedidos pesados (>50 kg)

    Usando la misma lista pesos_pedidos, crear una list comprehension que extraiga solo los pesos 
    mayores a 50 kg. """

pesos_pedidos = [12.5, 45.0, 23.5, 67.3, 18.2, 52.8, 31.0, 49.9]

pesos_mayores = [peso for peso in pesos_pedidos if peso > 50]
print(f"Los pesos mayores a 50 kg son: {pesos_mayores}")
