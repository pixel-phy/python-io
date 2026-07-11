"""Ejercicio 53: Modelo de Red con Capas

Diseña un sistema de redes neuronales para problemas de IO usando composición:

1. Clase Capa: Componente que representa una capa de la red
    - Métodos: forward(x), backward(grad), actualizar_pesos(lr)

2. Implementaciones: CapaDensa, CapaActivacion, CapaDropout

3. Clase RedNeuronal: Compone múltiples capas
    - Método: predecir(x), entrenar(X, y, epochs)

4. Aplicación a IO: Usar para predecir demanda, tiempos de servicio, etc.

    """

import random
import math

# ==========================================
# 1 & 2. COMPONENTES: CAPAS MODULARES
# ==========================================
class Capa:
    """Clase base (interfaz) para todas las capas de la red."""
    def forward(self, x):
        raise NotImplementedError
    
    def backward(self, grad_salida):
        raise NotImplementedError
    
    def actualizar_pesos(self, lr):
        pass  # No todas las capas tienen pesos (ej. Activación o Dropout)


class CapaDensa(Capa):
    """Capa Completamente Conectada (Linear / Dense)."""
    def __init__(self, num_entradas, num_salidas):
        # Inicialización aleatoria simple de Pesos (W) y Sesgos (b)
        self.pesos = [[random.gauss(0, 0.1) for _ in range(num_salidas)] for _ in range(num_entradas)]
        self.sesgos = [0.0 for _ in range(num_salidas)]
        
        # Guardamos la última entrada para calcular las derivadas en el backward
        self.ultima_entrada = None

    def forward(self, x):
        self.ultima_entrada = x
        salida = []
        # Multiplicación de matriz: x * W + b
        for j in range(len(self.sesgos)):
            suma = sum(x[i] * self.pesos[i][j] for i in range(len(x))) + self.sesgos[j]
            salida.append(suma)
        return salida

    def backward(self, grad_salida):
        # 1. Calcular el gradiente respecto a la entrada para pasar a la capa anterior
        grad_entrada = [0.0 for _ in range(len(self.ultima_entrada))]
        for i in range(len(self.ultima_entrada)):
            grad_entrada[i] = sum(grad_salida[j] * self.pesos[i][j] for j in range(len(grad_salida)))
            
        # 2. Guardamos internamente los gradientes de pesos y sesgos para la actualización
        self.grad_pesos = []
        for i in range(len(self.ultima_entrada)):
            fila_grad = [self.ultima_entrada[i] * g_out for g_out in grad_salida]
            self.grad_pesos.append(fila_grad)
        self.grad_sesgos = grad_salida
        
        return grad_entrada

    def actualizar_pesos(self, lr):
        # Descenso de Gradiente Estocástico (SGD)
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[0])):
                self.pesos[i][j] -= lr * self.grad_pesos[i][j]
        for j in range(len(self.sesgos)):
            self.sesgos[j] -= lr * self.grad_sesgos[j]


class CapaActivacionReLU(Capa):
    """Capa que aplica la función no lineal ReLU: f(x) = max(0, x)."""
    def __init__(self):
        self.ultima_salida = None

    def forward(self, x):
        self.ultima_salida = x
        return [max(0.0, valor) for valor in x]

    def backward(self, grad_salida):
        # La derivada de ReLU es 1 si x > 0, de lo contrario es 0
        return [g if x > 0 else 0.0 for x, g in zip(self.ultima_salida, grad_salida)]


class CapaDropout(Capa):
    """Capa de Regularización que apaga neuronas al azar para evitar sobreajuste."""
    def __init__(self, tasa_dropout=0.2):
        self.tasa_dropout = tasa_dropout
        self.mascara = None

    def forward(self, x):
        # Creamos una máscara binaria (1 para activar, 0 para apagar)
        self.mascara = [0.0 if random.random() < self.tasa_dropout else 1.0 for _ in x]
        # Escalamos los valores sobrevivientes para mantener la magnitud de los datos
        escala = 1.0 / (1.0 - self.tasa_dropout) if self.tasa_dropout < 1.0 else 1.0
        return [valor * m * escala for valor, m in zip(x, self.mascara)]

    def backward(self, grad_salida):
        # El gradiente solo fluye por las neuronas que no fueron apagadas
        escala = 1.0 / (1.0 - self.tasa_dropout) if self.tasa_dropout < 1.0 else 1.0
        return [g * m * escala for g, m in zip(grad_salida, self.mascara)]


# ==========================================
# 3. CLASE PRINCIPAL: RED NEURONAL (EL CONTENEDOR)
# ==========================================
class RedNeuronal:
    """Compone una lista ordenada de capas formando una arquitectura profunda."""
    def __init__(self):
        self.capas = []  # Lista de componentes (Composición)

    def agregar_capa(self, capa: Capa):
        self.capas.append(capa)

    def predecir(self, x):
        """Pasa los datos hacia adelante a través de todas las capas (Forward Pass)."""
        salida = x
        for capa in self.capas:
            salida = capa.forward(salida)
        return salida

    def entrenar(self, X, y, epochs, lr=0.01):
        """Bucle de entrenamiento usando MSE (Error Cuadrático Medio) y Backpropagation."""
        print(f"--- Iniciando Entrenamiento de la Red (Composición con {len(self.capas)} capas) ---")
        
        for epoch in range(1, epochs + 1):
            error_total = 0.0
            
            # Entrenamos muestra por muestra (Online Learning / SGD)
            for muestra_x, muestra_y in zip(X, y):
                # 1. Forward Pass
                prediccion = self.predecir(muestra_x)
                
                # Calcular el Error (MSE para salida escalar)
                error_total += sum((p - real) ** 2 for p, real in zip(prediccion, muestra_y))
                
                # 2. Inicializar Gradiente de la función de pérdida (Derivada de MSE respecto a la predicción)
                # dL/dy_pred = 2 * (y_pred - y_real)
                gradiente = [2.0 * (p - real) for p, real in zip(prediccion, muestra_y)]
                
                # 3. Backward Pass (Retropropagación en cadena, del final al principio)
                for capa in reversed(self.capas):
                    gradiente = capa.backward(gradiente)
                
                # 4. Actualización de Parámetros
                for capa in self.capas:
                    capa.actualizar_pesos(lr)
            
            # Reportar el progreso del error cuadrático promedio
            error_promedio = error_total / len(X)
            if epoch % 100 == 0 or epoch == 1:
                print(f"Epoch {epoch:03d} | Error Promedio (Loss): {error_promedio:.6f}")
        print("-" * 70 + "\n")

random.seed(10) # Fijamos semilla para repetibilidad

# Dataset de entrenamiento ficticio [Precio, Publicidad]
# Relación oculta: A menor precio y más publicidad, sube la demanda.
X_train = [
    [10.0, 5.0],
    [25.0, 1.0],
    [12.0, 4.5],
    [30.0, 0.5],
    [8.0,  8.0]
]
# Demanda real correspondiente (Normalizada dividiendo entre 100 por estabilidad numérica)
y_train = [[0.85], [0.20], [0.75], [0.10], [0.98]]

# --- Construcción de la Red mediante Composición ---
modelo_io = RedNeuronal()
modelo_io.agregar_capa(CapaDensa(num_entradas=2, num_salidas=3))
modelo_io.agregar_capa(CapaActivacionReLU())
modelo_io.agregar_capa(CapaDropout(tasa_dropout=0.1))
modelo_io.agregar_capa(CapaDensa(num_entradas=3, num_salidas=1))

# Entrenamos la red por 500 iteraciones
modelo_io.entrenar(X_train, y_train, epochs=500, lr=0.02)

# --- Fase de Predicción (Inferencia) ---
# Escenario de IO: ¿Cuánta demanda tendremos si ponemos un Precio=11.0 y Publicidad=6.0?
escenario_nuevo = [11.0, 6.0]
# Al hacer la predicción final, idealmente desactivaríamos el dropout, pero mantengamos el flujo base:
prediccion_normalizada = modelo_io.predecir(escenario_nuevo)[0]
demanda_estimada = prediccion_normalizada * 100 # Deshacemos la escala

print(f"Resultados del Modelo Operativo:")
print(f" └─ Para Precio: ${escenario_nuevo[0]} y Publicidad: {escenario_nuevo[1]} unidades")
print(f" └─ Demanda Estimada por la Red: {demanda_estimada:.1f} unidades.")
