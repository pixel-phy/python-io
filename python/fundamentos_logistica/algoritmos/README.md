# Semana 13: Algoritmos clásicos en logística

## 📊 Notación asintótica (Big O)

| Notación | Nombre | Significado | Ejemplo |
|----------|--------|-------------|---------|
| O(1) | Constante | Tiempo independiente del tamaño | Acceso por índice |
| O(log n) | Logarítmica | Se reduce a la mitad cada vez | Búsqueda binaria |
| O(n) | Lineal | Crece proporcionalmente | Búsqueda lineal |
| O(n²) | Cuadrática | Doble bucle | Burbuja, selección |

## 🔍 Búsqueda

| Algoritmo | Complejidad | Requisito | Método |
|-----------|-------------|-----------|--------|
| Lineal | O(n) | Ninguno | Recorre uno por uno |
| Binaria | O(log n) | Lista ordenada | Divide y vencerás |

## 🔄 Ordenamiento

| Algoritmo | Complejidad | Estable | In-place |
|-----------|-------------|---------|----------|
| Burbuja | O(n²) | ✅ Sí | ✅ Sí |
| Selección | O(n²) | ❌ No | ✅ Sí |
| Inserción | O(n²) | ✅ Sí | ✅ Sí |
| Merge Sort | O(n log n) | ✅ Sí | ❌ No |

## 💡 Invariantes de bucle

Propiedad que se mantiene verdadera antes, durante y después de cada iteración.
Sirve para **demostrar** que el algoritmo es correcto.
