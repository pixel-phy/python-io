"""Ejercicio 23: Modularidad y Cuellos de Botella (Componentes Fuertemente Conexas)

En una red de distribución urbana bidireccional, a veces se imponen sentidos únicos de tráfico.
Si la red se vuelve inconexa, camiones que salen de un nodo A podrían no poder regresar jamás
a él. Implementa una clase que use DFS para identificar si la red es Fuertemente Conexa (es decir,
si existe un camino válido de ida y vuelta entre cualquier par de ciudades de la red). """

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

class AnalizadorConexidad:
    """Analiza la conexidad fuerte de una red de distribución urbana."""
    
    def __init__(self):
        self.grafo: Dict[str, List[str]] = {}
        self.grafo_invertido: Dict[str, List[str]] = {}
        self.orden: List[str] = []
        self.componentes: List[Set[str]] = []
        
    def agregar_conexion(self, ciudad_origen: str, ciudad_destino: str) -> None:
        """
        Agrega una conexion dirigida entre dos ciudades.
        
        Args:
            ciudad_origen: Ciudad de origen (sentido de la via)
            ciudad_destino: Ciudad de destino (sentido de la via)
        """
        # Grafo original
        if ciudad_origen not in self.grafo:
            self.grafo[ciudad_origen] = []
        if ciudad_destino not in self.grafo:
            self.grafo[ciudad_destino] = []
        self.grafo[ciudad_origen].append(ciudad_destino)
        
        # Grafo invertido (para Kosaraju)
        if ciudad_destino not in self.grafo_invertido:
            self.grafo_invertido[ciudad_destino] = []
        if ciudad_origen not in self.grafo_invertido:
            self.grafo_invertido[ciudad_origen] = []
        self.grafo_invertido[ciudad_destino].append(ciudad_origen)
    
    def agregar_conexion_bidireccional(self, ciudad_a: str, ciudad_b: str) -> None:
        """Agrega una conexion bidireccional (dos sentidos)."""
        self.agregar_conexion(ciudad_a, ciudad_b)
        self.agregar_conexion(ciudad_b, ciudad_a)
    
    def _dfs_orden(self, nodo: str, visitados: Set[str]) -> None:
        """
        Primer DFS: Construye el orden de finalizacion.
        """
        visitados.add(nodo)
        
        for vecino in self.grafo[nodo]:
            if vecino not in visitados:
                self._dfs_orden(vecino, visitados)
        
        # Agregar al orden de finalizacion (postorden)
        self.orden.append(nodo)
    
    def _dfs_componente(self, nodo: str, visitados: Set[str], componente: Set[str]) -> None:
        """
        Segundo DFS: Encuentra una componente fuertemente conexa.
        """
        visitados.add(nodo)
        componente.add(nodo)
        
        for vecino in self.grafo_invertido[nodo]:
            if vecino not in visitados:
                self._dfs_componente(vecino, visitados, componente)
    
    def encontrar_componentes_fuertemente_conexas(self) -> List[Set[str]]:
        """
        Encuentra todas las componentes fuertemente conexas usando Kosaraju.
        
        Returns:
            List[Set[str]]: Lista de componentes fuertemente conexas
        """
        if not self.grafo:
            return []
        
        # Primer paso: DFS en grafo original para orden de finalizacion
        visitados = set()
        self.orden = []
        
        for nodo in self.grafo:
            if nodo not in visitados:
                self._dfs_orden(nodo, visitados)
        
        # Segundo paso: DFS en grafo invertido en orden inverso
        visitados = set()
        self.componentes = []
        
        for nodo in reversed(self.orden):
            if nodo not in visitados:
                componente = set()
                self._dfs_componente(nodo, visitados, componente)
                self.componentes.append(componente)
        
        return self.componentes
    
    def es_fuertemente_conexa(self) -> bool:
        """
        Determina si la red es fuertemente conexa.
        
        Returns:
            bool: True si la red es fuertemente conexa, False en caso contrario
        """
        componentes = self.encontrar_componentes_fuertemente_conexas()
        
        # Una red es fuertemente conexa si tiene una sola componente
        return len(componentes) == 1
    
    def encontrar_cuellos_de_botella(self) -> List[Tuple[str, str]]:
        """
        Identifica posibles cuellos de botella (aristas que conectan componentes).
        
        Returns:
            List[Tuple[str, str]]: Lista de aristas que conectan diferentes componentes
        """
        if self.es_fuertemente_conexa():
            return []
        
        # Mapear cada nodo a su componente
        nodo_a_componente = {}
        for i, componente in enumerate(self.componentes):
            for nodo in componente:
                nodo_a_componente[nodo] = i
        
        cuellos = []
        for origen, destinos in self.grafo.items():
            comp_origen = nodo_a_componente[origen]
            for destino in destinos:
                comp_destino = nodo_a_componente[destino]
                if comp_origen != comp_destino:
                    cuellos.append((origen, destino))
        
        return cuellos
    
    def verificar_accesibilidad(self, origen: str, destino: str) -> bool:
        """
        Verifica si existe un camino desde origen hasta destino.
        
        Args:
            origen: Nodo de inicio
            destino: Nodo de destino
            
        Returns:
            bool: True si existe camino, False en caso contrario
        """
        if origen not in self.grafo or destino not in self.grafo:
            return False
        
        visitados = set()
        stack = [origen]
        
        while stack:
            nodo = stack.pop()
            if nodo == destino:
                return True
            if nodo not in visitados:
                visitados.add(nodo)
                for vecino in self.grafo[nodo]:
                    if vecino not in visitados:
                        stack.append(vecino)
        
        return False
    
    def verificar_accesibilidad_bidireccional(self, origen: str, destino: str) -> bool:
        """
        Verifica si existe un camino de ida y vuelta entre dos nodos.
        
        Args:
            origen: Nodo de inicio
            destino: Nodo de destino
            
        Returns:
            bool: True si hay camino en ambos sentidos, False en caso contrario
        """
        return self.verificar_accesibilidad(origen, destino) and self.verificar_accesibilidad(destino, origen)
    
    def mostrar_analisis(self) -> None:
        """Muestra un analisis completo de la red."""
        print("ANALISIS DE CONEXIDAD DE LA RED DE DISTRIBUCION")
        print("=" * 60)
        
        # Encontrar componentes
        componentes = self.encontrar_componentes_fuertemente_conexas()
        
        print(f"Total de nodos: {len(self.grafo)}")
        print(f"Total de aristas dirigidas: {sum(len(v) for v in self.grafo.values())}")
        print(f"Numero de componentes fuertemente conexas: {len(componentes)}")
        print()
        
        if self.es_fuertemente_conexa():
            print("RESULTADO: La red ES FUERTEMENTE CONEXA")
            print("Cualquier camion puede salir de un nodo y regresar a el.")
        else:
            print("RESULTADO: La red NO ES FUERTEMENTE CONEXA")
            print("Hay camiones que no pueden regresar a su punto de partida.")
            print()
            
            print("Componentes fuertemente conexas:")
            for i, componente in enumerate(componentes, 1):
                print(f"  Componente {i}: {', '.join(sorted(componente))}")
            print()
            
            # Identificar cuellos de botella
            cuellos = self.encontrar_cuellos_de_botella()
            if cuellos:
                print("Cuellos de botella (aristas entre componentes):")
                for origen, destino in cuellos:
                    print(f"  {origen} -> {destino}")
        
        print("=" * 60)


# ===== EJEMPLO DE USO =====

def ejemplo_red_conexa():
    """Ejemplo de red fuertemente conexa."""
    print("EJEMPLO 1: RED FUERTEMENTE CONEXA")
    print("-" * 40)
    
    analizador = AnalizadorConexidad()
    
    # Red con todas las conexiones bidireccionales
    analizador.agregar_conexion_bidireccional("A", "B")
    analizador.agregar_conexion_bidireccional("B", "C")
    analizador.agregar_conexion_bidireccional("C", "D")
    analizador.agregar_conexion_bidireccional("D", "A")
    
    analizador.mostrar_analisis()
    print()

def ejemplo_red_inconexa():
    """Ejemplo de red no fuertemente conexa."""
    print("EJEMPLO 2: RED NO FUERTEMENTE CONEXA")
    print("-" * 40)
    
    analizador = AnalizadorConexidad()
    
    # Red con sentidos unicos que crea inconexidad
    analizador.agregar_conexion("A", "B")
    analizador.agregar_conexion("B", "C")
    analizador.agregar_conexion("C", "A")  # Ciclo A->B->C->A
    analizador.agregar_conexion("D", "E")
    analizador.agregar_conexion("E", "F")
    analizador.agregar_conexion("F", "D")  # Ciclo D->E->F->D
    analizador.agregar_conexion("C", "D")  # Conexion entre ciclos (solo un sentido)
    
    analizador.mostrar_analisis()
    print()
    
    # Verificar accesibilidad especifica
    print("VERIFICACION DE ACCESIBILIDAD:")
    print("-" * 40)
    pares = [("A", "D"), ("D", "A"), ("B", "E")]
    for origen, destino in pares:
        accesible = analizador.verificar_accesibilidad(origen, destino)
        bidireccional = analizador.verificar_accesibilidad_bidireccional(origen, destino)
        print(f"  {origen} -> {destino}: {accesible} (ida), {bidireccional} (ida y vuelta)")

def ejemplo_red_mixta():
    """Ejemplo de red con componentes mixtas."""
    print("EJEMPLO 3: RED CON COMPONENTES MIXTAS")
    print("-" * 40)
    
    analizador = AnalizadorConexidad()
    
    # Red de distribucion urbana con sentidos unicos
    analizador.agregar_conexion("Centro", "Norte")
    analizador.agregar_conexion("Centro", "Sur")
    analizador.agregar_conexion("Norte", "Este")
    analizador.agregar_conexion("Sur", "Oeste")
    analizador.agregar_conexion("Este", "Centro")  # Vuelve al centro desde este
    analizador.agregar_conexion("Oeste", "Centro")  # Vuelve al centro desde oeste
    analizador.agregar_conexion("Norte", "Norte")   # Auto-lazo (se ignora en componentes)
    
    analizador.mostrar_analisis()

# Ejecutar ejemplos
if __name__ == "__main__":
    ejemplo_red_conexa()
    print("\n" + "="*60 + "\n")
    ejemplo_red_inconexa()
    print("\n" + "="*60 + "\n")
    ejemplo_red_mixta()
