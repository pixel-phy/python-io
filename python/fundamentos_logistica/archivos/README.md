# Manejo de archivos en logística

En logística, los archivos son el corazón de las operaciones: rutas de transporte, inventarios, registros de simulación, bitácoras de eventos. Aprender a leer y escribir archivos te permitirá persistir información y procesar datos entre ejecuciones.

## Escenario práctico

Una flota de camiones necesita:
- Cargar coordenadas de entregas desde un archivo
- Guardar resultados de optimización de rutas
- Registrar simulaciones que pueden durar horas

## Modos de apertura fundamentales

| Modo | Descripción | Uso en logística |
|------|-------------|------------------|
| `"r"` | Lectura (read) | Cargar configuraciones, leer órdenes del día |
| `"w"` | Escritura (write) - **sobrescribe** | Generar reportes nuevos, guardar resultados |
| `"a"` | Append (añadir) - **no borra** | Bitácoras de eventos, logs de simulación |
| `"x"` | Creación exclusiva (error si existe) | Evitar sobrescribir datos críticos |

⚠️ **Modo `"w"` borra el archivo si ya existe** → ¡Cuidado con datos históricos!

---
## `write()` vs `writelines()`

```python
# write(): escribe un solo string
archivo.write("Ruta Norte activada\n")

# writelines(): escribe una lista de strings (sin saltos automáticos)
lineas = ["Bogota:4.71,-74.07\n", "Medellin:6.25,-75.56\n", "Cali:3.43,-76.52\n"]
archivo.writelines(lineas)
```

---
## `flush` -> GRabación inmediata en disco 
Por defecto, Python almacena datos en buffer (memoria temporal) y los escribe en bloque por eficiencia. En simulaciones largas o sistemas críticos, necesitas forzar la escritura inmediata.

```python
# Simulación de Montecarlo para logística aeroportuaria
with open("output/simulacion_colas.log", mode="a", encoding="utf-8") as archivo:
    archivo.write("Simulación iniciada: Minuto 1 - Llegaron 5 clientes.\n")
    archivo.flush()  # Forzar escritura en disco AHORA MISMO
    # Si el programa falla después de flush(), el log ya está guardado
```

---
## El bloque `with` -> Manejo automático de recursos
```python
# ❌ Sin with (requiere close() manual)
archivo = open("rutas.txt", "w")
archivo.write("Ruta 1\n")
archivo.close()  # Si olvidas esto, el archivo queda corrupto

# ✅ Con with (cierra automáticamente, incluso si hay errores)
with open("rutas.txt", "w", encoding="utf-8") as archivo:
    archivo.write("Ruta 1\n")
# Aquí el archivo ya está cerrado automáticamente
```

---
## Lectura de archivos: los 3 métodos esenciales
```python
with open("output/red_transporte.txt", "r", encoding="utf-8") as archivo:
    # 1. Leer todo el contenido (archivos pequeños)
    todo = archivo.read()
    
    # 2. Leer línea por línea (archivos grandes)
    for linea in archivo:
        ciudad, coordenadas = linea.strip().split(":")
        print(f"Ciudad: {ciudad}, Coordenadas: {coordenadas}")
    
    # 3. Leer todas las líneas en lista
    lineas = archivo.readlines()
```


