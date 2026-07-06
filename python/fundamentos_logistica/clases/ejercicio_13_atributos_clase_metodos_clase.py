
"""Ejercicio 13: Atributos de Clase y Métodos de Clase (@classmethod)

En Python, atributos de clase son variables compartidas por todas las instancias, mientras que métodos de
clase (@classmethod) operan sobre la clase en lugar de sobre instancias específicas.

Diferencias clave:

- Atributos de clase: Definidos fuera de __init__. Son como "variables globales" para todas las instancias.

- Atributos de instancia: Definidos con self. en __init__. Son específicos de cada objeto.

- Métodos de clase: Reciben cls (la clase) en lugar de self (la instancia). Pueden crear nuevas instancias.

"""
# Implementación en Python:
class Planta:
    """
    Representa una planta en un problema de localización.
    Atributo de clase: costo_transporte_por_km (compartido por todas las plantas).
    """
    # Atributos de clase
    costo_transporte_por_km = 2.5  # Costo global ($/km)
    tasa_descuento = 0.08          # Tasa global para proyectos
    contador_plantas = 0           # Contador de instancias creadas
    
    def __init__(self, id_planta: str, capacidad: float, costo_fijo: float, 
                 coordenada_x: float, coordenada_y: float):
        """
        Constructor de instancia.
        """
        self.id_planta = id_planta
        self.capacidad = capacidad
        self.costo_fijo = costo_fijo
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.produccion_actual = 0.0
        
        # Incrementar contador de plantas
        Planta.contador_plantas += 1

    def calcular_costo_transporte(self, distancia: float) -> float:
        """
        usa el atributo de clase costo_transporte_por_km.
        """
        return distancia * Planta.costo_transporte_por_km

    def calcular_costo_total_anualizado(self) -> float:
        """
        Usa la tasa de descuento global para anualizar costos fijos.
        """
        return self.costo_fijo * (1 + Planta.tasa_descuento)
    
    # Métodos de clase
    
    @classmethod
    def modificar_costo_transporte(cls, nuevo_costo: float):
        """
        Modifica el costo de transporte para TODAS las plantas.
        """
        if nuevo_costo < 0:
            raise ValueError("El costo de transporte no puede ser negativo")
        cls.costo_transporte_por_km = nuevo_costo
    
    @classmethod
    def modificar_tasa_descuento(cls, nueva_tasa: float):
        """
        Modifica la tasa de descuento para TODOS los proyectos.
        """
        if not 0 <= nueva_tasa <= 1:
            raise ValueError("La tasa debe estar entre 0 y 1")
        cls.tasa_descuento = nueva_tasa
    
    @classmethod
    def desde_csv(cls, nombre_archivo: str) -> list['Planta']:
        """
        Constructor alternativo: crea múltiples plantas desde un archivo CSV.
        """
        import csv
        plantas = []
        
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                planta = cls(
                    id_planta=fila['id'],
                    capacidad=float(fila['capacidad']),
                    costo_fijo=float(fila['costo_fijo']),
                    coordenada_x=float(fila['x']),
                    coordenada_y=float(fila['y'])
                )
                plantas.append(planta)
        
        return plantas
    
    @classmethod
    def desde_texto(cls, texto: str) -> 'Planta':
        """
        Constructor alternativo: crea una planta desde un string formateado.
        Formato: "id_planta,capacidad,costo_fijo,x,y"
        """
        partes = texto.strip().split(',')
        if len(partes) != 5:
            raise ValueError("Formato incorrecto. Esperado: id,capacidad,costo_fijo,x,y")
        
        return cls(
            id_planta=partes[0],
            capacidad=float(partes[1]),
            costo_fijo=float(partes[2]),
            coordenada_x=float(partes[3]),
            coordenada_y=float(partes[4])
        )
    
    @classmethod
    def reporte_estadistico(cls) -> str:
        """
        Método de clase que genera un reporte global sin necesidad de instancia.
        """
        return (f"ESTADÍSTICAS GLOBALES DE PLANTAS\n"
                f"   Costo transporte/km: ${cls.costo_transporte_por_km:.2f}\n"
                f"   Tasa de descuento: {cls.tasa_descuento:.1%}\n"
                f"   Total plantas creadas: {cls.contador_plantas}")
    
    # Representaciones
    def __repr__(self):
        return f"Planta(id='{self.id_planta}', capacidad={self.capacidad})"
    
    def __str__(self):
        return f"Planta {self.id_planta} (Cap: {self.capacidad:.0f})"


# Ejemplo de uso
if __name__ == "__main__":
    # Crear plantas usando constructor normal
    planta1 = Planta("P1", 100, 5000, 0, 0)
    planta2 = Planta("P2", 150, 7000, 10, 5)
    
    print("=== ESTADO INICIAL ===")
    print(Planta.reporte_estadistico())
    print(f"planta1: {planta1}")
    print(f"Costo transporte (dist 5km): ${planta1.calcular_costo_transporte(5):.2f}")
    print("\n")
    
    # Modificar parámetros globales con método de clase
    Planta.modificar_costo_transporte(3.0)
    Planta.modificar_tasa_descuento(0.10)
    
    print("=== DESPUÉS DE MODIFICAR PARÁMETROS GLOBALES ===")
    print(Planta.reporte_estadistico())
    print(f"Costo transporte (dist 5km): ${planta1.calcular_costo_transporte(5):.2f}")
    print("\n")
    
    # Constructor alternativo desde string
    texto_planta = "P3,200,8000,15,10"
    planta3 = Planta.desde_texto(texto_planta)
    print(f"Planta creada desde texto: {planta3}")
    print(f"Total plantas: {Planta.contador_plantas}")
