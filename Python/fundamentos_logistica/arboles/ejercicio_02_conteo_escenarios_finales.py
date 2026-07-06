"""Ejercicio 02: Conteo de Escenarios Finales

En un árbol de decisiones de inversión en inventario, las hojas representan los escenarios de demanda final
(Baja, Media, Alta). Escribe una función llamada contar_escenarios_finales(nodo) que reciba el nodo raíz y devuelva 
el número total de hojas (nodos que no tienen hijos). """

class Nodo:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos if hijos is not None else []

def contar_escenarios_finales(nodo):
    """
        Cuenta el número de hojas (nodos sin hijos) en un árbol de decisiones.

        Args: 
            nodo: Nodo raíz del árbol

        Returns:
            int: Número total de hojas
    """
    # Caso base: si el nodo no tiene hijos, es una hoja
    if not nodo.hijos:
        return 1

    # Caso recursivo: sumar las hojas de todos los hijos
    return sum(contar_escenarios_finales(hijo) for hijo in nodo.hijos)

# Pruebas:
# Se construye el árbol
hoja_baja = Nodo("Demanda Baja")
hoja_media = Nodo("Demanda Media")
hoja_alta = Nodo("Demanda Alta")

nodo_optimista = Nodo("Mercado optimista", [hoja_media, hoja_alta])
nodo_pesimista = Nodo("Mercado pesimista", [hoja_baja])

raiz = Nodo("Inversión", [nodo_optimista, nodo_pesimista])

# Prueda de la fucnión
print(f"Total de esceinarios finales: {contar_escenarios_finales(raiz)}")
