"""Ejercicio 08: Representación de Solución de Asignación

Modifica la clase VariableBinaria para que:

- __repr__ muestre: VariableBinaria('x', 1, 2, True)

- __str__ muestr: x[1][2] = True (formato amigable)

- Añade un método formato_matriz() que devuelva una cadena para visualizar la variable en 
  contexto de matriz.

"""
class VariableBinaria:
    def __init__(self, nombre: str, indice_fila: int, indice_columna: int):
        """
        Inicializa una variable de decisión binaria.
        """
        self.nombre = nombre
        self.indice_fila = indice_fila
        self.indice_columna = indice_columna
        self.valor = False  # Inicializado por defecto en False

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

    # --- NUEVOS MÉTODOS SOLICITADOS ---

    def __repr__(self) -> str:
        """
        Representación técnica del objeto.
        Muestra: VariableBinaria('x', 1, 2, True)
        """
        return f"VariableBinaria('{self.nombre}', {self.indice_fila}, {self.indice_columna}, {self.valor})"

    def __str__(self) -> str:
        """
        Representación amigable para el usuario.
        Muestra: x[1][2] = True
        """
        return f"{self.nombre}[{self.indice_fila}][{self.indice_columna}] = {self.valor}"

    def formato_matriz(self) -> str:
        """
        Devuelve una cadena para visualizar la variable en contexto de matriz.
        Muestra: x12 = 1 (si es True) o x12 = 0 (si es False)
        """
        # Convertimos el booleano (True/False) a entero (1/0)
        valor_numerico = 1 if self.valor else 0
        return f"{self.nombre}{self.indice_fila}{self.indice_columna} = {valor_numerico}"


# Prueba del Ejercicio:
if __name__ == "__main__":
    # 1. Crear la variable binaria
    x_1_2 = VariableBinaria(nombre="x", indice_fila=1, indice_columna=2)
    x_1_2.asignar(True)

    # 2. Probar __repr__
    print("Prueba de __repr__ (repr()):")
    print(repr(x_1_2))  
    print("-" * 30)

    # 3. Probar __str__
    print("Prueba de __str__ (print directo):")
    print(x_1_2)        
    print("-" * 30)

    # 4. Probar formato_matriz()
    print("Prueba de formato_matriz():")
    print(x_1_2.formato_matriz())
