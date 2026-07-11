"""Ejercicio 29: Gestor de Problemas de Asignación con Composición

Crea un sistema para problemas de asignación que incluya:
- Clase Tarea con atributos: id, duracion, prioridad
- Clase Maquina con atributos: id, eficiencia, disponible
- Clase Asignacion que relacione una tarea con una máquina (fecha, costo)
- Clase ProblemaAsignacion que contenga:
- Lista de Tarea (agregación)
- Lista de Maquina (agregación)
- Lista de Asignacion (composición)
- Método asignar(tarea_id, maquina_id, costo) con validaciones
- Método costo_total() que sume todos los costos
- Método es_factible() que verifique todas las tareas asignadas
"""

from datetime import datetime

class Tarea:
    def __init__(self, id_tarea, duracion, prioridad):
        """
        Atributos:
        - id: Identificador único (ej. 'T1')
        - duracion: Tiempo requerido (horas, minutos)
        - prioridad: Nivel de importancia (ej. 'Alta', 'Media', 'Baja')
        """
        self.id = id_tarea
        self.duracion = duracion
        self.prioridad = prioridad

    def __str__(self):
        return f"Tarea {self.id} [Duración: {self.duracion}, Prioridad: {self.prioridad}]"


class Maquina:
    def __init__(self, id_maquina, eficiencia, disponible=True):
        """
        Atributos:
        - id: Identificador único (ej. 'M1')
        - eficiencia: Factor multiplicador o rendimiento (ej. 0.95, 1.2)
        - disponible: Estado operativo de la máquina (True/False)
        """
        self.id = id_maquina
        self.eficiencia = eficiencia
        self.disponible = disponible

    def __str__(self):
        estado = "Disponible" if self.disponible else "No Disponible"
        return f"Máquina {self.id} [Eficiencia: {self.eficiencia}, Estado: {estado}]"


class Asignacion:
    def __init__(self, tarea, maquina, costo):
        """
        Clase intermedia que conecta una Tarea con una Máquina.
        Su ciclo de vida depende enteramente del Gestor/Problema.
        """
        self.tarea = tarea
        self.maquina = maquina
        self.costo = costo
        self.fecha_asignacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f" -> Tarea {self.tarea.id} asignada a Máquina {self.maquina.id} | Costo: ${self.costo:.2f} | Fecha: {self.fecha_asignacion}"


class ProblemaAsignacion:
    def __init__(self, nombre="Problema de Asignación"):
        self.nombre = nombre
        self.tareas = []       # Agregación
        self.maquinas = []     # Agregación
        self.asignaciones = [] # Composición

    # --- Métodos para registrar los recursos base ---
    def agregar_tarea(self, tarea):
        if isinstance(tarea, Tarea):
            self.tareas.append(tarea)
        else:
            print("Error: Objeto inválido para Tarea.")

    def agregar_maquina(self, maquina):
        if isinstance(maquina, Maquina):
            self.maquinas.append(maquina)
        else:
            print("Error: Objeto inválido para Máquina.")

    # --- Lógica de negocio y asignación ---
    def asignar(self, tarea_id, maquina_id, costo):
        """Crea una Asignación validando disponibilidad y existencia."""
        # 1. Buscar la tarea en el catálogo
        tarea = next((t for t in self.tareas if t.id == tarea_id), None)
        if not tarea:
            print(f"Error de asignación: La tarea '{tarea_id}' no existe en el problema.")
            return

        # 2. Buscar la máquina en el catálogo
        maquina = next((m for m in self.maquinas if m.id == maquina_id), None)
        if not maquina:
            print(f"Error de asignación: La máquina '{maquina_id}' no existe en el problema.")
            return

        # 3. Validar si la máquina está disponible operationalmente
        if not maquina.disponible:
            print(f"Error de asignación: La máquina '{maquina_id}' no está operativa.")
            return

        # 4. Validar si la tarea o la máquina ya han sido asignadas previamente
        for asig in self.asignaciones:
            if asig.tarea.id == tarea_id:
                print(f"Error de asignación: La tarea '{tarea_id}' ya fue asignada previamente.")
                return
            if asig.maquina.id == maquina_id:
                print(f"Error de asignación: La máquina '{maquina_id}' ya tiene una tarea asignada.")
                return

        # 5. Si pasa todas las validaciones, se crea la composición
        nueva_asignacion = Asignacion(tarea, maquina, costo)
        self.asignaciones.append(nueva_asignacion)
        print(f"Éxito: {tarea_id} ha sido asignada a {maquina_id}.")

    def costo_total(self):
        """Calcula la sumatoria de la función objetivo (costos)."""
        return sum(asig.costo for asig in self.asignaciones)

    def es_factible(self):
        """Verifica si el plan es factible (todas las tareas registradas deben tener una asignación)."""
        if not self.tareas:
            return False
            
        tareas_asignadas = [asig.tarea.id for asig in self.asignaciones]
        
        # Comprobar si cada ID de tarea está en la lista de asignadas
        for t in self.tareas:
            if t.id not in tareas_asignadas:
                return False
        return True

    def mostrar_resumen(self):
        """Imprime el estado completo del tablero de asignación."""
        print(f"\nRESUMEN: {self.nombre} ")
        print(f"Tareas registradas: {len(self.tareas)} | Máquinas registradas: {len(self.maquinas)}")
        print("\nAsignaciones actuales:")
        if self.asignaciones:
            for asig in self.asignaciones:
                print(asig)
        else:
            print("  (Ninguna asignación realizada)")
            
        print(f"\nCosto Total Acumulado: ${self.costo_total():.2f}")
        factibilidad = "SÍ" if self.es_factible() else "NO (Quedan tareas pendientes)"
        print(f"¿El modelo es factible?: {factibilidad}")

# 1. Instanciar el gestor del problema
problema = ProblemaAsignacion("Planificación de Planta de Inyección")

# 2. Crear y añadir recursos (Agregación)
t1 = Tarea("T1", duracion=4, prioridad="Alta")
t2 = Tarea("T2", duracion=2, prioridad="Media")
t3 = Tarea("T3", duracion=6, prioridad="Baja")

m1 = Maquina("M1", eficiencia=1.0)
m2 = Maquina("M2", eficiencia=1.2)
m3 = Maquina("M3", eficiencia=0.8, disponible=False) # Máquina en mantenimiento

problema.agregar_tarea(t1)
problema.agregar_tarea(t2)
problema.agregar_tarea(t3)

problema.agregar_maquina(m1)
problema.agregar_maquina(m2)
problema.agregar_maquina(m3)

print("\n--- INICIANDO PROCESO DE ASIGNACIÓN ---")

# Intento 1: Asignar a una máquina no disponible (M3) -> Debe fallar
problema.asignar(t1.id, m3.id, costo=150)

# Intento 2: Asignación válida
problema.asignar("T1", "M1", costo=200)

# Intento 3: Intentar reutilizar una máquina ya ocupada (M1) -> Debe fallar
problema.asignar("T2", "M1", costo=100)

# Intento 4: Asignación válida para T2
problema.asignar("T2", "M2", costo=120)

# Mostrar estado parcial (Veremos que NO es factible porque falta T3)
problema.mostrar_resumen()

# Cambiamos el estado de M3 a disponible para poder solucionar el problema
m3.disponible = True
print("-> Se ha reparado la Máquina M3. Volviendo a intentar...")

# Intento 5: Asignación final
problema.asignar("T3", "M3", costo=300)

# Mostrar estado final (Ahora DEBE ser factible)
problema.mostrar_resumen()
