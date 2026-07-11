"""Ejercicio 04: Arista Ponderada con Capacidad

Crear una clase Arista para una red de flujo con capacidad y costo:

- Atributos: origen(str), destino(str), capacidad (float), costo_unitario (float),
  flujo_actual (float).

- Método: flujo_disponible() que retorne la capacidad restante.

- Método: enviar_flujo(cantidad) que aumente el flujo_actual si no excede la capacidad.

- Método: costo_total() que calcule el costo del flujo actual.

- Validación: No permitir capacidades o costos negativos.

"""

class Arista:
    def __init__(self, origen: str, destino: str, capacidad: float, costo_unitario: float):
        """
        Inicializa una arista orientada para una red de flujo.
        """
        # Validaciones de valores no negativos
        if capacidad < 0:
            raise ValueError("La capacidad de la arista no puede ser negativa.")
        if costo_unitario < 0:
            raise ValueError("El costo unitario de la arista no puede ser negativo.")
            
        self.origen = origen
        self.destino = destino
        self.capacidad = float(capacidad)
        self.costo_unitario = float(costo_unitario)
        self.flujo_actual = 0.0  # El flujo arranca en cero por defecto

    def flujo_disponible(self) -> float:
        """
        Retorna la capacidad residual (restante) de la arista.
        """
        return self.capacidad - self.flujo_actual

    def enviar_flujo(self, cantidad: float):
        """
        Aumenta el flujo actual si hay suficiente capacidad disponible.
        """
        if cantidad < 0:
            raise ValueError("No se puede enviar una cantidad negativa de flujo.")
            
        if cantidad > self.flujo_disponible():
            raise ValueError(
                f"Capacidad excedida. Intentas enviar {cantidad}, "
                f"pero solo quedan {self.flujo_disponible()} unidades disponibles."
            )
            
        self.flujo_actual += float(cantidad)

    def costo_total(self) -> float:
        """
        Calcula el costo total del flujo que pasa actualmente por la arista.
        """
        return self.flujo_actual * self.costo_unitario

    def __repr__(self):
        """
        Representación en texto para facilitar la depuración.
        """
        return (f"Arista({self.origen} -> {self.destino}, "
                f"Flujo: {self.flujo_actual}/{self.capacidad}, "
                f"Costo Unitario: {self.costo_unitario})")


# Prueba:
if __name__ == "__main__":
    try:
        # 1. Crear una arista desde el nodo 'A' al nodo 'B'
        # Capacidad = 10.0, Costo Unitario = 2.5
        arista = Arista(origen="A", destino="B", capacidad=10.0, costo_unitario=2.5)
        print("Estado inicial:", arista)
        print(f"Flujo disponible inicial: {arista.flujo_disponible()}")

        print("\n" + "-"*40 + "\n")

        # 2. Enviar un flujo válido (4 unidades)
        arista.enviar_flujo(4.0)
        print("Después de enviar 4 unidades:", arista)
        print(f"Flujo disponible restante: {arista.flujo_disponible()}")
        print(f"Costo total acumulado: ${arista.costo_total()}")

        print("\n" + "-"*40 + "\n")

        # 3. Intentar enviar más flujo del permitido (quedan 6, intentamos enviar 7)
        print("Intentando enviar 7 unidades de flujo...")
        arista.enviar_flujo(7.0)

    except ValueError as e:
        print(f"Error detectado: {e}")
