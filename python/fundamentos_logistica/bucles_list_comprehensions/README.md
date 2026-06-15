# Bucles y list comprehensions

En logística, constantemente procesamos listas de envíos, rutas y paquetes. Los bucles nos permiten automatizar tareas repetitivas y las list comprehensions nos dan una forma más concisa y eficiente de crear y transformar listas.

## Escenario práctico

Imaginemos que tenemos una lista de órdenes de envío y necesitamos:
- Aplicar tarifas diferentes según la zona
- Filtrar paquetes urgentes
- Generar etiquetas automáticamente

## Bucle `for` → Recorrer listas, tuplas, diccionarios

```python
# Procesar cada orden de envío
ordenes = ["ORD-001", "ORD-002", "ORD-003"]

for orden in ordenes:
    print(f"Procesando {orden}...")

# Recorrer diccionario de envíos (clave: guía, valor: estado)
envios = {"GUI-1001": "Pendiente", "GUI-1002": "En ruta"}

for guia, estado in envios.items():
    if estado == "Pendiente":
        print(f"Asignar ruta a {guia}")
```

## Bucle `while` → Repetir hasta que se cumpla una condición
```python
# Reintentar conexión con el sistema de tracking
intentos = 0
max_intentos = 3

while intentos < max_intentos:
    print(f"Intentando conexión... ({intentos+1}/{max_intentos})")
    # Simular conexión exitosa
    conexion_exitosa = True
    if conexion_exitosa:
        print("Conexión establecida")
        break
    intentos += 1

# Esperar hasta que llegue un camión
camion_llego = False
while not camion_llego:
    print("Esperando camión...")
    # Verificar sensor
    camion_llego = True  # Simulación
  
```
## `break` y  `continue` → Control del flujo
```python
# break: salir del bucle cuando se encuentra un paquete problemático
paquetes = [2.3, 5.7, 28.5, 0.0, 15.2]  # pesos en kg

for peso in paquetes:
    if peso == 0.0:
        print("¡Paquete sin peso registrado! Deteniendo carga")
        break
    print(f"Cargando paquete de {peso} kg")

# continue: saltar elementos que no cumplen condición
pesos = [1.2, 0.5, 7.8, 0.0, 3.4, 0.0]

for peso in pesos:
    if peso == 0.0:
        print("Paquete vacío detectado, omitiendo...")
        continue
    print(f"Procesando paquete de {peso} kg")
```

## List Comprehensions  → Crear listas de forma compacta

### Sintaxis básica: `[expresion for elemento in iterable if condicion]`

```python
# Filtrar órdenes urgentes
ordenes = ["ORD-001", "ORD-002-U", "ORD-003", "ORD-004-U"]
urgentes = [orden for orden in ordenes if orden.endswith("-U")]
print(f"Órdenes urgentes: {urgentes}")

# Aplicar tarifa base según peso
pesos = [2, 15, 8, 30, 45]
tarifas = [peso * 1.5 if peso < 20 else peso * 1.2 for peso in pesos]
print(f"Tarifas calculadas: {tarifas}")

# Generar códigos de tracking
base = "TRK"
numeros = [101, 102, 103, 104]
tracking_ids = [f"{base}-{num}" for num in numeros]
print(f"IDs de tracking: {tracking_ids}")
```

