"""Ejercicio 48: Framework de Programación por Metas con Métodos Mágicos

Diseña un sistema completo de Programación por Metas (Goal Programming) usando clases abstractas
y métodos mágicos:

1. Clase abstracta Meta:

    - Atributos: nivel_prioridad (1 = más importante), peso
    - Métodos: evaluar_deviation(x), es_alcanzada(x)

2. Clases concretas de metas:

    - MetaIgualdad: objetivo = valor_objetivo
    - MetaCotaSuperior: objetivo ≤ valor_objetivo
    - MetaCotaInferior: objetivo ≥ valor_objetivo

3. Clase ProgramaMetas:

    - Colección de metas con diferentes prioridades
    - Método resolver() que usa programación por metas ponderadas
    - Métodos mágicos:
    - __add__ para agregar metas (metas + meta)
    - __iadd__ para agregar in-place
    - __len__ número de metas
    - __iter__ iterar sobre metas ordenadas por prioridad

4. Método de solución:

    - Implementa el algoritmo de programación por metas ponderadas
    - Calcula las desviaciones (positivas y negativas)
    - Optimiza la suma ponderada de desviaciones
    """

from abc import ABC, abstractmethod
import numpy as np
from scipy.optimize import minimize

class Meta(ABC):
    def __init__(self, funcion_objetivo, valor_meta, prioridad=1, peso=1.0, descripcion="Meta"):
        """
        - funcion_objetivo: un callable (función o lambda) que toma x y devuelve un float.
        - valor_meta: el nivel de aspiración (target).
        - prioridad: nivel de prioridad estricta (1 = máxima prioridad).
        - peso: ponderación interna dentro del mismo nivel de prioridad.
        """
        self.funcion = funcion_objetivo
        self.valor_meta = float(valor_meta)
        self.prioridad = int(prioridad)
        self.peso = float(peso)
        self.descripcion = descripcion

    @abstractmethod
    def evaluar_desviacion(self, x):
        """
        Debe retornar una tupla (d_menos, d_mas), ambas >= 0.
        - d_menos: cuánto le falta para llegar a la meta.
        - d_mas: cuánto se pasó de la meta.
        """
        pass

    @abstractmethod
    def penalizacion(self, x):
        """Calcula la penalización ponderada asociada a la desviación no deseada."""
        pass

    def es_alcanzada(self, x):
        """Retorna True si la penalización asociada es prácticamente cero."""
        return np.isclose(self.penalizacion(x), 0.0, atol=1e-5)


class MetaIgualdad(Meta):
    """Se penaliza tanto quedarse corto (d_menos) como pasarse (d_mas)."""
    def evaluar_desviacion(self, x):
        valor_actual = self.funcion(x)
        desviacion = valor_actual - self.valor_meta
        d_menos = max(0.0, -desviacion)
        d_mas = max(0.0, desviacion)
        return d_menos, d_mas

    def penalizacion(self, x):
        d_menos, d_mas = self.evaluar_desviacion(x)
        return self.peso * (d_menos + d_mas)


class MetaCotaSuperior(Meta):
    """Objetivo <= valor_meta. Solo se penaliza si se pasa (d_mas)."""
    def evaluar_desviacion(self, x):
        valor_actual = self.funcion(x)
        desviacion = valor_actual - self.valor_meta
        d_menos = max(0.0, -desviacion)
        d_mas = max(0.0, desviacion)
        return d_menos, d_mas

    def penalizacion(self, x):
        _, d_mas = self.evaluar_desviacion(x)
        return self.peso * d_mas


class MetaCotaInferior(Meta):
    """Objetivo >= valor_meta. Solo se penaliza si se queda corto (d_menos)."""
    def evaluar_desviacion(self, x):
        valor_actual = self.funcion(x)
        desviacion = valor_actual - self.valor_meta
        d_menos = max(0.0, -desviacion)
        d_mas = max(0.0, desviacion)
        return d_menos, d_mas

    def penalizacion(self, x):
        d_menos, _ = self.evaluar_desviacion(x)
        return self.peso * d_menos

class ProgramaMetas:
    def __init__(self):
        self.metas = []

    def agregar_meta(self, meta):
        if not isinstance(meta, Meta):
            raise TypeError("Solo se pueden agregar instancias de la clase Meta.")
        self.metas.append(meta)

    # --- Métodos Mágicos ---

    def __len__(self):
        """Número total de metas registradas."""
        return len(self.metas)

    def __iter__(self):
        """Itera sobre las metas ordenadas por nivel de prioridad (1 es primero)."""
        metas_ordenadas = sorted(self.metas, key=lambda m: m.prioridad)
        return iter(metas_ordenadas)

    def __add__(self, other):
        """Permite combinar programas o sumar una meta usando: nuevo = programa + meta"""
        nuevo_programa = ProgramaMetas()
        nuevo_programa.metas = self.metas.copy()
        if isinstance(other, Meta):
            nuevo_programa.agregar_meta(other)
        elif isinstance(other, ProgramaMetas):
            nuevo_programa.metas.extend(other.metas)
        else:
            return NotImplemented
        return nuevo_programa

    def __iadd__(self, other):
        """Permite agregar una meta in-place usando: programa += meta"""
        if isinstance(other, Meta):
            self.agregar_meta(other)
        elif isinstance(other, ProgramaMetas):
            self.metas.extend(other.metas)
        else:
            return NotImplemented
        return self

    # --- Algoritmo de Solución (Metas Ponderadas) ---

    def resolver(self, x_inicial, bounds=None):
        """
        Encuentra el punto x que minimiza la suma ponderada de las desviaciones.
        """
        x_inicial = np.array(x_inicial, dtype=float)

        # Función objetivo global para el optimizador numérico
        def funcion_global_penalizacion(x):
            suma_penalizaciones = 0.0
            for meta in self.metas:
                suma_penalizaciones += meta.penalizacion(x)
            return suma_penalizaciones

        # Ejecutar optimización numérica usando SciPy
        resultado = minimize(funcion_global_penalizacion, x_inicial, bounds=bounds, method='SLSQP')
        
        x_optimo = resultado.x
        
        # Estructurar reporte de resultados
        reporte = {
            "x_optimo": x_optimo,
            "exito": resultado.success,
            "metas_detalle": []
        }
        
        for meta in self: # Uso implícito de __iter__ (ordenado por prioridad)
            d_menos, d_mas = meta.evaluar_desviacion(x_optimo)
            reporte["metas_detalle"].append({
                "descripcion": meta.descripcion,
                "prioridad": meta.prioridad,
                "valor_obtenido": meta.funcion(x_optimo),
                "target": meta.valor_meta,
                "d_menos": d_menos,
                "d_mas": d_mas,
                "alcanzada": meta.es_alcanzada(x_optimo)
            })
            
        return reporte

# 1. Instanciar el programa
modelo_produccion = ProgramaMetas()

# 2. Definir las funciones objetivo asociadas a las metas
f_utilidad = lambda x: 20*x[0] + 30*x[1]
f_horas = lambda x: 2*x[0] + 1*x[1]
f_balance = lambda x: 2*x[0] - x[1]

# 3. Crear y agregar metas usando operadores mágicos
meta1 = MetaCotaInferior(f_utilidad, valor_meta=120.0, prioridad=1, peso=2.0, descripcion="Margen de Utilidad")
meta2 = MetaCotaSuperior(f_horas, valor_meta=40.0, prioridad=2, peso=1.0, descripcion="Horas de Mano de Obra")

# Añadir metas iniciales con += (__iadd__)
modelo_produccion += meta1
modelo_produccion += meta2

# Crear una tercera meta y añadir creando un nuevo objeto con + (__add__)
meta3 = MetaIgualdad(f_balance, valor_meta=0.0, prioridad=1, peso=5.0, descripcion="Balance de Portafolio")
modelo_produccion = modelo_produccion + meta3

print(f"Número total de metas en el framework (__len__): {len(modelo_produccion)}")

# 4. Resolver el sistema
# Punto de partida [0, 0] y restricción de que la producción no sea negativa (x >= 0)
limites = [(0, None), (0, None)] 
solucion = modelo_produccion.resolver(x_inicial=[0.0, 0.0], bounds=limites)

# 5. Mostrar reporte ordenado
print("\n=== RESULTADOS DE LA PROGRAMACIÓN POR METAS ===")
print(f"Plan de Producción Óptimo: Producto A = {solucion['x_optimo'][0]:.2f}, Producto B = {solucion['x_optimo'][1]:.2f}\n")

for m in solucion["metas_detalle"]:
    status = "ALCANZADA ✓" if m["alcanzada"] else "NO ALCANZADA ✗"
    print(f"Meta: {m['descripcion']} (Prioridad {m['prioridad']}) -> {status}")
    print(f"  Valor logrado: {m['valor_obtenido']:.2f} (Objetivo: {m['target']})")
    print(f"  Desviaciones -> d_minus: {m['d_menos']:.2f}, d_plus: {m['d_mas']:.2f}")
    print("-" * 50)
