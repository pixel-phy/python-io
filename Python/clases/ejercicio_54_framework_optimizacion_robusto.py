"""Ejercicio 54: Framework de Optimización Robusto (RO)

Diseña un sistema completo de Optimización Robusta usando composición:

1. Clase Incertidumbre: Representa la incertidumbre en parámetros
    - Tipos: IncertidumbreCaja (intervalo), IncertidumbreEllipsoidal (elipse), IncertidumbrePoliedro
    - Métodos: muestrear(), peor_caso(funcion)

2. Clase ModeloBase: Modelo determinista subyacente
    - Métodos: evaluar(x, params), restricciones(x, params)

3. Clase ModeloRobusto: Compone un modelo base con una incertidumbre
    - Métodos: evaluar_robusta(x), es_factible_robusta(x)

4. Clase OptimizadorRobusto: Compone el modelo robusto y un optimizador
    - Método: optimizar(x_inicial)

5. Aplicación: Resolver un problema de planificación de producción con demanda incierta:
    - Demanda: [100, 200] (incierta)
    - Costo producción: $10/unidad
    - Costo faltante: $5/unidad
    - Capacidad: 150 unidades
    - Encontrar la cantidad a producir que minimiza el costo en el peor caso

    """

import random

# ==========================================
# 1. COMPONENTES: CONJUNTOS DE INCERTIDUMBRE
# ==========================================
class Incertidumbre:
    """Clase base para modelar parámetros inciertos."""
    def muestrear(self, num_muestras):
        raise NotImplementedError
        
    def peor_caso(self, funcion_evaluacion, maximizar=True):
        """Busca el parámetro que genera el peor escenario mediante muestreo denso."""
        muestras = self.muestrear(num_muestras=500)
        if maximizar:
            # Para costos, el peor caso es el que MAXIMIZA el costo
            return max(muestras, key=funcion_evaluacion)
        else:
            return min(muestras, key=funcion_evaluacion)


class IncertidumbreCaja(Incertidumbre):
    """Incertidumbre tipo Intervalo o Caja [Límite Inferior, Límite Superior]."""
    def __init__(self, limites_por_parametro):
        # limites_por_parametro: lista de tuplas [(min, max), (min, max)...]
        self.limites = limites_por_parametro

    def muestrear(self, num_muestras=500):
        muestras = []
        for _ in range(num_muestras):
            # Genera un vector aleatorio dentro de la caja uniformemente
            muestra = [random.uniform(inf, sup) for inf, sup in self.limites]
            muestras.append(muestra)
        return muestras


# ==========================================
# 2. COMPONENTE: MODELO DETERMINISTA BASE
# ==========================================
class ModeloBase:
    """Modelo matemático sin incertidumbre."""
    def evaluar(self, x, params):
        raise NotImplementedError
        
    def restricciones(self, x, params):
        raise NotImplementedError


class PlanificacionProduccion(ModeloBase):
    """Problema específico de producción con demanda incierta."""
    def __init__(self, costo_prod, costo_faltante, capacidad):
        self.costo_prod = costo_prod
        self.costo_faltante = costo_faltante
        self.capacidad = capacidad

    def evaluar(self, x, params):
        # x: Cantidad a producir (decisión)
        # params: [Demanda del mercado] (parámetro incierto)
        cantidad_producida = x[0]
        demanda = params[0]
        
        # Calcular costos
        costo_fijo_prod = cantidad_producida * self.costo_prod
        unidades_faltantes = max(0.0, demanda - cantidad_producida)
        costo_penalizacion = unidades_faltantes * self.costo_faltante
        
        return costo_fijo_prod + costo_penalizacion

    def restricciones(self, x, params):
        cantidad_producida = x[0]
        # Retorna True si cumple con las restricciones físicas
        dentro_de_capacidad = 0.0 <= cantidad_producida <= self.capacidad
        return dentro_de_capacidad


# ==========================================
# 3. COMPONENTE: MODELO ROBUSTO (Une Base + Incertidumbre)
# ==========================================
class ModeloRobusto:
    """Clase intermedia que aplica el criterio del peor caso al modelo base."""
    def __init__(self, modelo_base: ModeloBase, incertidumbre: Incertidumbre):
        self.modelo_base = modelo_base         # Composición 1
        self.incertidumbre = incertidumbre     # Composición 2

    def evaluar_robusta(self, x):
        """Evalúa la decisión 'x' bajo el peor parámetro posible."""
        # Definimos una función rápida para evaluar params fijos con nuestra x actual
        def funcion_costo_parametro(params):
            return self.modelo_base.evaluar(x, params)
        
        # Encontramos el peor parámetro (aquel que maximiza nuestro costo)
        peor_parametro = self.incertidumbre.peor_caso(funcion_costo_parametro, maximizar=True)
        
        # El costo robusto es el costo en ese peor escenario
        return self.modelo_base.evaluar(x, peor_parametro), peor_parametro

    def es_factible_robusta(self, x):
        """Verifica si la restricción se cumple para todos los escenarios posibles."""
        muestras = self.incertidumbre.muestrear(num_muestras=100)
        # Debe ser factible en cada una de las muestras del conjunto de incertidumbre
        return all(self.modelo_base.restricciones(x, p) for p in muestras)


# ==========================================
# 4. COMPONENTE: OPTIMIZADOR ROBUSTO
# ==========================================
class OptimizadorRobusto:
    """Se encarga de explorar el espacio de decisiones para minimizar el peor caso."""
    def __init__(self, modelo_robusto: ModeloRobusto):
        self.modelo_robusto = modelo_robusto   # Composición 3

    def optimizar(self, x_inicial, paso=1.0):
        """Búsqueda local simple (Grid/Hill-Climbing) para encontrar la x óptima."""
        mejor_x = list(x_inicial)
        mejor_costo_robusto, _ = self.modelo_robusto.evaluar_robusta(mejor_x)
        
        print(f"--- Iniciando Optimización Robusta ---")
        
        # Para problemas continuos simples de una variable, exploramos el rango de capacidad
        # Evaluamos de 0 a 150 unidades de 1 en 1
        for propuesta_q in range(0, 151):
            x_propuesta = [float(propuesta_q)]
            
            if self.modelo_robusto.es_factible_robusta(x_propuesta):
                costo_robusto, peor_demanda = self.modelo_robusto.evaluar_robusta(x_propuesta)
                
                if costo_robusto < mejor_costo_robusto:
                    mejor_costo_robusto = costo_robusto
                    mejor_x = x_propuesta
                    
        return mejor_x, mejor_costo_robusto

random.seed(42) # Mantener consistencia en el muestreo

# 1. Definir el conjunto de incertidumbre: Demanda entre 100 y 200
# Al ser una "Incertidumbre de Caja", le pasamos el intervalo del único parámetro.
conjunto_incertidumbre = IncertidumbreCaja(limites_por_parametro=[(100.0, 200.0)])

# 2. Definir los parámetros económicos del problema determinista
# Costo producción: $10, Costo faltante: $5, Capacidad: 150 unidades
problema_produccion = PlanificacionProduccion(costo_prod=10.0, costo_faltante=5.0, capacidad=150.0)

# 3. Componer el Modelo Robusto (Base + Incertidumbre)
modelo_robusto_sistema = ModeloRobusto(modelo_base=problema_produccion, incertidumbre=conjunto_incertidumbre)

# 4. Pasar el modelo al Optimizador
optimizador = OptimizadorRobusto(modelo_robusto_sistema)

# Ejecutar la optimización buscando la mejor cantidad a producir
cantidad_inicial_propuesta = [0.0]
cantidad_optima, costo_peor_caso = optimizador.optimizar(cantidad_inicial_propuesta)

# --- ANALIZAR RESULTADO ---
print(f"\n=== Resultados de la Solución Robusta ===")
print(f" Cantidad óptima a producir: {cantidad_optima[0]} unidades.")
print(f" Costo garantizado en el PEOR de los casos: ${costo_peor_caso:.2f}")

# Validemos qué pasa si fabricamos menos (por ejemplo, el promedio de la demanda: 150)
costo_promedio_caso, peor_d = modelo_robusto_sistema.evaluar_robusta([150.0])
print(f"\nComparativa de control:")
print(f" Si produces 150 unidades (Capacidad Máxima), tu costo en el peor caso (Demanda={peor_d[0]:.1f}) sería: ${costo_promedio_caso:.2f}")
