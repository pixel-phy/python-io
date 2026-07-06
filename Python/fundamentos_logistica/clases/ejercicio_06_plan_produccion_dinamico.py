"""Ejercicio 06: Plan de Producción Dinámico

Crear una clase PlanProduccion que gestione un problema de producción multiperiodo:

Atributos:
- periodos (list[int]): lista de periodos.

- demanda_por_periodo (dict[int, float]). demanda en cada periodo.

- capacidad_por_periodo (dict[int, float]): capacidad máxima de producción

- costo_produccion_unitario (dict[int, float]): costo por unidad producida

- costo_inventario_unitario (float): costo de mantener inventario por periodo

- inventario_inicial (float)

- produccion_actual (dict[int, float]): diccionario que se llenará con las decisiones

- inventario_final_por_periodo (dict[int, float]): se calculará automáticamente

Métodos:

calcular_inventario_final(periodo): I_t = I_{t-1} + P_t - D_t

verificar_solucion_factible(): comprueba que no haya faltantes (inventario final >= 0)

calcular_costo_total(): suma costo de producción + costo de inventario

generar_plan_base(): genera una producción mínima que cubre la demanda (sin optimización)

optimizar_produccion(): desafío: implementa una lógica simple de optimización para minimizar costos.

"""

class PlanProduccion:
    def __init__(self, periodos: list[int], demanda: dict[int, float], 
                 capacidad: dict[int, float], costo_prod: dict[int, float], 
                 costo_inv_unitario: float, inventario_inicial: float):
        
        self.periodos = periodos
        self.demanda_por_periodo = demanda
        self.capacidad_por_periodo = capacidad
        self.costo_produccion_unitario = costo_prod
        self.costo_inventario_unitario = costo_inv_unitario
        self.inventario_inicial = inventario_inicial
        
        # Inicialización de planes y resultados
        self.produccion_actual = {t: 0.0 for t in periodos}
        self.inventario_final_por_periodo = {t: 0.0 for t in periodos}

    def calcular_inventario_final(self):
        """
        Calcula el inventario final para cada periodo usando la ecuación de balance:
        $$I_t = I_{t-1} + P_t - D_t$$
        """
        inv_anterior = self.inventario_inicial
        for t in self.periodos:
            p_t = self.produccion_actual.get(t, 0.0)
            d_t = self.demanda_por_periodo.get(t, 0.0)
            
            inv_actual = inv_anterior + p_t - d_t
            self.inventario_final_por_periodo[t] = inv_actual
            inv_anterior = inv_actual

    def verificar_solucion_factible(self) -> bool:
        """
        Comprueba que no haya faltantes (inventario final >= 0) y que no se 
        exceda la capacidad de producción de cada periodo.
        """
        self.calcular_inventario_final()
        
        for t in self.periodos:
            # 1. No se permiten faltantes (Backlogs)
            if self.inventario_final_por_periodo[t] < -1e-5: # Tolerancia de punto flotante
                return False
            # 2. No exceder capacidad
            if self.produccion_actual[t] > self.capacidad_por_periodo[t] + 1e-5:
                return False
        return True

    def calcular_costo_total(self) -> float:
        """
        Suma el costo total de producción + el costo de mantener inventario.
        """
        self.calcular_inventario_final()
        costo_prod = sum(self.produccion_actual[t] * self.costo_produccion_unitario[t] for t in self.periodos)
        costo_inv = sum(max(0.0, self.inventario_final_por_periodo[t]) * self.costo_inventario_unitario for t in self.periodos)
        return costo_prod + costo_inv

    def generar_plan_base(self):
        """
        Genera un plan reactivo: Produce exactamente lo necesario para cubrir la 
        demanda neta de cada periodo (Demanda - Inventario Inicial disponible).
        """
        inv_anterior = self.inventario_inicial
        for t in self.periodos:
            demanda_neta = self.demanda_por_periodo[t] - inv_anterior
            if demanda_neta > 0:
                # Producimos lo necesario limitado por la capacidad máxima
                produccion = min(demanda_neta, self.capacidad_por_periodo[t])
                self.produccion_actual[t] = float(produccion)
            else:
                self.produccion_actual[t] = 0.0
            
            inv_anterior = inv_anterior + self.produccion_actual[t] - self.demanda_por_periodo[t]
        
        self.calcular_inventario_final()

    def optimizar_produccion(self):
        """
        Desafío: Heurística de optimización basada en horizontes de planificación.
        Intenta mover producción a periodos más baratos en el pasado si hay capacidad,
        siempre que el ahorro de producción supere el costo de mantener el inventario.
        """
        # Comenzamos con el plan base para asegurar la factibilidad inicial
        self.generar_plan_base()
        
        # Intentamos optimizar iterando de atrás hacia adelante
        for t in reversed(self.periodos):
            # Vemos si podemos reducir producción en t y pasarla a un periodo anterior k más barato
            for k in self.periodos:
                if k >= t:
                    break
                
                # Calcular costo marginal de producir en k y almacenar hasta t
                costo_anticipado = self.costo_produccion_unitario[k] + (t - k) * self.costo_inventario_unitario
                
                # Si es más barato producir antes (en k) que producir ahora (en t)
                if costo_anticipado < self.costo_produccion_unitario[t]:
                    # Ver cuánta capacidad le queda a k y cuánto podemos quitarle a t
                    espacio_en_k = self.capacidad_por_periodo[k] - self.produccion_actual[k]
                    disponible_en_t = self.produccion_actual[t]
                    
                    cantidad_a_mover = min(espacio_en_k, disponible_en_t)
                    
                    if cantidad_a_mover > 0:
                        # Reasignamos producción
                        self.produccion_actual[k] += cantidad_a_mover
                        self.produccion_actual[t] -= cantidad_a_mover


# Prueba:
if __name__ == "__main__":
    # Configuración de un problema de 4 periodos
    periodos = [1, 2, 3, 4]
    demanda = {1: 100, 2: 150, 3: 200, 4: 100}
    capacidad = {1: 200, 2: 200, 3: 200, 4: 200}
    
    # El periodo 1 es extremadamente barato de producir
    costo_prod = {1: 10.0, 2: 25.0, 3: 25.0, 4: 25.0} 
    costo_inv_unitario = 2.0  # Conviene producir en 1 y guardar si el ahorro > 2.0 por periodo
    inventario_inicial = 20.0

    # Instanciamos el plan
    plan = PlanProduccion(periodos, demanda, capacidad, costo_prod, costo_inv_unitario, inventario_inicial)
    
    print("=== PLAN BASE (REACTIVO) ===")
    plan.generar_plan_base()
    print(f"Producción: {plan.produccion_actual}")
    print(f"Inventario Final: {plan.inventario_final_por_periodo}")
    print(f"¿Es Factible?: {plan.verificar_solucion_factible()}")
    print(f"Costo Total: ${plan.calcular_costo_total():,.2f}")
    
    print("\n")
    
    print("=== PLAN OPTIMIZADO ===")
    plan.optimizar_produccion()
    print(f"Producción óptima: {plan.produccion_actual}")
    print(f"Inventario Final: {plan.inventario_final_por_periodo}")
    print(f"¿Es Factible?: {plan.verificar_solucion_factible()}")
    print(f"Costo Total Optimizado: ${plan.calcular_costo_total():,.2f}")
