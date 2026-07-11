"""Ejercicio 20: Métodos estáticos de Distancia

Crea una clase CalculadoraDistancia con métodos estáticos:
- distancia_auclidiana(x1, y1, x2, y2): Calcula distancia euclidiana.
- distancia_manhattan(x1, y1, x2, y2): Calcula distancia Manhattan.
- distancia_chebyshev(x1, y1, x2, y2): Calcula distancia Chebyshev
- formatear_distancia(valor): Formatea mostrando 2 decimales y unidad "km"
- validar_coordenadas(x, y): Verifica que las coordenadas sean números válidos.
"""

import math

class CalculadoraDistancia:

    @staticmethod
    def distancia_euclidiana(x1, y1, x2, y2):
        """Calcula la distancia en línea recta (línea de un mapa)."""
        # Fórmula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    @staticmethod
    def distancia_manhattan(x1, y1, x2, y2):
        """Calcula la distancia moviéndose solo en ángulos rectos (como en una ciudad)."""
        # Fórmula: |x2 - x1| + |y2 - y1|
        return abs(x2 - x1) + abs(y2 - y1)

    @staticmethod
    def distancia_chebyshev(x1, y1, x2, y2):
        """Calcula la distancia considerando el máximo movimiento en cualquier eje (como el Rey en ajedrez)."""
        # Fórmula: max(|x2 - x1|, |y2 - y1|)
        return max(abs(x2 - x1), abs(y2 - y1))

    @staticmethod
    def formatear_distancia(valor):
        """Formatea mostrando 2 decimales y la unidad 'km'."""
        return f"{valor:.2f} km"

    @staticmethod
    def validar_coordenadas(x, y):
        """Verifica que las coordenadas sean números válidos (int o float)."""
        return isinstance(x, (int, float)) and isinstance(y, (int, float))
# Prueba
# 1. Definimos algunos puntos
p1_x, p1_y = 1.5, 2.0
p2_x, p2_y = 4.5, 6.0

# 2. Validamos que las coordenadas sean correctas
if CalculadoraDistancia.validar_coordenadas(p1_x, p1_y) and CalculadoraDistancia.validar_coordenadas(p2_x, p2_y):
    
    # 3. Calculamos las distancias
    dist_euclidiana = CalculadoraDistancia.distancia_euclidiana(p1_x, p1_y, p2_x, p2_y)
    dist_manhattan = CalculadoraDistancia.distancia_manhattan(p1_x, p1_y, p2_x, p2_y)
    dist_chebyshev = CalculadoraDistancia.distancia_chebyshev(p1_x, p1_y, p2_x, p2_y)
    
    # 4. Mostramos los resultados formateados
    print(f"Distancia Euclidiana: {CalculadoraDistancia.formatear_distancia(dist_euclidiana)}")
    print(f"Distancia Manhattan:  {CalculadoraDistancia.formatear_distancia(dist_manhattan)}")
    print(f"Distancia Chebyshev:  {CalculadoraDistancia.formatear_distancia(dist_chebyshev)}")
else:
    print("Error: Una o más coordenadas no son números válidos.")
