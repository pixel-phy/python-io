"""Ejercicio 27: Agregación de Variables en un Modelo PL

Modifica la clase ModeloPL del ejercicio anterior para que también contenga variables:
- Clase Variable con atributos: nombre, tipo ('binaria', 'entera', 'continua')
- ModeloPL debe tener una lista de Variable (agregación, pueden existir independientemente)
- Método agregar_variable() y eliminar_variable()
- Método generar_problema() que muestre el problema completo
"""

class Variable:
    def __init__(self, nombre, tipo='continua'):
        """
        Atributos:
        - nombre (str): Identificador de la variable (ej. 'x1')
        - tipo (str): 'binaria', 'entera' o 'continua'
        """
        self.nombre = nombre
        # Validación simple para asegurar tipos correctos
        if tipo.lower() in ['binaria', 'entera', 'continua']:
            self.tipo = tipo.lower()
        else:
            raise ValueError("El tipo debe ser 'binaria', 'entera' o 'continua'")

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class Restriccion:
    def __init__(self, nombre, coeficientes, tipo, lado_derecho):
        self.nombre = nombre
        self.coeficientes = coeficientes
        self.tipo = tipo
        self.lado_derecho = lado_derecho

    def __str__(self):
        terminos = []
        for i, coef in enumerate(self.coeficientes):
            signo = "+ " if coef >= 0 and i > 0 else ""
            if coef < 0 and i > 0:
                signo = "- "
                coef = abs(coef)
            elif coef < 0 and i == 0:
                signo = "-"
                coef = abs(coef)
                
            terminos.append(f"{signo}{coef}x{i+1}")
        
        izq = " ".join(terminos)
        return f"{self.nombre}: {izq} {self.tipo} {self.lado_derecho}"


class ModeloPL:
    def __init__(self, nombre_modelo="Modelo sin nombre"):
        self.nombre_modelo = nombre_modelo
        self.restricciones = []  # Composición
        self.variables = []      # Agregación (las variables se crean fuera y se añaden)

    # --- Métodos para Restricciones (Ejercicio Anterior) ---
    def agregar_restriccion(self, restriccion):
        if isinstance(restriccion, Restriccion):
            self.restricciones.append(restriccion)
        else:
            print("Error: El objeto debe ser una instancia de Restriccion.")

    def eliminar_restriccion(self, nombre):
        for r in self.restricciones:
            if r.nombre == nombre:
                self.restricciones.remove(r)
                return
        print(f"No se encontró la restricción '{nombre}'.")

    def formato_lp(self):
        lineas = [f"\\{self.nombre_modelo}", "Subject To"]
        for r in self.restricciones:
            lineas.append(f"  {r}")
        lineas.append("End")
        return "\n".join(lineas)

    # --- Métodos para Variables (Nuevos de este Ejercicio) ---
    def agregar_variable(self, variable):
        """Añade una instancia de Variable al modelo (Agregación)"""
        if isinstance(variable, Variable):
            self.variables.append(variable)
            print(f"Variable '{variable.nombre}' agregada al modelo.")
        else:
            print("Error: El objeto a agregar debe ser una instancia de Variable.")

    def eliminar_variable(self, nombre):
        """Elimina una variable del modelo buscando por su nombre"""
        for v in self.variables:
            if v.nombre == nombre:
                self.variables.remove(v)
                print(f"Variable '{nombre}' eliminada del modelo.")
                return
        print(f"No se encontró la variable con el nombre '{nombre}'.")

    def generar_problema(self):
        """Muestra el problema de programación lineal completo (Variables + Restricciones)"""
        print(f"\nPROBLEMA COMPLETO: {self.nombre_modelo} ")
        
        # Listado de Variables
        print("Variables del Sistema:")
        if self.variables:
            for v in self.variables:
                print(f"  - {v}")
        else:
            print("  (No hay variables definidas)")
        
        # Listado de Restricciones
        print("\nRestricciones del Modelo:")
        if self.restricciones:
            for r in self.restricciones:
                print(f"  {r}")
        else:
            print("  (No hay restricciones definidas)") 

    def __str__(self):
        return f"ModeloPL '{self.nombre_modelo}' con {len(self.variables)} variables y {len(self.restricciones)} restricciones."

# 1. Creamos las variables de manera independiente (Agregación)
x1 = Variable(nombre="x1", tipo="entera")
x2 = Variable(nombre="x2", tipo="continua")
x3 = Variable(nombre="x3", tipo="binaria")

# 2. Creamos el modelo PL
modelo_mixto = ModeloPL("Modelo de Red de Distribución")

# 3. Agregamos las variables al modelo
modelo_mixto.agregar_variable(x1)
modelo_mixto.agregar_variable(x2)
modelo_mixto.agregar_variable(x3)

# 4. Creamos y agregamos las restricciones
r1 = Restriccion("Capacidad_Max", [5, 3, 10], "<=", 500)
r2 = Restriccion("Demanda_Min", [1, 2, 0], ">=", 100)
modelo_mixto.agregar_restriccion(r1)
modelo_mixto.agregar_restriccion(r2)

# 5. Generamos el problema completo
modelo_mixto.generar_problema()

# 6. Probamos la eliminación de una variable
modelo_mixto.eliminar_variable("x3")

# 7. Volvemos a mostrar el problema para verificar el cambio
modelo_mixto.generar_problema()
