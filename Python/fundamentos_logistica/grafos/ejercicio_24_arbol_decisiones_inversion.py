"""Ejercicio 24: Árbol de Decisiones de Inversión en Capacidad

Una empresa evalúa expandir su capacidad logística a lo largo de 4 años. Cada decisión 
(ej, "Expander CD", "Arrendar Flota", "No hacer nada") abre un abanico de estados financieros
futuros en forma de árbol. Implementa un algoritmo DFS que recorra este árbol de decisiones
para encontrar la profundidad máxima del árbol y retorne el camino de decisiones que maximiza 
el Valor presente Neto (VPN) acumulado en las hojas. Cada arista tiene un costo/beneficio asociado. """

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import deque

@dataclass
class NodoDecision:
    """Representa un nodo en el árbol de decisiones."""
    nombre: str
    descripcion: str = ""
    vpn: float = 0.0  # VPN acumulado hasta este nodo
    
    def __str__(self):
        return f"{self.nombre} (VPN: {self.vpn:.2f})"

class ArbolDecisionInversion:
    """Árbol de decisiones para expansión de capacidad logística."""
    
    def __init__(self):
        self.raiz: Optional[NodoDecision] = None
        self.adyacencias: Dict[str, List[Tuple[str, float, str]]] = {}
        # Formato: nodo_origen -> [(nodo_destino, costo_beneficio, descripcion)]
        
        self.nodos: Dict[str, NodoDecision] = {}
        self.profundidad_maxima = 0
        self.mejor_camino: List[str] = []
        self.mejor_vpn = float('-inf')
        self.todos_caminos: List[List[str]] = []
        self.caminos_con_vpn: List[Tuple[List[str], float]] = []
    
    def agregar_nodo(self, nombre: str, descripcion: str = "", vpn: float = 0.0) -> None:
        """Agrega un nodo al árbol."""
        if nombre not in self.nodos:
            self.nodos[nombre] = NodoDecision(nombre, descripcion, vpn)
        
        if nombre not in self.adyacencias:
            self.adyacencias[nombre] = []
    
    def agregar_decision(self, nodo_origen: str, nodo_destino: str, 
                         costo_beneficio: float, descripcion: str = "") -> None:
        """
        Agrega una decisión (arista) entre dos nodos.
        
        Args:
            nodo_origen: Nodo de origen
            nodo_destino: Nodo de destino
            costo_beneficio: Costo (negativo) o beneficio (positivo) de la decisión
            descripcion: Descripción de la decisión
        """
        if nodo_origen not in self.adyacencias:
            self.adyacencias[nodo_origen] = []
        
        if nodo_destino not in self.nodos:
            self.agregar_nodo(nodo_destino)
        
        self.adyacencias[nodo_origen].append((nodo_destino, costo_beneficio, descripcion))
    
    def establecer_raiz(self, nombre_raiz: str) -> None:
        """Establece el nodo raíz del árbol."""
        if nombre_raiz in self.nodos:
            self.raiz = self.nodos[nombre_raiz]
        else:
            raise ValueError(f"El nodo {nombre_raiz} no existe en el árbol")
    
    def dfs_profundidad_maxima(self, nodo_actual: str, profundidad: int) -> int:
        """
        DFS para encontrar la profundidad máxima del árbol.
        
        Returns:
            int: Profundidad máxima desde el nodo actual
        """
        if not self.adyacencias.get(nodo_actual, []):
            return profundidad
        
        profundidad_max = profundidad
        for destino, _, _ in self.adyacencias[nodo_actual]:
            prof = self.dfs_profundidad_maxima(destino, profundidad + 1)
            profundidad_max = max(profundidad_max, prof)
        
        return profundidad_max
    
    def dfs_mejor_camino(self, nodo_actual: str, vpn_actual: float, 
                         camino_actual: List[str]) -> Tuple[float, List[str]]:
        """
        DFS con backtracking para encontrar el camino que maximiza el VPN.
        
        Returns:
            Tuple[float, List[str]]: (VPN máximo, camino que lo maximiza)
        """
        # Actualizar VPN con el valor del nodo actual
        vpn_actual += self.nodos[nodo_actual].vpn
        camino_actual.append(nodo_actual)
        
        # Si es hoja, evaluar el camino
        if not self.adyacencias.get(nodo_actual, []):
            # Guardar todos los caminos para análisis
            self.todos_caminos.append(camino_actual.copy())
            self.caminos_con_vpn.append((camino_actual.copy(), vpn_actual))
            
            # Actualizar mejor camino
            if vpn_actual > self.mejor_vpn:
                self.mejor_vpn = vpn_actual
                self.mejor_camino = camino_actual.copy()
            
            return vpn_actual, camino_actual.copy()
        
        # Explorar todas las decisiones
        mejor_vpn_local = float('-inf')
        mejor_camino_local = []
        
        for destino, costo_beneficio, _ in self.adyacencias[nodo_actual]:
            # Aplicar costo/beneficio de la arista
            vpn_con_decision = vpn_actual + costo_beneficio
            
            # DFS recursivo
            vpn_resultante, camino_resultante = self.dfs_mejor_camino(
                destino, vpn_con_decision, camino_actual.copy()
            )
            
            if vpn_resultante > mejor_vpn_local:
                mejor_vpn_local = vpn_resultante
                mejor_camino_local = camino_resultante
        
        return mejor_vpn_local, mejor_camino_local
    
    def dfs_iterativo_profundidad(self) -> Tuple[int, List[str]]:
        """
        DFS iterativo para encontrar profundidad máxima y el camino.
        
        Returns:
            Tuple[int, List[str]]: (Profundidad máxima, camino más profundo)
        """
        if not self.raiz:
            return 0, []
        
        profundidad_max = 0
        camino_mas_profundo = []
        
        # Stack: (nodo, profundidad, camino_actual)
        stack = [(self.raiz.nombre, 0, [self.raiz.nombre])]
        
        while stack:
            nodo, profundidad, camino = stack.pop()
            
            if profundidad > profundidad_max:
                profundidad_max = profundidad
                camino_mas_profundo = camino.copy()
            
            if nodo in self.adyacencias:
                for destino, _, _ in self.adyacencias[nodo]:
                    nuevo_camino = camino + [destino]
                    stack.append((destino, profundidad + 1, nuevo_camino))
        
        return profundidad_max, camino_mas_profundo
    
    def dfs_iterativo_vpn(self) -> Tuple[float, List[str]]:
        """
        DFS iterativo para encontrar el camino de máximo VPN.
        
        Returns:
            Tuple[float, List[str]]: (VPN máximo, camino que lo maximiza)
        """
        if not self.raiz:
            return 0.0, []
        
        mejor_vpn = float('-inf')
        mejor_camino = []
        
        # Stack: (nodo, vpn_acumulado, camino_actual)
        vpn_inicial = self.nodos[self.raiz.nombre].vpn
        stack = [(self.raiz.nombre, vpn_inicial, [self.raiz.nombre])]
        
        while stack:
            nodo, vpn_actual, camino = stack.pop()
            
            # Verificar si es hoja
            if not self.adyacencias.get(nodo, []):
                if vpn_actual > mejor_vpn:
                    mejor_vpn = vpn_actual
                    mejor_camino = camino.copy()
            
            # Explorar hijos
            if nodo in self.adyacencias:
                for destino, costo_beneficio, _ in self.adyacencias[nodo]:
                    nuevo_vpn = vpn_actual + costo_beneficio + self.nodos[destino].vpn
                    nuevo_camino = camino + [destino]
                    stack.append((destino, nuevo_vpn, nuevo_camino))
        
        return mejor_vpn, mejor_camino
    
    def mostrar_analisis_completo(self) -> None:
        """Muestra un análisis completo del árbol de decisiones."""
        if not self.raiz:
            print("El árbol está vacío. Agregue nodos y decisiones primero.")
            return
        
        print("ANALISIS DEL ARBOL DE DECISIONES DE INVERSION")
        print("=" * 70)
        
        # 1. Estructura del árbol
        print("\nESTRUCTURA DEL ARBOL:")
        print("-" * 40)
        self._imprimir_arbol(self.raiz.nombre, 0)
        
        # 2. Profundidad máxima
        print("\nPROFUNDIDAD MAXIMA:")
        print("-" * 40)
        prof_recursiva = self.dfs_profundidad_maxima(self.raiz.nombre, 0)
        prof_iterativa, camino_profundo = self.dfs_iterativo_profundidad()
        print(f"  Profundidad máxima (recursiva): {prof_recursiva}")
        print(f"  Profundidad máxima (iterativa): {prof_iterativa}")
        print(f"  Camino más profundo: {' -> '.join(camino_profundo)}")
        
        # 3. Mejor camino por VPN (DFS recursivo)
        print("\nMEJOR CAMINO POR VPN (DFS RECURSIVO):")
        print("-" * 40)
        vpn_max, camino_optimo = self.dfs_mejor_camino(
            self.raiz.nombre, 0.0, []
        )
        print(f"  VPN máximo: {vpn_max:.2f}")
        print(f"  Camino óptimo: {' -> '.join(camino_optimo)}")
        self._mostrar_detalles_camino(camino_optimo)
        
        # 4. Mejor camino por VPN (DFS iterativo)
        print("\nMEJOR CAMINO POR VPN (DFS ITERATIVO):")
        print("-" * 40)
        vpn_iter, camino_iter = self.dfs_iterativo_vpn()
        print(f"  VPN máximo: {vpn_iter:.2f}")
        print(f"  Camino óptimo: {' -> '.join(camino_iter)}")
        
        # 5. Análisis de todos los caminos
        print("\nANALISIS DE TODOS LOS CAMINOS POSIBLES:")
        print("-" * 60)
        print(f"  Total de caminos posibles: {len(self.todos_caminos)}")
        
        if self.todos_caminos:
            # Ordenar caminos por VPN
            caminos_ordenados = sorted(
                self.caminos_con_vpn, 
                key=lambda x: x[1], 
                reverse=True
            )
            
            print("\n  Top 5 caminos por VPN:")
            for i, (camino, vpn) in enumerate(caminos_ordenados[:5], 1):
                print(f"    {i}. VPN: {vpn:.2f} | Camino: {' -> '.join(camino)}")
        
        print("\n" + "=" * 70)
    
    def _imprimir_arbol(self, nodo: str, nivel: int) -> None:
        """Imprime la estructura del árbol de forma jerárquica."""
        indent = "  " * nivel
        desc = self.nodos[nodo].descripcion
        vpn = self.nodos[nodo].vpn
        print(f"{indent}├─ {nodo} (VPN: {vpn:.2f}){f' - {desc}' if desc else ''}")
        
        if nodo in self.adyacencias:
            for i, (destino, costo, desc_arista) in enumerate(self.adyacencias[nodo]):
                es_ultimo = (i == len(self.adyacencias[nodo]) - 1)
                prefijo = "  " * (nivel + 1) + ("└─" if es_ultimo else "├─")
                
                # Mostrar información de la arista
                signo = "+" if costo >= 0 else ""
                print(f"{prefijo}→ {destino} ({signo}{costo:.2f}){f' - {desc_arista}' if desc_arista else ''}")
                
                # Recursión para hijos
                self._imprimir_arbol_recursivo(destino, nivel + 2)
    
    def _imprimir_arbol_recursivo(self, nodo: str, nivel: int) -> None:
        """Método auxiliar para imprimir el árbol recursivamente."""
        if nodo in self.adyacencias:
            for i, (destino, costo, desc_arista) in enumerate(self.adyacencias[nodo]):
                es_ultimo = (i == len(self.adyacencias[nodo]) - 1)
                prefijo = "  " * nivel + ("└─" if es_ultimo else "├─")
                signo = "+" if costo >= 0 else ""
                print(f"{prefijo}→ {destino} ({signo}{costo:.2f}){f' - {desc_arista}' if desc_arista else ''}")
                
                # Mostrar VPN del nodo
                vpn_nodo = self.nodos[destino].vpn
                if vpn_nodo != 0:
                    print(f"{'  ' * (nivel + 1)}  (VPN nodo: {vpn_nodo:.2f})")
                
                self._imprimir_arbol_recursivo(destino, nivel + 1)
    
    def _mostrar_detalles_camino(self, camino: List[str]) -> None:
        """Muestra los detalles de un camino específico."""
        if len(camino) < 2:
            return
        
        print("  Detalles del camino:")
        vpn_acumulado = 0.0
        
        for i in range(len(camino) - 1):
            origen = camino[i]
            destino = camino[i + 1]
            
            # Buscar la arista
            if origen in self.adyacencias:
                for dest, costo, desc in self.adyacencias[origen]:
                    if dest == destino:
                        vpn_acumulado += costo + self.nodos[destino].vpn
                        signo = "+" if costo >= 0 else ""
                        print(f"    {origen} -> {destino}: {signo}{costo:.2f} "
                              f"(acumulado: {vpn_acumulado:.2f}) "
                              f"{f'- {desc}' if desc else ''}")
                        break


# ===== EJEMPLO DE USO =====
def crear_arbol_inversion_logistica() -> ArbolDecisionInversion:
    """Crea un árbol de decisiones para inversión en capacidad logística."""
    arbol = ArbolDecisionInversion()
    
    # Años: 0 (inicio), 1, 2, 3, 4 (final)
    
    # Nodo raíz - Año 0
    arbol.agregar_nodo("Inicio", "Decisión inicial de inversión", 0.0)
    
    # Año 1 - Decisiones iniciales
    arbol.agregar_nodo("Expandir CD", "Expandir Centro de Distribución", 50.0)
    arbol.agregar_nodo("Arrendar Flota", "Arrendar flota de camiones", 30.0)
    arbol.agregar_nodo("No hacer nada", "Mantener capacidad actual", 10.0)
    
    # Decisiones desde Inicio (Año 0 -> Año 1)
    arbol.agregar_decision("Inicio", "Expandir CD", -100.0, "Inversión en CD")
    arbol.agregar_decision("Inicio", "Arrendar Flota", -80.0, "Inversión en flota")
    arbol.agregar_decision("Inicio", "No hacer nada", 0.0, "Sin inversión")
    
    # Año 2 - Decisiones desde Expandir CD
    arbol.agregar_nodo("Alta demanda", "Alta demanda de capacidad", 80.0)
    arbol.agregar_nodo("Baja demanda", "Baja demanda de capacidad", 40.0)
    
    arbol.agregar_decision("Expandir CD", "Alta demanda", 60.0, "Buena respuesta del mercado")
    arbol.agregar_decision("Expandir CD", "Baja demanda", 20.0, "Mala respuesta del mercado")
    
    # Año 2 - Decisiones desde Arrendar Flota
    arbol.agregar_nodo("Expandir ruta", "Expandir rutas de distribución", 45.0)
    arbol.agregar_nodo("Optimizar rutas", "Optimizar rutas existentes", 35.0)
    
    arbol.agregar_decision("Arrendar Flota", "Expandir ruta", 40.0, "Nuevas rutas")
    arbol.agregar_decision("Arrendar Flota", "Optimizar rutas", 25.0, "Mejora continua")
    
    # Año 2 - Decisiones desde No hacer nada
    arbol.agregar_nodo("Esperar", "Esperar mejores condiciones", 15.0)
    arbol.agregar_nodo("Vender activos", "Vender activos logísticos", 5.0)
    
    arbol.agregar_decision("No hacer nada", "Esperar", 10.0, "Paciencia estratégica")
    arbol.agregar_decision("No hacer nada", "Vender activos", -20.0, "Liquidación")
    
    # Año 3 - Decisiones desde Alta demanda
    arbol.agregar_nodo("Contratar personal", "Contratar más personal", 70.0)
    arbol.agregar_nodo("Automatizar", "Automatizar procesos", 90.0)
    
    arbol.agregar_decision("Alta demanda", "Contratar personal", 30.0, "Capacidad humana")
    arbol.agregar_decision("Alta demanda", "Automatizar", 50.0, "Capacidad tecnológica")
    
    # Año 3 - Decisiones desde Baja demanda
    arbol.agregar_nodo("Reducir costos", "Reducir costos operativos", 20.0)
    arbol.agregar_nodo("Diversificar", "Diversificar servicios", 30.0)
    
    arbol.agregar_decision("Baja demanda", "Reducir costos", -10.0, "Austeridad")
    arbol.agregar_decision("Baja demanda", "Diversificar", 15.0, "Nuevos mercados")
    
    # Año 3 - Decisiones desde Expandir ruta
    arbol.agregar_nodo("Éxito expansión", "Éxito en nuevas rutas", 55.0)
    arbol.agregar_nodo("Fracaso expansión", "Fracaso en nuevas rutas", 25.0)
    
    arbol.agregar_decision("Expandir ruta", "Éxito expansión", 45.0, "Rutas rentables")
    arbol.agregar_decision("Expandir ruta", "Fracaso expansión", -15.0, "Rutas no rentables")
    
    # Año 4 - Nodos hoja (decisiones finales)
    arbol.agregar_nodo("Equipo eficiente", "Equipo altamente eficiente", 100.0)
    arbol.agregar_nodo("Equipo sobrecargado", "Equipo sobrecargado", 60.0)
    arbol.agregar_nodo("Tecnología obsoleta", "Tecnología obsoleta", 50.0)
    arbol.agregar_nodo("Tecnología innovadora", "Tecnología innovadora", 120.0)
    arbol.agregar_nodo("Operación eficiente", "Operación eficiente", 80.0)
    arbol.agregar_nodo("Operación ineficiente", "Operación ineficiente", 40.0)
    arbol.agregar_nodo("Mercado estable", "Mercado estable", 70.0)
    arbol.agregar_nodo("Mercado volátil", "Mercado volátil", 30.0)
    arbol.agregar_nodo("Expansión exitosa", "Expansión exitosa", 110.0)
    arbol.agregar_nodo("Expansión fallida", "Expansión fallida", 45.0)
    arbol.agregar_nodo("Retirada estratégica", "Retirada estratégica", 60.0)
    arbol.agregar_nodo("Retirada forzada", "Retirada forzada", 20.0)
    
    # Decisiones finales (Año 3 -> Año 4)
    # Desde Contratar personal
    arbol.agregar_decision("Contratar personal", "Equipo eficiente", 25.0, "Buen rendimiento")
    arbol.agregar_decision("Contratar personal", "Equipo sobrecargado", 10.0, "Mal rendimiento")
    
    # Desde Automatizar
    arbol.agregar_decision("Automatizar", "Tecnología obsoleta", 15.0, "Tecnología desactualizada")
    arbol.agregar_decision("Automatizar", "Tecnología innovadora", 35.0, "Tecnología de punta")
    
    # Desde Reducir costos
    arbol.agregar_decision("Reducir costos", "Operación eficiente", 20.0, "Ahorro exitoso")
    arbol.agregar_decision("Reducir costos", "Operación ineficiente", -5.0, "Ahorro fallido")
    
    # Desde Diversificar
    arbol.agregar_decision("Diversificar", "Mercado estable", 30.0, "Diversificación exitosa")
    arbol.agregar_decision("Diversificar", "Mercado volátil", 10.0, "Diversificación fallida")
    
    # Desde Éxito expansión
    arbol.agregar_decision("Éxito expansión", "Expansión exitosa", 40.0, "Crecimiento")
    arbol.agregar_decision("Éxito expansión", "Expansión fallida", 20.0, "Estancamiento")
    
    # Desde Fracaso expansión
    arbol.agregar_decision("Fracaso expansión", "Retirada estratégica", 15.0, "Repliegue")
    arbol.agregar_decision("Fracaso expansión", "Retirada forzada", -10.0, "Pérdidas")
    
    # Desde Esperar
    arbol.agregar_nodo("Espera productiva", "Espera productiva", 40.0)
    arbol.agregar_nodo("Espera improductiva", "Espera improductiva", 10.0)
    
    arbol.agregar_decision("Esperar", "Espera productiva", 15.0, "Oportunidad")
    arbol.agregar_decision("Esperar", "Espera improductiva", -5.0, "Pérdida de oportunidad")
    
    # Establecer raíz
    arbol.establecer_raiz("Inicio")
    
    return arbol


# Ejecutar análisis
if __name__ == "__main__":
    arbol = crear_arbol_inversion_logistica()
    arbol.mostrar_analisis_completo()
