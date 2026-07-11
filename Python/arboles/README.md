# Árboles

## Introducción

Este repositorio documenta mi **semana de inmersión** en el mundo de los árboles (estructuras de datos no lineales), para entender cómo esta estructura permitre modelar jerarquías, tomar decisiones secuenciales y optimizar recursos en entornos empresariales.

Mi perfil está orientado a **Investigación de Operaciones (IO)**. Por este motivo, cada ejemplo teórico, ejercicio práctico y proyecto estará ambientado en problemas reales como:

- **Optimización de inventarios**: (árboles de decisión para reabastecimiento).
- **Ruteo de vehículos** (VFR / TSP con estructuras jerárquicas).
- **Teoría de colas** (Prioridades y tiempos de espera).
- **Asignación de recursos** (balanceo de cargas en plantas).

---

## Ruta diaria de trabajo para la semana

| Día | Tema | Objetivo del Día (con foco IO) |
| :---: | :--- | :--- |
| **1** | **Conceptos básicos** (Nodos, raíz, hojas, profundidad) | Comprender la terminología y representar jerarquías organizacionales (ej. estructura de una empresa o cadena de suministro). |
| **2** | **Árbol binario** (Creación y recorrido básico) | Implementar un árbol desde cero y recorrerlo para "listar" tareas en una planta de producción. |
| **3** | **Árbol binario de búsqueda (BST)** (Propiedades y búsqueda) | Entender la eficiencia en búsquedas (O(log n)). Aplicación: localizar rápidamente un producto en un almacén gigante. |
| **4** | **Recorridos** (Inorden, Preorden, Postorden) | Diferenciar cuándo usar cada recorrido para resolver problemas de priorización (ej. órdenes de ensamblaje vs. desensamblaje). |
| **5** | **Insertar y eliminar en BST** (Operaciones básicas) | Mantener el árbol balanceado en operaciones dinámicas. Aplicación: gestión de flotas de transporte (altas/bajas de vehículos). |
| **6** | **Ejercicios integradores** | Resolver 3 problemas completos de IO que combinen todos los temas anteriores (ej. simulación de un sistema de colas con prioridades). |
| **7** | **Proyecto integrador** | Construir un **"Sistema de Decisión Logística"** usando árboles para recomendar rutas óptimas de entrega basadas en costos y tiempos. |

---

## Metodología de Trabajo (mejores prácticas para un IO)

Para asegurar un aprendizaje sólido y profesional, cada día seguiré esta estructura:

1. **Teoría con aplicaciones IO**: Explicación del concepto y su equivalente en un problema real.
2. **Implementación en Python**: Código limpio, tipado estático (type hints) y documentación.
3. **Benchmarking y Big O**: Análisis de complejidad temporal y especial de cada operación (crítico en IO para grandes volúmenes de datos).
4. **Ejercicio práctico callejero**: Resolver un mini-caso de IO usando el árbol aprendido.

---
