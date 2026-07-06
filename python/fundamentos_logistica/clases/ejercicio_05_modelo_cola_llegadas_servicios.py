"""Ejercicio 05: Modelo de Cola con llegadas y Servicios

Crear una clase SistemaCola que modele un sistema de colas M/M/1 simplificado:

- Atributos: tasa_llegada (lambda), tasa_servicio (mu), clientes_sistema (int),
  clientes_espera (int), estado (str: 'vacio', 'ocupado')

- Método: llegada_cliente(): incrementa clientes_sistema y si hay espera, no reduce 
  clientes_espera (solo en el próximo servicio).

- Método: factor_utilizacion(): calcula lambda/mu.

"""

class SistemaCola:
    def __init__(self, tasa_llegada: float, tasa_servicio: float):
        """
        Inicializa un sistema de cola M/M/1 simplificado.
        """
        if tasa_llegada < 0 or tasa_servicio <= 0:
            raise ValueError("Las tasas deben ser positivas y mu no puede ser 0.")
            
        self.tasa_llegada = float(tasa_llegada)  # Lambda
        self.tasa_servicio = float(tasa_servicio)  # Mu
        self.clientes_sistema = 0
        self.clientes_espera = 0
        self.estado = 'vacio'  # Puede ser 'vacio' u 'ocupado'

    def factor_utilizacion(self) -> float:
        """
        Calcula el factor de utilización del sistema (rho = lambda / mu).
        """
        return self.tasa_llegada / self.tasa_servicio

    def llegada_cliente(self):
        """
        Procesa la llegada de un nuevo cliente al sistema.
        """
        self.clientes_sistema += 1
        
        if self.estado == 'ocupado':
            # Si el servidor está ocupado, el cliente se queda esperando en la cola
            self.clientes_espera += 1
        else:
            # Si estaba vacío, el cliente pasa directo a ser atendido
            self.estado = 'ocupado'

    def servicio_completado(self):
        """
        Procesa la salida de un cliente tras completar su servicio.
        """
        if self.clientes_sistema == 0:
            print("El sistema ya está vacío, no hay servicios que completar.")
            return

        # Un cliente sale definitivamente del sistema
        self.clientes_sistema -= 1
        
        if self.clientes_espera > 0:
            # Si había gente esperando, el primero de la cola pasa al servidor.
            # Por lo tanto, la cola se reduce en 1.
            self.clientes_espera -= 1
            self.estado = 'ocupado'
        else:
            # Si no queda nadie ni en cola ni en el servidor
            self.estado = 'vacio'

    def __repr__(self):
        return (f"SistemaCola(Estado: '{self.estado}', "
                f"En Sistema: {self.clientes_sistema}, "
                f"En Espera: {self.clientes_espera}, "
                f"Utilización: {self.factor_utilizacion():.2f})")


# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Lambda = 2 clientes/hora, Mu = 4 clientes/hora (Utilización = 0.5)
    cola = SistemaCola(tasa_llegada=2.0, tasa_servicio=4.0)
    print("Estado inicial:", cola)
    
    # 1. Llega el primer cliente
    cola.llegada_cliente()
    print("\nLlega Cliente 1:", cola) # Debería estar ocupado, 1 en sistema, 0 en espera
    
    # 2. Llega un segundo cliente mientras el primero es atendido
    cola.llegada_cliente()
    print("Llega Cliente 2:", cola)
    
    # 3. Llega un tercer cliente
    cola.llegada_cliente()
    print("Llega Cliente 3:", cola)

    print("\n" + "-"*40 + "\n")

    # 4. Se completa el servicio del Cliente 1
    cola.servicio_completado()
    print("Servicio 1 listo:", cola)

    # 5. Se completa el servicio del Cliente 2
    cola.servicio_completado()
    print("Servicio 2 listo:", cola)

    # 6. Se completa el servicio del Cliente 3
    cola.servicio_completado()
    print("Servicio 3 listo:", cola)
