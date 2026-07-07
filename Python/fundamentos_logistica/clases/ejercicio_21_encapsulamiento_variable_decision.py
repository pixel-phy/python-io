"""Ejercicio 21: Encapsulamiento en Variable de Decisión

Modifica la clase VariableBinaria del día 1 para:
- Atributo privado __valor (con name mangling)
- Propiedad valor como getter que retorne el valor
- Setter de valor que valide que sea booleano
- Atributo protegido _nombre_completo que combine nombre + índices
- Método activar() y desactivar() como formas seguras de modificar
"""
class VariableBinaria:
    def __init__(self, nombre: str, indice_fila: int, indice_columna: int):
        """
        Inicializa una variable de decisión binaria con encapsulamiento.
        """
        self.nombre = nombre
        self.indice_fila = indice_fila
        self.indice_columna = indice_columna
        
        # - Atributo privado __valor (con name mangling)
        self.__valor = False 
        
        # - Atributo protegido _nombre_completo que combine nombre + índices
        self._nombre_completo = f"{nombre}_{indice_fila}_{indice_columna}"

    # - Propiedad valor como getter que retorne el valor
    @property
    def valor(self) -> bool:
        return self.__valor

    # - Setter de valor que valide que sea booleano
    @valor.setter
    def valor(self, nuevo_valor: bool):
        if not isinstance(nuevo_valor, bool):
            raise TypeError("El valor a asignar debe ser un booleano (True o False).")
        self.__valor = nuevo_valor

    # - Método activar() como forma segura de modificar
    def activar(self):
        """Activa la variable de decisión binaria (asigna True)."""
        self.valor = True

    # - Método desactivar() como forma segura de modificar
    def desactivar(self):
        """Desactiva la variable de decisión binaria (asigna False)."""
        self.valor = False

    def es_activa(self) -> bool:
        """Retorna True si la variable está activa, de lo contrario False."""
        return self.valor


# --- Prueba de funcionamiento ---
if __name__ == "__main__":
    # 1. Crear la variable binaria
    x_1_2 = VariableBinaria(nombre="x", indice_fila=1, indice_columna=2)
    print(f"Nombre completo (protegido): {x_1_2._nombre_completo}")
    print(f"¿Está activa inicialmente?: {x_1_2.es_activa()}")  # False

    # 2. Usar los métodos seguros activar() y desactivar()
    x_1_2.activar()
    print(f"Tras activar(): {x_1_2.valor}")  # True
    
    x_1_2.desactivar()
    print(f"Tras desactivar(): {x_1_2.valor}")  # False

    # 3. Probar el setter con asignación directa válida
    x_1_2.valor = True
    print(f"Asignación directa por setter: {x_1_2.valor}")  # True

    # 4. Demostración de Name Mangling (intentar acceder a __valor directamente fallará)
    try:
        print(x_1_2.__valor)
    except AttributeError:
        print("¡Correcto! No se puede acceder a '__valor' desde afuera debido al Name Mangling.")

    # 5. Intentar asignar un valor incorrecto mediante el setter para disparar el TypeError
    try:
        x_1_2.valor = "Texto no válido"
    except TypeError as e:
        print(f"Error de validación atrapado: {e}")
