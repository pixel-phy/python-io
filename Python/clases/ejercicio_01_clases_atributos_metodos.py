"""Teoría:

En Investigación de Operaciones, necesitamos representar entidades del mundo real: nodos en una red,
variables de decisión, restricciones, etc. Las clases nos permiten crear "Planitallas" para estos objetos,
encapsulando tanto sus datos (atributos) como su comportamiento (métodos).

- Conceptos clave:
    - class: Define un nuevo tipo de dato.
    - __init__: Método constructos que inicializa los atributos del objeto.
    - self: Referencia al objeto mismo, permite acceder a sus atributos y métodos.

"""
# Modelado de un Nodo en una red de transporte

class Nodo:
    """
    Representa un nodo en una red de transporte.
    Aplicación IO: Modelado de ciudades, centros de distribución o puntos de demanda.
    """
    
    def __init__(self, id_nodo: str, coordenada_x: float, coordenada_y: float, demanda: float = 0):
        """
        Constructor del nodo.
        
        Args:
            id_nodo: Identificador único del nodo (ej. 'A', 'B', 'C')
            coordenada_x: Coordenada en el eje X
            coordenada_y: Coordenada en el eje Y
            demanda: Demanda del nodo (por defecto 0 para nodos de oferta)
        """
        self.id_nodo = id_nodo
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.demanda = demanda
        self.oferta = 0  # Inicializado como 0, se modificará si es un nodo de oferta
        self.visitado = False  # Útil para algoritmos de búsqueda en grafos
        
    def set_oferta(self, cantidad: float):
        """Establece la oferta del nodo (ej. cantidad de producto disponible)."""
        if cantidad < 0:
            raise ValueError("La oferta no puede ser negativa")
        self.oferta = cantidad
        
    def calcular_distancia_a(self, otro_nodo: 'Nodo') -> float:
        """
        Calcula la distancia euclidiana a otro nodo.
        Útil para crear matrices de costos de transporte.
        """
        dx = self.coordenada_x - otro_nodo.coordenada_x
        dy = self.coordenada_y - otro_nodo.coordenada_y
        return (dx**2 + dy**2)**0.5
    
    def es_oferente(self) -> bool:
        """Verifica si el nodo tiene oferta disponible."""
        return self.oferta > 0
    
    def es_demandante(self) -> bool:
        """Verifica si el nodo tiene demanda."""
        return self.demanda > 0
    
    def balance(self) -> float:
        """Calcula el balance neto (oferta - demanda)."""
        return self.oferta - self.demanda

# Prueba:

# Crear nodos
nodo_a = Nodo('A', 0, 0, demanda=10)
nodo_b = Nodo('B', 4, 3, demanda=0)
nodo_b.set_oferta(15)

# Calcular distancia
distancia = nodo_a.calcular_distancia_a(nodo_b)

# Verificar balances
print(f"{nodo_a.id_nodo}: {nodo_a.balance()}")
print(f"{nodo_b.id_nodo}: {nodo_b.balance()}")
