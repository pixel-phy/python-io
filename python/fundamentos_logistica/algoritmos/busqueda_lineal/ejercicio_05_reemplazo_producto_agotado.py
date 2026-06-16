"""Ejercicio 4: Reemplazo de producto agotado:
Un sistema de inventario tiene una lista de productos con su stock (diccionarios). Cuando un producto se 
agota (stock = 0), se debe buscar linealmente el primer producto con stock > 0 de la misma categoría para 
sugerir como sustituto. Si no hay, retorna None. Categorías: "electrónica", "hogar", "alimentos". """

def buscar_sustituto(inventario: dict, producto_agotado: str):
    # Primero encontramos la categoría del producto agotado
    categoria_buscar = None
    for producto in inventario:
        if producto["nombre"] == producto_agotado:
            categoria_buscar = producto["categoria"]
            break

    if categoria_buscar is None:
        return None # Producto no encontrado

    # Buscamos el primer producto con stock > 0 de esa categoría.
    for producto in inventario:
        if (producto["categoria"] == categoria_buscar and
            producto["stock"] > 0 and
            producto["nombre"] != producto_agotado):
            return producto
    
    return None # No hay sustituto disponible

# Prueba:
inventario = [
    {"nombre": "TV", "categoria": "electrónica", "stock": 0},
    {"nombre": "Laptop", "categoria": "electrónica", "stock": 3},
    {"nombre": "Silla", "categoria": "hogar", "stock": 5}
]

print(buscar_sustituto(inventario, "TV"))
print(buscar_sustituto(inventario, "Silla"))
