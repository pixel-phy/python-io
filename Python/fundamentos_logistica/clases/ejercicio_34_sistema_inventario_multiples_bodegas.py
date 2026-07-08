"""Ejercicio 34: Sistema de Inventario con Múltiples Bodegas
Implementa una clase Bodega con atributos nombre, capacidad_maxima, stock_actual y un método
calcular_ocupacion() que retorne el porcentaje de ocupación. Crea BodegaRefrigerada que herede
de Bodega. Añade atributos temperatura y costo_energia_por_grado.
El método calcular_ocupacion() debe considerar que si la ocupación supera el 80%, el costo de energía
aumenta un 20%. Usa super() para acceder al método base y modificar el resultado.
    """

class Bodega:
    def __init__(self, nombre: str, capacidad_maxima: float, stock_actual: float):
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.stock_actual = stock_actual

    def calcular_ocupacion(self) -> float:
        """Retorna el porcentaje de ocupación de la bodega (de 0 a 100)."""
        if self.capacidad_maxima == 0:
            return 0.0
        porcentaje = (self.stock_actual / self.capacidad_maxima) * 100
        return round(porcentaje, 2)


class BodegaRefrigerada(Bodega):
    def __init__(self, nombre: str, capacidad_maxima: float, stock_actual: float, 
                 temperatura: float, costo_energia_por_grado: float):
        # Inicializamos los atributos de la bodega base
        super().__init__(nombre, capacidad_maxima, stock_actual)
        # Atributos específicos de la bodega fría
        self.temperatura = temperatura
        self.costo_energia_por_grado = costo_energia_por_grado

    def calcular_ocupacion(self) -> float:
        # 1. Usamos super() para obtener el porcentaje de ocupación básico
        porcentaje_ocupacion = super().calcular_ocupacion()
        
        # 2. Aplicamos la regla de negocio específica para refrigerados
        if porcentaje_ocupacion > 80.0:
            print(f"¡Alerta en {self.nombre}! Ocupación ({porcentaje_ocupacion}%) supera el 80%.")
            # Aumentamos el costo de energía un 20%
            self.costo_energia_por_grado *= 1.20
            print(f"El costo de energía por grado ha aumentado a: ${self.costo_energia_por_grado:.2f}")
            
        return porcentaje_ocupacion

# Prueba:
# Bodega 1: Operando normal (70% de ocupación)
bodega_pescado = BodegaRefrigerada("Cámara Pescados", capacidad_maxima=1000, stock_actual=700, 
                                   temperatura=-18.0, costo_energia_por_grado=5.0)

print(f"Ocupación: {bodega_pescado.calcular_ocupacion()}%")
print(f"Costo energía actual: ${bodega_pescado.costo_energia_por_grado}\n")

print("-" * 40)

# Bodega 2: Sobrecargada (90% de ocupación)
bodega_lacteos = BodegaRefrigerada("Cámara Lácteos", capacidad_maxima=1000, stock_actual=900, 
                                   temperatura=4.0, costo_energia_por_grado=5.0)

print(f"Ocupación: {bodega_lacteos.calcular_ocupacion()}%")
# Verás cómo el costo de 5.0 pasó a 6.0 automáticamente debido al incremento del 20%
print(f"Costo energía final: ${bodega_lacteos.costo_energia_por_grado}")
