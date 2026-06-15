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
pedido
while capacidad_restante > 0:
    for pedido in pedidos_pendientes:
        if pedido > capacidad_restante:

