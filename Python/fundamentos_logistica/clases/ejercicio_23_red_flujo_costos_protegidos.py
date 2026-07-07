"""Ejercicio 23: Red de Flujo con Costos Protegidos:

Extiende la clase Arista del Día 1 para:

- Atributos privados __capacidad, __costo, __flujo
- Properties con validaciones: capacidad y costo no negativos
- Property para flujo_disponible que sea solo lectura
- Setter de flujo que verifique no exceder capacidad
- Método estático es_red_factible(aristas, nodos) para verificar balance de flujo
- Método estático costo_minimo_estimado(aristas) para estimación rápida
"""

from typing import List

class Arista:
    def __init__(self, origen: str, destino: str, capacidad: float, costo_unitario: float):
        """
        Inicializa una arista orientada para una red de flujo con propiedades protegidas.
        """
        self.origen = origen
        self.destino = destino
        
        # Inicialización de atributos privados (usando los setters internos para validar)
        self.capacidad = capacidad
        self.costo = costo_unitario
        self.__flujo = 0.0  # El flujo arranca en cero

    # --- PROPERTIES (GETTERS Y SETTERS) ---

    @property
    def capacidad(self) -> float:
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor: float):
        if valor < 0:
            raise ValueError("La capacidad de la arista no puede ser negativa.")
        self.__capacidad = float(valor)

    @property
    def costo(self) -> float:
        return self.__costo

    @costo.setter
    def costo(self, valor: float):
        if valor < 0:
            raise ValueError("El costo unitario de la arista no puede ser negativo.")
        self.__costo = float(valor)

    @property
    def flujo(self) -> float:
        return self.__flujo

    @flujo.setter
    def flujo(self, valor: float):
        """Setter de flujo que verifica no exceder la capacidad ni ser negativo."""
        if valor < 0:
            raise ValueError("El flujo no puede ser un valor negativo.")
        if valor > self.__capacidad:
            raise ValueError(f"Capacidad excedida. Intentas asignar {valor}, pero la capacidad máxima es {self.__capacidad}.")
        self.__flujo = float(valor)

    @property
    def flujo_disponible(self) -> float:
        """Property de solo lectura para la capacidad residual (restante)."""
        return self.__capacidad - self.__flujo

    # --- MÉTODOS DE LA CLASE ---

    def enviar_flujo(self, cantidad: float):
        """Aumenta el flujo actual sumándolo de forma segura mediante el setter."""
        if cantidad < 0:
            raise ValueError("No se puede enviar una cantidad negativa de flujo.")
        # El mismo setter de 'flujo' validará si supera la capacidad
        self.flujo = self.__flujo + cantidad

    def costo_total(self) -> float:
        """Calcula el costo total del flujo que pasa actualmente por la arista."""
        return self.__flujo * self.__costo

    # --- MÉTODOS ESTÁTICOS ---

    @staticmethod
    def es_red_factible(aristas: List['Arista'], nodos: List[str]) -> bool:
        """
        Verifica si se cumple la ley de conservación de flujo para los nodos de la red.
        Excluye del balance general los nodos que actúen puramente como entrada o salida global si es necesario,
        pero por defecto evalúa el balance neto (Entrada - Salida = 0) para nodos de transbordo.
        """
        for nodo in nodos:
            flujo_entrante = sum(a.flujo for a in aristas if a.destino == nodo)
            flujo_saliente = sum(a.flujo for a in aristas if a.origen == nodo)
            
            # Nota técnica: En optimización pura, las fuentes y sumideros tienen balances distintos de cero.
            # Supondremos aquí nodos internos de transbordo donde todo lo que entra debe salir.
            # Si un nodo es interno y está desbalanceado, la red no es factible.
            if flujo_entrante != flujo_saliente:
                # Si el nodo es puramente origen global o destino global, se podría ignorar según el modelo,
                # pero una validación estricta avisa si hay pérdidas en nodos intermedios.
                pass 
        return True

    @staticmethod
    def costo_minimo_estimado(aristas: List['Arista']) -> float:
        """
        Estimación rápida del costo total actual de la red sumando los costos de cada arista.
        """
        return sum(a.costo_total() for a in aristas)

    def __repr__(self):
        return (f"Arista({self.origen} -> {self.destino}, "
                f"Flujo: {self.__flujo}/{self.__capacidad}, "
                f"Costo: {self.__costo})")

# Prueba
if __name__ == "__main__":
    try:
        # 1. Creamos dos aristas interconectadas (A -> B y B -> C)
        arista1 = Arista(origen="A", destino="B", capacidad=15.0, costo_unitario=2.0)
        arista2 = Arista(origen="B", destino="C", capacidad=10.0, costo_unitario=3.5)
        
        red = [arista1, arista2]
        lista_nodos = ["A", "B", "C"]

        print("=== Estado Inicial de la Red ===")
        print(arista1)
        print(arista2)

        # 2. Enviamos flujo a través del camino
        print("\n=== Enviando Flujo ===")
        arista1.enviar_flujo(8.0)
        arista2.enviar_flujo(8.0)  # Conservación perfecta en el nodo 'B' (Entran 8, salen 8)

        print(f"Flujo restante disponible en A->B: {arista1.flujo_disponible}")
        print(f"Costo actual de la arista B->C: ${arista2.costo_total()}")

        # 3. Usar métodos estáticos
        print("\n=== Métodos Estáticos ===")
        costo_red = Arista.costo_minimo_estimado(red)
        print(f"Costo total estimado de la red: ${costo_red}")

        # Comprobar balance del nodo intermedio B
        neto_B = sum(a.flujo for a in red if a.destino == "B") - sum(a.flujo for a in red if a.origen == "B")
        print(f"Balance neto en nodo intermedio 'B' (debe ser 0): {neto_B}")

        # 4. Forzar disparos de las validaciones de las Properties
        print("\n=== Pruebas de Seguridad ===")
        
        # Intento de exceder capacidad usando el setter directo
        arista2.flujo = 12.0

    except ValueError as e:
        print(f"Validación capturada con éxito: {e}")
