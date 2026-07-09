"""
Ejercicio 41: Evaluación de Riesgo con Diferentes Métricas

Crea una clase MetricaRiesgo con un método calcular(rendimientos) que lance NotImplementedError.

Implementa tres métricas:

1. VaR: Value at Risk (percentil 5% de los rendimientos)

2. CVaR: Conditional VaR (promedio de pérdidas más allá del VaR)

3. SharpeRatio: (rendimiento_promedio - tasa_libre_riesgo) / desviación_estándar

Crea una función polimórfica evaluar_riesgo(metrica, rendimientos) que reciba cualquier métrica
y retorne el resultado.

"""

import numpy as np

# --- CLASE BASE (INTERFAZ) ---
class MetricaRiesgo:
    """Clase base que define la estructura para cualquier métrica de riesgo."""
    def calcular(self, rendimientos, **kwargs):
        raise NotImplementedError("Las subclases deben implementar el método calcular().")


# --- CLASES HIJAS (MÉTRICAS ESPECÍFICAS) ---

class MetricaVaR(MetricaRiesgo):
    """Value at Risk (VaR) al 95% de confianza (percentil 5 de los rendimientos)."""
    def calcular(self, rendimientos, nivel_confianza=0.95):
        # El VaR al 95% busca el peor 5% de los escenarios (percentil 5)
        percentil = (1 - nivel_confianza) * 100
        var_resultado = np.percentile(rendimientos, percentil)
        return var_resultado


class MetricaCVaR(MetricaRiesgo):
    """Conditional Value at Risk (CVaR) o Expected Shortfall.
       Promedio de los rendimientos que son peores que el VaR.
    """
    def calcular(self, rendimientos, nivel_confianza=0.95):
        # 1. Primero calculamos el VaR para usarlo como límite
        percentil = (1 - nivel_confianza) * 100
        var_limite = np.percentile(rendimientos, percentil)
        
        # 2. Filtramos solo los rendimientos que caen por debajo (peores) que ese VaR
        peores_rendimientos = rendimientos[rendimientos <= var_limite]
        
        # 3. Retornamos el promedio de esas pérdidas extremas
        return np.mean(peores_rendimientos)


class MetricaSharpe(MetricaRiesgo):
    """Sharpe Ratio: Mide el retorno excedente por unidad de riesgo."""
    def calcular(self, rendimientos, tasa_libre_riesgo=0.0):
        promedio = np.mean(rendimientos)
        desviacion = np.std(rendimientos)
        
        if desviacion == 0:
            return 0.0
            
        # Fórmula: (Rp - Rf) / Sigma
        sharpe_ratio = (promedio - tasa_libre_riesgo) / desviacion
        return sharpe_ratio


# --- FUNCIÓN POLIMÓRFICA SOLICITADA ---
def evaluar_riesgo(metrica, rendimientos, **kwargs):
    """
    Función polimórfica que no sabe qué métrica está operando,
    solo confía en que tiene el método .calcular()
    """
    return metrica.calcular(rendimientos, **kwargs)


# --- EJEMPLO DE USO / PRUEBA ---
if __name__ == "__main__":
    # Simulamos rendimientos diarios de un activo (un array de numpy)
    # Algunos días gana (0.01 = 1%), otros días pierde (-0.02 = -2%)
    np.random.seed(42)  # Para que los resultados sean siempre iguales
    rendimientos_simulados = np.random.normal(loc=0.0005, scale=0.015, size=1000)

    # Instanciamos nuestras métricas
    var_95 = MetricaVaR()
    cvar_95 = MetricaCVaR()
    sharpe = MetricaSharpe()

    # Evaluamos usando la función polimórfica
    # Nota cómo usamos **kwargs para pasar parámetros específicos de algunas métricas
    resultado_var = evaluar_riesgo(var_95, rendimientos_simulados, nivel_confianza=0.95)
    resultado_cvar = evaluar_riesgo(cvar_95, rendimientos_simulados, nivel_confianza=0.95)
    resultado_sharpe = evaluar_riesgo(sharpe, rendimientos_simulados, tasa_libre_riesgo=0.0001)

    print("--- RESULTADOS DE LA EVALUACIÓN DE RIESGO ---")
    print(f"Value at Risk (VaR 95%):      {resultado_var * 100:.2f}% (En el peor 5% de los días, perderás al menos esto)")
    print(f"Conditional VaR (CVaR 95%):  {resultado_cvar * 100:.2f}% (Si superas el VaR, esta es la pérdida promedio)")
    print(f"Sharpe Ratio (Anualizado):   {resultado_sharpe:.4f}")
