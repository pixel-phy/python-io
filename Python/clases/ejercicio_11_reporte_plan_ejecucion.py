"""Ejercicio 11: Reporte de Plan de Producción

Añade a la clase PlanProduccion del Día 1:

__repr__: muestra configuración del problema (periodos, demanda promedio)

__str__: genera un reporte tabular con producción, demanda, inventario por periodo

__format__ (opcional): permite formateo personalizado (ej. f"{plan:compact}" para versión resumida)

exportar_a_csv(nombre_archivo): guarda el plan en formato CSV

    """
import csv

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
            if self.inventario_final_por_periodo[t] < -1e-5: # Tolerancia de punto flotante
                return False
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
        demanda neta de cada periodo.
        """
        inv_anterior = self.inventario_inicial
        for t in self.periodos:
            demanda_neta = self.demanda_por_periodo[t] - inv_anterior
            if demanda_neta > 0:
                produccion = min(demanda_neta, self.capacidad_por_periodo[t])
                self.produccion_actual[t] = float(produccion)
            else:
                self.produccion_actual[t] = 0.0
            
            inv_anterior = inv_anterior + self.produccion_actual[t] - self.demanda_por_periodo[t]
        
        self.calcular_inventario_final()

    def optimizar_produccion(self):
        """
        Heurística de optimización basada en horizontes de planificación.
        """
        self.generar_plan_base()
        
        for t in reversed(self.periodos):
            for k in self.periodos:
                if k >= t:
                    break
                
                costo_anticipado = self.costo_produccion_unitario[k] + (t - k) * self.costo_inventario_unitario
                
                if costo_anticipado < self.costo_produccion_unitario[t]:
                    espacio_en_k = self.capacidad_por_periodo[k] - self.produccion_actual[k]
                    disponible_en_t = self.produccion_actual[t]
                    
                    cantidad_a_mover = min(espacio_en_k, disponible_en_t)
                    
                    if cantidad_a_mover > 0:
                        self.produccion_actual[k] += cantidad_a_mover
                        self.produccion_actual[t] -= cantidad_a_mover

    # --- NUEVOS MÉTODOS DEL EJERCICIO 4 ---

    def __repr__(self) -> str:
        """
        Muestra la configuración inicial del problema para depuración.
        """
        demanda_promedio = sum(self.demanda_por_periodo.values()) / len(self.periodos) if self.periodos else 0.0
        return f"PlanProduccion(periodos={len(self.periodos)}, demanda_promedio={demanda_promedio:.2f})"

    def __str__(self) -> str:
        """
        Genera un reporte tabular completo del plan.
        """
        self.calcular_inventario_final()
        linea = "=" * 55
        encabezado = f"| {'Periodo':^9} | {'Demanda':^10} | {'Producción':^11} | {'Inventario':^11} |"
        
        tabla = [linea, encabezado, linea]
        for t in self.periodos:
            fila = (f"| {t:^9} | "
                    f"{self.demanda_por_periodo[t]:>10.1f} | "
                    f"{self.produccion_actual[t]:>11.1f} | "
                    f"{self.inventario_final_por_periodo[t]:>11.1f} |")
            tabla.append(fila)
        
        tabla.append(linea)
        tabla.append(f"Costo Total: ${self.calcular_costo_total():,.2f}")
        return "\n".join(tabla)

    def __format__(self, format_spec: str) -> str:
        """
        Permite formateo personalizado mediante f-strings.
        Soporta 'compact' para un resumen de una línea o vuelve a str() por defecto.
        """
        if format_spec == "compact":
            self.calcular_inventario_final()
            prod_lista = [f"P{t}:{self.produccion_actual[t]:.0f}" for t in self.periodos]
            return f"Plan Compacto -> " + ", ".join(prod_lista) + f" | Costo: ${self.calcular_costo_total():.2f}"
        
        # Si no se especifica un formato reconocido, usamos el __str__ por defecto
        return str(self)

    def exportar_a_csv(self, nombre_archivo: str):
        """
        Exporta los resultados detallados del plan de producción a un archivo CSV.
        """
        self.calcular_inventario_final()
        
        campos = ['Periodo', 'Demanda', 'Capacidad', 'Produccion_Asignada', 'Inventario_Final', 'Costo_Produccion_Unitario']
        
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            
            for t in self.periodos:
                escritor.writerow({
                    'Periodo': t,
                    'Demanda': self.demanda_por_periodo[t],
                    'Capacidad': self.capacidad_por_periodo[t],
                    'Produccion_Asignada': self.produccion_actual[t],
                    'Inventario_Final': self.inventario_final_por_periodo[t],
                    'Costo_Produccion_Unitario': self.costo_produccion_unitario[t]
                })


# --- Bloque de Prueba para comprobar el funcionamiento ---
if __name__ == "__main__":
    periodos = [1, 2, 3, 4]
    demanda = {1: 100, 2: 150, 3: 200, 4: 100}
    capacidad = {1: 200, 2: 200, 3: 200, 4: 200}
    costo_prod = {1: 10.0, 2: 25.0, 3: 25.0, 4: 25.0} 
    costo_inv_unitario = 2.0 
    inventario_inicial = 20.0

    plan = PlanProduccion(periodos, demanda, capacidad, costo_prod, costo_inv_unitario, inventario_inicial)
    plan.optimizar_produccion()
    
    # 1. Probar __repr__
    print(">>> 1. Prueba de __repr__:")
    print(repr(plan))
    print("\n")
    
    # 2. Probar __str__
    print(">>> 2. Prueba de __str__ (Reporte Tabular):")
    print(plan)
    print("\n")
    
    # 3. Probar __format__ con 'compact'
    print(">>> 3. Prueba de __format__ (Versión 'compact'):")
    print(f"{plan:compact}")
    print("\n")
    
    # 4. Probar exportar_a_csv()
    archivo_salida = "plan_produccion.csv"
    plan.exportar_a_csv(archivo_salida)
    print(f">>> 4. ¡Éxito! Plan exportado correctamente a '{archivo_salida}'.")
