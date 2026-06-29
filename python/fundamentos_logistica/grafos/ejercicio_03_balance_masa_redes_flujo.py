"""Balance de Masa en Redes de Flujo (Digrafo)

En una red de tuberías de refinamiento de petróleo (Grafo Dirigido), cada nodo tiene un tipo:
    Fuente (produce), Transbordo (pasa el flujo) o Sumidero (consume). Diseña una clase que 
    represente este grafo y una función que valide el Grado de Entrada (In-degree) y Grado de 
Salida (Out-degree) de un nodo específico. """

from enum import Enum
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class TipoNodo(Enum):
    """Tipos de nodos en la red de refinamiento"""
    FUENTE = "fuente"          # Produce petróleo/crudos
    TRANSBORDO = "transbordo"  # Pasa el flujo sin modificar
    SUMIDERO = "sumidero"      # Consume/refina el producto

class RedRefinamiento:
    """
    Clase que representa una red de tuberías de refinamiento de petróleo.
    
    Características:
    - Grafo dirigido (digrafo)
    - Nodos con tipos: fuente, transbordo o sumidero
    - Permite validar grados de entrada y salida
    - Verifica conservación de flujo en nodos de transbordo
    """
    
    def __init__(self):
        """Inicializa la red vacía"""
        # Diccionario de adyacencia: nodo -> lista de (nodo_destino, capacidad)
        self.adyacencias: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        
        # Diccionario inverso para eficiencia: nodo -> lista de (nodo_origen, capacidad)
        self.adyacencias_inversas: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        
        # Almacenar tipos de nodos
        self.tipos_nodos: Dict[str, TipoNodo] = {}
        
        # Capacidades totales por nodo
        self.flujo_entrada: Dict[str, float] = defaultdict(float)
        self.flujo_salida: Dict[str, float] = defaultdict(float)
    
    def agregar_nodo(self, nombre: str, tipo: TipoNodo) -> None:
        """
        Agrega un nodo a la red con su tipo específico
        
        Args:
            nombre: Identificador único del nodo
            tipo: Tipo de nodo (FUENTE, TRANSBORDO, SUMIDERO)
        """
        if nombre in self.tipos_nodos:
            raise ValueError(f"El nodo '{nombre}' ya existe en la red")
        
        self.tipos_nodos[nombre] = tipo
        # Inicializar listas de adyacencia si no existen
        if nombre not in self.adyacencias:
            self.adyacencias[nombre] = []
        if nombre not in self.adyacencias_inversas:
            self.adyacencias_inversas[nombre] = []
    
    def agregar_tuberia(self, origen: str, destino: str, capacidad: float = 1.0) -> None:
        """
        Agrega una tubería dirigida del origen al destino
        
        Args:
            origen: Nodo de inicio
            destino: Nodo de destino
            capacidad: Flujo máximo de la tubería (por defecto 1.0)
        """
        # Validar que los nodos existan
        if origen not in self.tipos_nodos:
            raise ValueError(f"El nodo origen '{origen}' no existe")
        if destino not in self.tipos_nodos:
            raise ValueError(f"El nodo destino '{destino}' no existe")
        
        # Validar que no sea un sumidero como origen o fuente como destino
        if self.tipos_nodos[origen] == TipoNodo.SUMIDERO:
            raise ValueError(f"Un nodo sumidero ('{origen}') no puede tener salidas")
        if self.tipos_nodos[destino] == TipoNodo.FUENTE:
            raise ValueError(f"Un nodo fuente ('{destino}') no puede tener entradas")
        
        # Agregar la arista dirigida
        self.adyacencias[origen].append((destino, capacidad))
        self.adyacencias_inversas[destino].append((origen, capacidad))
        
        # Actualizar flujos totales
        self.flujo_salida[origen] += capacidad
        self.flujo_entrada[destino] += capacidad
    
    def obtener_grado_entrada(self, nodo: str) -> Tuple[int, List[str]]:
        """
        Calcula el in-degree (grado de entrada) de un nodo
        
        Returns:
            Tuple[int, List[str]]: (cantidad de tuberías entrantes, lista de nodos origen)
        """
        if nodo not in self.tipos_nodos:
            raise ValueError(f"El nodo '{nodo}' no existe en la red")
        
        entrantes = [origen for origen, _ in self.adyacencias_inversas[nodo]]
        return len(entrantes), entrantes
    
    def obtener_grado_salida(self, nodo: str) -> Tuple[int, List[str]]:
        """
        Calcula el out-degree (grado de salida) de un nodo
        
        Returns:
            Tuple[int, List[str]]: (cantidad de tuberías salientes, lista de nodos destino)
        """
        if nodo not in self.tipos_nodos:
            raise ValueError(f"El nodo '{nodo}' no existe en la red")
        
        salientes = [destino for destino, _ in self.adyacencias[nodo]]
        return len(salientes), salientes
    
    def validar_conservacion_flujo(self, nodo: str) -> Dict:
        """
        Valida si un nodo de transbordo cumple con la conservación de flujo
        
        En un nodo de transbordo ideal:
        - Flujo de entrada = Flujo de salida (conservación de masa)
        - No debe acumular inventario
        
        Returns:
            Dict con información detallada de la validación
        """
        if nodo not in self.tipos_nodos:
            raise ValueError(f"El nodo '{nodo}' no existe en la red")
        
        tipo = self.tipos_nodos[nodo]
        flujo_in = sum(cap for _, cap in self.adyacencias_inversas[nodo])
        flujo_out = sum(cap for _, cap in self.adyacencias[nodo])
        
        resultado = {
            'nodo': nodo,
            'tipo': tipo.value,
            'flujo_entrada': flujo_in,
            'flujo_salida': flujo_out,
            'diferencia': flujo_in - flujo_out,
            'conserva_flujo': False,
            'acumula_inventario': False,
            'mensaje': ''
        }
        
        # Validación según tipo de nodo
        if tipo == TipoNodo.FUENTE:
            # Las fuentes solo producen, deberían tener flujo de salida
            resultado['mensaje'] = "FUENTE: Produce flujo, no requiere conservación"
            resultado['conserva_flujo'] = True  # No aplica para fuentes
            
        elif tipo == TipoNodo.SUMIDERO:
            # Los sumideros solo consumen
            resultado['mensaje'] = "SUMIDERO: Consume flujo, no requiere conservación"
            resultado['conserva_flujo'] = True  # No aplica para sumideros
            
        elif tipo == TipoNodo.TRANSBORDO:
            # Para transbordo: entrada debe ser igual a salida
            if abs(flujo_in - flujo_out) < 1e-9:  # Tolerancia para floats
                resultado['conserva_flujo'] = True
                resultado['mensaje'] = "TRANSBORDO: Conserva flujo perfectamente"
            elif flujo_in > flujo_out:
                resultado['acumula_inventario'] = True
                resultado['mensaje'] = f"TRANSBORDO: ACUMULA INVENTARIO (entra {flujo_in:.2f}, sale {flujo_out:.2f})"
            else:
                resultado['mensaje'] = f"TRANSBORDO: Déficit de flujo (entra {flujo_in:.2f}, sale {flujo_out:.2f})"
        return resultado
    
    def analizar_red_completa(self) -> Dict:
        """
        Analiza toda la red verificando conservación en todos los nodos de transbordo
        """
        resultados = {}
        nodos_con_problemas = []
        
        for nodo in self.tipos_nodos:
            if self.tipos_nodos[nodo] == TipoNodo.TRANSBORDO:
                info = self.validar_conservacion_flujo(nodo)
                resultados[nodo] = info
                if not info['conserva_flujo']:
                    nodos_con_problemas.append(nodo)
        
        return {
            'total_nodos_transbordo': len([n for n in self.tipos_nodos if self.tipos_nodos[n] == TipoNodo.TRANSBORDO]),
            'nodos_ok': len([n for n in resultados if resultados[n]['conserva_flujo']]),
            'nodos_con_problemas': nodos_con_problemas,
            'detalles': resultados
        }
    
    def mostrar_informacion_nodo(self, nodo: str) -> None:
        """
        Muestra información detallada y formateada de un nodo
        """
        if nodo not in self.tipos_nodos:
            print(f"El nodo '{nodo}' no existe en la red")
            return
        
        tipo = self.tipos_nodos[nodo]
        in_degree, entrantes = self.obtener_grado_entrada(nodo)
        out_degree, salientes = self.obtener_grado_salida(nodo)
        
        print(f"\n")
        print(f"NODO: {nodo}")
        print(f"Tipo: {tipo.value.upper()}")
        
        print(f"\nGRADOS:")
        print(f"In-degree (entrantes): {in_degree}")
        if entrantes:
            print(f"    └─ Desde: {', '.join(entrantes)}")
        else:
            print(f"    └─ Ninguno")
            
        print(f"Out-degree (salientes): {out_degree}")
        if salientes:
            print(f"    └─ Hacia: {', '.join(salientes)}")
        else:
            print(f"    └─ Ninguno")
        
        # Validación de conservación
        if tipo == TipoNodo.TRANSBORDO:
            print(f"\nCONSERVACIÓN DE FLUJO:")
            info = self.validar_conservacion_flujo(nodo)
            print(f"Flujo entrada: {info['flujo_entrada']:.2f}")
            print(f"Flujo salida: {info['flujo_salida']:.2f}")
            print(f"Diferencia: {info['diferencia']:.2f}")
            print(f"{info['mensaje']}")
            
            if info['acumula_inventario']:
                print(f"¡Acumulando inventario! Verificar capacidad de almacenamiento")
        
        print("\n")


# Prueba:

def crear_red_ejemplo() -> RedRefinamiento:
    """Crea una red de refinamiento de ejemplo para demostración"""
    red = RedRefinamiento()
    
    # Agregar nodos con sus tipos
    red.agregar_nodo("Pozo1", TipoNodo.FUENTE)
    red.agregar_nodo("Pozo2", TipoNodo.FUENTE)
    red.agregar_nodo("BombaA", TipoNodo.TRANSBORDO)
    red.agregar_nodo("BombaB", TipoNodo.TRANSBORDO)
    red.agregar_nodo("BombaC", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Tanque1", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Tanque2", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Refineria1", TipoNodo.SUMIDERO)
    red.agregar_nodo("Refineria2", TipoNodo.SUMIDERO)
    
    # Agregar tuberías (origen -> destino, capacidad)
    # Red con conservación perfecta
    red.agregar_tuberia("Pozo1", "BombaA", 100.0)
    red.agregar_tuberia("Pozo2", "BombaB", 80.0)
    red.agregar_tuberia("BombaA", "Tanque1", 60.0)
    red.agregar_tuberia("BombaA", "Tanque2", 40.0)
    red.agregar_tuberia("BombaB", "Tanque1", 80.0)
    red.agregar_tuberia("Tanque1", "Refineria1", 140.0)  # 60+80=140
    red.agregar_tuberia("Tanque2", "Refineria2", 40.0)
    red.agregar_tuberia("BombaB", "BombaC", 20.0)  # Esto crea un desbalance
    
    return red


def crear_red_con_problemas() -> RedRefinamiento:
    """Crea una red con problemas de conservación para demostración"""
    red = RedRefinamiento()
    
    # Nodos
    red.agregar_nodo("Fuente1", TipoNodo.FUENTE)
    red.agregar_nodo("Transbordo1", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Transbordo2", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Transbordo3", TipoNodo.TRANSBORDO)
    red.agregar_nodo("Sumidero1", TipoNodo.SUMIDERO)
    
    # Tuberías - Red con desbalances
    red.agregar_tuberia("Fuente1", "Transbordo1", 50.0)
    red.agregar_tuberia("Transbordo1", "Transbordo2", 30.0)  # Entra 50, sale 30 (acumula)
    red.agregar_tuberia("Transbordo2", "Sumidero1", 30.0)     # OK
    red.agregar_tuberia("Transbordo1", "Transbordo3", 10.0)  # Sale 10 adicional
    
    return red


if __name__ == "__main__":
    print("ANÁLISIS DE RED DE REFINAMIENTO DE PETRÓLEO")
    
    # Crear red de ejemplo
    red = crear_red_ejemplo()
    
    # Mostrar información de nodos específicos
    red.mostrar_informacion_nodo("BombaA")
    red.mostrar_informacion_nodo("BombaB")
    red.mostrar_informacion_nodo("Tanque1")
    
    # Análisis completo de la red
    print("\n")
    print("ANÁLISIS COMPLETO DE LA RED")
    
    analisis = red.analizar_red_completa()
    print(f"Total de nodos de transbordo: {analisis['total_nodos_transbordo']}")
    print(f"Nodos que conservan flujo: {analisis['nodos_ok']}")
    
    if analisis['nodos_con_problemas']:
        print(f"Nodos con problemas: {', '.join(analisis['nodos_con_problemas'])}")
        print("\nDetalles de problemas:")
        for nodo in analisis['nodos_con_problemas']:
            info = analisis['detalles'][nodo]
            print(f"  • {nodo}: {info['mensaje']}")
    else:
        print("¡Todos los nodos de transbordo conservan el flujo correctamente!")
    
    # Demostrar red con problemas
    print("\n")
    print("DEMOSTRACIÓN DE RED CON PROBLEMAS")
    
    red_problemas = crear_red_con_problemas()
    red_problemas.mostrar_informacion_nodo("Transbordo1")
    
    # Análisis de la red con problemas
    analisis_problemas = red_problemas.analizar_red_completa()
    print(f"\nAnálisis de red con problemas:")
    print(f"Nodos con problemas: {analisis_problemas['nodos_con_problemas']}")
