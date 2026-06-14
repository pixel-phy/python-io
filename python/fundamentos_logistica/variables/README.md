# Tipos de datos en logística

En logística, manejamos información muy variada:

## `int` → Cantidades de paquetes, códigos numéricos, tiempos en minutos
```python
paquetes = 150
codigo_almacen = 4823
tiempo_minutos = 45

```
---
## `float` → Pesos, distancias, costos con decimales

```python
peso_total = 23.7
distancia_km = 127.5
costo_envio = 159.99
```

---
## `str` → Nombres de rutas, IDs de envío, direcciones

```python
ruta = "Ruta Norte"
id_envio = "MX-4829B"
direccion = "Av. Reforma 123, CDMX"
```

---
---
## `list` → Lista de órdenes del día, paradas de un camión (ordenadas, mutables)

```python
ordenes_dia = ["ORD-001", "ORD-002", "ORD-003"]
paradas_camion = ["Bodega A", "Centro de distribución", "Cliente final"]
```

## `dict` → Información de un envío (clave: número de guía, valor: estado)

```python
envio = {
    "GUI-1001": "En tránsito",
    "GUI-1002": "Entregado",
    "GUI-1003": "Retrasado"
}
```

## `tuple` → Coordenadas fijas (latitud, longitud), horarios inmutables 

```python
coordenadas_almacen = (19.4326, -99.1332)
horario_reparto = ("09:00", "13:00", "17:00")
```


