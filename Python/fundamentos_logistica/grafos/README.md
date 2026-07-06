# Grafos

## Introducción

Los Grafos son una de las estructuras de datos más versátiles y fundamentales en la **Investigación de Operaciones**. El enfoque de estos ejercicios es práctico y orientado a trabajar en problemas reales en diferentes contextos:

Cada concepto, ejercicio y proyecto estará ambientado en casos concretos de IO como:

- **Ruteo de vehículos (VRP):** Encontrar rutas óptimas para flotas de entregas.
- **Flujo en redes:** Maximizar el flujo de productos en una cadena de suministro.
- **Diseño de Redes:** Ubicar centros de districión minimizando costos de transporte.
- **Camino más corto:** Calcular tiempos de entrega mínimos en mapas de carreteras.
- **Detección de ciclos:** Identificar cuellos de botella o dependencias circulares en procesos.

---

## Ruta de la semana

| Día | Tema | Objetivo del Día (con foco IO) |
| :---: | :--- | :--- |
| **1** | **Conceptos básicos** (Vértices, aristas, dirigido vs no dirigido) | Representar redes logísticas donde los vértices son almacenes/ciudades y las aristas son carreteras (con o sin dirección según flujo). |
| **2** | **Representación** (Matriz de adyacencia vs Lista de adyacencia) | Elegir la estructura de datos adecuada según la densidad de la red (ej. matriz para redes pequeñas/densas, listas para redes grandes/dispersas). Aplicación: matriz de costos de envío. |
| **3** | **Recorrido BFS** (Búsqueda en Anchura con cola) | Encontrar la ruta con el **menor número de paradas** en una red de distribución (ej. entregas urgentes con pocos intercambios). |
| **4** | **Recorrido DFS** (Búsqueda en Profundidad con pila) | Explorar completamente una ruta antes de retroceder. Aplicación: **detección de caminos factibles** en redes de producción o **topología de redes** eléctricas. |
| **5** | **Aplicaciones IO** (Camino más corto + Detección de ciclos) | Implementar **Dijkstra** para costo mínimo (ej. minimizar combustible en entregas) y **DFS** para detectar ciclos en redes de dependencias (ej. procesos productivos circulares). |
| **6** | **Ejercicios integradores** | Resolver 3 problemas completos de IO: (1) Ruta más corta con restricciones, (2) Flujo máximo en una red de tuberías, (3) Asignación de tareas con dependencias (grafos DAG). |
| **7** | **Proyecto integrador** | Construir un **"Sistema Inteligente de Optimización de Rutas"** que, dado un mapa de ciudades y costos, calcule la ruta más eficiente y detecte oportunidades de consolidación de carga (usando BFS, DFS y Dijkstra). |

---

## Metodología de Trabajo

Cada sesión seguirá este flujo de trabajo:

1. **Teoría con aplicación IO**: Explicación del concepto matemático y su equivalencia en problemas reales.
2. **Implementación en Python**: Código limpio, modular, con type hints, documentación y pruebas unitarias básicas.
3. **Análisis de complejidad**: Comparar eficiencia (Big O) de cada algoritmo, fundamental para escalar a redes con miles de nodos (algo común en IO).
4. **Ejercicios prácticos**: Resolver casos reales.
