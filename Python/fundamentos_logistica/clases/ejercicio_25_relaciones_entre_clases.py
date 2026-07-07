"""Ejercicio 25: Relaciones entre Clases (Composición y Agregación)

En Python, las clases pueden relacionarse de diferentes formas:
1. Composición:
- Una clase contiene instancias de otra clase como atributos.
- El ciclo de vida del objeto contenido depende del objeto contenedor.
- Ejemplo: Un Grafo contiene Nodos y Aristas.

2. Agregación:
- Similar a composición pero con independencia.
- El objeto contenido puede existir sin el contenedor.
- Ejemplo: Un modelo PL contiene Restricciones pero estas pueden existir independientemente.

3. Asociación:
- Las clases están relacionadas pero no se contienen.
- Ejemplo: Un Solver usa un ModeloPL para resolverlo.

4. Herencia:
- Relación jerárquica donde una clase extiende otra.
- Ejemplo: RedFlujoGlobal es una RedFlujo

"""

# Ejemplo de aplicación: Sistema de Red de transporte con Composición
from typing import List, Dict, Optional, Tuple
import math

class Nodo:
    """Representa un nodo en una red de transporte."""
    
    def __init__(self, id_nodo: str, x: float, y: float, demanda: float = 0):
        self.id_nodo = id_nodo
        self.x = x
        self.y = y
        self.demanda = demanda
        self.oferta = 0
        self.visitado = False
    
    def set_oferta(self, oferta: float):
        if oferta < 0:
            raise ValueError("La oferta no puede ser negativa")
        self.oferta = oferta
    
    def distancia_a(self, otro: 'Nodo') -> float:
        return math.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)
    
    def __repr__(self):
        return f"Nodo('{self.id_nodo}', x={self.x}, y={self.y})"
    
    def __str__(self):
        return f"Nodo {self.id_nodo} (Demanda: {self.demanda}, Oferta: {self.oferta})"


class Arista:
    """Representa una arista en una red de transporte."""
    
    def __init__(self, origen: str, destino: str, capacidad: float, costo: float):
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.costo = costo
        self.flujo = 0.0
    
    def enviar_flujo(self, cantidad: float):
        if cantidad < 0:
            raise ValueError("Cantidad negativa no permitida")
        if self.flujo + cantidad > self.capacidad:
            raise ValueError(f"Capacidad excedida. Capacidad: {self.capacidad}")
        self.flujo += cantidad
    
    def flujo_disponible(self) -> float:
        return self.capacidad - self.flujo
    
    def costo_total(self) -> float:
        return self.flujo * self.costo
    
    def __repr__(self):
        return f"Arista({self.origen}→{self.destino}, flujo={self.flujo}/{self.capacidad})"


class RedTransporte:
    """
    Clase que modela una red de transporte completa.
    RELACIONES DE COMPOSICIÓN: Contiene Nodos y Aristas.
    """
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._nodos: Dict[str, Nodo] = {}  # Composición: diccionario de nodos
        self._aristas: Dict[Tuple[str, str], Arista] = {}  # Composición: diccionario de aristas
        
    # --- GESTIÓN DE NODOS ---
    
    def agregar_nodo(self, id_nodo: str, x: float, y: float, demanda: float = 0) -> 'RedTransporte':
        """Agrega un nodo a la red (fluent interface)."""
        if id_nodo in self._nodos:
            raise ValueError(f"El nodo '{id_nodo}' ya existe")
        self._nodos[id_nodo] = Nodo(id_nodo, x, y, demanda)
        return self  # Permite encadenamiento
    
    def obtener_nodo(self, id_nodo: str) -> Nodo:
        """Obtiene un nodo por su ID."""
        if id_nodo not in self._nodos:
            raise KeyError(f"Nodo '{id_nodo}' no encontrado")
        return self._nodos[id_nodo]
    
    def eliminar_nodo(self, id_nodo: str):
        """Elimina un nodo y todas sus aristas asociadas."""
        if id_nodo not in self._nodos:
            raise KeyError(f"Nodo '{id_nodo}' no encontrado")
        
        # Eliminar aristas que involucran este nodo
        aristas_a_eliminar = [
            (o, d) for (o, d) in self._aristas.keys()
            if o == id_nodo or d == id_nodo
        ]
        for key in aristas_a_eliminar:
            del self._aristas[key]
        
        del self._nodos[id_nodo]
    
    # --- GESTIÓN DE ARISTAS ---
    
    def agregar_arista(self, origen: str, destino: str, capacidad: float, costo: float) -> 'RedTransporte':
        """Agrega una arista entre dos nodos existentes."""
        if origen not in self._nodos:
            raise ValueError(f"Nodo origen '{origen}' no existe")
        if destino not in self._nodos:
            raise ValueError(f"Nodo destino '{destino}' no existe")
        
        key = (origen, destino)
        if key in self._aristas:
            raise ValueError(f"Arista {origen}→{destino} ya existe")
        
        self._aristas[key] = Arista(origen, destino, capacidad, costo)
        return self  # Fluent interface
    
    def obtener_arista(self, origen: str, destino: str) -> Arista:
        """Obtiene una arista por su origen y destino."""
        key = (origen, destino)
        if key not in self._aristas:
            raise KeyError(f"Arista {origen}→{destino} no encontrada")
        return self._aristas[key]
    
    def aristas_desde(self, origen: str) -> List[Arista]:
        """Retorna todas las aristas que salen de un nodo."""
        return [a for (o, d), a in self._aristas.items() if o == origen]
    
    def aristas_hacia(self, destino: str) -> List[Arista]:
        """Retorna todas las aristas que llegan a un nodo."""
        return [a for (o, d), a in self._aristas.items() if d == destino]
    
    # --- MÉTODOS DE ANÁLISIS DE RED ---
    
    def flujo_total(self) -> float:
        """Calcula el flujo total en la red."""
        return sum(a.flujo for a in self._aristas.values())
    
    def costo_total(self) -> float:
        """Calcula el costo total de la red."""
        return sum(a.costo_total() for a in self._aristas.values())
    
    def nodos_saturados(self) -> List[str]:
        """Retorna IDs de nodos con todas sus aristas salientes saturadas."""
        saturados = []
        for id_nodo in self._nodos:
            aristas = self.aristas_desde(id_nodo)
            if aristas and all(a.flujo_disponible() == 0 for a in aristas):
                saturados.append(id_nodo)
        return saturados
    
    def es_conexa(self) -> bool:
        """Verifica si la red es conexa (todos los nodos alcanzables)."""
        if not self._nodos:
            return True
        
        # BFS desde el primer nodo
        inicio = next(iter(self._nodos))
        visitados = set()
        cola = [inicio]
        
        while cola:
            actual = cola.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            # Agregar vecinos
            for arista in self.aristas_desde(actual):
                if arista.destino not in visitados:
                    cola.append(arista.destino)
            # También considerar aristas que llegan (para redes no dirigidas)
            for arista in self.aristas_hacia(actual):
                if arista.origen not in visitados:
                    cola.append(arista.origen)
        
        return len(visitados) == len(self._nodos)
    
    def matriz_distancias(self) -> List[List[float]]:
        """Calcula la matriz de distancias entre todos los nodos (Dijkstra)."""
        # Simplificado: para redes completas, usar distancias euclidianas
        nodos_lista = list(self._nodos.values())
        n = len(nodos_lista)
        matriz = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    matriz[i][j] = nodos_lista[i].distancia_a(nodos_lista[j])
        
        return matriz
    
    # --- VISUALIZACIÓN ---
    
    def reporte_completo(self) -> str:
        """Genera un reporte completo de la red."""
        reporte = f"RED DE TRANSPORTE: {self.nombre}\n"
        reporte += "=" * 50 + "\n\n"
        
        reporte += f"NODOS ({len(self._nodos)}):\n"
        for nodo in self._nodos.values():
            reporte += f"  • {nodo}\n"
        
        reporte += f"\nARISTAS ({len(self._aristas)}):\n"
        for arista in self._aristas.values():
            reporte += f"  • {arista}\n"
        
        reporte += f"\nESTADÍSTICAS:\n"
        reporte += f"  Flujo total: {self.flujo_total():.2f}\n"
        reporte += f"  Costo total: ${self.costo_total():.2f}\n"
        reporte += f"  Red conexa: {'Sí' if self.es_conexa() else 'No'}\n"
        
        saturados = self.nodos_saturados()
        if saturados:
            reporte += f"  Nodos saturados: {', '.join(saturados)}"
        
        return reporte
    
    def __repr__(self):
        return f"RedTransporte('{self.nombre}', nodos={len(self._nodos)}, aristas={len(self._aristas)})"
    
    def __str__(self):
        return f"Red '{self.nombre}' - {len(self._nodos)} nodos, {len(self._aristas)} aristas"


# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    # Crear red usando Fluent Interface (encadenamiento)
    red = (RedTransporte("Red Distribución Central")
           .agregar_nodo("A", 0, 0, demanda=50)
           .agregar_nodo("B", 10, 0, demanda=0)
           .agregar_nodo("C", 5, 8, demanda=30)
           .agregar_nodo("D", 12, 5, demanda=20)
           .agregar_arista("A", "B", 100, 2.5)
           .agregar_arista("A", "C", 80, 3.0)
           .agregar_arista("B", "C", 60, 1.5)
           .agregar_arista("B", "D", 70, 2.0)
           .agregar_arista("C", "D", 50, 2.5))
    
    # Enviar flujo en algunas aristas
    red.obtener_arista("A", "B").enviar_flujo(80)
    red.obtener_arista("A", "C").enviar_flujo(40)
    red.obtener_arista("B", "D").enviar_flujo(60)
    
    # Mostrar reporte
    print(red.reporte_completo())
    
    print("\n" + "=" * 50)
    
    # Mostrar matriz de distancias
    print("\nMATRIZ DE DISTANCIAS:")
    matriz = red.matriz_distancias()
    for fila in matriz:
        print("  ".join(f"{v:6.2f}" for v in fila))
    
    # Verificar si la red es conexa
    print(f"\n¿Red conexa? {red.es_conexa()}")
