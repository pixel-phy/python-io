"""Validación de Conectividad en Almacenes

Una empresa logística tiene una red de distribución no dirigida. Crea una función/método
que reciba el nombre de un almacén y determine su grado (cuántas rutas directas entran/salen de él)
y cuáles son sus almacenes vecinos. """

class RedDistribucion:
    def __init__(self):
        """Inicializa la red como un diccionario de adyacencia"""
        self.grafo = {}
    
    def agregar_ruta(self, almacen1, almacen2):
        """Agrega una ruta bidireccional entre dos almacenes"""
        # Si el almacén no existe, lo creamos con una lista vacía
        if almacen1 not in self.grafo:
            self.grafo[almacen1] = []
        if almacen2 not in self.grafo:
            self.grafo[almacen2] = []
        
        # Agregamos la conexión bidireccional (grafo no dirigido)
        if almacen2 not in self.grafo[almacen1]:
            self.grafo[almacen1].append(almacen2)
        if almacen1 not in self.grafo[almacen2]:
            self.grafo[almacen2].append(almacen1)
    
    def obtener_grado_y_vecinos(self, almacen):
        """
        Retorna el grado y los vecinos de un almacén
        
        Returns:
            tuple: (grado, lista_vecinos)
        """
        # Validamos si el almacén existe en la red
        if almacen not in self.grafo:
            return 0, []  # O podríamos lanzar una excepción
        
        vecinos = self.grafo[almacen].copy()  # Copia para no modificar el original
        grado = len(vecinos)
        
        return grado, vecinos
    
    def mostrar_informacion(self, almacen):
        """Muestra información formateada del almacén"""
        grado, vecinos = self.obtener_grado_y_vecinos(almacen)
        
        if grado == 0 and almacen not in self.grafo:
            print(f" El almacén '{almacen}' no existe en la red.")
        else:
            print(f"Almacén: {almacen}")
            print(f"Grado: {grado} ruta(s) directa(s)")
            print(f"Vecinos: {vecinos if vecinos else 'Ninguno'}")

# Ejemplo de uso
if __name__ == "__main__":
    # Creamos la red de distribución
    red = RedDistribucion()
    
    # Agregamos rutas (conexiones)
    red.agregar_ruta("AlmacenA", "AlmacenB")
    red.agregar_ruta("AlmacenA", "AlmacenC")
    red.agregar_ruta("AlmacenB", "AlmacenD")
    red.agregar_ruta("AlmacenC", "AlmacenD")
    red.agregar_ruta("AlmacenC", "AlmacenE")
    red.agregar_ruta("AlmacenE", "AlmacenF")
    
    # Consultamos información
    red.mostrar_informacion("AlmacenA")
    red.mostrar_informacion("AlmacenC")
    red.mostrar_informacion("AlmacenF")
    red.mostrar_informacion("AlmacenZ") 
