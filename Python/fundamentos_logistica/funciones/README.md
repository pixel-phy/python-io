# Funciones 

En logística, las **funciones** son bloques de código reutilizable que permiten organizar, simplificar y escalar cualquier sistema logístico. En lugar de escribir una y otra vez la misma lógica para calcular costos, asignar vehículos o procesar pedidos, las funciones nos permiten definir una vez y usar muchas veces.

---
## Funciones básicas

```python
def calcular_costo_envio(peso_kg, distancia_km):
    costo = peso_kg * 0.5 + distancia_km * 0.3
    return costo
```

### Se practicará:
- Parámetros de entrada:  `peso_kg` y  `distancia_km` son los datos que la función recibe.
-  `return`: la función devuelve un resultado para que sea utilizado después.
- Llamar a la función desde diferentes partes del código.

---
## Parámetros por defecto

```python
def asignar_vehiculo(peso, zona="urbana", prioridad="normal"):
    if peso < 3:
        return "moto"
    elif peso <= 10 and zona == "urbana":
        return "furgoneta"
    else:
        return "camión"
```

### Se practicará:
• Valores por defecto: si no pasa `zona`, asume `urbana`; si no pasa `prioridad`, asume `normal`.
• Llamadas flexibles:
  - `asignar_vehiculo(25)` -> usa zona = "urbana", prioridad="normal"
  - `asignar_vehiculo(25,"rural")` -> específica zona, prioridad por defecto
  - `asignar_vehiculo(25, "rural", "express")` -> específica todo

---
## Retornar múltiples Valores
```python
def analizar_pedido(peso, zona, urgencia):
    vehiculo = asignar_vehiculo(peso, zona)
    costo = calcular_costo_envio(peso, 15)  # distancia fija ejemplo
    tiempo = calcular_tiempo(zona, urgencia)  # función hipotética
    return vehiculo, costo, tiempo

# Uso desempaquetando
veh, cost, time = analizar_pedido(15, "rural", "express")
```

### Se practicará:
• **Retornar tuplas** (implicitamente al usar  `valor1, valor2, valor3`)
• **Desempaquetar resultados** en varias variables a la vez.
• Alternativa: retornar un diccionario para mayor claridad.

```python
return {"vehiculo": vehiculo, "costo": costo, "tiempo": tiempo}
```
---
## Funciones que llaman a otras funciones (composición)
```python
def procesar_pedido(pedido):
    # pedido es un dict: {"id": 101, "peso": 8, "zona": "urbana"}
    vehiculo = asignar_vehiculo(pedido["peso"], pedido["zona"])
    costo = calcular_costo_envio(pedido["peso"], 15)
    return {**pedido, "vehiculo": vehiculo, "costo": costo}
```

### Se practicará:
• **Composición**: una función usa resultados (o llama a) otras funciones.
• **Modularidad**: Cambiar `asignar_vehiculo` o `calcular_costo_envio` no afecta a `procesar_pedido`, siempre que se respeten los parámetros esperados.
