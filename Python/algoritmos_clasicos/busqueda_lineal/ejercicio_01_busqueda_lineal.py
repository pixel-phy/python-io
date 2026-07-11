"""Búsqueda lineal en Investigación de Operaciones

La búsqueda lineal (O(n)) en IO es el punto de partida cuando los datos no están ordenados, cuando
las estructuras cambian dinámicamente o cuando evaluar la "condición de parada" requiere calcular
una función de costo en tiempo real.

    Ejemplo: Filtrado de Lotes de producción:
    Imagina un Backend que recibe un flujo de lotes de inventario con diferentes niveles de holgura
    de tiempo antes de vencerse. Necesitamos encontrar secuencialmente el primer lote que cumpla
    estrictamente con un requerimiento mínimo de día de vida útil para un cliente de alta prioridad. """

def find_first_eligible_batch(batches, min_days):
    for batch in batches:
        if batch['shlef_life_days'] >= min_days:
            return batch
    return None
