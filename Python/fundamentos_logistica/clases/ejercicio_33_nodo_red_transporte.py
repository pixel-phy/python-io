"""Ejercicio 33: Nodo en Red de Transporte
Define una clase NodoRed con atributos id_nodo, coord_x, coord_y y una lista de conexiones. 
Incluye un método agregar_conexion(). Crea NodoDemanda que herede de NodoRed. 
Añade atributos demanda (cantidad requerida) y penalizacion (costo por unidad no satisfecha). 
Usa super() en su constructor.
    """
class NodoRed:
    def __init__(self, id_nodo: str, coord_x: float, coord_y: float):
        self.id_nodo = id_nodo
        self.coord_x = coord_x
        self.coord_y = coord_y
        # Iniciamos con una lista vacía de conexiones hacia otros nodos
        self.conexiones = []

    def agregar_conexion(self, otro_nodo: 'NodoRed'):
        """Añade un nodo vecino a la lista de conexiones si no existe ya."""
        if otro_nodo not in self.conexiones:
            self.conexiones.append(otro_nodo)
            print(f"Conexión añadida: {self.id_nodo} -> {otro_nodo.id_nodo}")
        else:
            print(f"La conexión de {self.id_nodo} a {otro_nodo.id_nodo} ya existe.")


class NodoDemanda(NodoRed):
    def __init__(self, id_nodo: str, coord_x: float, coord_y: float, demanda: float, penalizacion: float):
        # Inicializamos los atributos geométricos y de red usando la clase base
        super().__init__(id_nodo, coord_x, coord_y)
        
        # Atributos específicos del nodo de demanda
        self.demanda = demanda
        self.penalizacion = penalizacion

# Prueba:
# Crear el centro de distribución (Nodo genérico)
centro_dist = NodoRed(id_nodo="CD_Central", coord_x=0.0, coord_y=0.0)

# Crear clientes (Nodos de demanda)
cliente_A = NodoDemanda(id_nodo="Cliente_A", coord_x=3.5, coord_y=4.2, demanda=150, penalizacion=25.0)
cliente_B = NodoDemanda(id_nodo="Cliente_B", coord_x=-1.2, coord_y=5.0, demanda=80, penalizacion=40.0)

# Conectar el centro de distribución con los clientes
centro_dist.agregar_conexion(cliente_A)
centro_dist.agregar_conexion(cliente_B)

# Al heredar de NodoRed, el cliente A también puede conectarse con el cliente B
cliente_A.agregar_conexion(cliente_B)

print(f"\nEl {cliente_A.id_nodo} tiene una demanda de {cliente_A.demanda} unidades.")
