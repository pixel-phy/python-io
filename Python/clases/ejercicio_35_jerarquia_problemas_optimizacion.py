"""Ejercicio 35: Jerarquía de Problemas de Optimización
Diseña una clase ProblemaOptimizacion con atributos variables, restricciones (lista), 
tipo ("min" o "max"). Incluye métodos agregar_restriccion() y evaluar() (que retorne un mensaje genérico).
Crea ProblemaLineal que herede de ProblemaOptimizacion. Añade atributos matriz_A (coeficientes) y
vector_b (lado derecho). Sobrescribe evaluar() para que, dado un vector de solución,
calcule el valor de la función objetivo (supón función objetivo como suma de variables).
"""

class ProblemaOptimizacion:
    def __init__(self, variables: list[str], tipo: str = "min"):
        self.variables = variables
        self.restricciones = []
        
        if tipo.lower() in ["min", "max"]:
            self.tipo = tipo.lower()
        else:
            raise ValueError("El tipo debe ser 'min' o 'max'")

    def agregar_restriccion(self, restriccion: str):
        """Añade una descripción de restricción en texto al problema."""
        self.restricciones.append(restriccion)
        print(f"Restricción añadida: {restriccion}")

    def evaluar(self, solucion: list[float]) -> str:
        """Método genérico para evaluar una solución."""
        return "Evaluación genérica: Solución recibida pero no procesada matemáticamente."


class ProblemaLineal(ProblemaOptimizacion):
    def __init__(self, variables: list[str], matriz_A: list[list[float]], vector_b: list[float], tipo: str = "min"):
        # Inicializamos la jerarquía base
        super().__init__(variables, tipo)
        
        # Atributos específicos del problema lineal (Representación Ax <= b)
        self.matriz_A = matriz_A
        self.vector_b = vector_b

    def evaluar(self, solucion: list[float]) -> str:
        """
        Sobrescribe evaluar(). Calcula la función objetivo (suma de las variables)
        y verifica que la longitud de la solución coincida con el número de variables.
        """
        # Validación de dimensiones
        if len(solucion) != len(self.variables):
            return f"Error: La solución tiene {len(solucion)} elementos, pero se esperaban {len(self.variables)}."

        # Supuesto del enunciado: Función objetivo es la suma de las variables (f(x) = x1 + x2 + ... + xn)
        valor_objetivo = sum(solucion)
        
        # Construimos el mensaje de retorno detallado
        mensaje = (
            f"--- Evaluación del Problema Lineal ({self.tipo.upper()}) ---\n"
            f"Variables: {self.variables}\n"
            f"Solución evaluada: {solucion}\n"
            f"Valor de la Función Objetivo: {valor_objetivo}\n"
            f"Estructura matricial registrada: Matriz A ({len(self.matriz_A)}x{len(self.matriz_A[0]) if self.matriz_A else 0}), Vector b ({len(self.vector_b)} dimensiones)"
        )
        return mensaje

#Prueba:

# Definimos los componentes de un problema lineal estándar
# Ejemplo: 2 restricciones, 3 variables
variables_modelo = ["x1", "x2", "x3"]
matriz_restricciones = [
    [1.0, 2.0, 1.0],  # Coeficientes restricción 1
    [2.0, 1.0, 3.0]   # Coeficientes restricción 2
]
lado_derecho = [4.0, 10.0] # Límites (vector b)

# Creamos la instancia del problema lineal para Maximizar
problema_produccion = ProblemaLineal(
    variables=variables_modelo,
    matriz_A=matriz_restricciones,
    vector_b=lado_derecho,
    tipo="max"
)

# Añadimos texto descriptivo usando el método heredado de la clase base
problema_produccion.agregar_restriccion("x1 + 2x2 + x3 <= 4")
problema_produccion.agregar_restriccion("2x1 + x2 + 3x3 <= 10")

print("\n" + "="*40 + "\n")

# Proponemos una solución candidata (valores para x1, x2, x3)
solucion_candidata = [1.5, 0.5, 1.0]

# Evaluamos la solución usando el método sobrescrito
resultado_evaluacion = problema_produccion.evaluar(solucion_candidata)
print(resultado_evaluacion)
