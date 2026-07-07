"""Ejercicio 22: Sistema de Inventario con Validación

Crea una clase SistemaInventario que gestione múltiples productos con:
- Atributo privado __productos (diccionario de productos)
- Getter de producto con validación de existencia
- Setter para cantidades que valide no negativas
- Método estático calcular_costo_pedido(cantidad, costo_unitario, descuento=0)
- Método estático calcular_punto_reorden(demanda_diaria, lead_time, stock_seguridad)
- Método estático formatear_inventario(data) para formatear reportes
- Método agregar_producto(nombre, cantidad, costo, punto_reorden) con validaciones
"""

class SistemaInventario:
    def __init__(self):
        # - Atributo privado __productos (diccionario de productos)
        # Estructura interna: { "nombre_producto": {"cantidad": int, "costo": float, "punto_reorden": int} }
        self.__productos = {}

    # - Getter de producto con validación de existencia
    def obtener_producto(self, nombre: str) -> dict:
        """Devuelve la información de un producto si existe."""
        if nombre not in self.__productos:
            raise KeyError(f"El producto '{nombre}' no existe en el inventario.")
        return self.__productos[nombre]

    # - Setter para cantidades que valide no negativas
    def actualizar_cantidad(self, nombre: str, nueva_cantidad: int):
        """Modifica la cantidad de un producto existente validando que no sea negativa."""
        if nombre not in self.__productos:
            raise KeyError(f"El producto '{nombre}' no existe en el inventario.")
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero mayor o igual a cero.")
        
        self.__productos[nombre]["cantidad"] = nueva_cantidad

    # - Método agregar_producto con validaciones básicas de tipo y valores
    def agregar_producto(self, nombre: str, cantidad: int, costo: float, punto_reorden: int):
        """Añade un nuevo producto al inventario realizando validaciones previas."""
        if nombre in self.__productos:
            raise ValueError(f"El producto '{nombre}' ya existe. Usa actualizar_cantidad().")
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad inicial no puede ser negativa.")
        if not isinstance(costo, (int, float)) or costo < 0:
            raise ValueError("El costo unitario no puede ser negativo.")
        if not isinstance(punto_reorden, int) or punto_reorden < 0:
            raise ValueError("El punto de reorden debe ser un entero no negativo.")

        # Guardamos en el diccionario privado
        self.__productos[nombre] = {
            "cantidad": cantidad,
            "costo": costo,
            "punto_reorden": punto_reorden
        }

    # - Método estático calcular_costo_pedido
    @staticmethod
    def calcular_costo_pedido(cantidad: int, costo_unitario: float, descuento: float = 0.0) -> float:
        """Calcula el costo total aplicando un porcentaje de descuento (ej: 0.10 para 10%)."""
        costo_base = cantidad * costo_unitario
        return costo_base * (1 - descuento)

    # - Método estático calcular_punto_reorden
    @staticmethod
    def calcular_punto_reorden(demanda_diaria: float, lead_time: int, stock_seguridad: int) -> float:
        """Calcula el stock mínimo antes de tener que pedir más producto."""
        # Fórmula clásica de logística: (Demanda Diaria * Tiempo de Entrega) + Stock de Seguridad
        return (demanda_diaria * lead_time) + stock_seguridad

    # - Método estático formatear_inventario
    @staticmethod
    def formatear_inventario(data: dict) -> str:
        """Formatea la información de un producto o del inventario para reportes."""
        reporte = []
        for producto, info in data.items():
            linea = (f"Producto: {producto.upper()}\n"
                     f"   Stock Actual: {info['cantidad']} unidades\n"
                     f"   Costo Unitario: ${info['costo']:.2f}\n"
                     f"   Punto de Reorden: {info['punto_reorden']} u.")
            reporte.append(linea)
        return "\n" + "─" * 40 + "\n" + "\n".join(reporte) + "\n" + "─" * 40

    # Método auxiliar (getter) para poder pasarle los datos de forma segura al formateador
    def exportar_datos(self) -> dict:
        """Retorna una copia del diccionario para no comprometer la referencia original."""
        return self.__productos.copy()

# Prueba
if __name__ == "__main__":
    # 1. Instanciar el inventario
    mi_inventario = SistemaInventario()

    # 2. Usar métodos estáticos de logística para planificar compras antes de agregar productos
    # Supongamos que vendemos 5 laptops al día, tardan 3 días en llegar y queremos 10 de seguridad
    reorden_laptops = mi_inventario.calcular_punto_reorden(demanda_diaria=5, lead_time=3, stock_seguridad=10)
    print(f"Punto de reorden calculado para Laptops: {reorden_laptops} unidades.")

    # 3. Agregar productos válidos
    mi_inventario.agregar_producto(nombre="Laptop", cantidad=25, costo=850.0, punto_reorden=int(reorden_laptops))
    mi_inventario.agregar_producto(nombre="Mouse", cantidad=100, costo=15.50, punto_reorden=15)

    # 4. Mostrar el reporte usando el formateador estático
    datos_actuales = mi_inventario.exportar_datos()
    print(mi_inventario.formatear_inventario(datos_actuales))

    # 5. Probar el Setter con validación de cantidad no negativa
    print("Modificando stock de Mouse...")
    mi_inventario.actualizar_cantidad("Mouse", 80) # Válido
    
    # 6. Intentar romper las validaciones (Bloques Try-Except)
    print("\n--- Pruebas de Seguridad ---")
    
    try:
        # Intento de cantidad negativa
        mi_inventario.actualizar_cantidad("Mouse", -5)
    except ValueError as e:
        print(f"Validación exitosa (Cantidad negativa): {e}")

    try:
        # Intento de buscar producto inexistente
        mi_inventario.obtener_producto("Teclado")
    except KeyError as e:
        print(f"Validación exitosa (No existe producto): {e}")

    # 7. Calcular un presupuesto de compra externa usando el método estático
    # Comprar 50 mouses con el 10% de descuento (0.10)
    costo_pedido = mi_inventario.calcular_costo_pedido(cantidad=50, costo_unitario=15.50, descuento=0.10)
    print(f"\nCosto estimado para pedir 50 Mouses (10% desc): ${costo_pedido:.2f}")
