"""Ejercicio 46: Sistema de Evaluación de Escenarios con Simulación

1. Crea un sistema de simulación Monte Carlo usando clases abstractas y métodos mágicos:

    - Clase abstracta Distribucion:
    - Métodos abstractos: muestrear(), media(), varianza()
    - Método mágico: __call__ que retorne una muestra

2. Clases concretas:

    - DistribucionNormal (media, desviación)
    - DistribucionUniforme (min, max)
    - DistribucionExponencial (lambda)

3. Clase Escenario:

    - Tiene un diccionario de variables aleatorias (nombre → Distribucion)
    - Método simular(n): ejecuta n simulaciones
    - Métodos mágicos: __len__ (número de variables), __getitem__ (acceso a distribución)
"""

from abc import ABC, abstractmethod
import numpy as np

class Distribucion(ABC):
    """Clase abstracta para definir el comportamiento de una distribución de probabilidad."""
    
    @abstractmethod
    def muestrear(self, n=1):
        """Genera un array de n muestras de la distribución."""
        pass
    
    @abstractmethod
    def media(self):
        """Retorna el valor esperado (media) teórico."""
        pass
    
    @abstractmethod
    def varianza(self):
        """Retorna la varianza teórica."""
        pass
        
    def __call__(self, n=1):
        """Método mágico que permite hacer 'objeto(n)' para obtener muestras."""
        return self.muestrear(n)


class DistribucionNormal(Distribucion):
    def __init__(self, mu, sigma):
        self.mu = float(mu)
        self.sigma = float(sigma)
        
    def muestrear(self, n=1):
        return np.random.normal(self.mu, self.sigma, size=n)
        
    def media(self):
        return self.mu
        
    def varianza(self):
        return self.sigma ** 2


class DistribucionUniforme(Distribucion):
    def __init__(self, minimo, maximo):
        self.minimo = float(minimo)
        self.maximo = float(maximo)
        
    def muestrear(self, n=1):
        return np.random.uniform(self.minimo, self.maximo, size=n)
        
    def media(self):
        return (self.minimo + self.maximo) / 2
        
    def varianza(self):
        return ((self.maximo - self.minimo) ** 2) / 12


class DistribucionExponencial(Distribucion):
    def __init__(self, lam):
        if lam <= 0:
            raise ValueError("Lambda debe ser mayor que cero.")
        self.lam = float(lam)
        
    def muestrear(self, n=1):
        # En numpy, el parámetro es la escala (1/lambda)
        return np.random.exponential(1 / self.lam, size=n)
        
    def media(self):
        return 1 / self.lam
        
    def varianza(self):
        return 1 / (self.lam ** 2)

class Escenario:
    def __init__(self, nombre_escenario):
        self.nombre_escenario = nombre_escenario
        self.variables = {}  # diccionario: nombre -> Distribucion
        
    def agregar_variable(self, nombre, distribucion):
        """Añade una variable aleatoria al escenario."""
        if not isinstance(distribucion, Distribucion):
            raise TypeError("Debe ser una instancia de la clase Distribucion.")
        self.variables[nombre] = distribucion
        
    def simular(self, n=1000):
        """
        Ejecuta la simulación Monte Carlo para todas las variables.
        Retorna un diccionario con los arrays de resultados.
        """
        resultados = {}
        for nombre, distribucion in self.variables.items():
            # Aquí usamos el método mágico __call__ (distribucion(n))
            resultados[nombre] = distribucion(n)
        return resultados

    # --- Métodos Mágicos ---
    
    def __len__(self):
        """Retorna el número de variables aleatorias en el escenario."""
        return len(self.variables)
        
    def __getitem__(self, nombre):
        """Permite acceder a una distribución usando corchetes: escenario['variable']"""
        return self.variables[nombre]
        
    def __repr__(self):
        return f"Escenario('{self.nombre_escenario}', Variables: {list(self.variables.keys())})"

# 1. Crear el escenario
proyecto_infra = Escenario("Lanzamiento de App 2026")

# 2. Registrar variables aleatorias
proyecto_infra.agregar_variable("usuarios", DistribucionNormal(mu=10000, sigma=1500))
proyecto_infra.agregar_variable("costo_servidor", DistribucionUniforme(minimo=200, maximo=500))
proyecto_infra.agregar_variable("tiempo_falla_horas", DistribucionExponencial(lam=0.05)) # Promedio 20 horas

print("--- Probando métodos mágicos de Escenario ---")
print(f"Total variables registradas (__len__): {len(proyecto_infra)}")
# Acceso directo a una distribución mediante __getitem__
print(f"Media teórica de la variable 'usuarios': {proyecto_infra['usuarios'].media()}") 

print("\n--- Ejecutando Simulación Monte Carlo (n=5) ---")
# Hacemos una simulación pequeña para ver los datos impresos
simulacion_pequena = proyecto_infra.simular(n=5)

for var, muestras in simulacion_pequena.items():
    print(f"Variable '{var}': {muestras}")

print("\n--- Análisis de Riesgo con Simulación Masiva (n=100,000) ---")
# Una simulación real masiva para calcular métricas de riesgo globales
simulacion_real = proyecto_infra.simular(n=100000)

# Calcular una métrica derivada: Costo por usuario en el peor de los escenarios
costo_por_usuario = simulacion_real["costo_servidor"] / simulacion_real["usuarios"]
print(f"Costo por usuario promedio simulado: ${costo_por_usuario.mean():.4f}")
print(f"Costo por usuario en el peor escenario (Percentil 95): ${np.percentile(costo_por_usuario, 95):.4f}")
