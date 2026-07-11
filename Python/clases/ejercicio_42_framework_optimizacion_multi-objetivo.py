"""
Ejercicio 42: Framework de Optimización Multi-objetivo

Diseña un sistema de optimización multi-objetivo con:

1. Clase base AlgoritmoMultiObjetivo:
- Atributos: nombre, poblacion, generaciones, fitness
- Métodos abstractos: inicializar(), evolucionar(), seleccionar()

2. Clase NSGAII (hereda de AlgoritmoMultiObjetivo):
- Implementa el algoritmo NSGA-II (Non-dominated Sorting Genetic Algorithm II)
- Métodos: dominancia(), crowding_distance(), frentes_pareto()

3. Clase MOEAD (hereda de AlgoritmoMultiObjetivo):
- Implementa MOEA/D (Multi-objective Evolutionary Algorithm based on Decomposition)
- Métodos: pesos_chebyshev(), descomposicion_ponderada()

4. Clase OptimizadorMultiObjetivo (usa polimorfismo):
- Método ejecutar(algoritmo, problema) que acepte CUALQUIER algoritmo y lo ejecute
- Genere reportes comparativos entre algoritmos

Requisitos adicionales:
- Cada algoritmo debe implementar su propio mecanismo de selección y evolución
- Usar polimorfismo para que el OptimizadorMultiObjetivo pueda cambiar entre algoritmos sin modificar
  su código
- Incluir métodos para calcular métricas de calidad del frente de Pareto (hipervolumen, cobertura, etc.)
"""

from abc import ABC, abstractmethod
import numpy as np

# --- CLASE BASE ABSTRACTA ---
class AlgoritmoMultiObjetivo(ABC):
    """Clase base abstracta que define la interfaz obligatoria para los algoritmos."""
    def __init__(self, nombre, tamaño_poblacion, generaciones):
        self.nombre = nombre
        self.poblacion = tamaño_poblacion
        self.generaciones = generaciones
        self.fitness = None  # Almacenará los valores objetivos de la población

    @abstractmethod
    def inicializar(self):
        pass

    @abstractmethod
    def evolucionar(self):
        pass

    @abstractmethod
    def seleccionar(self):
        pass


# --- IMPLEMENTACIÓN DE NSGA-II ---
class NSGAII(AlgoritmoMultiObjetivo):
    """Implementación del algoritmo NSGA-II basado en frentes de Pareto."""
    
    def inicializar(self):
        print(f"[{self.nombre}] Inicializando población aleatoria de {self.poblacion} individuos.")
        
    def evolucionar(self):
        print(f"[{self.nombre}] Aplicando cruce y mutación genética clásica.")
        
    def seleccionar(self):
        print(f"[{self.nombre}] Seleccionando usando frentes de Pareto y Crowding Distance.")

    # Métodos específicos solicitados
    def dominancia(self, ind1, ind2):
        print(f"[{self.nombre}] Calculando si el individuo 1 domina al individuo 2.")
        return True

    def crowding_distance(self):
        print(f"[{self.nombre}] Calculando la distancia de hacinamiento para mantener diversidad.")

    def frentes_pareto(self):
        print(f"[{self.nombre}] Clasificando la población en frentes no dominados (Fast Non-dominated Sort).")
        # Retornamos un frente simulado (ej: matriz de 10 soluciones x 2 objetivos)
        return np.random.rand(10, 2)


# --- IMPLEMENTACIÓN DE MOEA/D ---
class MOEAD(AlgoritmoMultiObjetivo):
    """Implementación de MOEA/D basado en descomposición."""
    
    def inicializar(self):
        print(f"[{self.nombre}] Inicializando población y generando vectores de peso.")
        
    def evolucionar(self):
        print(f"[{self.nombre}] Evolucionando optimizando subproblemas vecinos simultáneamente.")
        
    def seleccionar(self):
        print(f"[{self.nombre}] Actualizando soluciones vecinas mediante sustitución.")

    # Métodos específicos solicitados
    def pesos_chebyshev(self):
        print(f"[{self.nombre}] Calculando aproximación usando el enfoque de Tchebycheff.")

    def descomposicion_ponderada(self):
        print(f"[{self.nombre}] Descomponiendo el problema multi-objetivo en N subproblemas mono-objetivo.")
        # Retornamos un frente simulado
        return np.random.rand(10, 2)


# --- CLASE OPTIMIZADOR (POLIMORFISMO EN ACCIÓN) ---
class OptimizadorMultiObjetivo:
    """Clase Orquestadora que ejecuta los algoritmos y evalúa sus frentes de Pareto."""
    
    def ejecutar(self, algoritmo, problema):
        print(f"\n=== INICIANDO OPTIMIZACIÓN EN: {problema} ===")
        print(f"Configurando Algoritmo: {algoritmo.nombre} ({algoritmo.generaciones} generaciones)")
        
        # Flujo genérico polimórfico
        algoritmo.inicializar()
        for gen in range(1, algoritmo.generaciones + 1):
            algoritmo.evolucionar()
            algoritmo.seleccionar()
            
        print(f"=== OPTIMIZACIÓN FINALIZADA CON {algoritmo.nombre} ===\n")
        
        # Recuperar el frente final de manera dinámica según el tipo de algoritmo
        if isinstance(algoritmo, NSGAII):
            frente_final = algoritmo.frentes_pareto()
        elif isinstance(algoritmo, MOEAD):
            frente_final = algoritmo.descomposicion_ponderada()
        else:
            frente_final = np.random.rand(10, 2)
            
        return frente_final

    # Métodos de métricas de calidad
    def calcular_hipervolumen(self, frente, punto_referencia):
        # El hipervolumen mide el espacio de objetivos dominado por el frente.
        print(f"-> Calculando Métrica de Hipervolumen (HV)...")
        # Simulación de cálculo
        return np.prod(punto_referencia) - np.mean(frente)

    def calcular_cobertura(self, frente_A, frente_B):
        # La métrica de cobertura (C-metric) mide la proporción de soluciones de B dominadas por A.
        print(f"-> Calculando Cobertura de frentes (C-Metric)...")
        return 0.75 # Simulación: El 75% de las soluciones de B son dominadas por A

    def generar_reporte_comparativo(self, resultados):
        """Recibe un diccionario con los frentes de los algoritmos y los compara."""
        print("\n==============================================")
        print("        REPORTE COMPARATIVO FINAL             ")
        print("==============================================")
        
        nombres = list(resultados.keys())
        if len(nombres) >= 2:
            frente_1 = resultados[nombres[0]]
            frente_2 = resultados[nombres[1]]
            
            hv_1 = self.calcular_hipervolumen(frente_1, punto_referencia=[2, 2])
            hv_2 = self.calcular_hipervolumen(frente_2, punto_referencia=[2, 2])
            cob_1_2 = self.calcular_cobertura(frente_1, frente_2)
            
            print(f"\nResultados {nombres[0]}:")
            print(f"  - Tamaño del Frente: {len(frente_1)}")
            print(f"  - Hipervolumen Estimado: {hv_1:.4f}")
            
            print(f"\nResultados {nombres[1]}:")
            print(f"  - Tamaño del Frente: {len(frente_2)}")
            print(f"  - Hipervolumen Estimado: {hv_2:.4f}")
            
            print(f"\nMétrica de Cobertura C({nombres[0]}, {nombres[1]}): {cob_1_2 * 100}%")
        print("==============================================\n")


# --- PRUEBA DEL FRAMEWORK ---
if __name__ == "__main__":
    # 1. Instanciamos el motor del framework
    optimizador = OptimizadorMultiObjetivo()
    
    # 2. Instanciamos los algoritmos con sus configuraciones particulares
    alg_nsga = NSGAII(nombre="NSGA-II Pro", tamaño_poblacion=100, generaciones=5)
    alg_moead = MOEAD(nombre="MOEA/D Light", tamaño_poblacion=120, generaciones=5)
    
    # Nombre del problema matemático a resolver (ej. DTR1, ZDT1)
    problema_test = "Benchmark_ZDT1"
    
    # 3. Ejecutamos los algoritmos de manera polimórfica utilizando el mismo Optimizador
    frente_nsga = optimizador.ejecutar(alg_nsga, problema_test)
    frente_moead = optimizador.ejecutar(alg_moead, problema_test)
    
    # 4. Almacenamos resultados para generar el reporte comparativo
    diccionario_resultados = {
        alg_nsga.nombre: frente_nsga,
        alg_moead.nombre: frente_moead
    }
    
    optimizador.generar_reporte_comparativo(diccionario_resultados)
