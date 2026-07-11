"""Métodos mágicos para Comparación de Soluciones

Crea una clase Solucion que represente una solución de un problema de optimización con:

- Atributos: vector (array numpy), valor_objetivo (float), factible (bool)

- Métodos mágicos:

    - __lt__, __le__, __eq__ para comparar por valor objetivo

    - __add__ y __sub__ para operaciones con vectores (combinación convexa)

    - __len__ que retorne la dimensión del vector 
"""

import numpy as np

class Solucion:
    def __init__(self, vector, valor_objetivo, factible=True):
        """
        Representa una solución en un espacio de optimización.
        
        - vector: array de numpy (o lista que se convertirá en array).
        - valor_objetivo: float que indica la calidad de la solución.
        - factible: bool que indica si la solución cumple las restricciones.
        """
        self.vector = np.array(vector, dtype=float)
        self.valor_objetivo = float(valor_objetivo)
        self.factible = bool(factible)
        
    def __len__(self):
        """Retorna la dimensión del vector de variables de decisión."""
        return len(self.vector)

    # --- Métodos Mágicos de Comparación (Criterio: Menor valor objetivo es mejor) ---
    # Nota: Asumimos un problema de MINIMIZACIÓN. 
    # Si fuera maximización, invertirías el sentido de < y >.

    def __lt__(self, other):
        """Operador 'Menor que' (<). Compara por valor_objetivo."""
        if not isinstance(other, Solucion):
            return NotImplemented
        return self.valor_objetivo < other.valor_objetivo

    def __le__(self, other):
        """Operador 'Menor o igual que' (<=). Compara por valor_objetivo."""
        if not isinstance(other, Solucion):
            return NotImplemented
        return self.valor_objetivo <= other.valor_objetivo

    def __eq__(self, other):
        """Operador 'Igual que' (==). Compara por valor_objetivo."""
        if not isinstance(other, Solucion):
            return NotImplemented
        return self.valor_objetivo == other.valor_objetivo

    # --- Métodos Mágicos de Aritmética (Combinación / Operaciones Vectoriales) ---

    def __add__(self, other):
        """
        Operador Suma (+). Permite sumar los vectores de dos soluciones.
        Útil para cruces en algoritmos genéticos o movimientos vectoriales.
        """
        if not isinstance(other, Solucion):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("No se pueden sumar soluciones de diferentes dimensiones.")
        
        # Al sumar dos soluciones, el nuevo vector es la suma. 
        # El valor_objetivo se inicializa en None o se recalcula después, 
        # ya que la nueva posición tendrá un valor diferente en la función objetivo.
        nuevo_vector = self.vector + other.vector
        return Solucion(nuevo_vector, valor_objetivo=0.0, factible=True)

    def __sub__(self, other):
        """
        Operador Resta (-). Resta el vector de otra solución.
        Muy usado en optimización por enjambre de partículas (PSO) o Evolución Diferencial.
        """
        if not isinstance(other, Solucion):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("No se pueden restar soluciones de diferentes dimensiones.")
        
        nuevo_vector = self.vector - other.vector
        return Solucion(nuevo_vector, valor_objetivo=0.0, factible=True)

    # --- Extra: Representación en texto ---
    def __repr__(self):
        """Hace que al imprimir la solución se vea limpia en la consola."""
        estatus = "Factible" if self.factible else "No Factible"
        return f"Solucion(Dim: {len(self)}, FO: {self.valor_objetivo:.4f}, {estatus})"

# Creemos tres soluciones distintas
sol1 = Solucion(vector=[1.0, 2.0, 3.0], valor_objetivo=10.5)
sol2 = Solucion(vector=[1.5, 2.5, 3.5], valor_objetivo=5.2)
sol3 = Solucion(vector=[0.0, 1.0, 2.0], valor_objetivo=10.5)

print("--- Probando __len__ ---")
print(f"Dimensión de sol1: {len(sol1)}")  # Devuelve 3

print("\n--- Probando Comparaciones (Minimización) ---")
print(f"¿Es sol1 mejor (menor) que sol2?: {sol1 < sol2}")   # False (10.5 < 5.2 es Falso)
print(f"¿Es sol2 mejor (menor) que sol1?: {sol2 < sol1}")   # True
print(f"¿Tienen sol1 y sol3 el mismo valor?: {sol1 == sol3}") # True

print("\n--- Ordenando una lista de soluciones automáticamente ---")
poblacion = [sol1, sol2, sol3]
# Al definir __lt__, la función sorted() de Python sabe exactamente cómo ordenarlas
poblacion_ordenada = sorted(poblacion)
print(poblacion_ordenada) 
# Imprime primero sol2 (FO: 5.2) y luego las de 10.5

print("\n--- Probando Operaciones Aritméticas (Combinación) ---")
# Supongamos una combinación convexa o una operación de mutación/cruce:
# Nueva = sol1 + sol2
sol_suma = sol1 + sol2
print(f"Vector resultante de la suma: {sol_suma.vector}")  # [2.5, 4.5, 6.5]

# Resta (ej. vector de velocidad/dirección entre dos soluciones)
sol_direccion = sol1 - sol2
print(f"Vector diferencia (sol1 - sol2): {sol_direccion.vector}")  # [-0.5, -0.5, -0.5]
