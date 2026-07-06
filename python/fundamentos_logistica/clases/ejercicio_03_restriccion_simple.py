"""Ejercicio 02: Restricción Simple

Crea una clase RestriccionLineal que modele una restricción en un problema de programación lineal:

- Atributos: nombre(str), lado_izquierdo(float), lado_derecho(float), tipo(str:'<=', '>=', '==')

- Método: verificar_cumplimiento(variables_dict) que reciba un diccionario con los valores de las variables
  y retorne True si la restricción se cumple. (Asume una estructura simpla: suma de variables = lado_izquierdo)

"""

class RestriccionLineal:
    def __init__(self, nombre: str, lado_derecho: float, tipo: str):
        """
        Inicializa una restricción lineal.
        Nota: 'lado_izquierdo' se calculará dinámicamente en base a las variables.
        """
        if tipo not in ['<=', '>=', '==']:
            raise ValueError("El tipo de restricción debe ser '<=', '>=' o '=='.")
        
        self.nombre = nombre
        self.lado_derecho = lado_derecho
        self.tipo = tipo
        self.lado_izquierdo = 0.0 # Se actualizará al verificar el cumplimiento

    def verificar_cumplimiento(self, variables_dict: dict) -> bool:
        """
            Recibe un diccionario {nombre_variable: valor},
            calcula la suma (lado_izquierdo) y valúa si cumple la restricción.
        """
        # Sumamos todos los valores de las variables presentes en el diccionario
        self.lado_izquierdo = float(sum(variables_dict.values()))

        # Evaluamos el cumplimiento según el tipo de operador
        if self.tipo == '<=':
            return self.lado_izquierdo <= self.lado_derecho
        elif self.tipo == '>=':
            return self.lado_izquierdo >= self.lado_derecho
        elif self.tipo == '==':
            return self.lado_izquierdo == self.lado_derecho

        return False

    def __repr__(self):
        """
        Método de representación formal para depuración.
        Devuelve una cadena que idealmente permitiría recrear el objeto.
        """
        return f"RestriccionLineal('{self.nombre}', {self.lado_derecho}, '{self.tipo}')"

# Prueba:
if __name__ == "__main__":
    # Creamos un par de restricciones
    r1 = RestriccionLineal(nombre="R1", lado_derecho=5.0, tipo="<=")
    r2 = RestriccionLineal(nombre="R2", lado_derecho=10.0, tipo="==")
    
    # 1. Al imprimir el objeto directamente en consola:
    print("Impresión directa del objeto:")
    print(r1)
    
    print("\n")

    # 2. Al tener los objetos dentro de una estructura de datos (como una lista):
    lista_restricciones = [r1, r2]
    print("Impresión de una lista que contiene los objetos:")
    print(lista_restricciones)
