"""
Teoría 37: Sobrescritura de Métodos y Polimorfismo

El polimorfismo nos permite tratar diferentes tipos de objetos de manera uniforme, mientras uno implementa
su comportamiento específico. Esto es fundamental en IO porque:

- Diferentes algoritmos de optimización (Simplex, Gradiente, Genético) pueden compartir una interfaz común.
- Distintas estrategias de inventario (EOQ, Newsvendor, JIT) responden al mismo método calcular_pedido().
- Múltiples tipos de restricciones (lineales, no lineales, enteras) se evalúan con el mismo método es_factible().

La sobrescritura de métodos permite que las clases hijas proporcionen implementaciones específicas, mientras
que el polimorfismo nos permite escribir código que trabaje con la clase base y automáticamente use la
implementación correcta

"""

# Ejemplo de uso: Estrategias de optimización

from abc import ABC, abstractmethod
import math

class EstrategiaOptimizacion(ABC):
    """Clase base para estrategias de optimización"""
    
    def __init__(self, nombre: str, tolerancia: float = 1e-6):
        self.nombre = nombre
        self.tolerancia = tolerancia
        self.iteraciones = 0
        self.historial = []
    
    @abstractmethod
    def optimizar(self, funcion_objetivo, x_inicial: list[float]) -> tuple[list[float], float]:
        """Método abstracto que debe ser implementado por cada estrategia"""
        pass
    
    def registrar_iteracion(self, x: list[float], valor: float):
        """Método común para todas las estrategias"""
        self.iteraciones += 1
        self.historial.append({'iteracion': self.iteraciones, 'x': x.copy(), 'valor': valor})
    
    def reportar_resultados(self) -> str:
        """Reporte común de resultados"""
        return f"{self.nombre}: {self.iteraciones} iteraciones, último valor: {self.historial[-1]['valor']:.4f}"


class EstrategiaGradiente(EstrategiaOptimizacion):
    """Método de descenso por gradiente"""
    
    def __init__(self, nombre: str, tasa_aprendizaje: float = 0.01, max_iter: int = 1000):
        super().__init__(nombre)
        self.tasa_aprendizaje = tasa_aprendizaje
        self.max_iter = max_iter
    
    def optimizar(self, funcion_objetivo, x_inicial: list[float]) -> tuple[list[float], float]:
        """Implementación del descenso por gradiente"""
        x = x_inicial.copy()
        
        for i in range(self.max_iter):
            # Calcular gradiente numérico (simplificado)
            gradiente = self._calcular_gradiente(funcion_objetivo, x)
            
            # Actualizar posición
            x_nuevo = [x[j] - self.tasa_aprendizaje * gradiente[j] for j in range(len(x))]
            
            # Evaluar
            valor_actual = funcion_objetivo(x)
            valor_nuevo = funcion_objetivo(x_nuevo)
            
            self.registrar_iteracion(x_nuevo, valor_nuevo)
            
            # Criterio de convergencia
            if abs(valor_nuevo - valor_actual) < self.tolerancia:
                break
            
            x = x_nuevo
        
        return x, funcion_objetivo(x)
    
    def _calcular_gradiente(self, func, x: list[float]) -> list[float]:
        """Cálculo numérico del gradiente"""
        epsilon = 1e-8
        gradiente = []
        
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += epsilon
            x_minus = x.copy()
            x_minus[i] -= epsilon
            
            derivada = (func(x_plus) - func(x_minus)) / (2 * epsilon)
            gradiente.append(derivada)
        
        return gradiente


class EstrategiaSimulatedAnnealing(EstrategiaOptimizacion):
    """Algoritmo de Recocido Simulado"""
    
    def __init__(self, nombre: str, temp_inicial: float = 100.0, enfriamiento: float = 0.95):
        super().__init__(nombre)
        self.temp_inicial = temp_inicial
        self.enfriamiento = enfriamiento
    
    def optimizar(self, funcion_objetivo, x_inicial: list[float]) -> tuple[list[float], float]:
        """Implementación del recocido simulado"""
        x_actual = x_inicial.copy()
        valor_actual = funcion_objetivo(x_actual)
        temp = self.temp_inicial
        
        self.registrar_iteracion(x_actual, valor_actual)
        
        for i in range(1000):  # Iteraciones limitadas para ejemplo
            # Generar vecino (perturbación aleatoria)
            x_vecino = [x_actual[j] + (2 * (0.5 - __import__('random').random())) for j in range(len(x_actual))]
            valor_vecino = funcion_objetivo(x_vecino)
            
            # Criterio de aceptación
            delta = valor_vecino - valor_actual
            if delta < 0 or __import__('random').random() < math.exp(-delta / temp):
                x_actual = x_vecino
                valor_actual = valor_vecino
                self.registrar_iteracion(x_actual, valor_actual)
            
            # Enfriamiento
            temp *= self.enfriamiento
            
            if temp < 1e-6:
                break
        
        return x_actual, valor_actual


def optimizar_con_estrategia(estrategia: EstrategiaOptimizacion, funcion, x_inicial):
    """
    Función polimórfica: trabaja con CUALQUIER estrategia
    """
    print(f"Iniciando optimización con {estrategia.nombre}")
    x_optimo, valor_optimo = estrategia.optimizar(funcion, x_inicial)
    print(estrategia.reportar_resultados())
    return x_optimo, valor_optimo

# Ejemplo de uso
if __name__ == "__main__":
    # Función objetivo: Rosenbrock (clásica en optimización)
    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    
    x_inicial = [-1.5, 1.5]
    
    # Polimorfismo en acción: ambas estrategias usan la misma interfaz
    estrategias = [
        EstrategiaGradiente("Gradiente", tasa_aprendizaje=0.001),
        EstrategiaSimulatedAnnealing("Recocido", temp_inicial=50)
    ]
    
    for estrategia in estrategias:
        x_opt, valor = optimizar_con_estrategia(estrategia, rosenbrock, x_inicial)
        print(f"  → Óptimo: {x_opt}, Valor: {valor:.4f}\n")
