"""Ejercicio 03: Simular carga de camión

    Un camión tiene capacidad máxima de 200 kg. Tenemos la lista de pedidos:

    pedidos_pendientes = [45.0, 52.5, 30.0, 68.5, 23.0, 41.5, 35.0]

    Simular la carga:
    - Usar while loop para cargar pedidos en orden hasta que el siguiente pedido supere
    la capacidad restante.
    - Muestra:
        - Pedidos cargados.
        - Peso total cargado.
        - Capacidad restante.

    Si un peso no cabe, se detiene el proceso. """

pedidos_pendientes = [45.0, 52.5, 30.0, 68.5, 23.0, 41.5, 35.0]

capacidad_maxima = 200
capacidad_restante = capacidad_maxima
pedidos_cargados = []

i = 0
while i < len(pedidos_pendientes):
    pedido = pedidos_pendientes[i]
    if pedido <= capacidad_restante:
        pedidos_cargados.append(pedido)
        capacidad_restante -= pedido
        i += 1
    else:
        break

suma_pesos = 0
for peso in pedidos_cargados:
    suma_pesos += peso

print(f"Pedidos cargados: {pedidos_cargados}")
print(f"Peso total cargado: {suma_pesos}")
print(f"Capacidad restante: {capacidad_restante}")
