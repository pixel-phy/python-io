"""
Ejercicio 32: Modelo de Colas Básico
Crea una clase Servidor con atributos nombre, tasa_servicio (clientes por hora) y clientes_atendidos. 
Implementa un método atender() que incremente los clientes atendidos.Luego, crea una clase 
ServidorPrioritario que herede de Servidor. Debe tener un atributo adicional nivel_prioridad (1-5)
y sobrescribir el método __init__ usando super() para inicializar todos los atributos.
    """

class Servidor:
    def __init__(self, nombre: str, tasa_servicio: float):
        self.nombre = nombre
        self.tasa_servicio = tasa_servicio  # Clientes por hora
        self.clientes_atendidos = 0         # Inicia en cero por defecto

    def atender(self):
        """Incrementa en 1 el contador de clientes atendidos."""
        self.clientes_atendidos += 1
        print(f"[{self.nombre}] Ha atendido a un cliente. Total: {self.clientes_atendidos}")

class ServidorPrioritario(Servidor):
    def __init__(self, nombre: str, tasa_servicio: float, nivel_prioridad: int):
        # Usamos super() para inicializar los atributos de la clase padre (Servidor)
        super().__init__(nombre, tasa_servicio)

        # Validamos que el nivel de prioridad esté entre 1 y 5
        if 1 <= nivel_prioridad <= 5:
            self.nivel_prioridad = nivel_prioridad
        else:
            raise ValueError("El nivel de prioridad debe estar entre 1 y 5.")

# Prueba:

# Creación de un servidor normal
servidor_estandar = Servidor("Caja 01", 15.5)
servidor_estandar.atender()
servidor_estandar.atender()

print("---")

# Creación de un servidor prioritario
servidor_vip = ServidorPrioritario("Caja VIP", 20.0, nivel_prioridad=5)
servidor_vip.atender()
print(f"Servidor: {servidor_vip.nombre} | Prioridad: {servidor_vip.nivel_prioridad}")
