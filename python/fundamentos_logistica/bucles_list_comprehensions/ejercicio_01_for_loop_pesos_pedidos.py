"""Ejercicio 1: For loop con pesos de pedidos

Tenemos la siguiente lista con pesos de pedidos:
    pesos_pedidos = [12.5, 45.0, 23.5, 67.3, 18.2, 52.8, 31.0, 49.9]

Usando un bucle for, calcular y mostrar:
    1. El peso total de todos los pedidos.
    2. Cuántos pedidos pesan más de 30 kg. """

pesos_pedidos = [12.5, 45.0, 23.5, 67.3, 18.2, 52.8, 31.0, 49.9]

peso_total = 0
contador_pedidos = 0
for peso in pesos_pedidos:
    peso_total += peso
    if peso > 30:
        contador_pedidos += 1

print(f"Peso total de todos los pedidos: {peso_total}")
print(f"Pedidos de más de 30 kg: {contador_pedidos}")
