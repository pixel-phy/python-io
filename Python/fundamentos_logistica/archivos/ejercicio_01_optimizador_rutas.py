"""Optimizador de rutas:
    En IO, antes de correr un algoritmo que calcule la ruta más barata para una flota de camiones, necesitas leer las ubicaciones
    y pasárelas al modelo. Tenemos la siguiente lista de nodos (ciudades y coordenadas de entrega x,y):

    nodos_entrega = ["Bogota:4.71,-74.07", "Medellin:6.25,-75.56", "Cali:3.43,-76.52"]

    Escribir un script que use writelines() para guardar estos nodos en un archivo llamado red_transporte.txt. Cada nodo debe quedar en 
    una línea separada. """

archivo = open("output/red_transporte.txt", mode="w", encoding="utf-8")

nodos_entrega = ["Bogota:4.71,-74.07", "Medellin:6.25,-75.56", "Cali:3.43,-76.52"]

nodos_con_salto = [f"{nodo}\n" for nodo in nodos_entrega]

archivo.writelines(nodos_con_salto)

archivo.close()

