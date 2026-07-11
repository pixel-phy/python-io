"""
Ejercicio 38: Polimorfismo en Modelos de Inventario

Crea una clase base ModeloInventario con métodos calcular_cantidad_pedido() y calcular_costo_total()
(que retornen valores genéricos).

Luego, crea dos clases hijas:

- ModeloEOQ: Implementa la fórmula de Lote Económico
 - calcular_cantidad_pedido(demanda, costo_pedido, costo_mantenimiento) → √(2DS/H)
 - calcular_costo_total(demanda, costo_pedido, costo_mantenimiento) → √(2DSH) + costo_compra

- ModeloNovedad: Implementa el modelo del Vendedor de Periódicos (Newsvendor)

 - calcular_cantidad_pedido(demanda_media, demanda_std, precio_venta, costo_compra, valor_rescate)
   → Usa la distribución normal

"""

import math
from scipy.stats import norm

class ModeloInventario:
    """Clase base genérica para modelos de inventario."""
    
    def calcular_cantidad_pedido(self, *args, **kwargs):
        print("Cálculo de cantidad genérico: No implementado.")
        return 0

    def calcular_costo_total(self, *args, **kwargs):
        print("Cálculo de costo genérico: No implementado.")
        return 0


class ModeloEOQ(ModeloInventario):
    """Modelo de Lote Económico (Economic Order Quantity)."""
    
    def calcular_cantidad_pedido(self, demanda, costo_pedido, costo_mantenimiento):
        # Fórmula: Q = sqrt((2 * D * S) / H)
        q = math.sqrt((2 * demanda * costo_pedido) / costo_mantenimiento)
        return q

    def calcular_costo_total(self, demanda, costo_pedido, costo_mantenimiento, costo_compra=0):
        # Fórmula: Costo = sqrt(2 * D * S * H) + Costo de Compra
        # Nota: El costo de gestión real es (D/Q)*S + (Q/2)*H, que en el óptimo Q* equivale a sqrt(2DSH)
        costo_gestion = math.sqrt(2 * demanda * costo_pedido * costo_mantenimiento)
        return costo_gestion + costo_compra


class ModeloNovedad(ModeloInventario):
    """Modelo del Vendedor de Periódicos (Newsvendor Model)."""
    
    def calcular_cantidad_pedido(self, demanda_media, demanda_std, precio_venta, costo_compra, valor_rescate):
        # 1. Calcular el Costo de Subestimar (Cu) y el Costo de Sobreestimar (Co)
        cu = precio_venta - costo_compra  # Margen de ganancia por unidad vendida
        co = costo_compra - valor_rescate # Pérdida por unidad no vendida
        
        # 2. Calcular la Razón Crítica (Nivel de servicio óptimo)
        razon_critica = cu / (cu + co)
        
        # 3. Encontrar el factor Z de la distribución normal estándar
        z = norm.ppf(razon_critica)
        
        # 4. Calcular la cantidad óptima de pedido: Q = media + Z * std
        q = demanda_media + (z * demanda_std)
        return q
    
    # El ejercicio no especificó fórmula de costo total para Newsvendor, 
    # pero podemos heredar el método genérico o adaptarlo si lo necesitas.


# --- EJEMPLO DE USO / PRUEBA ---
if __name__ == "__main__":
    print("--- Probando Modelo EOQ ---")
    eoq = ModeloEOQ()
    D = 1000  # Demanda anual
    S = 20    # Costo por pedido
    H = 2     # Costo de mantener por unidad al año
    
    q_eoq = eoq.calcular_cantidad_pedido(D, S, H)
    costo_eoq = eoq.calcular_costo_total(D, S, H, costo_compra=5000)
    
    print(f"Cantidad óptima de pedido (Q): {q_eoq:.2f}")
    print(f"Costo total estimado: ${costo_eoq:.2f}\n")

    print("--- Probando Modelo Novedad (Newsvendor) ---")
    newsvendor = ModeloNovedad()
    media = 100
    desviacion = 15
    precio = 15
    costo = 10
    rescate = 5
    
    q_novedad = newsvendor.calcular_cantidad_pedido(media, desviacion, precio, costo, rescate)
    print(f"Cantidad óptima a pedir para la novedad: {q_novedad:.2f}")
