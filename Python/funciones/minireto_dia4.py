""" Mini Reto:
    Crear 3 funciones reutilizables y usarlas juntas para procesar múltiples pedidos. """

def asignar_vehiculo(peso: float, zona: str, lluvia: bool):
    if peso < 3:
        vehiculo = "Moto"
    elif 3 <= peso <= 10:
        if zona == "urbana":
            vehiculo = "Furgoneta"
        elif zona == "rural" and not lluvia:
            vehiculo = "Furgoneta"
        elif zona == "rural" and lluvia:
            vehiculo = "Camión pequeño"
    else:
        vehiculo = "Camión"
    return vehiculo

def calcular_costo_envio(vehiculo: str, urgencia: str, distancia_km: float):
    tarifas = {
        "Moto": {"base": 5000, "costo_km": 1000},
        "Furgoneta": {"base": 8000, "costo_km": 800},
        "Camión": {"base": 15000, "costo_km": 500},
        "Camión pequeño": {"base": 10000, "costo_km": 600}
    }

    datos = tarifas[vehiculo]
    costo_base = datos["base"] + (datos["costo_km"] * distancia_km)
    costo_final = costo_base * 1.30 if urgencia == "express" else costo_base

    return round(costo_final, 2)

def priorizar_pedido(peso: float, urgencia: str, zona: str):
    if urgencia == "express":
        return "alta"
    if peso > 15:
        return "alta"
    if zona == "rural":
        return "media"
    return "baja"

def procesar_pedido_completo(pedido: dict, distancia_km: float):
    peso = pedido["peso"]
    zona = pedido["zona"]
    urgencia = pedido["urgencia"]
    lluvia = pedido["lluvia"]

    vehiculo = asignar_vehiculo(peso, zona, lluvia)
    costo = calcular_costo_envio(vehiculo, urgencia, distancia_km)
    prioridad = priorizar_pedido(peso, urgencia, zona)

    return {
        "vehiculo": vehiculo,
        "costo_total": costo,
        "prioridad": prioridad,
        "distancia_km": distancia_km,
        "urgencia": urgencia,
        "zona": zona
    }
# Pruebas:

pedidos = [
    {"peso": 2, "zona": "urbana", "urgencia": "express", "lluvia": False},
    {"peso": 8, "zona": "rural", "urgencia": "normal", "lluvia": True},
    {"peso": 18, "zona": "urbana", "urgencia": "express", "lluvia": False}
]

print("Sultados\n")
for i, pedido in enumerate(pedidos, 1):
    resultado = procesar_pedido_completo(pedido, distancia_km=12)
    print(f"Pedido {i}:")
    print(f" Peso: {pedido['peso']} kg | Zona: {pedido['zona']} | Urgencia: {pedido['urgencia']}")
    print(f"    Vehículo: {resultado['vehiculo']}")
    print(f"    Costo Total: ${resultado['costo_total']:,.0f}")
    print(f"    Prioridad: {resultado['prioridad']}")
    print(f"    Distancia: {resultado['distancia_km']}km\n")
