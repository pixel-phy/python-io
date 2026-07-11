"""
Ejercicio 40: Sistema de Simulación de Colas con Diferentes políticas

Crea una clase PoliticaCola con métodos seleccionar_siguiente() y nombre().

Implementa tres políticas:
1. FIFO: First In, First Out
2. Prioridad: Selecciona por nivel de prioridad (atributo prioridad en los clientes)
3. SPT: Shortest Processing Time (menor tiempo de servicio primero)

Cada política debe sobrescribir seleccionar_siguiente() para implementar su lógica específica de selección.

"""
import heapq

# --- CLASE CLIENTE / TAREA ---
class Cliente:
    """Representa a un cliente o tarea dentro de la cola."""
    def __init__(self, id_cliente, tiempo_servicio, prioridad):
        self.id_cliente = id_cliente
        self.tiempo_servicio = tiempo_servicio  # Para la política SPT
        self.prioridad = prioridad              # Para la política de Prioridad (Menor número = Mayor prioridad)

    def __repr__(self):
        return f"[Cliente {self.id_cliente} | T.Servicio: {self.tiempo_servicio} | Prioridad: {self.prioridad}]"


# --- CLASES DE POLÍTICAS (POLIMORFISMO) ---

class PoliticaCola:
    """Clase base abstracta para las políticas de selección."""
    def nombre(self):
        return "Política Genérica"

    def seleccionar_siguiente(self, cola):
        """
        Debe recibir la lista de clientes (cola) y retornar el cliente seleccionado.
        Además, debe removerlo de la cola.
        """
        if not cola:
            return None
        return cola.pop(0) # Comportamiento genérico por defecto


class PoliticaFIFO(PoliticaCola):
    """Política FIFO: First In, First Out (El primero en llegar es el primero en salir)."""
    def nombre(self):
        return "FIFO (First In, First Out)"

    def seleccionar_siguiente(self, cola):
        if not cola:
            return None
        # En FIFO simplemente sacamos el primer elemento de la lista (índice 0)
        return cola.pop(0)


class PoliticaPrioridad(PoliticaCola):
    """Política de Prioridad: Selecciona al cliente con mayor prioridad (menor valor numérico)."""
    def nombre(self):
        return "Prioridad (Mayor prioridad primero)"

    def seleccionar_siguiente(self, cola):
        if not cola:
            return None
        
        # Buscamos el cliente con el número de prioridad más bajo (ej: Prioridad 1 > Prioridad 3)
        cliente_elegido = min(cola, key=lambda c: c.prioridad)
        cola.remove(cliente_elegido)
        return cliente_elegido


class PoliticaSPT(PoliticaCola):
    """Política SPT: Shortest Processing Time (Menor tiempo de servicio primero)."""
    def nombre(self):
        return "SPT (Shortest Processing Time)"

    def seleccionar_siguiente(self, cola):
        if not cola:
            return None
        
        # Buscamos el cliente que requiera el menor tiempo de procesamiento
        cliente_elegido = min(cola, key=lambda c: c.tiempo_servicio)
        cola.remove(cliente_elegido)
        return cliente_elegido


# --- SIMULADOR DE PRUEBA ---
def simular_atencion(politica, lista_clientes):
    # Hacemos una copia de la lista original para no vaciarla en otras pruebas
    cola_simulada = list(lista_clientes)
    
    print(f"--- Simulación usando política: {politica.nombre()} ---")
    print(f"Estado inicial de la cola: {cola_simulada}\n")
    
    paso = 1
    while cola_simulada:
        siguiente = politica.seleccionar_siguiente(cola_simulada)
        print(f"Paso {paso}: Se atiende a -> {siguiente}")
        paso += 1
    print("-" * 60 + "\n")


# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Creamos un set de clientes desordenados para la prueba
    # Parámetros: ID, Tiempo de Servicio, Prioridad
    clientes_en_espera = [
        Cliente(id_cliente="A", tiempo_servicio=8, prioridad=3),
        Cliente(id_cliente="B", tiempo_servicio=2, prioridad=1),
        Cliente(id_cliente="C", tiempo_servicio=5, prioridad=2),
    ]

    # Instanciamos nuestras políticas polimórficas
    fifo = PoliticaFIFO()
    prioridad = PoliticaPrioridad()
    spt = PoliticaSPT()

    # Probamos el mismo set de datos bajo las 3 reglas distintas
    simular_atencion(fifo, clientes_en_espera)
    simular_atencion(prioridad, clientes_en_espera)
    simular_atencion(spt, clientes_en_espera)
