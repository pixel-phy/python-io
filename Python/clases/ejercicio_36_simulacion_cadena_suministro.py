""" Ejercicio 36: Simulación de Cadena de Suministro

Modela una jerarquía de 3 niveles:

Clase base ActorCadena: atributos nombre, capacidad_produccion, costo_unitario.
Métodos: producir(cantidad) que actualice inventario, calcular_costo_total(cantidad).

Clase Proveedor (hereda de ActorCadena): añade tiempo_entrega (días), descuento_por_volumen
(diccionario {cantidad_min: descuento}). Sobrescribe calcular_costo_total() aplicando descuentos.

Clase Distribuidor (hereda de Proveedor): añade flota_vehiculos (lista de vehículos con capacidades),
costo_transporte_por_km. Implementa método calcular_costo_distribucion(distancia) que use 
super().calcular_costo_total() y sume el transporte.

Requisito extra: Los constructores deben usar super() en todos los niveles, y el método producir()
del Distribuidor debe verificar si tiene suficiente capacidad propia, y si no, solicitar producción
al proveedor (simulado con un print).

"""

class ActorCadena:
    def __init__(self, nombre: str, capacidad_produccion: float, costo_unitario: float):
        self.nombre = nombre
        self.capacidad_produccion = capacidad_produccion
        self.costo_unitario = costo_unitario
        self.inventario = 0.0

    def producir(self, cantidad: float):
        """Actualiza el inventario sumando la cantidad producida."""
        self.inventario += cantidad
        print(f"[{self.nombre}] Ha producido {cantidad} unidades. Inventario actual: {self.inventario}")

    def calcular_costo_total(self, cantidad: float) -> float:
        """Cálculo base del costo lineal: cantidad * costo unitario."""
        return cantidad * self.costo_unitario


class Proveedor(ActorCadena):
    def __init__(self, nombre: str, capacidad_produccion: float, costo_unitario: float, 
                 tiempo_entrega: int, descuento_por_volumen: dict[int, float]):
        # super() apunta a ActorCadena
        super().__init__(nombre, capacidad_produccion, costo_unitario)
        self.tiempo_entrega = tiempo_entrega
        # Diccionario esperado: {cantidad_minima: porcentaje_descuento_en_decimal} -> ej: {100: 0.10}
        self.descuento_por_volumen = descuento_por_volumen

    def calcular_costo_total(self, cantidad: float) -> float:
        """Sobrescribe el costo aplicando descuentos por volumen de compra."""
        costo_base = super().calcular_costo_total(cantidad)
        descuento_aplicable = 0.0
        
        # Evaluamos cuál es el mayor descuento que el volumen alcanza
        for cant_min, desc in sorted(self.descuento_por_volumen.items()):
            if cantidad >= cant_min:
                descuento_aplicable = desc
                
        costo_final = costo_base * (1 - descuento_aplicable)
        if descuento_aplicable > 0:
            print(f"   ↳ [Descuento Aplicado] {descuento_aplicable * 100}% de descuento por superar las {cant_min} unidades.")
        return costo_final


class Distribuidor(Proveedor):
    def __init__(self, nombre: str, capacidad_produccion: float, costo_unitario: float, 
                 tiempo_entrega: int, descuento_por_volumen: dict[int, float], 
                 flota_vehiculos: list[float], costo_transporte_por_km: float):
        # super() aquí apunta a Proveedor, y este a su vez a ActorCadena
        super().__init__(nombre, capacidad_produccion, costo_unitario, tiempo_entrega, descuento_por_volumen)
        self.flota_vehiculos = flota_vehiculos  # Lista con capacidades máximas de cada vehículo
        self.costo_transporte_por_km = costo_transporte_por_km

    def calcular_costo_distribucion(self, cantidad: float, distancia: float) -> float:
        """Utiliza el cálculo de costo del proveedor (con descuentos) y añade el costo del viaje."""
        costo_adquisicion_o_prod = super().calcular_costo_total(cantidad)
        costo_viaje = distancia * self.costo_transporte_por_km
        return costo_adquisicion_o_prod + costo_viaje

    def producir(self, cantidad: float):
        """
        Verifica capacidad. Si hace falta, simula pedir la diferencia al 
        eslabón anterior (Proveedor).
        """
        if cantidad <= self.capacidad_produccion:
            # Tiene capacidad propia, ejecuta el producir del abuelo/padre
            super().producir(cantidad)
        else:
            producido_propio = self.capacidad_produccion
            faltante = cantidad - producido_propio
            
            print(f"[{self.nombre}] ¡Capacidad excedida! Límite propio: {producido_propio}. Solicitando {faltante} al proveedor.")
            
            # Produce lo que puede internamente
            if producido_propio > 0:
                super().producir(producido_propio)
            
            # Simulación del requisito extra (compra externa)
            print(f"--> [ORDEN EXTERNA] Pedido de {faltante} unidades enviado al Proveedor de la cadena.")

# Prueba:
# 1. Configuración de datos
esquema_descuentos = {50: 0.05, 100: 0.10} # 5% a partir de 50 unidades, 10% a partir de 100
capacidades_camiones = [10.0, 20.0, 50.0]  # Capacidad de carga de la flota

# 2. Instanciar el Distribuidor (que hereda todo el árbol)
distribuidor_logistico = Distribuidor(
    nombre="Logística Central S.A.",
    capacidad_produccion=80,          # Capacidad máxima propia
    costo_unitario=15.0,              # Costo base
    tiempo_entrega=3,                 # Días
    descuento_por_volumen=esquema_descuentos,
    flota_vehiculos=capacidades_camiones,
    costo_transporte_por_km=2.5       # Costo por kilómetro recorrido
)

# --- ESCENARIO A: Producir dentro del límite ---
print("--- Escenario A: Pedido de 50 unidades ---")
distribuidor_logistico.producir(50)

print("\n" + "="*50 + "\n")

# --- ESCENARIO B: Exceder la capacidad propia ---
print("--- Escenario B: Pedido de 120 unidades ---")
distribuidor_logistico.producir(120)

print("\n" + "="*50 + "\n")

# --- ESCENARIO C: Cálculo de costos financieros con descuento y transporte ---
print("--- Escenario C: Costos para mover 110 unidades a 200 km ---")
# 110 unidades activa el descuento del 10% en el costo unitario
total_financiero = distribuidor_logistico.calcular_costo_distribucion(cantidad=110, distancia=200)
print(f"\nCOSTO TOTAL DE LA OPERACIÓN: ${total_financiero:,.2f}")
