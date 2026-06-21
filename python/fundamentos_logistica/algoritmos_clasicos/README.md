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

## 📊 Notación asintótica (Big O)

| Notación | Nombre | Significado | Ejemplo |
|----------|--------|-------------|---------|
| O(1) | Constante | Tiempo independiente del tamaño | Acceso por índice |
| O(log n) | Logarítmica | Se reduce a la mitad cada vez | Búsqueda binaria |
| O(n) | Lineal | Crece proporcionalmente | Búsqueda lineal |
| O(n²) | Cuadrática | Doble bucle | Burbuja, selección |
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
```


---
## Las funciones más comunes (de mejor a peor)

1. $O(1)$ - Tiempo constante: El tiempo no cambia sin importar el tamaño de los datos (ej. Acceder al primer elemento de una lista.).
2. $O(log n)$ - Tiempo Logarítmico: Altamente eficiente. El problema se reduce a la mitad en cada paso. (Ej. Búsqueda binaria en una agenda teléfonica ordenada).
3. $O(n) - Tiempo lineal: El tiempo crece proporcionalmente al tamaño de los datos. (Ej. Buscar en una lista desordenada).
4. $O(n log n)$ - Teimpo cuasi - lineal: Es el estandar de oro para los algoritmos de ordenamiento eficientes como Merge Sort o Heap Sort.
5. $O(n²) - Tiempo cuadrático: El tiempo crece de forma cuadrática. Suele ocurrir cuando tienes bucles anidados (un ciclo dentro de otro ciclo). (Ej. Comparar todos los elementos de una lista contra todos los demás).
6. $O(2^n) - Tiempo exponencial: El tiempo se duplica con cada elemento nuevo. Se vuelve imposible calcular para valores de n medianos (ej. n = 50). Muchos problemas de optimización matemática pura sufren de esto si se intentan resolver por fuerza bruta.
