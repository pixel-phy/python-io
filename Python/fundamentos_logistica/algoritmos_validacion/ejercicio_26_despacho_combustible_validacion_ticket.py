"""Ejercicio 26: Despacho de Combustible con validación de Ticket

Un camión cisterna llega a cargar combustible. Para automatizar la carga, el operario digita el registro:
"TICKET_DAMM,LITROS". El sistema debe rechazar el registro de inmediato si el ticket tiene un error     
de dedo (usando el algoritmo de Damm). Si el ticket es válido, debe comprobar la restricción operativa:
los litros cargados no pueden superar la capacidad restante del tanque de la estación (5000 litros).

    Escribir una función que reciba la lista de registros de carga de combustible y retorne qué cargas 
fueron válidas y si la suma total de litros respeta el límite de 5000 litros de la estación.

    Input de prueba: 
    registros = ["5724,2000", "5274,1500", "5724,3500"] """

  # Tabla de Damm
damm_table = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
]

def validador_damm(ticket: str) -> bool:
    """
    Valida un ticket usando el algoritmo de Damm.
    Retorna True si el ticket es válido, False en caso contrario.
    """
      
    interim = 0
    for digit in ticket:
        if not digit.isdigit():
            return False
        interim = damm_table[interim][int(digit)]
    
    return interim == 0


def procesar_cargas(registros):
    """
    Procesa una lista de registros de carga de combustible.
    
    Args:
        registros: Lista de strings con formato "TICKET,LITROS"
    
    Returns:
        tuple: (cargas_validas, suma_total_respeta_limite)
        - cargas_validas: Lista de registros que pasaron ambas validaciones
        - suma_total_respeta_limite: Booleano indicando si la suma total <= 5000
    """
    capacidad_max = 5000
    cargas_validas = []
    suma_total_litros = 0
    
    for registro in registros:
        # Validar formato
        if ',' not in registro:
            continue
            
        ticket, litros_str = registro.split(',', 1)
        
        # Validar que los litros sean un número
        try:
            litros = float(litros_str)
            # Los litros deben ser positivos y enteros (o al menos no negativos)
            if litros < 0 or litros != int(litros):
                continue
            litros = int(litros)
        except ValueError:
            continue
        
        # Validar ticket con Damm
        if not validador_damm(ticket):
            continue
        
        # Validar restricción operativa (capacidad acumulada)
        if suma_total_litros + litros <= capacidad_max:
            cargas_validas.append(registro)
            suma_total_litros += litros
    
    # Verificar si la suma total respeta el límite
    suma_total_respeta_limite = suma_total_litros <= capacidad_max
    
    return cargas_validas, suma_total_respeta_limite


# Prueba con el input proporcionado
if __name__ == "__main__":
    registros = ["5724,2000", "5274,1500", "5724,3500"]
    
    cargas_validas, respeta_limite = procesar_cargas(registros)
    
    print("Cargas válidas:", cargas_validas)
    print("Suma total respeta límite de 5000 litros:", respeta_limite)
