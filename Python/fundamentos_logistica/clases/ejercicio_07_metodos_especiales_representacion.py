"""Ejercicio 07: Métodos especiales de Representación

En python, los métodos especiales __str__ y __repr__ controlan cómo se representan nuestros
objetos como cadenas de texto. Son fundamentales para:

- Depuración: Ver el estado interno de objetos complejos.
- Reportes: Generar salidas legibles para stakeholders.
- Logging: Registrar evolución de sistemas en simulación.
- Visualización: Presentar soluciones de optimización.

Diferencias clave:

- __repr__: Representación 'Oficial' (para desarrolladores). Debe ser inequívoca y, si es posible,
  permitir recrear el objeto.
- __str__: Representación 'amigable' (para usuarios). Debe ser legible y contextual.

"""

# Ejemplo: Representación de una solución de Ruta Óptima

class RutaOptima:
    """
    Representa una ruta óptima en un problema de transporte.
    Aplicación IO: Visualización de soluciones de problemas de ruteo.
    """
    
    def __init__(self, origen: str, destino: str, costo_total: float, 
                 nodos_intermedios: list[str] = None, flujo: float = 0):
        self.origen = origen
        self.destino = destino
        self.costo_total = costo_total
        self.nodos_intermedios = nodos_intermedios or []
        self.flujo = flujo
        self.tiempo_ejecucion = 0.0  # Se setea después de resolver
        
    def ruta_completa(self) -> list[str]:
        """Devuelve la secuencia completa de nodos en la ruta."""
        return [self.origen] + self.nodos_intermedios + [self.destino]
    
    def __repr__(self):
        """
        Representación para desarrolladores: permite recrear el objeto.
        """
        return (f"RutaOptima(origen='{self.origen}', destino='{self.destino}', "
                f"costo_total={self.costo_total:.2f}, "
                f"nodos_intermedios={self.nodos_intermedios}, "
                f"flujo={self.flujo:.2f})")
    
    def __str__(self):
        """
        Representación amigable para usuarios: formato tabular y claro.
        """
        ruta_str = " → ".join(self.ruta_completa())
        
        # Información resumida en formato amigable
        return (f"RUTA ÓPTIMA\n"
                f"   {'=' * 40}\n"
                f"   Recorrido: {ruta_str}\n"
                f"   Costo Total: ${self.costo_total:,.2f}\n"
                f"   Flujo Transportado: {self.flujo:.2f} unidades\n"
                f"   Nodos intermedios: {len(self.nodos_intermedios)}\n"
                f"   Tiempo solución: {self.tiempo_ejecucion:.3f}s")
    
    def generar_reporte_detallado(self) -> str:
        """Genera un reporte completo con todos los detalles de la ruta."""
        reporte = "=" * 60 + "\n"
        reporte += "REPORTE DE RUTA ÓPTIMA - ANÁLISIS DETALLADO\n"
        reporte += "=" * 60 + "\n\n"
        
        # Información de la ruta
        reporte += f"ORIGEN: {self.origen}\n"
        reporte += f"DESTINO: {self.destino}\n"
        reporte += f"FLUJO: {self.flujo:.2f} unidades\n"
        reporte += f"COSTO TOTAL: ${self.costo_total:,.2f}\n\n"
        
        # Desglose de segmentos
        reporte += "DETALLE DE SEGMENTOS:\n"
        reporte += "-" * 40 + "\n"
        ruta_completa = self.ruta_completa()
        for i in range(len(ruta_completa) - 1):
            segmento = f"{ruta_completa[i]} → {ruta_completa[i+1]}"
            reporte += f"  {i+1}. {segmento}\n"
        
        # Métricas adicionales
        if self.nodos_intermedios:
            reporte += f"\nPUNTOS DE PARADA: {len(self.nodos_intermedios)}\n"
            reporte += f"  {' → '.join(self.nodos_intermedios)}\n"
        
        reporte += f"\nTIEMPO DE CÁLCULO: {self.tiempo_ejecucion:.3f} segundos"
        reporte += "\n" + "=" * 60
        
        return reporte


# Ejemplo de uso
if __name__ == "__main__":
    ruta = RutaOptima(
        origen="Bogotá",
        destino="Medellín",
        costo_total=1250.75,
        nodos_intermedios=["Manizales", "Pereira"],
        flujo=150.0
    )
    ruta.tiempo_ejecucion = 2.34
    
    print("=== REPRESENTACIÓN (__repr__) ===")
    print(repr(ruta))
    print("\n")
    
    print("=== REPRESENTACIÓN AMIGABLE (__str__) ===")
    print(ruta)
    print("\n")
    
    print("=== REPORTE DETALLADO ===")
    print(ruta.generar_reporte_detallado())
