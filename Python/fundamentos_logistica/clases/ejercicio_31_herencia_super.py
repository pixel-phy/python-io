"""Herencia y super()

En investigación de Operaciones, frecuentemente trabajamos con jerarquías de modelos.
Por ejemplo:
- Todos los problemas de optimización comparten atributos (variables, restricciones, función objetivo)
- Los problemas específicos (PL, PLE, Programación No Lineal) heredan estos atributos y añaden particularidades.

La herencia nos permite:
- Reutilizar código evitando duplicación.
- Extender funcionalidades sin modificar clases base.
- Crear familias de modelos con comportamientos comunes.

El Método super() permite llamar al constructor de la clase padre, asegurando que todos los atributos base sean 
inicializados correctamente.

"""

# Ejemplo práctico: Sistema gestión de inventarios

class Producto:
    """Clase base para productos en un sistema de inventario"""

    def __init__(self, codigo, nombre, costo_unitario, demanda_anual):
        self.codigo = codigo
        self.nombre = nombre
        self.costo_unitario = costo_unitario
        self.demanda_anual = demanda_anual
        self.stock_actual = 0

    def calcular_costo_almacenamiento(self, tasa_almacenamiento): 
        """Costo anual de mantener una unidad en inventario"""
        return self.costo_unitario * tasa_almacenamiento

    def __str__(self):
        return f"{self.codigo}: {self.nombre} (${self.costo_unitario:.2f})"

class ProductoPerecedero(Producto):
    """Producto con fecha de caducidad - hereda de Producto"""

    def __init__(self, codigo, nombre, costo_unitario, demanda_anual, fecha_caducidad, tasa_deterioro):
        # Llamamos al constructor de la clase padre
        super().__init__(codigo, nombre, costo_unitario, demanda_anual)
        self.fecha_caducidad = fecha_caducidad
        self.tasa_deterioro = tasa_deterioro
        self.dias_restantes = 0 # Se actualiza con la fecha actual
    
    def calcular_costo_almacenamiento(self, tasa_almacenamiento):
        """Sobreescribimos para incluir costo por deterioro"""
        costo_base = super().calcular_costo_almacenamiento(tasa_almacenamiento)
        costo_deterioro = self.costo_unitario * self.tasa_deterioro
        return costo_base + costo_deterioro

    def actualizar_stock(self, cantidad):
        """Actualiza stock considerando productos que caducan"""
        self.stock_actual += cantidad
        # Lógica de rotación de inventario
        return self.stock_actual

# Ejemplo:
from datetime import date, timedelta

# Arroz: Producto normal (Código, Nombre, Costo Unitario, Demanda Anual)
arroz = Producto("A101", "Arroz Premium 1kg", 1.50, 5000)

# Leche: Producto perecedero (Suma: Fecha caducidad y Tasa de deterioro)
fecha_vencimiento = date.today() + timedelta(days=10)
leche = ProductoPerecedero("P202", "Leche Entera 1L", 1.20, 12000, fecha_vencimiento, 0.15)

# 2. Simulación de operaciones de inventario

# Recibimos mercancía en el almacén
arroz.stock_actual = 400
leche.actualizar_stock(1000)  # Usando el método propio de ProductoPerecedero

print("--- Estado Inicial del Inventario ---")
print(f"{arroz} | Stock actual: {arroz.stock_actual} unidades")
print(f"{leche} | Stock actual: {leche.stock_actual} unidades | Caduca el: {leche.fecha_caducidad}")
print("-" * 40)

# 3. Cálculo de Costos de Almacenamiento (Polimorfismo)

# Definimos una tasa de almacenamiento general del 10% (0.10) anual
TASA_ALMACENAMIENTO_BASE = 0.10

print("\n--- Análisis de Costos de Almacenamiento Anual por Unidad ---")

# Aunque llamamos al mismo método, cada objeto responde según su clase
costo_arroz = arroz.calcular_costo_almacenamiento(TASA_ALMACENAMIENTO_BASE)
costo_leche = leche.calcular_costo_almacenamiento(TASA_ALMACENAMIENTO_BASE)

print(f"Costo por mantener 1 unidad de {arroz.nombre}: ${costo_arroz:.2f}")

print(f"Costo por mantener 1 unidad de {leche.nombre}: ${costo_leche:.2f}")
