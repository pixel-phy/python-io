"""Ejercicio 14: Parámetros Globales para Sistema de Colas

Modifica la clase de SistemaCola del día 1 para incluir:

- Atributo de clase: tiempo_espera_maximo = 10.0 (minutos, compartido por todos los sistemas)

- Método de clase: modificar_tiempo_espera_maximo(nuevo_tiempo) que valide que sea positivo

- Método de instancia: verificar_congestion() que retorne True si el tiempo estimado de espera 
  (clientes_espera * tiempo_servicio_promedio) supera el máximo global.

"""
class SistemaCola:
    # 1. Atributo de clase compartido por todas las instancias
    tiempo_espera_maximo = 10.0  # en minutos

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

    # 2. Método de clase para modificar el parámetro global
    @classmethod
    def modificar_tiempo_espera_maximo(cls, nuevo_tiempo: float):
        """
        Modifica el tiempo de espera máximo global tras validar que sea positivo.
        """
        if nuevo_tiempo <= 0:
            raise ValueError("El tiempo de espera máximo debe ser un valor positivo.")
        cls.tiempo_espera_maximo = float(nuevo_tiempo)

    # 3. Método de instancia para verificar si hay congestión
    def verificar_congestion(self) -> bool:
        """
        Retorna True si el tiempo estimado de espera supera el máximo global.
        Tiempo estimado = clientes en espera * tiempo de servicio promedio.
        Nota: tiempo_servicio_promedio = 1 / tasa_servicio
        """
        tiempo_servicio_promedio = 1.0 / self.tasa_servicio
        tiempo_estimado_espera = self.clientes_espera * tiempo_servicio_promedio
        
        return tiempo_estimado_espera > self.tiempo_espera_maximo

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
            self.clientes_espera += 1
        else:
            self.estado = 'ocupado'

    def servicio_completado(self):
        """
        Procesa la salida de un cliente tras completar su servicio.
        """
        if self.clientes_sistema == 0:
            print("El sistema ya está vacío, no hay servicios que completar.")
            return

        self.clientes_sistema -= 1
        
        if self.clientes_espera > 0:
            self.clientes_espera -= 1
            self.estado = 'ocupado'
        else:
            self.estado = 'vacio'

    def __repr__(self):
        return (f"SistemaCola(Estado: '{self.estado}', "
                f"En Sistema: {self.clientes_sistema}, "
                f"En Espera: {self.clientes_espera}, "
                f"Utilización: {self.factor_utilizacion():.2f})")


# Prueba
if __name__ == "__main__":
    # Supongamos que las tasas están dadas en clientes por MINUTO para que coincida con las unidades.
    # Mu = 0.2 clientes/minuto (significa que toma 5 minutos atender a cada cliente)
    cola = SistemaCola(tasa_llegada=0.1, tasa_servicio=0.2)
    
    print(f"Tiempo máximo global inicial: {SistemaCola.tiempo_espera_maximo} minutos")
    
    # Añadimos clientes para generar cola
    cola.llegada_cliente()
    cola.llegada_cliente()
    cola.llegada_cliente()
    
    print("\n--- Con 2 clientes en espera ---")
    print(cola)
    print(f"¿Está congestionado? {cola.verificar_congestion()}")
    
    cola.llegada_cliente()
    print("\n--- Con 3 clientes en espera ---")
    print(cola)
    print(f"¿Está congestionado? {cola.verificar_congestion()}")
    
    # Modificamos el parámetro global usando el método de clase
    print("\nModificando el tiempo de espera máximo global a 20.0 minutos...")
    SistemaCola.modificar_tiempo_espera_maximo(20.0)
    
    print(f"¿Está congestionado ahora con el nuevo límite? {cola.verificar_congestion()}")
