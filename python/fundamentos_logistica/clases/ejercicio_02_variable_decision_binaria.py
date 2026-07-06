"""Ejercicio 02: Variable de Decisión Binaria

Crea una clase VariableBinaria que represente una variable de decisión en un problema de 
optimización combinatoria. Debe tener:

- Atributos: nombre(str), indice_fila(int), indice_columna(int), valor(bool, inicializado en False)

- Método: asignar(valor) que reciba un booleano y lo asigne, validando que sea booleano.

- Método: es_activa() que retorne si la variable es True.

"""

class VariableBinaria:
    def __init__(self, nombre: str, indice_fila: int, indice_columna: int):
        """
            Inicializa una variable de decisión binaria.
        """
        self.nombre = nombre
        self.indice_fila = indice_fila
        self.indice_columna = indice_columna
        self.valor = False # Inicializado por defecto en False

    def asignar(self, nuevo_valor: bool):
        """
            Asigna un nuevo valor booleano a la variable, validando el tipo de dato.
        """
        if not isinstance(nuevo_valor, bool):
            raise TypeError("El valor a asignar debe ser un booleano (True o False).")
        self.valor = nuevo_valor

    def es_activa(self) -> bool:
        """
        Retorna True si la variable está activa (su valor es True), de lo contrario False.
        """
        return self.valor

# Prueba:
if __name__ == "__main__":
    try:
        # 1. Crear la variable binaria
        x_1_2 = VariableBinaria(nombre="x", indice_fila=1, indice_columna=2)
        print(f"Variable creada: {x_1_2.nombre}[{x_1_2.indice_fila}][{x_1_2.indice_columna}]")
        print(f"¿Está activa inicialmente?: {x_1_2.es_activa()}")  # Debería ser False

        # 2. Asignar un valor correcto
        x_1_2.asignar(True)
        print(f"¿Está activa después de asignar True?: {x_1_2.es_activa()}")  # Debería ser True

        # 3. Intentar asignar un valor incorrecto (descomenta para probar el error)
        # x_1_2.asignar("No soy un booleano") 
        
    except TypeError as e:
        print(f"Error de validación: {e}")
