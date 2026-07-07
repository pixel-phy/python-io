"""Ejercicio 30: Sistema de optimización de Cartera con Múltiples Relaciones
Crea un sistema completo de gestión de cartera de inversiones con:

a) Clase Activo con:
- Atributos: nombre, precio_actual, rendimiento_esperado, riesgo (desviación)
- Métodos para calcular rendimiento y riesgo

b) Clase Cartera que contenga:
- Diccionario de activos con sus pesos (composición)
- Métodos: agregar_activo(), eliminar_activo(), rebalancear()
- Propiedad rendimiento_total y riesgo_total (calculados)
- Método frontera_eficiente() que genere puntos para la frontera

c) Clase OptimizadorCartera con:
- Referencia a una Cartera (asociación)
- Métodos estáticos: maximizar_rendimiento(), minimizar_riesgo()
- Método de instancia: optimizar_riesgo_rendimiento(objetivo)
- Análisis de sensibilidad del portafolio

d) Implementar:
- Método simular_historicos(periodos) que genere datos de prueba
- __str__ que muestre la composición y métricas de la cartera
- Validación de que los pesos sumen 1
- Método de clase desde_csv() para cargar activos desde archivo
"""

import csv
import math
import random

class Activo:
    def __init__(self, nombre, precio_actual, rendimiento_esperado, riesgo):
        """
        Atributos:
        - nombre (str): Identificador del activo (ej. 'AAPL', 'BTC')
        - precio_actual (float): Valor actual de mercado
        - rendimiento_esperado (float): Rendimiento medio esperado (ej. 0.12 para 12%)
        - riesgo (float): Desviación estándar del rendimiento (ej. 0.18 para 18%)
        """
        self.nombre = nombre
        self.precio_actual = float(precio_actual)
        self.rendimiento_esperado = float(rendimiento_esperado)
        self.riesgo = float(riesgo)

    def calcular_rendimiento_simulado(self, volatilidad_mercado=0.0):
        """Simula un rendimiento usando una distribución normal básica."""
        desviacion_total = self.riesgo + volatilidad_mercado
        return random.gauss(self.rendimiento_esperado, desviacion_total)

    def __str__(self):
        return f"{self.nombre} | Rendimiento Esp: {self.rendimiento_esperado*100:.1f}% | Riesgo: {self.riesgo*100:.1f}%"


class Cartera:
    def __init__(self, nombre="Mi Cartera"):
        self.nombre = nombre
        # Composición: Diccionario {Activo: peso}
        self.activos_pesos = {}
        # Matriz de correlación simulada por simplicidad (clave: (nombre1, nombre2) -> correlacion)
        self._matriz_correlacion = {}

    def agregar_activos_masivos(self, diccionario_activos):
        """Permite agregar múltiples activos con sus pesos de golpe."""
        for activo, peso in diccionario_activos.items():
            if isinstance(activo, Activo):
                self.activos_pesos[activo] = float(peso)
        self._inicializar_correlaciones_simuladas()

    def agregar_activo(self, activo, peso):
        """Agrega o actualiza un activo en la cartera con un peso específico."""
        if not isinstance(activo, Activo):
            raise TypeError("El objeto debe ser una instancia de Activo.")
        self.activos_pesos[activo] = float(peso)
        self._inicializar_correlaciones_simuladas()

    def eliminar_activo(self, nombre_activo):
        """Elimina un activo de la cartera por su nombre."""
        activo_a_borrar = next((a for a in self.activos_pesos if a.nombre == nombre_activo), None)
        if activo_a_borrar:
            del self.activos_pesos[activo_a_borrar]
            print(f"Activo {nombre_activo} eliminado de la cartera.")
            self._inicializar_correlaciones_simuladas()
        else:
            print(f"No se encontró el activo {nombre_activo} en la cartera.")

    def validar_pesos(self):
        """Verifica si la suma de los pesos es igual a 1 (con tolerancia flotante)."""
        suma_pesos = sum(self.activos_pesos.values())
        return math.isclose(suma_pesos, 1.0, abs_tol=1e-5)

    def rebalancear(self):
        """Rebalancea equitativamente los activos de la cartera para que sumen 1."""
        if not self.activos_pesos:
            return
        num_activos = len(self.activos_pesos)
        peso_equitativo = 1.0 / num_activos
        for activo in self.activos_pesos:
            self.activos_pesos[activo] = peso_equitativo
        print("Cartera rebalanceada automáticamente con pesos equitativos.")

    def _inicializar_correlaciones_simuladas(self):
        """Genera correlaciones por defecto entre los activos para el cálculo del riesgo."""
        nombres = [a.nombre for a in self.activos_pesos]
        for n1 in nombres:
            for n2 in nombres:
                if (n1, n2) not in self._matriz_correlacion:
                    if n1 == n2:
                        self._matriz_correlacion[(n1, n2)] = 1.0
                    else:
                        # Correlación aleatoria pero fija entre 0.1 y 0.5 para simular diversificación
                        random.seed(hash(n1) + hash(n2))
                        self._matriz_correlacion[(n1, n2)] = random.uniform(0.1, 0.5)

    @property
    def rendimiento_total(self):
        """Propiedad calculada: Rendimiento esperado del portafolio (Suma ponderada)."""
        return sum(activo.rendimiento_esperado * peso for activo, peso in self.activos_pesos.items())

    @property
    def riesgo_total(self):
        """Propiedad calculada: Riesgo total del portafolio usando la fórmula de Markowitz."""
        varianza = 0.0
        activos = list(self.activos_pesos.keys())
        
        for a1 in activos:
            for a2 in activos:
                w1 = self.activos_pesos[a1]
                w2 = self.activos_pesos[a2]
                sig1 = a1.riesgo
                sig2 = a2.riesgo
                rho = self._matriz_correlacion.get((a1.nombre, a2.nombre), 0.2)
                
                varianza += w1 * w2 * sig1 * sig2 * rho
                
        return math.sqrt(varianza) if varianza > 0 else 0.0

    def frontera_eficiente(self, puntos=5):
        """Genera puntos simulados de combinaciones óptimas riesgo-rendimiento."""
        print(f"\n--- Puntos de la Frontera Eficiente ({self.nombre}) ---")
        if len(self.activos_pesos) < 2:
            print("Se requieren al menos 2 activos para trazar una frontera.")
            return []
            
        resultados = []
        # Guardar pesos originales para no destruir la configuración actual
        pesos_originales = self.activos_pesos.copy()
        activos = list(self.activos_pesos.keys())
        
        # Simular variaciones de pesos entre los dos primeros activos para hallar curvas
        for i in range(puntos):
            w1 = i / (puntos - 1)
            w2 = 1.0 - w1
            
            # Asignar pesos temporales distribuidos
            for idx, activo in enumerate(activos):
                if idx == 0: self.activos_pesos[activo] = w1
                elif idx == 1: self.activos_pesos[activo] = w2
                else: self.activos_pesos[activo] = 0.0
                
            resultados.append((self.riesgo_total, self.rendimiento_total))
            print(f"Punto {i+1}: Riesgo = {self.riesgo_total*100:.2f}% | Rendimiento = {self.rendimiento_total*100:.2f}%")
            
        # Restaurar la cartera a su estado original
        self.activos_pesos = pesos_originales
        return resultados

    @classmethod
    def desde_csv(cls, ruta_archivo, nombre_cartera="Cartera Importada"):
        """Método de clase para instanciar una cartera leyendo activos de un CSV."""
        instancia_cartera = cls(nombre_cartera)
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    activo = Activo(
                        nombre=fila['nombre'],
                        precio_actual=fila['precio_actual'],
                        rendimiento_esperado=fila['rendimiento_esperado'],
                        riesgo=fila['riesgo']
                    )
                    # Inicialmente se agrega con peso 0; requiere rebalancear o asignar
                    instancia_cartera.agregar_activo(activo, 0.0)
            print(f"Archivo '{ruta_archivo}' cargado con éxito. {len(instancia_cartera.activos_pesos)} activos añadidos.")
            instancia_cartera.rebalancear() # Asigna pesos equitativos por defecto
            return instancia_cartera
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo CSV en la ruta: {ruta_archivo}")
            return instancia_cartera

    def __str__(self):
        estado_pesos = "VÁLIDO (Suma 100%)" if self.validar_pesos() else "INVÁLIDO (No suma 100%)"
        lineas = [
            f"\n CARTERA: {self.nombre} ",
            f"Estado de los Pesos: {estado_pesos}",
            "Composición:"
        ]
        for activo, peso in self.activos_pesos.items():
            lineas.append(f"  - {activo.nombre}: Peso = {peso*100:.1f}% | [Precio Actual: ${activo.precio_actual:.2f}]")
        lineas.append("-" * 50)
        lineas.append(f"RENDIMIENTO ESPERADO TOTAL : {self.rendimiento_total*100:.2f}%")
        lineas.append(f"RIESGO TOTAL (VOLATILIDAD) : {self.riesgo_total*100:.2f}%") 
        return "\n".join(lineas)


class OptimizadorCartera:
    def __init__(self, cartera=None):
        # Asociación: El optimizador hace referencia a una cartera, pero esta existe por separado
        self.cartera = cartera

    @staticmethod
    def maximizar_rendimiento(activos):
        """Método estático: Encuentra el activo con mayor rendimiento individual."""
        if not activos: return None
        mejor = max(activos, key=lambda a: a.rendimiento_esperado)
        return mejor.nombre, mejor.rendimiento_esperado

    @staticmethod
    def minimizar_riesgo(activos):
        """Método estático: Encuentra el activo más seguro individualmente."""
        if not activos: return None
        mas_seguro = min(activos, key=lambda a: a.riesgo)
        return mas_seguro.nombre, mas_seguro.riesgo

    def optimizar_riesgo_rendimiento(self, objetivo='sharpe'):
        """Asigna pesos de forma algorítmica simulada de acuerdo a un objetivo."""
        if not self.cartera or not self.cartera.activos_pesos:
            print("No hay una cartera asociada o está vacía.")
            return

        activos = list(self.cartera.activos_pesos.keys())
        
        if objetivo.lower() == 'rendimiento':
            # Todo al que rinde más
            for a in activos:
                self.cartera.activos_pesos[a] = 1.0 if a.nombre == max(activos, key=lambda x: x.rendimiento_esperado).nombre else 0.0
        elif objetivo.lower() == 'riesgo':
            # Todo al que tiene menos riesgo
            for a in activos:
                self.cartera.activos_pesos[a] = 1.0 if a.nombre == min(activos, key=lambda x: x.riesgo).nombre else 0.0
        else:
            # Simulación de optimización mixta (Sharpe Ratio optimizado)
            self.cartera.rebalancear()
            
        print(f"Optimización completada bajo el criterio: '{objetivo.upper()}'")

    def analisis_sensibilidad(self, incremento_volatilidad=0.05):
        """Evalúa cómo afecta un shock de mercado al riesgo y rendimiento global."""
        if not self.cartera: return
        print(f"Análisis de Sensibilidad (Shock de estrés al mercado de +{incremento_volatilidad*100:.0f}%):")
        
        rendimiento_actual = self.cartera.rendimiento_total
        riesgo_actual = self.cartera.riesgo_total
        
        # Modificación temporal de las propiedades intrínsecas de los activos asociados
        for activo in self.cartera.activos_pesos:
            activo.riesgo += incremento_volatilidad
            
        print(f"  > Riesgo Inicial: {riesgo_actual*100:.2f}% -> Riesgo Post-Crisis: {self.cartera.riesgo_total*100:.2f}%")
        
        # Restaurar valores originales
        for activo in self.cartera.activos_pesos:
            activo.riesgo -= incremento_volatilidad


# --- Función Global Auxiliar (Requerimiento d) ---
def simular_historicos(periodos=10):
    """Genera una lista de activos simulados con datos sintéticos para pruebas."""
    nombres_ejemplo = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]
    activos_simulados = []
    for i in range(min(periodos, len(nombres_ejemplo))):
        activo = Activo(
            nombre=nombres_ejemplo[i],
            precio_actual=random.uniform(100, 3000),
            rendimiento_esperado=random.uniform(0.05, 0.25), # entre 5% y 25%
            riesgo=random.uniform(0.10, 0.35)                # entre 10% y 35%
        )
        activos_simulados.append(activo)
    return activos_simulados

# Creación de datos de prueba usando el simulador histórico
activos_mercado = simular_historicos(4)

print("--- Activos Disponibles en el Mercado simulado ---")
for act in activos_mercado:
    print(act)

# 1. Creación de la Cartera (Composición interna de pesos)
mi_portafolio = Cartera("Portafolio de Crecimiento Tecnológico")

# Añadimos los activos dándoles un peso manual inicial de 25% a cada uno (Suma 1.0)
for a in activos_mercado:
    mi_portafolio.agregar_activo(a, 0.25)

# Imprimimos la cartera actual y sus métricas calculadas automáticas
print(mi_portafolio)

# 2. Uso del Optimizador (Asociación)
optimizador = OptimizadorCartera(cartera=mi_portafolio)

# Probando Métodos Estáticos
print("--- Análisis del Analista Externo (Métodos Estáticos) ---")
print(f"Activo óptimo para maximizar rendimiento: {OptimizadorCartera.maximizar_rendimiento(activos_mercado)}")
print(f"Activo óptimo para minimizar riesgo: {OptimizadorCartera.minimizar_riesgo(activos_mercado)}")

# 3. Alterando los pesos para probar la validación
print("\n--- Forzando una mala asignación de pesos ---")
activo_cualquiera = activos_mercado[0]
mi_portafolio.agregar_activo(activo_cualquiera, 0.90) # Ahora la suma superará el 100%
print(f"¿Los pesos de la cartera son válidos?: {mi_portafolio.validar_pesos()}")
print(mi_portafolio)

# Corregimos usando el método de rebalanceo interno
mi_portafolio.rebalancear()
print(f"¿Los pesos tras rebalancear son válidos?: {mi_portafolio.validar_pesos()}")

# 4. Generación de Frontera Eficiente
mi_portafolio.frontera_eficiente(puntos=4)

# 5. Análisis de Sensibilidad ante crisis
print("")
optimizador.analisis_sensibilidad(incremento_volatilidad=0.08)

# 6. Demostración de optimización de instancia
optimizador.optimizar_riesgo_rendimiento(objetivo='riesgo')
print(mi_portafolio)
