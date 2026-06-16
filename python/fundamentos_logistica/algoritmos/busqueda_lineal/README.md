# Día 1: La "Tecnología" de los Algoritmos y Notación Asintótica

## Introducción

Somos la persona encargada de gestionar la logística de una ciudad con 1,000,000 de paquetes. Un algoritmo ineficiente podría tardar **días** donde uno eficiente tarda **segundos**. La diferencia no está en la computadora, sino en la **tecnología invisible** que llamamos algoritmos.

> *"El hardware es la velocidad máxima de tu camión. El algoritmo es la ruta que eliges."*

---

## ¿Por qué importa en logística?

| Problema real | Tamaño típico | Mal algoritmo | Buen algoritmo |
|---------------|---------------|---------------|----------------|
| Buscar un pedido en almacén | 50,000 productos | 50,000 ops | ~16 ops |
| Asignar rutas de reparto | 200 direcciones | 40,000 ops | ~2,000 ops |
| Optimizar carga de camiones | 10,000 paquetes | 100M ops | ~50,000 ops |

El hardware no escala linealmente con los datos. **La eficiencia algorítmica sí**.

---

## Las tres notaciones clave

Para medir la eficiencia **sin depender** de la computadora donde se ejecute el código, usamos la **notación asintótica**:

| Notación | Nombre | Significado | Analogía logística |
|----------|--------|-------------|--------------------|
| **$O$** (Big O) | Límite superior | *"Tu algoritmo no tardará más que esto en el peor caso"* | El tiempo máximo que un camión puede tardar en tráfico denso |
| **$\Omega$** (Omega) | Límite inferior | *"Tu algoritmo tardará al menos esto en el mejor caso"* | El tiempo mínimo si no hay tráfico y todo sale perfecto |
| **$\Theta$** (Theta) | Límite estricto | *"El mejor y peor caso crecen al mismo ritmo"* | Una ruta que siempre toma exactamente el doble si la distancia se duplica |

### Ejemplo práctico con búsqueda de paquetes

```python
def buscar_paquete(almacen, id_paquete):
    for paquete in almacen:  # recorre de principio a fin
        if paquete.id == id_paquete:
            return paquete
    return None

• ** Mejor caso ($\Omega$ (1))**: el paquete está al principio -> 1 operación.
• ** Peor caso ($\Omega$ (n))**: el paquete no está o está al final -> hay que revisar todo.
• En este algoritmo, mejor y peor caso no crecen igual -> no tiene **$\Theta$** puro.
