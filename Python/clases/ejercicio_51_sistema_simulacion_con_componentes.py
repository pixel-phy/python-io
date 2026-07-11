"""Ejercicio 51: Sistema de Simulación de Componentes

Diseña un sistema de simulación de eventos discretos usando composición:

1. Clase GeneradorLlegadas: Componente que genera llegadas

    - Método: proxima_llegada() (retorna el tiempo hasta la próxima llegada)

2. Clase Servidor: Componente que procesa clientes

    - Métodos: atender(cliente), esta_ocupado(), tiempo_servicio()

3. Clase PoliticaCola: Componente que decide qué cliente atender

    - Métodos: seleccionar(cliente), agregar(cliente)

4. Clase Simulador: Compone los componentes anteriores

    - Método: ejecutar(tiempo_simulacion)

    """

import random

# --- 1. COMPONENTE: GENERADOR DE LLEGADAS ---
class GeneradorLlegadas:
    """Genera los tiempos de interarribo de los clientes (frecuencia)."""
    def __init__(self, tasa_llegadas=2.0):
        # Usamos una distribución exponencial, común en teoría de colas (Proceso de Poisson)
        self.tasa_llegadas = tasa_llegadas

    def proxima_llegada(self):
        """Retorna el tiempo que pasará hasta que llegue el próximo cliente."""
        return random.expovariate(1.0 / self.tasa_llegadas)


# --- 2. COMPONENTE: SERVIDOR ---
class Servidor:
    """Representa al agente, cajero o máquina que atiende a los clientes."""
    def __init__(self, tiempo_promedio_servicio=3.0):
        self.tiempo_promedio_servicio = tiempo_promedio_servicio
        self.cliente_actual = None
        self.tiempo_liberacion = 0.0  # Momento exacto en el que terminará de atender

    def atender(self, cliente, tiempo_actual):
        """Asigna un cliente al servidor y calcula cuándo terminará."""
        self.cliente_actual = cliente
        duracion = self.tiempo_servicio()
        self.tiempo_liberacion = tiempo_actual + duracion
        return duracion

    def esta_ocupado(self, tiempo_actual):
        """Verifica si el servidor sigue ocupado en el tiempo actual."""
        if self.cliente_actual and tiempo_actual >= self.tiempo_liberacion:
            self.cliente_actual = None  # Se liberó
        return self.cliente_actual is not None

    def tiempo_servicio(self):
        """Calcula de forma aleatoria cuánto tardará la atención en sí."""
        return random.exponential(self.tiempo_promedio_servicio) if hasattr(random, 'exponential') else random.expovariate(1.0 / self.tiempo_promedio_servicio)


# --- 3. COMPONENTE: POLÍTICA DE COLA ---
class PoliticaCola:
    """Maneja la lista de espera de los clientes."""
    def __init__(self, nombre_politica="FIFO (First In, First Out)"):
        self.cola = []
        self._nombre = nombre_politica

    def agregar(self, cliente):
        """Añade un cliente a la espera."""
        self.cola.append(cliente)

    def seleccionar(self):
        """Decide qué cliente sale de la cola según la política."""
        if not self.cola:
            return None
        # Por defecto implementamos FIFO (el primero de la lista)
        return self.cola.pop(0)

    @property
    def tamanio(self):
        return len(self.cola)


# --- 4. CLASE PRINCIPAL: SIMULADOR (EL COORDINADOR) ---
class Simulador:
    """Une todos los componentes mediante composición y ejecuta el bucle de eventos."""
    def __init__(self, generador: GeneradorLlegadas, servidor: Servidor, politica_cola: PoliticaCola):
        self.generador = generador
        self.servidor = servidor
        self.politica_cola = politica_cola
        
        # Estado del sistema
        self.tiempo_actual = 0.0
        self.historial_atendidos = 0

    def ejecutar(self, tiempo_max_simulacion):
        """Ejecuta la simulación saltando de evento en evento."""
        print(f"=== Iniciando Simulación de Eventos Discretos ===")
        print(f"Política de atención: {self.politica_cola._nombre}\n")

        # Programamos la primerísima llegada
        tiempo_proxima_llegada = self.generador.proxima_llegada()
        id_cliente = 1

        while self.tiempo_actual < tiempo_max_simulacion:
            # Determinamos cuál es el próximo evento en el tiempo:
            # ¿Llega un cliente o se libera el servidor?
            
            tiempo_proximo_evento = tiempo_proxima_llegada
            es_llegada = True

            # Si el servidor está ocupado y termina antes de la próxima llegada
            if self.servidor.esta_ocupado(self.tiempo_actual) and self.servidor.tiempo_liberacion < tiempo_proximo_evento:
                tiempo_proximo_evento = self.servidor.tiempo_liberacion
                es_llegada = False

            # Avanzamos el reloj del sistema directamente al evento
            self.tiempo_actual = tiempo_proximo_evento
            
            if self.tiempo_actual > tiempo_max_simulacion:
                break

            # --- MANEJO DEL EVENTO ---
            if es_llegada:
                # Evento 1: Llega un cliente
                cliente = f"Cliente-{id_cliente}"
                print(f"[{self.tiempo_actual:.2f}] {cliente} entra a la instalación.")
                
                self.politica_cola.agregar(cliente)
                id_cliente += 1
                
                # Programar la siguiente llegada
                tiempo_proxima_llegada = self.tiempo_actual + self.generador.proxima_llegada()
            else:
                # Evento 2: El servidor termina de atender
                print(f"[{self.tiempo_actual:.2f}] El servidor termina de atender a {self.servidor.cliente_actual}.")
                self.servidor.esta_ocupado(self.tiempo_actual) # Forzar liberación del estado
                self.historial_atendidos += 1

            # --- ACCIÓN POST-EVENTO: ¿Podemos meter a alguien al servidor? ---
            if not self.servidor.esta_ocupado(self.tiempo_actual) and self.politica_cola.tamanio > 0:
                siguiente_cliente = self.politica_cola.seleccionar()
                duracion = self.servidor.atender(siguiente_cliente, self.tiempo_actual)
                print(f"[{self.tiempo_actual:.2f}] El servidor comienza a atender a {siguiente_cliente} (Duración: {duracion:.2f}). En cola quedan: {self.politica_cola.tamanio}")

        print(f"\n=== Simulación Terminada ===")
        print(f"Tiempo total simulado: {self.tiempo_actual:.2f} unidades de tiempo.")
        print(f"Clientes totalmente atendidos: {self.historial_atendidos}")
        print(f"Clientes que se quedaron esperando en cola: {self.politica_cola.tamanio}")

# Fijamos una semilla para que los números aleatorios sean siempre los mismos en esta prueba
random.seed(42)

# Configuración de componentes:
# Llega un cliente cada 2 minutos en promedio, pero el servidor tarda 3 minutos en atender (¡Se va a armar cuello de botella!)
generador = GeneradorLlegadas(tasa_llegadas=2.0)
cajero = Servidor(tiempo_promedio_servicio=3.0)
cola_prioridad = PoliticaCola()

# Inyectamos los componentes al simulador
simulador_banco = Simulador(generador, cajero, cola_prioridad)

# Ejecutamos la simulación por 20 unidades de tiempo (minutos)
simulador_banco.ejecutar(tiempo_max_simulacion=20.0)
