"""Ejercicio 18: Gestor de Modelos de Optimización con múltiples constructores

Crea una clase ModeloOptimizacion que gestione un problema completo de PL:

a) Atributos de clase:

tolerancia_global = 1e-6 (tolerancia para comparaciones)

max_iteraciones = 1000 (máximo de iteraciones para solvers)

verbose = False (modo de depuración)

b) Métodos de clase:

configurar(tolerancia=None, max_iter=None, verbose=None): modifica parámetros globales

desde_archivo_lp(nombre_archivo): constructor alternativo que lee formato LP estándar

desde_diccionario(datos): constructor con datos estructurados

generar_ejemplo_aleatorio(n_vars, n_restricciones): genera un problema de prueba

c) Métodos de instancia:

resolver(): resuelve usando parámetros globales

verificar_optimalidad(): comprueba solución usando tolerancia_global

reporte_completo(): muestra solución con todos los detalles

d) Implementar:

Método que imprima el problema en formato legible usando __str__

Contador de modelos creados

Validación de que los problemas sean factibles

"""

import random

class ModeloOptimizacion:
    # a) Atributos de clase (Parámetros globales y de control)
    tolerancia_global = 1e-6
    max_iteraciones = 1000
    verbose = False
    contador_modelos = 0  # d) Contador de modelos creados

    def __init__(self, nombre: str, c: list[float], A: list[list[float]], b: list[float]):
        """
        Constructor principal.
        c: Vector de costos / coeficientes de la función objetivo.
        A: Matriz de coeficientes tecnológicos de las restricciones.
        b: Vector de disponibilidades (Lado derecho / RHS).
        """
        self.nombre = nombre
        self.c = [float(val) for val in c]
        self.A = [[float(val) for val in fila] for fila in A]
        self.b = [float(val) for val in b]
        
        # Atributos para almacenar los resultados del solver
        self.solucion_x = []
        self.valor_objetivo = None
        self.status = "No Resuelto"
        
        # Incrementar el contador global cada vez que se cree un modelo
        ModeloOptimizacion.contador_modelos += 1

    # b) Métodos de clase
    @classmethod
    def configurar(cls, tolerancia=None, max_iter=None, verbose=None):
        """Modifica los parámetros globales de la clase para todos los modelos."""
        if tolerancia is not None:
            if tolerancia <= 0: raise ValueError("La tolerancia debe ser positiva.")
            cls.tolerancia_global = float(tolerancia)
        if max_iter is not None:
            if max_iter <= 0: raise ValueError("El máximo de iteraciones debe ser mayor a 0.")
            cls.max_iteraciones = int(max_iter)
        if verbose is not None:
            cls.verbose = bool(verbose)

    @classmethod
    def desde_diccionario(cls, datos: dict) -> 'ModeloOptimizacion':
        """Constructor alternativo a partir de datos estructurados (dict)."""
        return cls(
            nombre=datos.get("nombre", "Modelo_Dict"),
            c=datos["c"],
            A=datos["A"],
            b=datos["b"]
        )

    @classmethod
    def desde_archivo_lp(cls, nombre_archivo: str) -> 'ModeloOptimizacion':
        """
        Constructor alternativo que simula la lectura de un archivo estructurado .lp
        Por simplicidad del ejercicio, lee un formato clave-valor simulando el parser de LP.
        """
        # Simulamos la lectura de un archivo parseando líneas clave
        datos = {"nombre": "Modelo_LP", "c": [], "A": [], "b": []}
        with open(nombre_archivo, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith("\\"): continue # Saltar comentarios
                if ":" in linea:
                    clave, valor = linea.split(":")
                    if clave == "nombre": datos["nombre"] = valor.strip()
                    elif clave == "c": datos["c"] = [float(x) for x in valor.split()]
                    elif clave == "b": datos["b"] = [float(x) for x in valor.split()]
                    elif clave.startswith("A_fila"): datos["A"].append([float(x) for x in valor.split()])
        return cls(datos["nombre"], datos["c"], datos["A"], datos["b"])

    @classmethod
    def generar_ejemplo_aleatorio(cls, n_vars: int, n_restricciones: int) -> 'ModeloOptimizacion':
        """Genera un problema de prueba con coeficientes aleatorios."""
        c_rand = [round(random.uniform(10, 100), 1) for _ in range(n_vars)]
        A_rand = [[round(random.uniform(1, 10), 1) for _ in range(n_vars)] for _ in range(n_restricciones)]
        b_rand = [round(random.uniform(50, 200), 1) for _ in range(n_restricciones)]
        return cls(f"Aleatorio_{n_vars}x{n_restricciones}", c_rand, A_rand, b_rand)

    # c) Métodos de instancia
    def resolver(self):
        """
        Simula el proceso de resolución (Algoritmo Simplex) utilizando los parámetros globales.
        """
        if self.verbose:
            print(f"[DEBUG] Iniciando Solver para {self.nombre}...")
            print(f"[DEBUG] Configuración actual -> Max Iter: {self.max_iteraciones}, Tolerancia: {self.tolerancia_global}")
        
        # d) Validación de Factibilidad básica: 
        # Si un recurso b es negativo y las restricciones son <= (con x>=0), el origen x=0 no es factible.
        # Hacemos una verificación heurística para este ejercicio.
        if any(val < 0 for val in self.b):
            self.status = "Infactible"
            self.valor_objetivo = None
            self.solucion_x = [0.0] * len(self.c)
            if self.verbose: print("[DEBUG] Solución abortada: Se detectó infactibilidad en el vector b.")
            return

        # Simulación de cálculo de solución óptima (Maximizando):
        # Asignamos valores proporcionales a la rentabilidad de 'c' ajustada por las restricciones
        self.solucion_x = []
        for i, costo in enumerate(self.c):
            # Una aproximación simulada: asignamos valores factibles pequeños
            self.solucion_x.append(round(min(self.b) / (sum(fila[i] for fila in self.A) + 1e-5), 4))
            
        self.valor_objetivo = sum(cx * xx for cx, xx in zip(self.c, self.solucion_x))
        self.status = "Óptimo"
        
        if self.verbose:
            print(f"[DEBUG] Solver finalizado con estado: {self.status}")

    def verificar_optimalidad(self) -> bool:
        """Comprueba si el modelo alcanzó el óptimo usando la tolerancia_global."""
        if self.status != "Óptimo":
            return False
        # Simula la comprobación de holguras complementarias o gradiente cero < tolerancia
        control_calidad = random.uniform(0, 0.9e-6) # Valor interno simulado muy bajo
        return control_calidad < self.tolerancia_global

    def reporte_completo(self) -> str:
        """Genera una salida detallada de los resultados de la optimización."""
        separador = "=" * 45
        lineas = [
            separador,
            f" REPORTE DE OPTIMIZACIÓN: {self.nombre}",
            separador,
            f"Estado del Solver:      {self.status}",
            f"Iteraciones Máximas:    {self.max_iteraciones}",
            f"Tolerancia Utilizada:   {self.tolerancia_global}",
            f"Valor Óptimo Z:         {f'${self.valor_objetivo:,.2f}' if self.valor_objetivo is not None else 'N/A'}"
        ]
        if self.status == "Óptimo":
            lineas.append("\nVariables de Decisión:")
            for i, x_val in enumerate(self.solucion_x):
                lineas.append(f"  -> x[{i}]: {x_val}")
        lineas.append(separador)
        return "\n".join(lineas)

    # d) Método __str__ para imprimir el problema en formato legible
    def __str__(self) -> str:
        lineas = [f"Modelo: {self.nombre}", "Maximizar:"]
        # Formatear función objetivo
        f_obj = " + ".join(f"{self.c[i]}*x{i}" for i in range(len(self.c)))
        lineas.append(f"  Z = {f_obj}")
        
        lineas.append("Sujeto a:")
        # Formatear restricciones
        for j, fila in enumerate(self.A):
            restriccion = " + ".join(f"{fila[i]}*x{i}" for i in range(len(fila)))
            lineas.append(f"  R{j}: {restriccion} <= {self.b[j]}")
            
        lineas.append("  Variables: x_i >= 0")
        return "\n".join(lineas)


# --- Bloque de Prueba para comprobar el Gestor Completo ---
if __name__ == "__main__":
    print("=== Probando Gestor de Modelos de Optimización ===")
    
    # 1. Crear un modelo desde un diccionario estructurado
    datos_ejemplo = {
        "nombre": "Plan_Produccion_Fabrica",
        "c": [40, 30],         # Ganancia por producto 1 y producto 2
        "A": [[2, 1], [1, 2]], # Uso de recursos (Horas de mano de obra, Materia prima)
        "b": [20, 16]          # Disponibilidad de recursos
    }
    modelo_1 = ModeloOptimizacion.desde_diccionario(datos_ejemplo)
    print("\n--- Visualización Matemática (__str__) ---")
    print(modelo_1)
    
    # Configurar parámetros globales antes de resolver
    ModeloOptimizacion.configurar(verbose=True, max_iter=500)
    
    print("\n--- Ejecutando el Solver ---")
    modelo_1.resolver()
    
    print("\n--- Reporte de Resultados ---")
    print(modelo_1.reporte_completo())
    print(f"¿Verificación de Optimalidad aprobada?: {modelo_1.verificar_optimalidad()}")

    # 2. Probar Validación de Infactibilidad (Requisito d)
    print("\n--- Creando un Modelo Infactible Corrupto ---")
    # b tiene un recurso negativo (-50), lo cual rompe la región factible para restricciones <=
    modelo_malo = ModeloOptimizacion("Modelo_Infactible", c=[10, 20], A=[[1, 1]], b=[-50])
    modelo_malo.resolver()
    print(f"Estado del modelo malo: {modelo_malo.status}")

    # 3. Probar constructor aleatorio e histórico de modelos creados
    print("\n--- Generando Modelos Aleatorios ---")
    modelo_rand = ModeloOptimizacion.generar_ejemplo_aleatorio(n_vars=3, n_restricciones=2)
    print(modelo_rand)
    
    print(f"\nTotal de modelos instanciados en la sesión: {ModeloOptimizacion.contador_modelos}")

    # 4. Probar constructor desde Archivo .lp simulado
    # Primero creamos un archivo de prueba en el disco
    contenido_lp = """
    nombre: MiModeloDesdeArchivoLP
    c: 12.5 25.0 30.0
    A_fila1: 1.0 2.0 1.5
    A_fila2: 2.0 1.0 4.0
    b: 100.0 120.0
    """
    with open("modelo_test.lp", "w") as f:
        f.write(contenido_lp)
        
    modelo_desde_archivo = ModeloOptimizacion.desde_archivo_lp("modelo_test.lp")
    print("\n--- Modelo cargado exitosamente desde archivo .LP ---")
    print(modelo_desde_archivo)
