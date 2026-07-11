"""Ejercicio 47: Álgebra de Restricciones con Métodos Mágicos

Extiende el sistema de restricciones del ejemplo con:

1. Clase RestriccionNoLineal (hereda de Restriccion):

    - Acepta una función lambda para evaluar

    - Implementa evaluar(), es_factible(), __repr__

2. Métodos mágicos adicionales:

    - __and__: intersección de restricciones (AND lógico)

    - __or__: unión de restricciones (OR lógico)

    - __neg__: negación de una restricción

3. Clase RestriccionCompuesta:

    - Combina múltiples restricciones con operadores lógicos

    - Implementa evaluar() y es_factible() evaluando la combinación
    """

from abc import ABC, abstractmethod
import numpy as np

class Restriccion(ABC):
    """Clase base abstracta para todas las restricciones."""
    
    @abstractmethod
    def evaluar(self, x):
        pass
        
    @abstractmethod
    def es_factible(self, x):
        pass

    # --- Métodos Mágicos para el Álgebra de Restricciones ---
    
    def __and__(self, other):
        """Operador AND lógico (&)."""
        return RestriccionCompuesta(self, other, operador="AND")
        
    def __or__(self, other):
        """Operador OR lógico (|)."""
        return RestriccionCompuesta(self, other, operador="OR")
        
    def __invert__(self):
        """Operador NOT lógico (~). Ahora sí responde correctamente a la tilde."""
        return RestriccionCompuesta(self, None, operador="NOT")

class RestriccionNoLineal(Restriccion):
    def __init__(self, funcion_lambda, signo="<=", limite=0.0, descripcion="No Lineal"):
        """
        g(x) [signo] limite  (ejemplo: x0**2 + x1**2 <= 1)
        """
        self.funcion = funcion_lambda
        self.signo = signo
        self.limite = float(limite)
        self.descripcion = descripcion
        
    def evaluar(self, x):
        # Calcula la desviación respecto al límite
        x = np.array(x, dtype=float)
        valor_g = self.funcion(x)
        return valor_g - self.limite

    def es_factible(self, x):
        x = np.array(x, dtype=float)
        valor_g = self.funcion(x)
        
        if self.signo == "<=":
            return valor_g <= self.limite
        elif self.signo == ">=":
            return valor_g >= self.limite
        elif self.signo == "==":
            return np.isclose(valor_g, self.limite)
        else:
            raise ValueError(f"Signo de restricción no soportado: {self.signo}")
            
    def __repr__(self):
        return f"RestriccionNoLineal('{self.descripcion}': g(x) {self.signo} {self.limite})"

class RestriccionCompuesta(Restriccion):
    def __init__(self, r1, r2=None, operador="AND"):
        """
        Combina una o dos restricciones mediante un operador lógico ('AND', 'OR', 'NOT').
        """
        self.r1 = r1
        self.r2 = r2
        self.operador = operador.upper()
        
    def evaluar(self, x):
        """
        Para restricciones compuestas, la evaluación numérica suele representar 
        el grado de violación. Aquí retornamos una aproximación o penalización lógica.
        """
        if self.operador == "NOT":
            return -self.r1.evaluar(x)
        elif self.operador == "AND":
            # Si es AND, la penalización es el peor escenario de incumplimiento (máximo)
            return max(self.r1.evaluar(x), self.r2.evaluar(x))
        elif self.operador == "OR":
            # Si es OR, basta con que una esté bien; penalizamos con el mínimo
            return min(self.r1.evaluar(x), self.r2.evaluar(x))

    def es_factible(self, x):
        """Evalúa la combinación lógica de viabilidad."""
        if self.operador == "NOT":
            return not self.r1.es_factible(x)
            
        elif self.operador == "AND":
            return self.r1.es_factible(x) and self.r2.es_factible(x)
            
        elif self.operador == "OR":
            return self.r1.es_factible(x) or self.r2.es_factible(x)
            
        raise ValueError(f"Operador lógico desconocido: {self.operador}")
        
    def __repr__(self):
        if self.operador == "NOT":
            return f"(~{self.r1})"
        return f"({self.r1} {self.operador} {self.r2})"

# 1. Definir restricciones individuales usando lambdas
dentro_circulo = RestriccionNoLineal(lambda x: x[0]**2 + x[1]**2, "<=", 4.0, "Círculo R=2")
en_semiplano_positivo = RestriccionNoLineal(lambda x: x[1], ">=", 0.0, "Y positivo")
zona_prohibida = RestriccionNoLineal(lambda x: x[0], "<=", 0.0, "X negativo")

print("--- Restricciones base creadas ---")
print(dentro_circulo)

# 2. Construir el Álgebra de Restricciones usando operadores mágicos
# "Debe estar dentro del círculo Y en el semiplano positivo, O NO estar en la zona prohibida"
sistema_restricciones = (dentro_circulo & en_semiplano_positivo) | (~zona_prohibida)

print("\n--- Expresión del Sistema Compuesto ---")
print(sistema_restricciones)

print("\n--- Evaluando Puntos ---")

# Caso A: Punto [1, 1] 
# Está dentro del círculo (1+1 <= 4) y Y >= 0. Debería ser Factible.
p1 = [1.0, 1.0]
print(f"Punto {p1} -> ¿Es factible?: {sistema_restricciones.es_factible(p1)}")

# Caso B: Punto [3, 3]
# Está lejísimos fuera del círculo. Pero X > 0, por lo tanto NO está en la zona prohibida. 
# Como usamos un operador OR (| ~zona_prohibida), este punto se vuelve aceptable por la segunda rama.
p2 = [3.0, 3.0]
print(f"Punto {p2} -> ¿Es factible?: {sistema_restricciones.es_factible(p2)}")

# Caso C: Punto [-1, -3]
# Fuera del círculo, Y es negativo, y además cae en la zona prohibida (X <= 0). Infactible total.
p3 = [-1.0, -3.0]
print(f"Punto {p3} -> ¿Es factible?: {sistema_restricciones.es_factible(p3)}")
