"""Ejercicio 28: Sistema de Simulación de Colas en Composición

Crea un sistema de simulación de colas compuesto por:
- Clase Cliente con atributos: id, tiempo_llegada, tiempo_servicio
- Clase Servidor con atributos: id, ocupado, cliente_actual, tiempo_restante
- Clase SimulacionCola que contenga:
- Lista de Servidor (composición)
- Cola de Cliente (agregación)
- Métodos: llegada_cliente(), atender_siguiente(), avanzar_tiempo()
- Método estadisticas() que muestre: clientes atendidos, tiempo promedio, uso de servidores
"""

from collections import deque

class Cliente:
    def __init__(self, id_cliente, tiempo_llegada, tiempo_servicio):
        """
        Atributos:
        - id: Identificador único del cliente.
        - tiempo_llegada: Minuto/segundo en el que entra a la cola.
        - tiempo_servicio: Duración total requerida para ser atendido.
        """
        self.id = id_cliente
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_servicio = tiempo_servicio
        self.tiempo_salida = None  # Se calculará al terminar su servicio


class Servidor:
    def __init__(self, id_servidor):
        """
        Atributos:
        - id: Identificador único del servidor.
        - ocupado: Estado del servidor (True/False).
        - cliente_actual: Objeto Cliente al que está atendiendo.
        - tiempo_restante: Cuánto le falta para terminar el servicio actual.
        - tiempo_total_activo: Contador acumulativo para medir el uso/eficiencia.
        """
        self.id = id_servidor
        self.ocupado = False
        self.cliente_actual = None
        self.tiempo_restante = 0
        self.tiempo_total_activo = 0


class SimulacionCola:
    def __init__(self, num_servidores):
        # 1. Composición: La simulación crea y es dueña de los servidores
        self.servidores = [Servidor(i + 1) for i in range(num_servidores)]
        
        # 2. Agregación: Los clientes se añaden dinámicamente a la cola
        self.cola_clientes = deque()
        
        # Atributos de control y estadísticas
        self.tiempo_actual = 0
        self.historico_atendidos = []

    def llegada_cliente(self, cliente):
        """Agrega un cliente a la cola del sistema (Agregación)."""
        if isinstance(cliente, Cliente):
            self.cola_clientes.append(cliente)
            print(f"[Tiempo {self.tiempo_actual}] Cliente {cliente.id} ha llegado a la cola (Servicio requerido: {cliente.tiempo_servicio}).")
        else:
            print("Error: El objeto debe ser una instancia de Cliente.")

    def atender_siguiente(self):
        """Asigna clientes en espera a los servidores que estén libres."""
        for servidor in self.servidores:
            # Si el servidor está libre y hay clientes esperando en la cola
            if not servidor.ocupado and self.cola_clientes:
                cliente = self.cola_clientes.popleft()
                servidor.cliente_actual = cliente
                servidor.ocupado = True
                servidor.tiempo_restante = cliente.tiempo_servicio
                print(f"[Tiempo {self.tiempo_actual}] Servidor {servidor.id} comienza a atender al Cliente {cliente.id}.")

    def avanzar_tiempo(self, pasos=1):
        """Avanza el reloj de la simulación y procesa el trabajo de los servidores."""
        for _ in range(pasos):
            self.tiempo_actual += 1
            
            for servidor in self.servidores:
                if servidor.ocupado:
                    servidor.tiempo_restante -= 1
                    servidor.tiempo_total_activo += 1
                    
                    # Si el servidor termina con el cliente en este paso de tiempo
                    if servidor.tiempo_restante == 0:
                        cliente = servidor.cliente_actual
                        cliente.tiempo_salida = self.tiempo_actual
                        self.historico_atendidos.append(cliente)
                        
                        print(f"[Tiempo {self.tiempo_actual}] Servidor {servidor.id} terminó de atender al Cliente {cliente.id}.")
                        
                        # Liberar servidor
                        servidor.ocupado = False
                        servidor.cliente_actual = None
            
            # Intentar reasignar nuevos clientes de la cola tras liberar servidores
            self.atender_siguiente()

    def estadisticas(self):
        """Calcula y muestra métricas clave del rendimiento del sistema."""
        print(f"\n ESTADÍSTICAS (Tiempo total simulado: {self.tiempo_actual}) ")
        
        # 1. Clientes atendidos
        total_atendidos = len(self.historico_atendidos)
        print(f"Clientes totalmente atendidos: {total_atendidos}")
        
        # 2. Tiempo promedio en el sistema (Espera + Servicio)
        if total_atendidos > 0:
            tiempos_sistema = [c.tiempo_salida - c.tiempo_llegada for c in self.historico_atendidos]
            promedio = sum(tiempos_sistema) / total_atendidos
            print(f"Tiempo promedio de los clientes en el sistema: {promedio:.2f} unidades de tiempo")
        else:
            print("Tiempo promedio en el sistema: N/A (Ningún cliente finalizado)")
            
        # 3. Uso de servidores
        print("Uso/Ocupación de los servidores:")
        for s in self.servidores:
            porcentaje_uso = (s.tiempo_total_activo / self.tiempo_actual) * 100 if self.tiempo_actual > 0 else 0
            print(f"  - Servidor {s.id}: {porcentaje_uso:.1f}% de ocupación ({s.tiempo_total_activo} unidades activo)")
            
        # Clientes que se quedaron esperando en la cola al finalizar
        print(f"Clientes remanentes en cola: {len(self.cola_clientes)}")


# 1. Inicializamos la simulación con 2 servidores disponibles (Composición)
sim = SimulacionCola(num_servidores=2)

print("--- INICIANDO SIMULACIÓN ---")

# Minuto 0: Llegan los dos primeros clientes
c1 = Cliente(id_cliente="C1", tiempo_llegada=0, tiempo_servicio=3)
c2 = Cliente(id_cliente="C2", tiempo_llegada=0, tiempo_servicio=5)
sim.llegada_cliente(c1)
sim.llegada_cliente(c2)

# Asignamos los clientes iniciales a los servidores libres
sim.atender_siguiente()

# Avanzamos el tiempo 2 unidades (Minutos 1 y 2)
sim.avanzar_tiempo(pasos=2)

# Minuto 2: Llega un tercer cliente con alta carga de trabajo
c3 = Cliente(id_cliente="C3", tiempo_llegada=2, tiempo_servicio=4)
sim.llegada_cliente(c3)

# El sistema intentará meter a C3 si hay espacio (no lo habrá porque C1 y C2 siguen adentro)
sim.atender_siguiente()

# Avanzamos el tiempo 5 unidades más para vaciar el sistema
sim.avanzar_tiempo(pasos=5)

# 2. Desplegamos los resultados finales
sim.estadisticas()
