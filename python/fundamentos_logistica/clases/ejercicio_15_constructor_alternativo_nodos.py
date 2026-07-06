"""Ejercicio 15: Constructor Alternativo para Nodos

Añade a la clase Nodo del Día 1:

Método de clase desde_csv() que cree múltiples nodos desde un archivo CSV con columnas: 
id, x, y, demanda, oferta

Método de clase desde_lista() que cree nodos desde una lista de tuplas: [("A", 0, 0, 10, 0), ...]

Atributo de clase contador_nodos que se incremente en cada creación

"""

import csv

class Nodo:
    """
    Representa un nodo en una red de transporte.
    Aplicación IO: Modelado de ciudades, centros de distribución o puntos de demanda.
    """
    
    # 1. Atributo de clase global para contar las instancias creadas
    contador_nodos = 0
    
    def __init__(self, id_nodo: str, coordenada_x: float, coordenada_y: float, demanda: float = 0):
        """
        Constructor del nodo.
        """
        self.id_nodo = id_nodo
        self.coordenada_x = float(coordenada_x)
        self.coordenada_y = float(coordenada_y)
        self.demanda = float(demanda)
        self.oferta = 0  # Inicializado como 0, se modificará si es un nodo de oferta
        self.visitado = False  # Útil para algoritmos de búsqueda en grafos
        
        # Incrementa automáticamente el contador global al instanciar cualquier nodo
        Nodo.contador_nodos += 1
        
    # 2. Método de clase para crear múltiples nodos desde una lista de tuplas
    @classmethod
    def desde_lista(cls, lista_nodos: list) -> list:
        """
        Crea nodos desde una lista de tuplas: [("A", 0, 0, 10, 0), ...]
        Retorna una lista de instancias de Nodo.
        """
        instancias = []
        for id_n, x, y, demanda, oferta in lista_nodos:
            # Creamos la instancia invocando a cls (que es la clase Nodo)
            nodo = cls(id_n, x, y, demanda)
            nodo.set_oferta(oferta)
            instancias.append(nodo)
        return instancias

    # 3. Método de clase para crear múltiples nodos desde un archivo CSV
    @classmethod
    def desde_csv(cls, ruta_archivo: str) -> list:
        """
        Crea múltiples nodos desde un archivo CSV con columnas: id, x, y, demanda, oferta.
        Retorna una lista de instancias de Nodo.
        """
        instancias = []
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            # Usamos DictReader para manejar las columnas mediante sus nombres/cabeceras
            lector = csv.DictReader(archivo)
            for fila in lector:
                nodo = cls(
                    id_nodo=fila['id'],
                    coordenada_x=float(fila['x']),
                    coordenada_y=float(fila['y']),
                    demanda=float(fila['demanda'])
                )
                nodo.set_oferta(float(fila['oferta']))
                instancias.append(nodo)
        return instancias
        
    def set_oferta(self, cantidad: float):
        """Establece la oferta del nodo (ej. cantidad de producto disponible)."""
        if cantidad < 0:
            raise ValueError("La oferta no puede ser negativa")
        self.oferta = cantidad
        
    def calcular_distancia_a(self, otro_nodo: 'Nodo') -> float:
        """Calcula la distancia euclidiana a otro nodo."""
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

    def __repr__(self):
        return f"Nodo('{self.id_nodo}', x={self.coordenada_x}, y={self.coordenada_y}, Demanda={self.demanda}, Oferta={self.oferta})"


# Pruebas: 

if __name__ == "__main__":
    print(f"Contador inicial: {Nodo.contador_nodos}")
    
    # 1. Probar creación manual (Tradicional)
    nodo_manual = Nodo('M1', 1, 1, demanda=5)
    print(f"Contador tras 1 nodo manual: {Nodo.contador_nodos}")
    
    # 2. Probar desde_lista()
    datos_lista = [
        ("A", 0, 0, 10, 0),
        ("B", 4, 3, 0, 15),
        ("C", 2, 2, 5, 5)
    ]
    nodos_desde_lista = Nodo.desde_lista(datos_lista)
    print(f"\nNodos creados desde lista:")
    for n in nodos_desde_lista:
        print(f"  {n}")
        
    print(f"Contador tras procesar lista: {Nodo.contador_nodos}")
    
    # 3. Probar desde_csv() (Simulado creando un archivo temporal primero)
    contenido_csv = """id,x,y,demanda,oferta
D,10,10,0,50
E,12,15,30,0
"""
    with open("nodos_prueba.csv", "w", encoding="utf-8") as f:
        f.write(contenido_csv)
        
    nodos_desde_csv = Nodo.desde_csv("nodos_prueba.csv")
    print(f"\nNodos creados desde CSV:")
    for n in nodos_desde_csv:
        print(f"  {n}")
        
    print(f"Contador final de nodos creados en total: {Nodo.contador_nodos}")
