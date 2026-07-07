"""Ejercicio 26: Composición de Restricciones en un ModeloPL
Crea una clase Restriccion con atributos básicos (nombre, coeficientes, lado_derecho, tipo)
y una clase ModeloPL que:
- Contenga una lista de Restriccion (composición)
- Método agregar_restriccion() para añadir restricciones
- Método eliminar_restriccion() por nombre
- Método formato_lp() que genere el modelo en formato estándar
- Método __str__ que muestre el modelo completo
"""

class Restriccion:
    def __init__(self, nombre, coeficientes, tipo, lado_derecho):
        """
        Atributos:
        - nombre (str): Identificador de la restricción (ej. 'R1')
        - coeficientes (list): Lista de números con los coeficientes de las variables [c1, c2, ...]
        - tipo (str): '<=', '>=' o '='
        - lado_derecho (float/int): El valor del lado derecho (RHS)
        """
        self.nombre = nombre
        self.coeficientes = coeficientes
        self.tipo = tipo
        self.lado_derecho = lado_derecho

    def __str__(self):
        # Construye la expresión del lado izquierdo (ej. "2x1 + 3x2")
        terminos = []
        for i, coef in enumerate(self.coeficientes):
            # Formateo básico para que se vea limpio
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
        # Composición: El modelo TIENE una lista de restricciones
        self.restricciones = []

    def agregar_restriccion(self, restriccion):
        """Añade una instancia de Restriccion a la lista."""
        if isinstance(restriccion, Restriccion):
            self.restricciones.append(restriccion)
            print(f"Restricción '{restriccion.nombre}' agregada con éxito.")
        else:
            print("Error: El objeto a agregar debe ser una instancia de Restriccion.")

    def eliminar_restriccion(self, nombre):
        """Busca y elimina una restricción por su nombre."""
        for r in self.restricciones:
            if r.nombre == nombre:
                self.restricciones.remove(r)
                print(f"Restricción '{nombre}' eliminada con éxito.")
                return
        print(f"No se encontró ninguna restricción con el nombre '{nombre}'.")

    def formato_lp(self):
        """Genera una cadena de texto en un formato estándar tipo archivo .lp"""
        lineas = [f"\\{self.nombre_modelo}", "Subject To"]
        for r in self.restricciones:
            lineas.append(f"  {r}")
        lineas.append("End")
        return "\n".join(lineas)

    def __str__(self):
        """Muestra el modelo completo en un formato amigable."""
        if not self.restricciones:
            return f"--- {self.nombre_modelo} ---\nEl modelo no tiene restricciones asignadas."
        
        res_str = "\n".join([f"  {r}" for r in self.restricciones])
        return f"--- {self.nombre_modelo} ---\nRestricciones:\n{res_str}"

# 1. Creamos el modelo matemático
mi_modelo = ModeloPL("Optimización de Producción")

# 2. Creamos algunas restricciones
# Supongamos: 2x1 + 3x2 <= 120
r1 = Restriccion(nombre="R1_MateriaPrima", coeficientes=[2, 3], tipo="<=", lado_derecho=120)
# Supongamos: 1x1 - 2x2 >= 40
r2 = Restriccion(nombre="R2_DemandaMinima", coeficientes=[1, -2], tipo=">=", lado_derecho=40)
# Supongamos: 4x1 + 4x2 = 80
r3 = Restriccion(nombre="R3_Presupuesto", coeficientes=[4, 4], tipo="=", lado_derecho=80)

# 3. Agregamos las restricciones al modelo
print("--- Añadiendo Restricciones ---")
mi_modelo.agregar_restriccion(r1)
mi_modelo.agregar_restriccion(r2)
mi_modelo.agregar_restriccion(r3)

# 4. Mostramos el modelo usando __str__
print("\n--- Vista del Modelo (__str__) ---")
print(mi_modelo)

# 5. Generamos el formato estándar .lp
print("\n--- Formato LP Estándar ---")
print(mi_modelo.formato_lp())

# 6. Probamos eliminar una restricción
print("\n--- Eliminando Restricción ---")
mi_modelo.eliminar_restriccion("R2_DemandaMinima")

# 7. Verificamos el modelo final
print("\n--- Modelo Final ---")
print(mi_modelo)
