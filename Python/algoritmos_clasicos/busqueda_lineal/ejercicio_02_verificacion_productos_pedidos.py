"""Ejercicio 1: Verificación de productos en un pedido

Un centro de distribución recibe un pedido con códigos de productos. El sistema debe verificar 
si todos los productos solicitados existen en el inventario actual. Crea una función que reciba 
la lista de productos del pedido y la lista del inventario, y retorne True solo si todos los 
productos del pedido están en el inventario. """

def verificar_pedido(pedido: list, inventario: list):
    # Recorremos cada producto del pedido
    for producto_pedido in pedido:
        encontrado = False
        # Búsqueda lineal en inventario
        for producto_inv in inventario:
            if producto_pedido == producto_inv:
                encontrado = True
                break # Salimos del bucle interno si lo contramos
        # Si un producto del pedido no está en inventario, se retorna False.
        if not encontrado:
            return False
    # Si todos los productos están, se retorna True
    return True

# Prueba:
pedido = ["P101", "P205", "P309"]
inventario = ["P101", "P205", "P307", "P402", "P309"]
print(verificar_pedido(pedido, inventario))

pedido2 = ["P101", "P999"]
print(verificar_pedido(pedido2, inventario))
