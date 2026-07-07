"""Ejercicio 24: Sistema de Optimización de Producción con Parámetros Críticos

Crea un sistema completo SistemaProduccion que integre:

a) Clase Producto con:

- Atributos privados: __nombre, __demanda, __costo_produccion, __precio_venta
- Propiedades con validaciones (demanda ≥ 0, costos ≥ 0)
- Propiedad calculada: margen_contribucion = precio - costo

b) Clase PlanProduccion con:

- Lista de productos (composición)
- Atributo privado __capacidad_total con setter validado
- Atributo privado __asignacion (diccionario producto -> cantidad)
- Método de instancia asignar_produccion(producto, cantidad) con validación

c) Métodos estáticos en PlanProduccion:

- calcular_costo_total(asignacion, costos): calcula costo total
- calcular_ingreso_total(asignacion, precios): calcula ingreso
- calcular_beneficio(asignacion, costos, precios): beneficio neto
- validar_capacidad(asignacion, capacidad): verifica no exceder capacidad
- generar_plan_inicial(productos, capacidad): plan heurístico de producción

d) Implementar:

- Método optimizar() que maximice beneficio usando la capacidad disponible
- Método reporte_financiero() que muestre costos, ingresos y beneficio
- Protección contra asignaciones inválidas (exceso de capacidad, cantidades negativas)
- Método estático analisis_sensibilidad(plan, productos, variacion) para análisis de escenarios
"""
from typing import List, Dict

class Producto:
    def __init__(self, nombre: str, demanda: int, costo_produccion: float, precio_venta: float):
        self.__nombre = nombre
        self.demanda = demanda              # Usa el setter para validar
        self.costo_produccion = costo_produccion  # Usa el setter para validar
        self.precio_venta = precio_venta    # Usa el setter para validar

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def demanda(self) -> int:
        return self.__demanda

    @demanda.setter
    def demanda(self, valor: int):
        if valor < 0:
            raise ValueError("La demanda no puede ser negativa.")
        self.__demanda = int(valor)

    @property
    def costo_produccion(self) -> float:
        return self.__costo_produccion

    @costo_produccion.setter
    def costo_produccion(self, valor: float):
        if valor < 0:
            raise ValueError("El costo de producción no puede ser negativo.")
        self.__costo_produccion = float(valor)

    @property
    def precio_venta(self) -> float:
        return self.__precio_venta

    @precio_venta.setter
    def precio_venta(self, valor: float):
        if valor < 0:
            raise ValueError("El precio de venta no puede ser negativo.")
        self.__precio_venta = float(valor)

    # Propiedad calculada
    @property
    def margen_contribucion(self) -> float:
        """Margen de contribución = precio_venta - costo_produccion"""
        return self.__precio_venta - self.__costo_produccion

    def __repr__(self):
        return f"Producto({self.__nombre}, Margen: ${self.margen_contribucion:.2f}, Demanda: {self.__demanda})"

class PlanProduccion:
    def __init__(self, productos: List[Producto], capacidad_total: int):
        self.productos = productos  # Composición
        self.capacidad_total = capacidad_total  # Usa el setter para validar
        # Atributo privado __asignacion { nombre_producto: cantidad_asignada }
        self.__asignacion: Dict[str, int] = {p.nombre: 0 for p in productos}

    @property
    def capacidad_total(self) -> int:
        return self.__capacidad_total

    @capacidad_total.setter
    def capacity_total(self, valor: int): # Manejo interno por nombre semántico estándar o el pedido:
        pass

    @property
    def capacidad_total(self) -> int:
        return self.__capacidad_total

    @capacidad_total.setter
    def capacidad_total(self, valor: int):
        if valor < 0:
            raise ValueError("La capacidad total de la planta no puede ser negativa.")
        self.__capacidad_total = int(valor)

    @property
    def asignacion(self) -> Dict[str, int]:
        return self.__asignacion

    def asignar_produccion(self, producto: Producto, cantidad: int):
        """Asigna de forma segura una cantidad a fabricar de un producto."""
        if cantidad < 0:
            raise ValueError("La cantidad asignada no puede ser negativa.")
        if producto.nombre not in self.__asignacion:
            raise KeyError(f"El producto '{producto.nombre}' no pertenece a este plan.")
        
        # Validar si este cambio excede la capacidad total
        copia_asignacion = self.__asignacion.copy()
        copia_asignacion[producto.nombre] = cantidad
        
        if not self.validar_capacidad(copia_asignacion, self.__capacidad_total):
            raise ValueError("Asignación inválida: Supera la capacidad total de la planta.")
        if cantidad > producto.demanda:
            raise ValueError(f"Asignación inválida: Supera la demanda máxima del producto ({producto.demanda}).")
            
        self.__asignacion[producto.nombre] = cantidad

    # --- MÉTODOS ESTÁTICOS FINANCIEROS Y LOGÍSTICOS ---

    @staticmethod
    def calcular_costo_total(asignacion: Dict[str, int], costos: Dict[str, float]) -> float:
        return sum(cantidad * costos.get(prod, 0.0) for prod, cantidad in asignacion.items())

    @staticmethod
    def calcular_ingreso_total(asignacion: Dict[str, int], precios: Dict[str, float]) -> float:
        return sum(cantidad * precios.get(prod, 0.0) for prod, cantidad in asignacion.items())

    @staticmethod
    def calcular_beneficio(asignacion: Dict[str, int], costos: Dict[str, float], precios: Dict[str, float]) -> float:
        ingresos = PlanProduccion.calcular_ingreso_total(asignacion, precios)
        costos_t = PlanProduccion.calcular_costo_total(asignacion, costos)
        return ingresos - costos_t

    @staticmethod
    def validar_capacidad(asignacion: Dict[str, int], capacidad: int) -> bool:
        """Verifica que la suma de las cantidades no exceda la capacidad."""
        return sum(asignacion.values()) <= capacidad

    @staticmethod
    def generar_plan_inicial(productos: List[Producto], capacidad: int) -> Dict[str, int]:
        """Heurística 'Greedy' para maximizar beneficio usando el margen de contribución."""
        # Ordenamos los productos de mayor a menor margen
        productos_ordenados = sorted(productos, key=lambda x: x.margen_contribucion, reverse=True)
        plan = {p.nombre: 0 for p in productos}
        capacidad_restante = capacidad

        for prod in productos_ordenados:
            if capacidad_restante <= 0:
                break
            # Asignamos el mínimo entre lo que queda de planta y la demanda máxima del producto
            cantidad_a_producir = min(capacidad_restante, prod.demanda)
            plan[prod.nombre] = cantidad_a_producir
            capacidad_restante -= cantidad_a_producir

        return plan

    # --- MÉTODOS DE INSTANCIA AVANZADOS ---

    def optimizar(self):
        """Ejecuta la optimización y guarda el resultado en la asignación del plan."""
        plan_optimo = self.generar_plan_inicial(self.productos, self.__capacidad_total)
        for nombre_prod, cantidad in plan_optimo.items():
            # Buscamos el objeto producto correspondiente
            producto_obj = next(p for p in self.productos if p.nombre == nombre_prod)
            self.asignar_produccion(producto_obj, cantidad)

    def reporte_financiero(self) -> str:
        """Genera un string formateado con el resumen financiero actual."""
        costos_dict = {p.nombre: p.costo_produccion for p in self.productos}
        precios_dict = {p.nombre: p.precio_venta for p in self.productos}
        
        costo_t = self.calcular_costo_total(self.__asignacion, costos_dict)
        ingreso_t = self.calcular_ingreso_total(self.__asignacion, precios_dict)
        beneficio_t = self.calcular_beneficio(self.__asignacion, costos_dict, precios_dict)
        capacidad_usada = sum(self.__asignacion.values())

        reporte = (
            f"\n\n"
            f"REPORTE FINANCIERO DE PRODUCCIÓN\n"
            f"\n"
            f"Capacidad Utilizada: {capacidad_usada}/{self.__capacidad_total} unidades.\n"
            f"----------------------------------------\n"
            f"Asignación por Producto:\n"
        )
        for prod, cant in self.__asignacion.items():
            reporte += f"  - {prod.upper()}: {cant} unidades\n"
            
        reporte += (
            f"----------------------------------------\n"
            f"Ingresos Totales:   ${ingreso_t:,.2f}\n"
            f"Costos Totales:     ${costo_t:,.2f}\n"
            f"Beneficio Neto:     ${beneficio_t:,.2f}\n"
            f"========================================\n"
        )
        return reporte

    @staticmethod
    def analisis_sensibilidad(plan: 'PlanProduccion', productos: List[Producto], variacion: float) -> str:
        """
        Calcula cómo cambia el beneficio si los costos de producción aumentan/disminuyen 
        un porcentaje dado (ej: 0.10 para +10% o -0.10 para -10%).
        """
        costos_alterados = {p.nombre: p.costo_produccion * (1 + variacion) for p in productos}
        precios_dict = {p.nombre: p.precio_venta for p in productos}
        
        beneficio_original = plan.calcular_beneficio(
            plan.asignacion, 
            {p.nombre: p.costo_produccion for p in productos}, 
            precios_dict
        )
        beneficio_nuevo = plan.calcular_beneficio(plan.asignacion, costos_alterados, precios_dict)
        
        return (
            f"ANÁLISIS DE SENSIBILIDAD (Variación de costos: {variacion*100:+.1f}%):\n"
            f"   • Beneficio Original: ${beneficio_original:,.2f}\n"
            f"   • Beneficio Escenario: ${beneficio_nuevo:,.2f}\n"
            f"   • Impacto Neto:        ${beneficio_nuevo - beneficio_original:,.2f}\n"
        )

if __name__ == "__main__":
    # 1. Definimos nuestro portafolio de productos con sus demandas y márgenes financieros
    prod1 = Producto(nombre="Laptop", demanda=50, costo_produccion=400.0, precio_venta=750.0)      # MC = 350
    prod2 = Producto(nombre="Tablet", demanda=80, costo_produccion=150.0, precio_venta=300.0)      # MC = 150
    prod3 = Producto(nombre="Smartphone", demanda=100, costo_produccion=200.0, precio_venta=600.0)  # MC = 400

    mis_productos = [prod1, prod2, prod3]
    
    # Capacidad de la planta es de 180 unidades totales
    capacidad_fabrica = 180 

    # 2. Inicializamos el plan de producción
    mi_plan = PlanProduccion(productos=mis_productos, capacidad_total=capacidad_fabrica)

    # 3. Corremos el optimizador (Heurística de beneficio máximo)
    # Debería priorizar Smartphones (MC: 400), luego Laptops (MC: 350) y finalmente usar lo sobrante en Tablets (MC: 150)
    mi_plan.optimizar()

    # 4. Imprimir Reporte Financiero de la optimización
    print(mi_plan.reporte_financiero())

    # 5. Ejecutar Análisis de Sensibilidad
    # ¿Qué pasa si los costos de producción suben un 15% debido a la inflación?
    print(PlanProduccion.analisis_sensibilidad(mi_plan, mis_productos, variacion=0.15))

    # 6. Intentar romper las reglas (Protección contra asignaciones inválidas)
    print("--- Test de Seguridad ---")
    try:
        # Intentemos obligar a la planta a hacer 100 laptops (la demanda es de 50)
        mi_plan.asignar_produccion(prod1, 100)
    except ValueError as e:
        print(f"Validación exitosa: {e}")
