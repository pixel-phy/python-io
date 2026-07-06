"""Ejercicio 10: Visualización de Red de Flujo

Crea una clase RedFlujo que contenga una lista de objetos Arista y añade:

__repr__: muestra el número de aristas y nodos

__str__: genera una tabla con todas las aristas (origen, destino, flujo/capacidad, costo)

generar_matriz_adyacencia(): devuelve una representación matricial del flujo

resumen_red(): muestra estadísticas agregadas (flujo total, costo total, aristas saturadas)

"""
class Arista:
    def __init__(self, origen: int, destino: int, capacidad: float, costo: float, flujo: float = 0.0):
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.costo = costo
        self.flujo = flujo

    def es_saturada(self) -> bool:
        """Una arista está saturada si el flujo alcanza o supera su capacidad."""
        return self.flujo >= self.capacidad


class RedFlujo:
    def __init__(self, aristas: list[Arista]):
        self.aristas = aristas
        # Determinamos de forma dinámica el conjunto único de nodos en la red
        self.nodos = set()
        for a in aristas:
            self.nodos.add(a.origen)
            self.nodos.add(a.destino)
            
    def __repr__(self) -> str:
        """Representación técnica de depuración."""
        return f"RedFlujo(nodos={len(self.nodos)}, aristas={len(self.aristas)})"

    def __str__(self) -> str:
        """Genera una tabla limpia y alineada con todas las aristas."""
        linea_separadora = "-" * 53
        encabezado = f"| {'Origen':<6} | {'Destino':<7} | {'Flujo/Capacidad':<15} | {'Costo':<5} |"
        
        tabla = [linea_separadora, encabezado, linea_separadora]
        
        for a in self.aristas:
            flujo_cap = f"{a.flujo}/{a.capacidad}"
            fila = f"| {a.origen:<6} | {a.destino:<7} | {flujo_cap:<15} | {a.costo:<5} |"
            tabla.append(fila)
            
        tabla.append(linea_separadora)
        return "\n".join(tabla)

    def generar_matriz_adyacencia(self) -> list[list[float]]:
        """
        Devuelve una representación matricial del flujo.
        Las filas representan el origen y las columnas el destino.
        Se asume que los nodos están indexados de 0 a N-1.
        """
        num_nodos = max(self.nodos) + 1 if self.nodos else 0
        # Inicializamos la matriz con ceros
        matriz = [[0.0 for _ in range(num_nodos)] for _ in range(num_nodos)]
        
        for a in self.aristas:
            matriz[a.origen][a.destino] = a.flujo
            
        return matriz

    def resumen_red(self) -> str:
        """Muestra estadísticas agregadas de la red."""
        flujo_total = sum(a.flujo for a in self.aristas if a.origen == min(self.nodos)) # Flujo que sale de las fuentes
        costo_total = sum(a.flujo * a.costo for a in self.aristas)
        aristas_saturadas = sum(1 for a in self.aristas if a.es_saturada())
        
        resumen = (
            f"=== RESUMEN DE LA RED ===\n"
            f"Flujo Total Enviado (Salida): {flujo_total}\n"
            f"Costo Total de la Red:        {costo_total}\n"
            f"Aristas Saturadas:            {aristas_saturadas}/{len(self.aristas)}"
        )
        return resumen


# --- Bloque de Prueba para comprobar el funcionamiento ---
if __name__ == "__main__":
    # Creamos un conjunto de aristas para una red de 4 nodos (0, 1, 2, 3)
    # Formato: Arista(origen, destino, capacidad, costo, flujo)
    red_datos = [
        Arista(0, 1, capacidad=10, costo=2, flujo=8),
        Arista(0, 2, capacidad=5,  costo=5, flujo=5),  # Saturada
        Arista(1, 2, capacidad=2,  costo=1, flujo=2),  # Saturada
        Arista(1, 3, capacidad=8,  costo=4, flujo=6),
        Arista(2, 3, capacidad=10, costo=2, flujo=7)
    ]
    
    red = RedFlujo(red_datos)
    
    # 1. Prueba de __repr__
    print(">>> Prueba de __repr__:")
    print(repr(red))
    print("\n")
    
    # 2. Prueba de __str__ (Tabla de Aristas)
    print(">>> Prueba de __str__ (Tabla de Aristas):")
    print(red)
    print("\n")
    
    # 3. Prueba de generar_matriz_adyacencia()
    print(">>> Matriz de Adyacencia (Flujos):")
    matriz = red.generar_matriz_adyacencia()
    for fila in matriz:
        print(fila)
    print("\n")
    
    # 4. Prueba de resumen_red()
    print(">>> Resumen Estadístico:")
    print(red.resumen_red())
