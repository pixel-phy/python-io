"""Ejercicio 12: Sistema de Gestión de Rutas con Visualización

Crea un sistema completo que integre:

a) Clase Nodo (de Día 1) con:

__repr__: muestra ID y coordenadas

__str__: muestra nombre amigable del nodo

b) Clase RedTransporte que contenga:

Lista de nodos

Diccionario de aristas

Matriz de distancias (calculada con método estático)

c) Métodos de visualización:

reporte_rutas_optimas(): genera reporte de todas las rutas posibles

visualizar_red_simple(): representa la red en texto (ASCII art o formato tabular)

exportar_a_formato_io(): genera un archivo de texto con todos los datos del problema

d) Implementa el problema del agente viajero (TSP) simple:

Encuentra la ruta más corta que visita todos los nodos (fuerza bruta para ≤ 6 nodos)

Muestra el resultado usando todas las representaciones creadas

"""
import itertools
import math

class Nodo:
    """
    Representa un nodo en una red de transporte.
    """
    def __init__(self, id_nodo: str, coordenada_x: float, coordenada_y: float, demanda: float = 0):
        self.id_nodo = id_nodo
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.demanda = demanda
        self.oferta = 0  
        self.visitado = False  
        
    def set_oferta(self, cantidad: float):
        if cantidad < 0:
            raise ValueError("La oferta no puede ser negativa")
        self.oferta = cantidad
        
    def calcular_distancia_a(self, otro_nodo: 'Nodo') -> float:
        dx = self.coordenada_x - otro_nodo.coordenada_x
        dy = self.coordenada_y - otro_nodo.coordenada_y
        return (dx**2 + dy**2)**0.5
    
    def es_oferente(self) -> bool:
        return self.oferta > 0
    
    def es_demandante(self) -> bool:
        return self.demanda > 0
    
    def balance(self) -> float:
        return self.oferta - self.demanda

    # --- NUEVOS MÉTODOS NODO (EJERCICIO 5) ---
    def __repr__(self) -> str:
        """Representación técnica de depuración."""
        return f"Nodo(ID: '{self.id_nodo}', X: {self.coordenada_x}, Y: {self.coordenada_y})"

    def __str__(self) -> str:
        """Representación amigable del nodo."""
        tipo = "Oferta" if self.es_oferente() else ("Demanda" if self.es_demandante() else "De Paso")
        return f"Nodo [{self.id_nodo}] ({tipo})"


class RedTransporte:
    def __init__(self, lista_nodos: list[Nodo]):
        self.nodos = lista_nodos
        # Diccionario de aristas mapeando (id_origen, id_destino) -> distancia
        self.aristas = {}
        # Matriz de distancias implícita
        self.matriz_distancias = self.calcular_matriz_distancias(self.nodos)
        self.generar_diccionario_aristas()

    @staticmethod
    def calcular_matriz_distancias(nodos: list[Nodo]) -> list[list[float]]:
        """Método estático para calcular la matriz completa de distancias euclidianas."""
        n = len(nodos)
        matriz = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matriz[i][j] = nodos[i].calcular_distancia_a(nodos[j])
        return matriz

    def generar_diccionario_aristas(self):
        """Puebla el diccionario de aristas utilizando la matriz generada."""
        for i, nodo_i in enumerate(self.nodos):
            for j, nodo_j in enumerate(self.nodos):
                if i != j:
                    self.aristas[(nodo_i.id_nodo, nodo_j.id_nodo)] = self.matriz_distancias[i][j]

    # --- MÉTODOS DE VISUALIZACIÓN ---

    def visualizar_red_simple(self) -> str:
        """Representa la red y sus distancias en un formato tabular limpio."""
        linea = "-" * 45
        salida = [linea, f"| {'Origen':^8} | {'Destino':^9} | {'Distancia':^14} |", linea]
        
        for (origen, destino), dist in sorted(self.aristas.items()):
            salida.append(f"| {origen:^8} | {destino:^9} | {dist:>12.2f} |")
        
        salida.append(linea)
        return "\n".join(salida)

    def reporte_rutas_optimas(self) -> str:
        """Genera un reporte de todas las permutaciones (rutas) posibles para el TSP."""
        if len(self.nodos) > 6:
            return "Reporte omitido: Demasiados nodos para fuerza bruta (> 6)."

        salida = ["=== REPORTE DE TODAS LAS RUTAS POSIBLES (TSP) ==="]
        id_nodos = [n.id_nodo for n in self.nodos]
        nodo_inicial = id_nodos[0]
        nodos_restantes = id_nodos[1:]

        # Generar permutaciones de los nodos intermedios
        for perm in itertools.permutations(nodos_restantes):
            ruta = [nodo_inicial] + list(perm) + [nodo_inicial]
            distancia_total = 0.0
            
            for k in range(len(ruta) - 1):
                distancia_total += self.aristas[(ruta[k], ruta[k+1])]
                
            ruta_str = " -> ".join(ruta)
            salida.append(f"Ruta: {ruta_str} | Distancia Total: {distancia_total:.2f}")

        return "\n".join(salida)

    def exportar_a_formato_io(self, nombre_archivo: str):
        """Genera un archivo estructurado con los datos puros para solvers de IO."""
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("=== DATOS DE ENTRADA DEL PROBLEMA DE TRANSPORTE / TSP ===\n")
            f.write(f"NUM_NODOS: {len(self.nodos)}\n\n")
            f.write("ID\tCOORD_X\tCOORD_Y\tOFERTA\tDEMANDA\n")
            for n in self.nodos:
                f.write(f"{n.id_nodo}\t{n.coordenada_x}\t{n.coordenada_y}\t{n.oferta}\t{n.demanda}\n")
            
            f.write("\nMATRIZ DE DISTANCIAS\n\t")
            f.write("\t".join(n.id_nodo for n in self.nodos) + "\n")
            for i, nodo in enumerate(self.nodos):
                valores_fila = "\t".join(f"{val:.2f}" for val in self.matriz_distancias[i])
                f.write(f"{nodo.id_nodo}\t{valores_fila}\n")

   # --- RESOLUCIÓN DEL TSP (FUERZA BRUTA) ---

    def resolver_tsp_fuerza_bruta(self) -> tuple[list[str], float]:
        """
        Encuentra la ruta óptima del TSP regresando al nodo origen.
        Fuerza bruta limitada por seguridad a <= 6 nodos.
        """
        id_nodos = [n.id_nodo for n in self.nodos]
        if len(id_nodos) > 6:
            raise ValueError("Límite de seguridad de fuerza bruta excedido (> 6 nodos).")

        nodo_inicial = id_nodos[0]
        nodos_restantes = id_nodos[1:]
        
        mejor_ruta = []
        mejor_distancia = float('inf')

        # Evaluación exhaustiva
        for perm in itertools.permutations(nodos_restantes):
            ruta_actual = [nodo_inicial] + list(perm) + [nodo_inicial]
            distancia_actual = 0.0
            
            for i in range(len(ruta_actual) - 1):
                distancia_actual += self.aristas[(ruta_actual[i], ruta_actual[i+1])]
                
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_ruta = ruta_actual

        return mejor_ruta, mejor_distancia

# --- BLOQUE DE COMPROBACIÓN Y PRUEBA ---
if __name__ == "__main__":
    # 1. Instanciar 4 Ciudades/Nodos geográficos
    ciudad_A = Nodo("A", 0, 0)
    ciudad_B = Nodo("B", 0, 4)  # Distancia A-B = 4
    ciudad_C = Nodo("C", 3, 4)  # Distancia B-C = 3, A-C = 5
    ciudad_D = Nodo("D", 3, 0)  # Distancia C-D = 4, A-D = 3, B-D = 5

    # Añadir un poco de contexto operativo de IO
    ciudad_A.set_oferta(100)
    ciudad_C.demanda = 50

    lista_nodos = [ciudad_A, ciudad_B, ciudad_C, ciudad_D]

    print(">>> 1. PROBANDO REPRESENTACIONES INDIVIDUALES (Nodos):")
    print("__repr__ de Nodo A:", repr(ciudad_A))
    print("__str__ de Nodo A :", ciudad_A)
    print("__str__ de Nodo C :", ciudad_C)
    print("-" * 60 + "\n")

    # 2. Inicializar la red de transporte
    red = RedTransporte(lista_nodos)

    print(">>> 2. VISUALIZACIÓN DE LA RED (Formato Tabular):")
    print(red.visualizar_red_simple())
    print("-" * 60 + "\n")

    print(">>> 3. REPORTE COMPLETO DE RUTAS POSIBLES:")
    print(red.reporte_rutas_optimas())
    print("-" * 60 + "\n")

    print(">>> 4. EJECUTANDO SOLVER EXACTO TSP (Fuerza Bruta):")
    ruta_optima, dist_optima = red.resolver_tsp_fuerza_bruta()
    print(f"¡Ruta Óptima Encontrada!: {' -> '.join(ruta_optima)}")
    print(f"Distancia Total Mínima : {dist_optima:.2f}")
    print("-" * 60 + "\n")

    # 5. Exportar datos del problema
    archivo_io = "datos_red_io.txt"
    red.exportar_a_formato_io(archivo_io)
    print(f">>> 5. ¡Éxito! Datos de IO exportados correctamente a '{archivo_io}'.")
