"""
Ejercicio 39: Diferentes métodos de Solución para Problemas de Transporte

Define una clase ProblemaTransporte con atributos costos (matriz), oferta (lista), demanda (lista)
y un método resolver() que imprima "Resolviendo problema de transporte...".

Crea dos clases hijas:

- MetodoEsquinaNoroeste: Sobrescribe resolver() para implementar el método de la esquina noroeste
  (solución inicial factible).

- MetodoVogel: Sobrescribe resolver() para implementar el método de aproximación de Vogel.

"""

import numpy as np

class ProblemaTransporte:
    """Clase base para representar un problema de transporte."""
    def __init__(self, costos, oferta, demanda):
        # Convertimos a arreglos de numpy para facilitar la manipulación matemática
        self.costos = np.array(costos, dtype=float)
        self.oferta = np.array(oferta, dtype=float)
        self.demanda = np.array(demanda, dtype=float)
        
        # Validar si el problema está balanceado
        if sum(self.oferta) != sum(self.demanda):
            print("Advertencia: El problema no está balanceado (Oferta != Demanda).")

    def resolver(self):
        print("Resolviendo problema de transporte...")
        return None


class MetodoEsquinaNoroeste(ProblemaTransporte):
    """Clase hija que implementa el algoritmo de la Esquina Noroeste."""
    def resolver(self):
        super().resolver()
        print("-> Ejecutando Método de la Esquina Noroeste...")
        
        # Copias locales para no modificar los datos originales
        oferta_local = self.oferta.copy()
        demanda_local = self.demanda.copy()
        
        filas, columnas = self.costos.shape
        x = np.zeros((filas, columnas))  # Matriz de asignación de flujos
        
        i, j = 0, 0
        while i < filas and j < columnas:
            # Asignar lo máximo posible (el mínimo entre la oferta y demanda actual)
            asignacion = min(oferta_local[i], demanda_local[j])
            x[i, j] = asignacion
            
            oferta_local[i] -= asignacion
            demanda_local[j] -= asignacion
            
            # Moverse en la matriz según quién se haya agotado
            if oferta_local[i] == 0:
                i += 1
            elif demanda_local[j] == 0:
                j += 1
                
        self._imprimir_resultados(x)
        return x

    def _imprimir_resultados(self, matriz_asignacion):
        costo_total = np.sum(matriz_asignacion * self.costos)
        print("Matriz de Asignación Final:")
        print(matriz_asignacion)
        print(f"Costo Total Inicial: ${costo_total:.2f}\n")


class MetodoVogel(ProblemaTransporte):
    """Clase hija que implementa el Método de Aproximación de Vogel (VAM)."""
    def resolver(self):
        super().resolver()
        print("-> Ejecutando Método de Aproximación de Vogel...")
        
        oferta_local = self.oferta.copy()
        demanda_local = self.demanda.copy()
        filas, columnas = self.costos.shape
        x = np.zeros((filas, columnas))
        
        # Filas y columnas activas (que aún tienen oferta/demanda)
        filas_activas = list(range(filas))
        columnas_activas = list(range(columnas))
        
        while filas_activas and columnas_activas:
            penalizaciones_filas = {}
            penalizaciones_columnas = {}
            
            # 1. Calcular penalizaciones de filas (diferencia entre los dos costos más bajos)
            for i in filas_activas:
                costos_disponibles = sorted([self.costos[i, j] for j in columnas_activas])
                if len(costos_disponibles) > 1:
                    penalizaciones_filas[i] = costos_disponibles[1] - costos_disponibles[0]
                else:
                    penalizaciones_filas[i] = costos_disponibles[0]
                    
            # 2. Calcular penalizaciones de columnas
            for j in columnas_activas:
                costos_disponibles = sorted([self.costos[i, j] for i in filas_activas])
                if len(costos_disponibles) > 1:
                    penalizaciones_columnas[j] = costos_disponibles[1] - costos_disponibles[0]
                else:
                    penalizaciones_columnas[j] = costos_disponibles[0]
            
            # 3. Identificar la penalización máxima
            max_p_fila = max(penalizaciones_filas.values()) if penalizaciones_filas else -1
            max_p_col = max(penalizaciones_columnas.values()) if penalizaciones_columnas else -1
            
            if max_p_fila >= max_p_col:
                # La fila con mayor penalización
                i_sel = max(penalizaciones_filas, key=penalizaciones_filas.get)
                # Buscar el costo mínimo en esa fila entre las columnas activas
                j_sel = min(columnas_activas, key=lambda c: self.costos[i_sel, c])
            else:
                # La columna con mayor penalización
                j_sel = max(penalizaciones_columnas, key=penalizaciones_columnas.get)
                # Buscar el costo mínimo en esa columna entre las filas activas
                i_sel = min(filas_activas, key=lambda f: self.costos[f, j_sel])
                
            # 4. Asignar flujo
            asignacion = min(oferta_local[i_sel], demanda_local[j_sel])
            x[i_sel, j_sel] = asignacion
            
            oferta_local[i_sel] -= asignacion
            demanda_local[j_sel] -= asignacion
            
            # 5. Eliminar filas o columnas agotadas
            if oferta_local[i_sel] == 0:
                filas_activas.remove(i_sel)
            elif demanda_local[j_sel] == 0:
                columnas_activas.remove(j_sel)
                
        self._imprimir_resultados(x)
        return x

    def _imprimir_resultados(self, matriz_asignacion):
        costo_total = np.sum(matriz_asignacion * self.costos)
        print("Matriz de Asignación Final:")
        print(matriz_asignacion)
        print(f"Costo Total Inicial: ${costo_total:.2f}\n")


# --- PRUEBA DEL SISTEMA ---
if __name__ == "__main__":
    # Matriz de costos de ejemplo (3 orígenes, 4 destinos)
    matriz_costos = [
        [2, 3, 11, 7],
        [1, 0,  6, 1],
        [5, 8, 15, 9]
    ]
    oferta = [6, 1, 10]
    demanda = [7, 5, 3, 2]

    # Ejecución con la Esquina Noroeste
    problema_noroeste = MetodoEsquinaNoroeste(matriz_costos, oferta, demanda)
    problema_noroeste.resolver()
    
    print("-" * 40)
    
    # Ejecución con Vogel
    problema_vogel = MetodoVogel(matriz_costos, oferta, demanda)
    problema_vogel.resolver()
