"""Understanding Shape and Reshape

Comprender la forma de una matriz es como conocer el tamaño de una caja: nos indica cómo podemos 
manipularla. Por otro lado, redimensionar una matriz es como cambiar las dimensiones de la caja
para adaptarla a nuestras necesidades.
    """

import numpy as np

# Arreglo de juguetes
juguetes = np.array(["oso teddy", "robot", "muñeca", "pelota", "yo-yo"])

# Mostramos el número de juguetes
print("Número de juguetes:", juguetes.shape)

# Dividimos en dos cajas (forma de matriz)
cajas_juguetes = np.array([["oso teddy", "robot", "carro"], 
                           ["muñeca", "pelota", "yo-yo"]])

# Imprimimos Shape de la caja de juguetes
print("Dimensiones de las cajas:", cajas_juguetes.shape)

# Reshape
juguetes1 = np.array(["oso teddy", "robot", "muñeca", "pelota", "yo-yo", "carro"])
cajas_juguetes1 = juguetes1.reshape(3, 2)

print(cajas_juguetes1)
