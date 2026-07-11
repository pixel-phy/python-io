"""Clases abstractas y Métodos Mágicos

Las clases abstractas definen contratos que todas las clases hijas deben cumplir, garantizan que
ciertos métodos estén implementados y son ideales para definir interfaces de modelos de optimización,
simulaciones, etc...

Los métodos mágicos, permiten que nuestros objetos se comporten como tipos nativos de Python, hacen 
el código más intuitivo y legible; y facilitan operaciones matemáticas, comparaciones y conversiones.

"""
# Ejemplo práctico:
from abc import ABC, abstractmethod
import numpy as np
from typing import List, Union, Optional

class Restriccion(ABC):
    """
    Clase abstracta que define el contrato para todas las restricciones.
    Cualquier restricción debe poder evaluarse y verificar factibilidad.
    """
    
    @abstractmethod
    def evaluar(self, x: np.ndarray) -> float:
        """Evalúa el valor de la restricción en el punto x."""
        pass
    
    @abstractmethod
    def es_factible(self, x: np.ndarray, tolerancia: float = 1e-6) -> bool:
        """Verifica si el punto x satisface la restricción."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Representación legible de la restricción."""
        pass


class RestriccionLineal(Restriccion):
    """Restricción lineal de la forma: a·x ≤ b"""
    
    def __init__(self, coeficientes: List[float], lado_derecho: float, 
                 tipo: str = "≤"):
        self.coeficientes = np.array(coeficientes)
        self.lado_derecho = lado_derecho
        self.tipo = tipo  # ≤, ≥, =
    
    def evaluar(self, x: np.ndarray) -> float:
        """Calcula el valor de a·x"""
        return np.dot(self.coeficientes, x)
    
    def es_factible(self, x: np.ndarray, tolerancia: float = 1e-6) -> bool:
        valor = self.evaluar(x)
        
        if self.tipo == "≤":
            return valor <= self.lado_derecho + tolerancia
        elif self.tipo == "≥":
            return valor >= self.lado_derecho - tolerancia
        else:  # ==
            return abs(valor - self.lado_derecho) <= tolerancia
    
    def __repr__(self) -> str:
        coef_str = " + ".join([f"{c:.2f}*x{i}" for i, c in enumerate(self.coeficientes)])
        return f"{coef_str} {self.tipo} {self.lado_derecho:.2f}"
    
    # Métodos mágicos para operaciones matemáticas
    def __add__(self, other: 'RestriccionLineal') -> 'RestriccionLineal':
        """Suma dos restricciones lineales (suma de coeficientes y lados derechos)"""
        if not isinstance(other, RestriccionLineal):
            raise TypeError("Solo se pueden sumar restricciones lineales")
        
        if len(self.coeficientes) != len(other.coeficientes):
            raise ValueError("Las restricciones deben tener el mismo número de variables")
        
        # Asumimos que sumamos restricciones con el mismo tipo
        return RestriccionLineal(
            self.coeficientes + other.coeficientes,
            self.lado_derecho + other.lado_derecho,
            self.tipo
        )
    
    def __mul__(self, escalar: float) -> 'RestriccionLineal':
        """Multiplica una restricción por un escalar"""
        if not isinstance(escalar, (int, float)):
            raise TypeError("Solo se puede multiplicar por un número")
        
        return RestriccionLineal(
            self.coeficientes * escalar,
            self.lado_derecho * escalar,
            self.tipo
        )
    
    def __rmul__(self, escalar: float) -> 'RestriccionLineal':
        """Multiplicación por la izquierda (escalar * restricción)"""
        return self.__mul__(escalar)


class SistemaRestricciones:
    """Sistema de restricciones que puede ser evaluado como un todo"""
    
    def __init__(self, restricciones: Optional[List[Restriccion]] = None):
        self.restricciones = restricciones or []
    
    def agregar(self, restriccion: Restriccion):
        self.restricciones.append(restriccion)
        return self  # Permite encadenamiento
    
    def evaluar_todas(self, x: np.ndarray) -> List[float]:
        """Evalúa todas las restricciones en el punto x"""
        return [r.evaluar(x) for r in self.restricciones]
    
    def es_factible(self, x: np.ndarray) -> bool:
        """Verifica si x satisface todas las restricciones"""
        return all(r.es_factible(x) for r in self.restricciones)
    
    # Método mágico: len() retorna el número de restricciones
    def __len__(self) -> int:
        return len(self.restricciones)
    
    # Método mágico: acceso por índice
    def __getitem__(self, idx: int) -> Restriccion:
        return self.restricciones[idx]
    
    # Método mágico: iteración
    def __iter__(self):
        return iter(self.restricciones)
    
    # Método mágico: representación
    def __repr__(self) -> str:
        if not self.restricciones:
            return "SistemaRestricciones(vacío)"
        
        restricciones_str = "\n  ".join([repr(r) for r in self.restricciones])
        return f"SistemaRestricciones:\n  {restricciones_str}"


# Ejemplo de uso
if __name__ == "__main__":
    # Crear restricciones
    r1 = RestriccionLineal([2.0, 1.0], 10.0, "≤")
    r2 = RestriccionLineal([1.0, 3.0], 15.0, "≤")
    
    # Demostrar métodos mágicos
    print(f"Restricción 1: {r1}")
    print(f"Restricción 2: {r2}")
    
    # Suma de restricciones
    r3 = r1 + r2
    print(f"Suma: {r3}")
    
    # Multiplicación
    r4 = 2 * r1
    print(f"Multiplicación: {r4}")
    
    # Sistema de restricciones
    sistema = SistemaRestricciones()
    sistema.agregar(r1).agregar(r2)
    
    print(f"\n{sistema}")
    print(f"Número de restricciones: {len(sistema)}")
    
    # Probar factibilidad
    x_test = np.array([2.0, 3.0])
    print(f"x={x_test} es factible: {sistema.es_factible(x_test)}")
    
    x_test2 = np.array([10.0, 10.0])
    print(f"x={x_test2} es factible: {sistema.es_factible(x_test2)}")


