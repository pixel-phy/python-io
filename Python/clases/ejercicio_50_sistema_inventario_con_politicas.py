"""Ejercicio 50: Sistema de Inventario con Políticas

Crea un sistema de inventario usando composición:

1. Clase PoliticaInventario: Componente que define cómo se toman decisiones de pedido
    - Métodos: calcular_pedido(inventario_actual, demanda), nombre()

2. Clase PoliticaCantidadFija: Pedir siempre una cantidad fija Q cuando el inventario baja de R
    - Atributos: cantidad_pedido, punto_reorden

3. Clase PoliticaPeriodica: Revisar cada T períodos y pedir hasta un nivel máximo S
    - Atributos: periodo, nivel_maximo

4. Clase SistemaInventario: Compone una política y simula su comportamiento
    - Atributos: politica, inventario_actual, historial
    - Métodos: simular(demanda_diaria, dias)

    """

class PoliticaInventario:
    """Clase base (interfaz) para las políticas de inventario."""
    def calcular_pedido(self, inventario_actual, demanda):
        raise NotImplementedError("Este método debe ser implementado por la subclase")

    def nombre(self):
        raise NotImplementedError("Este método debe ser implementado por la subclase")


class PoliticaCantidadFija(PoliticaInventario):
    """Política (Q, R): Pide una cantidad fija Q cuando el inventario baja de R."""
    def __init__(self, cantidad_pedido, punto_reorden):
        self.cantidad_pedido = cantidad_pedido
        self.punto_reorden = punto_reorden

    def calcular_pedido(self, inventario_actual, demanda):
        # Si el inventario después de la demanda cae por debajo o igual al punto de reorden
        inventario_proyectado = inventario_actual - demanda
        if inventario_proyectado <= self.punto_reorden:
            return self.cantidad_pedido
        return 0

    def nombre(self):
        return f"Política de Cantidad Fija (Q={self.cantidad_pedido}, R={self.punto_reorden})"


class PoliticaPeriodica(PoliticaInventario):
    """Política (T, S): Revisa cada T períodos y pide hasta llegar a S."""
    def __init__(self, periodo, nivel_maximo):
        self.periodo = periodo
        self.nivel_maximo = nivel_maximo
        self.contador_dias = 0  # Para rastrear los días transcurridos

    def calcular_pedido(self, inventario_actual, demanda):
        self.contador_dias += 1
        inventario_proyectado = inventario_actual - demanda
        
        # Si es el día de revisión (cada T períodos)
        if self.contador_dias % self.periodo == 0:
            # Pedimos lo necesario para volver a llenar el inventario hasta S
            cantidad_a_pedir = max(0, self.nivel_maximo - inventario_proyectado)
            return cantidad_a_pedir
        return 0

    def nombre(self):
        return f"Política Periódica (T={self.periodo}, S={self.nivel_maximo})"


class SistemaInventario:
    """Clase principal que simula el inventario usando COMPOSICIÓN."""
    def __init__(self, politica: PoliticaInventario, inventario_inicial):
        self.politica = politica  # Aquí se inyecta el componente (composición)
        self.inventario_actual = inventario_inicial
        self.historial = []

    def simular(self, demanda_diaria, dias):
        """Simula el comportamiento del inventario día a día."""
        print(f"--- Iniciando Simulación con: {self.politica.nombre()} ---")
        print(f"Inventario inicial: {self.inventario_actual}\n")
        
        # Limpiamos historial para una nueva simulación
        self.historial = []

        for dia in range(1, dias + 1):
            # 1. Obtener la demanda del día (manejamos si la lista se queda corta)
            demanda_hoy = demanda_diaria[dia - 1] if (dia - 1) < len(demanda_diaria) else 0
            
            # 2. Consultar a la política si se debe realizar un pedido
            pedido = self.politica.calcular_pedido(self.inventario_actual, demanda_hoy)
            
            # 3. Actualizar el inventario: se resta la demanda y se suma el pedido
            # (Asumimos por simplicidad que el pedido llega inmediatamente al final del día)
            inventario_antes = self.inventario_actual
            self.inventario_actual = max(0, self.inventario_actual - demanda_hoy) + pedido
            
            # 4. Registrar en el historial
            registro = {
                "dia": dia,
                "inventario_inicial": inventario_antes,
                "demanda": demanda_hoy,
                "pedido_realizado": pedido,
                "inventario_final": self.inventario_actual
            }
            self.historial.append(registro)
            
            print(f"Día {dia:02d} | Inv. Inicial: {registro['inventario_inicial']:3d} | "
                  f"Demanda: {registro['demanda']:2d} | Pedido: {registro['pedido_realizado']:3d} | "
                  f"Inv. Final: {registro['inventario_final']:3d}")
        print("-" * 60 + "\n")

# Demanda aleatoria para 7 días
demanda_ejemplo = [10, 15, 20, 5, 12, 18, 8]
inventario_inicial = 50

# --- Prueba 1: Política de Cantidad Fija ---
# Si baja de 25 unidades, pide 40 más.
politica_fija = PoliticaCantidadFija(cantidad_pedido=40, punto_reorden=25)
sistema_q = SistemaInventario(politica_fija, inventario_inicial)
sistema_q.simular(demanda_ejemplo, dias=7)

# --- Prueba 2: Política Periódica ---
# Revisa cada 3 días y pide hasta completar 60 unidades.
politica_periodica = PoliticaPeriodica(periodo=3, nivel_maximo=60)
sistema_t = SistemaInventario(politica_periodica, inventario_inicial)
sistema_t.simular(demanda_ejemplo, dias=7)
