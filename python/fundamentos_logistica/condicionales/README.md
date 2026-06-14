## Condicionales en logística

En logística, las decisiones de envío dependen de múltiples factores:

- **Peso**: determina la capacidad del vehículo.
- **Zona**: afecta tiempos y restricciones.
- **Urgencia**: modifica prioridad y costo.

### Estructura típica

```python
if peso <= 5:          # Primera condición (más específica o ligera)
    vehiculo = "moto"
elif peso <= 50:       # Segunda condición (rango intermedio)
    vehiculo = "furgoneta"
else:                  # Caso por defecto (pesado)
    vehiculo = "camión"
```

---
### Principio clave
Python evalúa las condiciones de arriba abajo, ejecuta if o elif que se cumple y sale del bloque.

