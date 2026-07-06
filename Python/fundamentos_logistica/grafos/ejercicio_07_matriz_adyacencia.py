"""Ejercicio 07: Matriz de Adyacencia

Es una tabla bidimencional (matriz de V x V, donde V es el número de nodos) donde las filas 
representan los nodos de origen y las columnas los nodos de destino.

  - Si hay una conexión entre el nodo i y el nodo j, la celda matrix[i][j] guarda un 1 
    (o el peso/costo si es un grafo valorado).
  - Si no hay conexión, guarda un 0 (o infinito / None si tiene pesos)."""

# Implementación en Python:

class GrafoMatriz:
  def __init__(self, num_nodos: int):
    self.V = num_nodos
    # Inicializamos la matriz con 0 (sin conexiones)
    self.matriz = [[0] * num_nodos for _ in range(num_nodos)]

  def agregar_arco(self, origen: int, destino: int, peso: float = 1.0):
    # O(1) - Acceso e inserción instantánea
    self.matriz[origen][destino] = peso

  def mostrar(self):
    for fila in self.matriz:
      print(fila)

# Caso de prueba:
grafo = GrafoMatriz(3) # Nodos: 0, 1, 2
grafo.agregar_arco(0, 1, 4.5) # Arco de 0 a 1 con peso 4.5
grafo.agregar_arco(1, 2, 2.0)
grafo.mostrar()

""" Lista de adyacencia:

Representa el grafo como un arreglo o diccionario de listas. Cada nodo tiene asociada
una colección (lista, conjunto o diccionario) que contiene únicamente a sus vecinos directos. """

# Implementación en Python:
from collections import defaultdict
from typing import Dict, List, Tuple

class GrafoLista:
    def __init__(self):
        # Usamos un diccionario de listas (o diccionarios) para flexibilidad
        self.lista_ady: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
        
    def agregar_arco(self, origen: int, destino: int, peso: float = 1.0):
        # O(1) - Agrega al final de la lista del nodo origen
        self.lista_ady[origen].append((destino, peso))

    def mostrar(self):
        for nodo, vecinos in self.lista_ady.items():
            print(f"Nodo {nodo} se conecta con: {vecinos}")

# Ejemplo de uso
grafo = GrafoLista()
grafo.agregar_arco(0, 1, 4.5)
grafo.agregar_arco(1, 2, 2.0)
grafo.mostrar()
