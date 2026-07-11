"""Ejercicio 52: Sistema de optimización con Múltiples Metaheuríticas

Crea un framework de optimización usando composición:

1. Clase OperadorMutacion: Componente que aplica mutaciones
    - Implementaciones: MutacionUniforme, MutacionGaussiana, MutacionAleatoria

2. Clase OperadorCruce: Componente que combina soluciones
    - Implementaciones: CruceUniforme, CrucePunto, CruceAritmetico

3. Clase OperadorSeleccion: Componente que selecciona individuos
    - Implementaciones: SeleccionTorneo, SeleccionRuleta, SeleccionRanking

4. Clase AlgoritmoGenetico: Compone los operadores anteriores
    - Método: evolucionar(poblacion, generaciones)

    """

import random

# ==========================================
# 1. COMPONENTES: OPERADORES DE MUTACIÓN
# ==========================================
class OperadorMutacion:
    def mutar(self, individuo, tasa_mutacion):
        raise NotImplementedError

class MutacionUniforme(OperadorMutacion):
    def mutar(self, individuo, tasa_mutacion):
        # Altera un gen sumando o restando un valor fijo uniforme
        return [gen + random.uniform(-0.5, 0.5) if random.random() < tasa_mutacion else gen for gen in individuo]

class MutacionGaussiana(OperadorMutacion):
    def mutar(self, individuo, tasa_mutacion):
        # Altera un gen usando una distribución normal (cambios más biológicos/naturales)
        return [gen + random.gauss(0, 0.2) if random.random() < tasa_mutacion else gen for gen in individuo]


# ==========================================
# 2. COMPONENTES: OPERADORES DE CRUCE
# ==========================================
class OperadorCruce:
    def cruzar(self, padre1, padre2):
        raise NotImplementedError

class CrucePunto(OperadorCruce):
    def cruzar(self, padre1, padre2):
        # Corta a la mitad y combina
        punto = len(padre1) // 2
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2

class CruceAritmetico(OperadorCruce):
    def cruzar(self, padre1, padre2):
        # Promedia los valores de ambos padres (cruce continuo)
        hijo1 = [p1 * 0.7 + p2 * 0.3 for p1, p2 in zip(padre1, padre2)]
        hijo2 = [p1 * 0.3 + p2 * 0.7 for p1, p2 in zip(padre1, padre2)]
        return hijo1, hijo2


# ==========================================
# 3. COMPONENTES: OPERADORES DE SELECCIÓN
# ==========================================
class OperadorSeleccion:
    def seleccionar(self, poblacion, aptitudes, k):
        raise NotImplementedError

class SeleccionTorneo(OperadorSeleccion):
    def seleccionar(self, poblacion, aptitudes, k=3):
        # Elige 'k' individuos al azar y el de mejor aptitud gana el torneo
        aspirantes = random.sample(list(zip(poblacion, aptitudes)), k)
        aspirantes.sort(key=lambda x: x[1], reverse=True) # Ordenar de mayor a menor aptitud
        return aspirantes[0][0] # Retorna el cromosoma ganador


# ==========================================
# 4. CLASE PRINCIPAL: ALGORITMO GENÉTICO (EL FRAMEWORK)
# ==========================================
class AlgoritmoGenetico:
    """Clase que compone los tres tipos de operadores mediante composición."""
    def __init__(self, seleccion: OperadorSeleccion, cruce: OperadorCruce, mutacion: OperadorMutacion, tasa_mutacion=0.1):
        self.seleccion = seleccion
        self.cruce = cruce
        self.mutacion = mutacion
        self.tasa_mutacion = tasa_mutacion

    def funcion_aptitud(self, individuo):
        """Función objetivo ficticia a optimizar. 
        Por ejemplo, queremos que la suma de los genes sea lo más cercana a 100."""
        objetivo = 100.0
        suma = sum(individuo)
        # Retornamos un valor de aptitud inversamente proporcional al error (mayor es mejor)
        return 1.0 / (1.0 + abs(objetivo - suma))

    def evolucionar(self, poblacion, generaciones):
        """Ejecuta el ciclo de vida evolutivo."""
        print(f"--- Iniciando Evolución ---")
        print(f"Configuración de Metaheurística:")
        print(f" └─ Selección: {self.seleccion.__class__.__name__}")
        print(f" └─ Cruce:     {self.cruce.__class__.__name__}")
        print(f" └─ Mutación:  {self.mutacion.__class__.__name__}\n")

        for gen in range(1, generaciones + 1):
            # 1. Evaluar aptitud de la población actual
            aptitudes = [self.funcion_aptitud(ind) for ind in poblacion]
            
            # Guardar el mejor para reportar progreso
            mejor_aptitud = max(aptitudes)
            mejor_ind = poblacion[aptitudes.index(mejor_aptitud)]
            
            if gen % 5 == 0 or gen == 1:
                print(f"Generación {gen:02d} | Mejor Aptitud: {mejor_aptitud:.4f} | Suma genes: {sum(mejor_ind):.2f}")

            # 2. Crear la nueva generación (Nueva Población)
            nueva_poblacion = []
            while len(nueva_poblacion) < len(poblacion):
                # Selección
                padre1 = self.seleccion.seleccionar(poblacion, aptitudes)
                padre2 = self.seleccion.seleccionar(poblacion, aptitudes)
                
                # Cruce
                hijo1, hijo2 = self.cruce.cruzar(padre1, padre2)
                
                # Mutación
                hijo1 = self.mutacion.mutar(hijo1, self.tasa_mutacion)
                hijo2 = self.mutacion.mutar(hijo2, self.tasa_mutacion)
                
                nueva_poblacion.extend([hijo1, hijo2])
            
            # Ajustar tamaño en caso de pasarnos por el par de hijos
            poblacion = nueva_poblacion[:len(poblacion)]
            
        # Retornar el campeón final
        aptitudes_finales = [self.funcion_aptitud(ind) for ind in poblacion]
        mejor_final = poblacion[aptitudes_finales.index(max(aptitudes_finales))]
        return mejor_final

# Crear una población inicial aleatoria: 20 individuos con 4 genes cada uno
poblacion_inicial = [[random.uniform(10, 30) for _ in range(4)] for _ in range(20)]

print("PROBANDO CONFIGURACIÓN A:")
# Combinación A: Torneo + Cruce de Punto + Mutación Gaussiana
ag_config_A = AlgoritmoGenetico(
    seleccion=SeleccionTorneo(),
    cruce=CrucePunto(),
    mutacion=MutacionGaussiana(),
    tasa_mutacion=0.15
)
campeon_A = ag_config_A.evolucionar(list(poblacion_inicial), generaciones=15)
print(f"Resultado Campeón A: {campeon_A} (Suma: {sum(campeon_A):.2f})\n")


print("PROBANDO CONFIGURACIÓN B (Mismo problema, diferentes operadores):")
# Combinación B: Torneo + Cruce Aritmético + Mutación Uniforme
ag_config_B = AlgoritmoGenetico(
    seleccion=SeleccionTorneo(),
    cruce=CruceAritmetico(),
    mutacion=MutacionUniforme(),
    tasa_mutacion=0.2
)
campeon_B = ag_config_B.evolucionar(list(poblacion_inicial), generaciones=15)
print(f"Resultado Campeón B: {campeon_B} (Suma: {sum(campeon_B):.2f})")
