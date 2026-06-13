"""El grabador de Simulación (Uso crítico de flush())

En IO se hacen simulaciones de Montecarlo (Por ejemplo, simular el tráfico de un aeropuerto por 24 horas
para ver cuántas salas de abordaje se necesitan). Estas simulaciones pueden tardar horas en completarse
y consumen mucha CPU.
    Escribe un script que simule el paso del tiempo en una fila de banco.
    1. Abre un archivo llamado simulacion_colas.log en modo a.
    2. Escribe la línea: "Simulación iniciada: Minuto 1 - Llegaron 5 clientes. \n".
    3. Aplica flush() inmediatamente. 
    4. Cierra el archivo final. """

# Abrimos el archivo en la ruta específica
archivo_simulacion = open("output/simulacion_colas.log", mode="a", encoding="utf-8")

# Agregamos el texto
archivo_simulacion.write("Simulación iniciada: Minuto 1 - Llegaron 5 clientes.\n")

# Grabamos en disco duro 
archivo_simulacion.flush()

# Cerramos archivo
archivo_simulacion.close()
