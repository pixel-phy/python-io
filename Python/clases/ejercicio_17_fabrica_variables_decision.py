"""Ejercicio 17: Fábrica de Variables de Decisión

Crea una clase VariableFactory que:

Atributo de clase: contador_variables = 0

Atributo de clase: formato_nombre = "x" (formato base para nombres)

Método de clase: crear_variable_binaria(fila, columna) que retorne una VariableBinaria (del Día 1) con nombre automático usando el formato

Método de clase: crear_variables_matriz(n_filas, n_columnas) que cree una matriz completa de variables

Método de clase: reiniciar_contador() para resetear el contador (útil en nuevos modelos)

Método de clase: reporte_variables() que muestre cuántas variables se han creado
"""
class VariableBinaria:
    def __init__(self, nombre: str, indice_fila: int, indice_columna: int):
        """Initializa una variable de decisión binaria."""
        self.nombre = nombre
        self.indice_fila = indice_fila
        self.indice_columna = indice_columna
        self.valor = False  # Inicializado por defecto en False

    def asignar(self, nuevo_valor: bool):
        """Asigna un nuevo valor booleano a la variable, validando el tipo de dato."""
        if not isinstance(nuevo_valor, bool):
            raise TypeError("El valor a asignar debe ser un booleano (True o False).")
        self.valor = nuevo_valor

    def es_activa(self) -> bool:
        """Retorna True si la variable está activa (su valor es True), de lo contrario False."""
        return self.valor

    def __repr__(self):
        return f"{self.nombre}_{self.indice_fila}_{self.indice_columna}(Valor={self.valor})"

# Clase nueva: VariableFactory (Patrón Fábrica)

class VariableFactory:
    # 1. Atributos de clase
    contador_variables = 0
    formato_nombre = "x"  # Formato base por defecto

    # 2. Método de clase para crear una variable individual con nombre automático
    @classmethod
    def crear_variable_binaria(cls, fila: int, columna: int) -> VariableBinaria:
        """
        Crea una VariableBinaria con nombre automático (ej. x_0_1)
        e incrementa el contador global de la fábrica.
        """
        # Formateamos el nombre combinando la base y los índices
        nombre_automatico = f"{cls.formato_nombre}_{fila}_{columna}"
        
        # Incrementamos el contador global de la fábrica
        cls.contador_variables += 1
        
        # Retornamos la instancia de VariableBinaria
        return VariableBinaria(nombre=nombre_automatico, indice_fila=fila, indice_columna=columna)

    # 3. Método de clase para crear una matriz bidimensional (lista de listas) de variables
    @classmethod
    def crear_variables_matriz(cls, n_filas: int, n_columnas: int) -> list[list[VariableBinaria]]:
        """
        Genera una matriz completa de n_filas x n_columnas llena de variables binarias.
        """
        matriz = []
        for i in range(n_filas):
            fila_variables = []
            for j in range(n_columnas):
                # Reutilizamos el método de creación individual para mantener consistencia
                nueva_var = cls.crear_variable_binaria(fila=i, columna=j)
                fila_variables.append(nueva_var)
            matriz.append(fila_variables)
        return matriz

    # 4. Método de clase para reiniciar el contador
    @classmethod
    def reiniciar_contador(cls):
        """Resetea el contador global de variables a cero."""
        cls.contador_variables = 0

    # 5. Método de clase para imprimir el reporte de variables creadas
    @classmethod
    def reporte_variables(cls) -> str:
        """Devuelve un string con el conteo de variables generadas por la fábrica."""
        return f"--- REPORTE DE LA FÁBRICA ---\nVariables creadas hasta el momento: {cls.contador_variables}"


# --- Bloque de Prueba para comprobar la Fábrica ---
if __name__ == "__main__":
    print("=== Probando VariableFactory ===\n")
    
    # 1. Crear una sola variable binaria
    v1 = VariableFactory.crear_variable_binaria(fila=1, columna=5)
    print(f"Variable individual creada: {v1}")
    print(VariableFactory.reporte_variables())
    print("\n" + "-"*40 + "\n")

    # 2. Crear una matriz completa de variables (ejemplo: 3 orígenes y 4 destinos)
    # Útil para problemas de transporte
    print("Creando una matriz de variables de asignación (3x4)...")
    matriz_x = VariableFactory.crear_variables_matriz(n_filas=3, n_columnas=4)
    
    # Imprimir la matriz de variables de forma visual
    for fila in matriz_x:
        print("  ", fila)
        
    print("\n" + VariableFactory.reporte_variables())
    print("\n" + "-"*40 + "\n")

    # 3. Cambiar el formato de nombre de la fábrica y reiniciar
    print("Cambiando configuración de fábrica para un nuevo modelo (Ej: Asignación de Tareas 'y')...")
    VariableFactory.reiniciar_contador()
    VariableFactory.formato_nombre = "y"
    
    # Crear variables con la nueva configuración
    matriz_y = VariableFactory.crear_variables_matriz(n_filas=2, n_columnas=2)
    for fila in matriz_y:
        print("  ", fila)
        
    print("\n" + VariableFactory.reporte_variables())
