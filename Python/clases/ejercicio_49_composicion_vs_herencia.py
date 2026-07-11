"""
Composición vs Herencia

La herencia establece una relación "es-un" (ej. un problema lineal es un problema de optimización).
La composición establece una relación "tiene-un" (ej. un modelo de inventario tiene una política de reorden).

Ventajas de Composición sobre herencia:

1. Mayor flexibilidad: Se puede cambiar comportamientos en tiempo de ejecución.
2. Menor acoplamiento: Las clases son más independientes.
3. Reutilización: Se pueden combinar componentes de diferentes maneras.
4. Evita la jerarquía rígida: No se necesita forzar relaciones "es-un" que no son naturales.

    """
from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Callable, List, Dict, Any
import time

# COMPONENTES: Estrategias de Optimización

class EstrategiaOptimizacion(ABC):
    """Componente que encapsula un algoritmo de optimización."""
    
    @abstractmethod
    def optimizar(self, funcion_objetivo: Callable, 
                  x_inicial: np.ndarray,
                  **kwargs) -> Dict[str, Any]:
        """Ejecuta la optimización y retorna resultados."""
        pass
    
    @abstractmethod
    def nombre(self) -> str:
        """Retorna el nombre de la estrategia."""
        pass


class EstrategiaGradiente(EstrategiaOptimizacion):
    """Estrategia de descenso por gradiente."""
    
    def __init__(self, tasa_aprendizaje: float = 0.01, 
                 max_iter: int = 1000,
                 tolerancia: float = 1e-6):
        self.tasa_aprendizaje = tasa_aprendizaje
        self.max_iter = max_iter
        self.tolerancia = tolerancia
    
    def optimizar(self, funcion_objetivo: Callable, 
                  x_inicial: np.ndarray,
                  **kwargs) -> Dict[str, Any]:
        x = x_inicial.copy()
        historial = [x.copy()]
        valores = [funcion_objetivo(x)]
        
        for i in range(self.max_iter):
            # Calcular gradiente numérico
            grad = self._gradiente_numerico(funcion_objetivo, x)
            x_nuevo = x - self.tasa_aprendizaje * grad
            valor = funcion_objetivo(x_nuevo)
            
            historial.append(x_nuevo.copy())
            valores.append(valor)
            
            if np.linalg.norm(x_nuevo - x) < self.tolerancia:
                break
            
            x = x_nuevo
        
        return {
            'x_optimo': x,
            'valor_optimo': valor,
            'iteraciones': len(historial),
            'historial': historial,
            'valores': valores,
            'convergio': len(historial) < self.max_iter
        }
    
    def _gradiente_numerico(self, func: Callable, x: np.ndarray) -> np.ndarray:
        epsilon = 1e-8
        grad = np.zeros_like(x)
        
        for i in range(len(x)):
            x_plus = x.copy()
            x_plus[i] += epsilon
            x_minus = x.copy()
            x_minus[i] -= epsilon
            
            grad[i] = (func(x_plus) - func(x_minus)) / (2 * epsilon)
        
        return grad
    
    def nombre(self) -> str:
        return f"Gradiente (lr={self.tasa_aprendizaje})"


class EstrategiaNelderMead(EstrategiaOptimizacion):
    """Estrategia de Nelder-Mead (sin derivadas)."""
    
    def __init__(self, max_iter: int = 1000, 
                 tolerancia: float = 1e-6):
        self.max_iter = max_iter
        self.tolerancia = tolerancia
    
    def optimizar(self, funcion_objetivo: Callable, 
                  x_inicial: np.ndarray,
                  **kwargs) -> Dict[str, Any]:
        from scipy.optimize import minimize
        
        resultado = minimize(
            funcion_objetivo, 
            x_inicial,
            method='Nelder-Mead',
            options={
                'maxiter': self.max_iter,
                'xatol': self.tolerancia,
                'fatol': self.tolerancia
            }
        )
        
        return {
            'x_optimo': resultado.x,
            'valor_optimo': resultado.fun,
            'iteraciones': resultado.nit if hasattr(resultado, 'nit') else 0,
            'convergio': resultado.success,
            'mensaje': resultado.message
        }
    
    def nombre(self) -> str:
        return "Nelder-Mead"

# COMPONENTES: Criterios de Parada

class CriterioParada(ABC):
    """Componente que decide cuándo detener una optimización."""
    
    @abstractmethod
    def debe_detener(self, iteracion: int, x: np.ndarray, 
                     valor: float, historial: List) -> bool:
        pass
    
    @abstractmethod
    def descripcion(self) -> str:
        pass


class CriterioMaxIteraciones(CriterioParada):
    """Detiene después de un número máximo de iteraciones."""
    
    def __init__(self, max_iter: int = 1000):
        self.max_iter = max_iter
    
    def debe_detener(self, iteracion: int, x: np.ndarray, 
                     valor: float, historial: List) -> bool:
        return iteracion >= self.max_iter
    
    def descripcion(self) -> str:
        return f"Máximo {self.max_iter} iteraciones"


class CriterioTolerancia(CriterioParada):
    """Detiene cuando el cambio en x o en valor es muy pequeño."""
    
    def __init__(self, tolerancia_x: float = 1e-6, 
                 tolerancia_f: float = 1e-6):
        self.tolerancia_x = tolerancia_x
        self.tolerancia_f = tolerancia_f
    
    def debe_detener(self, iteracion: int, x: np.ndarray, 
                     valor: float, historial: List) -> bool:
        if len(historial) < 2:
            return False
        
        # CORRECCIÓN: Usamos el historial de valores si es una lista de floats
        # o el historial de x si es una lista de arrays
        if len(historial) > 0 and isinstance(historial[0], (int, float)):
            # Historial de valores
            valor_anterior = historial[-2]
            cambio_f = abs(valor - valor_anterior)
            return cambio_f < self.tolerancia_f
        else:
            # Historial de puntos (arrays)
            x_anterior = historial[-2]
            cambio_x = np.linalg.norm(x - x_anterior)
            return cambio_x < self.tolerancia_x
    
    def descripcion(self) -> str:
        return f"Tolerancia (x={self.tolerancia_x}, f={self.tolerancia_f})"


class CriterioCombinado(CriterioParada):
    """Combina múltiples criterios (OR lógico)."""
    
    def __init__(self, *criterios: CriterioParada):
        self.criterios = criterios
    
    def debe_detener(self, iteracion: int, x: np.ndarray, 
                     valor: float, historial: List) -> bool:
        # CORRECCIÓN: Convertir cada resultado a bool explícitamente
        for c in self.criterios:
            resultado = c.debe_detener(iteracion, x, valor, historial)
            # Si es un array, convertir a bool usando any() o all()
            if isinstance(resultado, np.ndarray):
                if resultado.any():
                    return True
            elif resultado:
                return True
        return False
    
    def descripcion(self) -> str:
        return " o ".join(c.descripcion() for c in self.criterios)

# COMPONENTES: Registro de Progreso

class RegistroProgreso(ABC):
    """Componente que registra el progreso de la optimización."""
    
    @abstractmethod
    def registrar(self, iteracion: int, x: np.ndarray, 
                  valor: float, **kwargs):
        pass


class RegistroConsola(RegistroProgreso):
    """Registra el progreso en la consola."""
    
    def __init__(self, frecuencia: int = 10):
        self.frecuencia = frecuencia
    
    def registrar(self, iteracion: int, x: np.ndarray, 
                  valor: float, **kwargs):
        if iteracion % self.frecuencia == 0:
            print(f"Iter {iteracion:4d}: x={x}, f={valor:.6f}")


class RegistroHistorial(RegistroProgreso):
    """Almacena el historial completo de la optimización."""
    
    def __init__(self):
        self.historial_x = []
        self.historial_f = []
        self.historial_tiempos = []
    
    def registrar(self, iteracion: int, x: np.ndarray, 
                  valor: float, **kwargs):
        self.historial_x.append(x.copy())
        self.historial_f.append(valor)
        if 'tiempo' in kwargs:
            self.historial_tiempos.append(kwargs['tiempo'])
    
    def obtener_historial(self):
        return {
            'x': self.historial_x,
            'f': self.historial_f,
            'tiempos': self.historial_tiempos
        }

# CLASE PRINCIPAL: Optimizador (COMPOSICIÓN)

class Optimizador:
    """
    Sistema de optimización que utiliza composición para combinar
    diferentes estrategias, criterios y registradores.
    """
    
    def __init__(self, 
                 estrategia: EstrategiaOptimizacion,
                 criterio_parada: Optional[CriterioParada] = None,
                 registradores: Optional[List[RegistroProgreso]] = None):
        """
        El optimizador COMPONE diferentes componentes:
        - Una estrategia de optimización
        - Un criterio de parada
        - Múltiples registradores de progreso
        """
        self.estrategia = estrategia
        self.criterio_parada = criterio_parada or CriterioMaxIteraciones(1000)
        self.registradores = registradores or []
        
        # El optimizador TIENE un historial
        self.historial = {
            'iteraciones': [],
            'x': [],
            'valores': [],
            'tiempos': []
        }
    
    def agregar_registrador(self, registrador: RegistroProgreso):
        """Agrega un nuevo registrador al optimizador."""
        self.registradores.append(registrador)
    
    def optimizar(self, funcion_objetivo: Callable, 
                  x_inicial: np.ndarray,
                  **kwargs) -> Dict[str, Any]:
        """
        Ejecuta la optimización usando la estrategia configurada
        y los criterios de parada.
        """
        x = x_inicial.copy()
        valor = funcion_objetivo(x)
        iteracion = 0
        
        self._registrar(iteracion, x, valor)
        
        start_time = time.time()
        
        # CORRECCIÓN: Usar un bucle while con verificación de parada al inicio
        while True:
            # Verificar criterio de parada ANTES de ejecutar más iteraciones
            # CORRECCIÓN: Pasar el historial de valores para mejor compatibilidad
            if self.criterio_parada.debe_detener(iteracion, x, valor, 
                                                self.historial['valores']):
                break
            
            # Usar la estrategia para dar un paso
            paso = self._paso_optimizacion(funcion_objetivo, x)
            x = paso['x']
            valor = paso['valor']
            iteracion += 1
            
            self._registrar(iteracion, x, valor, 
                           tiempo=time.time() - start_time)
        
        return {
            'x_optimo': x,
            'valor_optimo': valor,
            'iteraciones': iteracion,
            'historial': self.historial,
            'estrategia': self.estrategia.nombre(),
            'criterio_parada': self.criterio_parada.descripcion()
        }
    
    def _paso_optimizacion(self, func: Callable, x: np.ndarray) -> Dict:
        """Delega el paso de optimización a la estrategia."""
        # En una implementación real, la estrategia daría un paso
        # Por simplicidad, usamos scipy para el ejemplo
        from scipy.optimize import minimize
        resultado = minimize(func, x, method='BFGS')
        return {'x': resultado.x, 'valor': resultado.fun}
    
    def _registrar(self, iteracion: int, x: np.ndarray, 
                   valor: float, **kwargs):
        """Registra el progreso usando todos los registradores."""
        self.historial['iteraciones'].append(iteracion)
        self.historial['x'].append(x.copy())
        self.historial['valores'].append(valor)
        
        for registrador in self.registradores:
            registrador.registrar(iteracion, x, valor, **kwargs)

# EJEMPLO DE USO

if __name__ == "__main__":
    # Función objetivo de ejemplo: Rosenbrock
    def rosenbrock(x):
        return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    
    x_inicial = np.array([-1.5, 1.5])
    
    # Crear componentes
    estrategia_grad = EstrategiaGradiente(tasa_aprendizaje=0.001)
    criterio = CriterioCombinado(
        CriterioMaxIteraciones(500),
        CriterioTolerancia(tolerancia_x=1e-6, tolerancia_f=1e-6)
    )
    
    # Crear registradores
    registrador_consola = RegistroConsola(frecuencia=50)
    registrador_historial = RegistroHistorial()
    
    # Crear optimizador por COMPOSICIÓN
    optimizador = Optimizador(
        estrategia=estrategia_grad,
        criterio_parada=criterio,
        registradores=[registrador_consola, registrador_historial]
    )
    
    # Ejecutar optimización
    print("Iniciando optimización...")
    resultados = optimizador.optimizar(rosenbrock, x_inicial)
    
    print(f"\nOptimización completada:")
    print(f"  Estrategia: {resultados['estrategia']}")
    print(f"  Criterio: {resultados['criterio_parada']}")
    print(f"  Iteraciones: {resultados['iteraciones']}")
    print(f"  Óptimo: {resultados['x_optimo']}")
    print(f"  Valor: {resultados['valor_optimo']:.6f}")
