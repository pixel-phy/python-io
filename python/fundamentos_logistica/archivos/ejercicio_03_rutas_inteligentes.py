"""Rutas Inteligentas con pathlib

En IO, un script puede requerir un archivo de datos que está en otra carpeta. Usar cadenas de texto como 
"archivos/datos.txt" es peligroso porque Windows usa diagonales invertidas (\) y Linux/Mac usando diagonales
(/). La librería nativa pathlib soluciona esto creando objetos de ruta independientes del sistema operativo.

 from pathlib import Path 

 # Definimos una ruta hacia la carpeta 'datos' y el archivo 'modelo.dat'
    ruta_archivo = Path("datos" / "modelo.dat")"""
