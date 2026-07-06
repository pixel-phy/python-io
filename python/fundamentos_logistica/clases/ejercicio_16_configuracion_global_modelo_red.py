"""Ejercicio 16: Configuración global para Modelo de Red

Crea una clase RedFlujoGlobal que extienda RedFlujo del Día 1 con:

Atributo de clase: costo_por_unidad_flujo = 1.0 (costo global si no se especifica en arista)

Atributo de clase: metodo_resolucion = 'simplex' (opciones: 'simplex', 'interior', 'heuristica')

Método de clase: configurar_metodo(nuevo_metodo) que valide la opción

Método de instancia: calcular_costo_total_global() que calcule el costo usando el costo_por_unidad_flujo 
para aristas sin costo específico

Constructor alternativo: desde_diccionario(datos) donde datos es un dict con nodos y aristas

"""

class Arista:
    # Modificamos el constructor para aceptar costo = None por defecto
    def __init__(self, origen: int, destino: int, capacidad: float, costo: float = None, flujo: float = 0.0):
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.costo = costo  # Puede ser un float o None si no se especifica
        self.flujo = flujo

    def es_saturada(self) -> bool:
        """Una arista está saturada si el flujo alcanza o supera su capacidad."""
        return self.flujo >= self.capacidad


class RedFlujo:
    def __init__(self, aristas: list[Arista]):
        self.aristas = aristas
        self.nodos = set()
        for a in aristas:
            self.nodos.add(a.origen)
            self.nodos.add(a.destino)
            
    def __repr__(self) -> str:
        return f"RedFlujo(nodos={len(self.nodos)}, aristas={len(self.aristas)})"

    def __str__(self) -> str:
        linea_separadora = "-" * 53
        encabezado = f"| {'Origen':<6} | {'Destino':<7} | {'Flujo/Capacidad':<15} | {'Costo':<5} |"
        tabla = [linea_separadora, encabezado, linea_separadora]
        
        for a in self.aristas:
            flujo_cap = f"{a.flujo}/{a.capacidad}"
            costo_str = str(a.costo) if a.costo is not None else "Global"
            fila = f"| {a.origen:<6} | {a.destino:<7} | {flujo_cap:<15} | {costo_str:<5} |"
            tabla.append(fila)
            
        tabla.append(linea_separadora)
        return "\n".join(tabla)

    def generar_matriz_adyacencia(self) -> list[list[float]]:
        num_nodos = max(self.nodos) + 1 if self.nodos else 0
        matriz = [[0.0 for _ in range(num_nodos)] for _ in range(num_nodos)]
        for a in self.aristas:
            matriz[a.origen][a.destino] = a.flujo
        return matriz

    def resumen_red(self) -> str:
        flujo_total = sum(a.flujo for a in self.aristas if a.origen == min(self.nodos))
        # Nota: La clase base usa el costo directo, si hay None podría fallar. 
        # RedFlujoGlobal resolverá esto con su propio método de cálculo.
        costo_total = sum(a.flujo * (a.costo if a.costo is not None else 0) for a in self.aristas)
        aristas_saturadas = sum(1 for a in self.aristas if a.es_saturada())
        
        resumen = (
            f"=== RESUMEN DE LA RED ===\n"
            f"Flujo Total Enviado (Salida): {flujo_total}\n"
            f"Aristas Saturadas:            {aristas_saturadas}/{len(self.aristas)}"
        )
        return resumen

# Clase nueva: RedFlujoGlobal (Hereda de RedFlujo)

class RedFlujoGlobal(RedFlujo):
    # 1. Atributos de clase globales
    costo_por_unidad_flujo = 1.0
    metodo_resolucion = 'simplex'
    _METODOS_VALIDOS = {'simplex', 'interior', 'heuristica'}

    # 2. Método de clase para configurar y validar el método de resolución
    @classmethod
    def configurar_metodo(cls, nuevo_metodo: str):
        """Valida que el método pertenezca a las opciones permitidas."""
        if nuevo_metodo not in cls._METODOS_VALIDOS:
            raise ValueError(f"Método '{nuevo_metodo}' no válido. Opciones: {cls._METODOS_VALIDOS}")
        cls.metodo_resolucion = nuevo_metodo

    # 3. Método de instancia para calcular el costo total usando el respaldo global
    def calcular_costo_total_global(self) -> float:
        """
        Calcula el costo total de la red. Si una arista no tiene costo específico (None),
        utiliza el atributo de clase costo_por_unidad_flujo.
        """
        costo_total = 0.0
        for a in self.aristas:
            # Si a.costo es None, usa el costo_por_unidad_flujo de la clase
            costo_arista = a.costo if a.costo is not None else self.costo_por_unidad_flujo
            costo_total += a.flujo * costo_arista
        return costo_total

    # 4. Constructor alternativo desde un diccionario
    @classmethod
    def desde_diccionario(cls, datos: dict) -> 'RedFlujoGlobal':
        """
        Crea una instancia a partir de un diccionario estructurado.
        Ejemplo de formato:
        datos = {
            "aristas": [
                {"origen": 0, "destino": 1, "capacidad": 10, "flujo": 5}, # sin costo
                {"origen": 1, "destino": 2, "capacidad": 5, "costo": 3.5, "flujo": 2}
            ]
        }
        """
        lista_aristas = []
        for arista_dict in datos.get("aristas", []):
            # Usamos .get('costo', None) para que si no existe la clave 'costo', pase None
            arista = Arista(
                origen=arista_dict["origen"],
                destino=arista_dict["destino"],
                capacidad=arista_dict["capacidad"],
                costo=arista_dict.get("costo", None),
                flujo=arista_dict.get("flujo", 0.0)
            )
            lista_aristas.append(arista)
        
        # Retornamos la nueva instancia de la clase llamando al constructor principal mediante cls
        return cls(lista_aristas)


# --- Bloque de Prueba para comprobar RedFlujoGlobal ---
if __name__ == "__main__":
    print("=== Probando RedFlujoGlobal ===")
    
    # 1. Definir datos en un diccionario (algunas aristas tienen costo, otras no)
    datos_red = {
        "aristas": [
            {"origen": 0, "destino": 1, "capacidad": 10, "costo": 3.0, "flujo": 5}, # Costo específico = 3.0
            {"origen": 0, "destino": 2, "capacidad": 15, "flujo": 10},             # Sin costo (usará el global)
            {"origen": 1, "destino": 2, "capacidad": 5, "costo": 2.0, "flujo": 2}  # Costo específico = 2.0
        ]
    }
    
    # 2. Probar constructor alternativo desde_diccionario
    red_global = RedFlujoGlobal.desde_diccionario(datos_red)
    print("\nRed cargada desde diccionario:")
    print(red_global)
    
    # 3. Calcular costo con el costo_por_unidad_flujo inicial (1.0)
    # Costo esperado: (5 * 3.0) + (10 * 1.0) + (2 * 2.0) = 15 + 10 + 4 = 29.0
    print(f"Costo total (Costo global por defecto = {RedFlujoGlobal.costo_por_unidad_flujo}):")
    print(f"-> ${red_global.calcular_costo_total_global()}")
    
    # 4. Cambiar el costo global de la clase a 5.0
    RedFlujoGlobal.costo_por_unidad_flujo = 5.0
    # Nuevo costo esperado: (5 * 3.0) + (10 * 5.0) + (2 * 2.0) = 15 + 50 + 4 = 69.0
    print(f"\nCosto total tras cambiar costo global a {RedFlujoGlobal.costo_por_unidad_flujo}:")
    print(f"-> ${red_global.calcular_costo_total_global()}")
    
    # 5. Probar configuración del método de resolución
    print(f"\nMétodo de resolución actual: {RedFlujoGlobal.metodo_resolucion}")
    RedFlujoGlobal.configurar_metodo('interior')
    print(f"Nuevo método de resolución: {RedFlujoGlobal.metodo_resolucion}")
    
    # Intentar un método inválido para comprobar la validación
    try:
        print("\nIntentando configurar un método inválido...")
        RedFlujoGlobal.configurar_metodo('algoritmo_genetico')
    except ValueError as e:
        print(f"Error capturado exitosamente: {e}")
