"""Ejercicio 44: Clase abstracta para funciones objetivo

Crea una clase abstracta FuncionObjetivo con métodos abstractos:
    - evaluar(x): evalúa la función en el punto x.
    - grediente(x): calcula el gradiente en x.
    - hessiana(x): calcula la matriz Hessiana en x (opcional)

Implementa dos clases concretas:
    - FuncionCuadratica: f(x) = x^T Q x + c^T x + d
    - FuncionRosenbrock: f(x) = (1-x0)² + 100*(x1-x0²)²

"""

from abc import ABC, abstractmethod
import numpy as np

class FuncionObjetivo(ABC):
    """Clase abstracta que define la estructura para funciones objetivo."""
    
    @abstractmethod
    def evaluar(self, x):
        """Evalúa la función en el punto x (un array de numpy)."""
        pass
    
    @abstractmethod
    def gradiente(self, x):
        """Calcula el vector gradiente en el punto x."""
        pass
    
    def hessiana(self, x):
        """Calcula la matriz Hessiana en x. Es opcional (por defecto devuelve None)."""
        return None

class FuncionCuadratica(FuncionObjetivo):
    def __init__(self, Q, c, d=0.0):
        self.Q = np.array(Q, dtype=float)
        self.c = np.array(c, dtype=float)
        self.d = float(d)
        
    def evaluar(self, x):
        x = np.array(x, dtype=float)
        # x.T @ Q @ x + c.T @ x + d
        return x.T @ self.Q @ x + self.c.T @ x + self.d
    
    def gradiente(self, x):
        x = np.array(x, dtype=float)
        # Gradiente general: (Q + Q.T)x + c
        return (self.Q + self.Q.T) @ x + self.c
    
    def hessiana(self, x):
        # Hessiana general: Q + Q.T (es constante, no depende de x)
        return self.Q + self.Q.T

class FuncionRosenbrock(FuncionObjetivo):
    def evaluar(self, x):
        x0, x1 = x[0], x[1]
        return (1 - x0)**2 + 100 * (x1 - x0**2)**2
    
    def gradiente(self, x):
        x0, x1 = x[0], x[1]
        df_dx0 = -2 * (1 - x0) - 400 * x0 * (x1 - x0**2)
        df_dx1 = 200 * (x1 - x0**2)
        return np.array([df_dx0, df_dx1])
    
    def hessiana(self, x):
        x0, x1 = x[0], x[1]
        d2f_dx02 = 2 - 400 * x1 + 1200 * x0**2
        d2f_dx0dx1 = -400 * x0
        d2f_dx12 = 200
        
        return np.array([
            [d2f_dx02, d2f_dx0dx1],
            [d2f_dx0dx1, d2f_dx12]
        ])

# --- Prueba de la Función Cuadrática ---
# f(x) = x_0^2 + x_1^2  -> Q = identidad, c = [0,0], d = 0
Q = np.array([[1.0, 0.0], [0.0, 1.0]])
c = np.array([0.0, 0.0])
f_cuadratica = FuncionCuadratica(Q, c)

punto_q = np.array([2.0, 3.0])
print("--- Función Cuadrática en [2, 3] ---")
print(f"Evaluación: {f_cuadratica.evaluar(punto_q)}")  # 2^2 + 3^2 = 13
print(f"Gradiente:  {f_cuadratica.gradiente(punto_q)}")   # [4, 6]
print(f"Hessiana:\n{f_cuadratica.hessiana(punto_q)}")

print("\n" + "="*40 + "\n")

# --- Prueba de Rosenbrock ---
f_rosen = FuncionRosenbrock()
punto_r = np.array([1.0, 1.0]) # El mínimo global

print("--- Función Rosenbrock en el mínimo [1, 1] ---")
print(f"Evaluación: {f_rosen.evaluar(punto_r)}")  # Debería ser 0
print(f"Gradiente:  {f_rosen.gradiente(punto_r)}")   # Debería ser [0, 0]
print(f"Hessiana:\n{f_rosen.hessiana(punto_r)}")
