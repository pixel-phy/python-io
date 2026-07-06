"""Ejercicio 09: Representación de Estado de Cola

Extiende la clase SistemaCola con:

- __repr__: formato completo para depuración

- __str__: formato resumido mostrando el estado más relevante

- Crea un método indicador_rendimiento() que devuelva un emoji según el estado 
  (✅ si está vacío, ⚠️ si está ocupado con espera, 🔴 si está sobrecargado con más de 5 en espera)

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
            self.clientes_espera -= 1
            self.estado = 'ocupado'
        else:
            # Si no queda nadie ni en cola ni en el servidor
            self.estado = 'vacio'

    # --- NUEVOS MÉTODOS Y MODIFICACIONES ---

    def __repr__(self):
        """
        Formato completo y detallado para depuración técnica.
        """
        return (f"SistemaCola(tasa_llegada={self.tasa_llegada}, tasa_servicio={self.tasa_servicio}, "
                f"estado='{self.estado}', clientes_sistema={self.clientes_sistema}, "
                f"clientes_espera={self.clientes_espera}, utilizacion={self.factor_utilizacion():.2f})")

    def __str__(self):
        """
        Formato resumido mostrando el estado más relevante para el usuario.
        """
        return f"[{self.estado.upper()}] En sistema: {self.clientes_sistema} | En cola: {self.clientes_espera} {self.indicador_rendimiento()}"

    def indicador_rendimiento(self) -> str:
        """
        Devuelve un emoji según el estado de la cola de espera:
        - ✅ Si está vacío (cero en espera)
        - 🔴 Si está sobrecargado (más de 5 en espera)
        - ⚠️ Si está ocupado con espera (entre 1 y 5 en espera)
        """
        if self.clientes_espera == 0:
            return "✅"
        elif self.clientes_espera > 5:
            return "🔴"
        else:
            return "⚠️"


# --- Ejemplo de uso y pruebas del Ejercicio 2 ---
if __name__ == "__main__":
    # Creamos un sistema con Lambda = 5.0 y Mu = 2.0 (tiende a saturarse)
    cola = SistemaCola(tasa_llegada=5.0, tasa_servicio=2.0)
    
    print("--- PRUEBA DE REPRESENTACIONES INICIALES ---")
    print("Formato Técnico (__repr__):")
    print(repr(cola))
    print("\nFormato Amigable (__str__):")
    print(cola)
    print("-" * 50)

    print("\n--- SIMULANDO LLEGADAS PARA LLENAR LA COLA ---")
    # Forzamos la llegada de 8 clientes consecutivamente sin despachar a ninguno
    for i in range(1, 9):
        cola.llegada_cliente()
        print(f"Llegada #{i}: {cola}")
        
        # En la llegada 3 debería cambiar a ⚠️ (ya hay gente en cola)
        # En la llegada 7 debería cambiar a 🔴 (más de 5 en cola, exactamente 6)

    print("\n" + "-" * 50)
    print("--- VERIFICACIÓN FINAL DE DEPURACIÓN (CON COLA LLENA) ---")
    print(repr(cola))
