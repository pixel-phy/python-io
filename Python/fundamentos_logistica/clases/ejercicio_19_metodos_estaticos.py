"""Ejercicio 19: Métodos estáticos (@staticmethod)

Son funciones que pertenecen a una clase pero no reciben self ni cls. 
Son útiles para:

- Funciones matemáticas auxiliares: Cálculo de distancias, matrices, estadísticas.
- Validaciones: Verificar formatos, rangos, tipos de datos.
- Conversiones: Transformar datos entre formatos.
- Utilidades: Operaciones que no dependen del estado de la clase.

Encapsulamiento:

- Atributos privados: Convención _atributo (protegido) y __atributo (privado, name mangling).
- Getters yy Setters: Controlan el acceso y modificación de atributos.
- Propiedades (@property): Permiten acceso estilo atributo con lógica detrás.
"""

# Ejemplo de aplicación:

import math
from typing import Optional

class Inventario:
    """
    Sistema de gestión de inventario con validación de parámetros críticos.
    """
    
    def __init__(self, producto: str, cantidad_inicial: float, 
                 costo_unitario: float, punto_reorden: float):
        self._producto = producto
        self._cantidad = 0.0  # Inicializado en 0
        self._costo_unitario = 0.0
        self._punto_reorden = 0.0
        self._historico_pedidos = []
        
        # Usar setters para validar datos iniciales
        self.cantidad = cantidad_inicial
        self.costo_unitario = costo_unitario
        self.punto_reorden = punto_reorden
    
    # MÉTODOS ESTÁTICOS (Funciones auxiliares)
    
    @staticmethod
    def calcular_costo_total(cantidad: float, costo_unitario: float) -> float:
        """Calcula el costo total de un pedido."""
        return cantidad * costo_unitario
    
    @staticmethod
    def calcular_rotacion_inventario(costo_ventas: float, inventario_promedio: float) -> float:
        """Calcula la rotación del inventario (veces que se renueva)."""
        if inventario_promedio <= 0:
            raise ValueError("El inventario promedio debe ser positivo")
        return costo_ventas / inventario_promedio
    
    @staticmethod
    def calcular_dias_inventario(rotacion: float) -> float:
        """Calcula los días de inventario disponible."""
        if rotacion <= 0:
            raise ValueError("La rotación debe ser positiva")
        return 365 / rotacion
    
    @staticmethod
    def formatear_moneda(valor: float) -> str:
        """Formatea un valor como moneda."""
        return f"${valor:,.2f}"
    
    @staticmethod
    def validar_cantidad_positiva(valor: float, nombre: str) -> float:
        """Valida que un valor sea positivo."""
        if valor < 0:
            raise ValueError(f"{nombre} no puede ser negativo")
        return valor
    
    # PROPERTIES (Getters y Setters con validación)
    
    @property
    def cantidad(self) -> float:
        """Getter para cantidad."""
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, valor: float):
        """Setter para cantidad con validación."""
        if valor < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = float(valor)
    
    @property
    def costo_unitario(self) -> float:
        """Getter para costo unitario."""
        return self._costo_unitario
    
    @costo_unitario.setter
    def costo_unitario(self, valor: float):
        """Setter para costo unitario con validación."""
        if valor < 0:
            raise ValueError("El costo unitario no puede ser negativo")
        self._costo_unitario = float(valor)
    
    @property
    def punto_reorden(self) -> float:
        """Getter para punto de reorden."""
        return self._punto_reorden
    
    @punto_reorden.setter
    def punto_reorden(self, valor: float):
        """Setter para punto de reorden con validación."""
        if valor < 0:
            raise ValueError("El punto de reorden no puede ser negativo")
        self._punto_reorden = float(valor)
    
    @property
    def valor_total_inventario(self) -> float:
        """Propiedad calculada: valor total del inventario."""
        return self._cantidad * self._costo_unitario
    
    @property
    def necesita_reabastecer(self) -> bool:
        """Indica si se necesita reabastecer."""
        return self._cantidad <= self._punto_reorden
    
    # MÉTODOS DE INSTANCIA 
    
    def agregar_inventario(self, cantidad: float, costo: Optional[float] = None):
        """Agrega inventario con validación."""
        self.validar_cantidad_positiva(cantidad, "Cantidad a agregar")
        
        costo_real = costo if costo is not None else self._costo_unitario
        self._validar_costo_positivo(costo_real)
        
        costo_pedido = self.calcular_costo_total(cantidad, costo_real)
        self._historico_pedidos.append({
            'fecha': '2024-01-01',  # Simplificado
            'cantidad': cantidad,
            'costo_unitario': costo_real,
            'costo_total': costo_pedido
        })
        
        self._cantidad += cantidad
    
    def reducir_inventario(self, cantidad: float):
        """Reduce inventario por ventas/uso."""
        self.validar_cantidad_positiva(cantidad, "Cantidad a reducir")
        
        if cantidad > self._cantidad:
            raise ValueError(f"No hay suficiente inventario. Disponible: {self._cantidad}")
        
        self._cantidad -= cantidad
    
    def _validar_costo_positivo(self, costo: float):
        """Método privado para validar costos."""
        if costo < 0:
            raise ValueError("El costo no puede ser negativo")
    
    def __repr__(self):
        return (f"Inventario(producto='{self._producto}', cantidad={self._cantidad}, "
                f"costo_unitario={self._costo_unitario})")
    
    def __str__(self):
        return (f"{self._producto}\n"
                f"   Cantidad: {self._cantidad:.0f} unidades\n"
                f"   Costo unitario: {self.formatear_moneda(self._costo_unitario)}\n"
                f"   Valor total: {self.formatear_moneda(self.valor_total_inventario)}\n"
                f"   Punto reorden: {self._punto_reorden:.0f}\n"
                f"   {'¡REABASTECER!' if self.necesita_reabastecer else 'Nivel ok'}")


# Ejemplo de uso
if __name__ == "__main__":
    print(" USO DE MÉTODOS ESTÁTICOS \n")
    
    # Métodos estáticos se llaman desde la clase
    print(f"Costo total: {Inventario.formatear_moneda(Inventario.calcular_costo_total(100, 25.50))}")
    
    rotacion = Inventario.calcular_rotacion_inventario(50000, 10000)
    print(f"Rotación: {rotacion:.2f} veces/año")
    print(f"Días de inventario: {Inventario.calcular_dias_inventario(rotacion):.0f} días")
    
    print("\n CREANDO INVENTARIO CON VALIDACIÓN \n")
    
    # Crear inventario
    inventario = Inventario("Producto A", 100, 25.50, 20)
    print(inventario)
    
    print("\n AGREGANDO INVENTARIO \n")
    inventario.agregar_inventario(50)
    print(inventario)
    
    print("\n INTENTANDO VALOR NEGATIVO (DEBE FALLAR) \n")
    try:
        inventario.cantidad = -10
    except ValueError as e:
        print(f"Error capturado: {e}")
