"""Ejercicio 18: Ventanas de tiempo en Entregas

En problemas de optimización de rutas, cada cliente tiene una ventana de tiempo [inicio, fin]
en la que debe ser atendido. Si el chofer llega después de la hora de fin, la restricción se rompe.
    - Escribe una función que reciba la hora de llegada del chofer y una tupla con la ventana permitida
    (inicio, fin). Debe retornar True si es factible o False si se viola la restricción.

    Input de prueba: LLegada: 600, Ventana: (400, 570) (Debe ser False porque llegó tarde). """

def validar_ventana_tiempo(llegada: int, ventana: tuple[int, int])-> bool:
    """
        Valida si la hora de llegada está dentro de la ventana de tiempo permitida.

        Args:
            llegada (int): Hora de llegada en minutos desde el inicio del día
            ventana (tuple): Tupla (inicio, fin) con los limites de la ventana en minutos

        Returns:
            bool: True si la llegada está dentro de la ventana, False en caso contrario
    """

    inicio, fin = ventana

    return inicio <= llegada <= fin

# Prueba

llegada = 600
ventana = (480, 570)
resultado = validar_ventana_tiempo(llegada, ventana)

print(f"Llegada: {llegada} minutos")
print(f"Ventana: {ventana}")
print(f"¿Es factible? : {resultado}")
