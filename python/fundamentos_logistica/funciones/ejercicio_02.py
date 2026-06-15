"""Ejercicio 02:
    Define procesar_pedido(pedido) donde pedido es un dict como:
    
    ejemplo_pedido = {
        "peso": 8,
        "zona": "rural",
        "urgencia": "express",
        "lluvia": True
    }
    Reglas simplificadas:
    - Peso < 3 kg: "Moto" (Si es express -> prioridad alta)
    - Peso 3-10 kg + zona urbana -> "Furgoneta" (express -> priodidad alta)
    - Peso 3-10 kg + rural + lluvia -> "Camión pequeño" (no furgoneta)
    - Peso 3-10 kg + rural + sin lluvia -> "Furgoneta"
    - Peso > 10 kg -> "Camión" (express -> +2 mensajeros y prioridad alta)

    Debe retornar un dict con:
{
    "vehiculo": "Furgoneta",
    "prioridad": "alta" | "normal",
    "mensajeros": 1,  # 1 por defecto, 3 si es >10kg y express
    "observaciones": "" # si hay algo especial
} """

def procesar_pedido(pedido: dict):
    peso = pedido["peso"]
    zona = pedido["zona"]
    urgencia = pedido["urgencia"]
    lluvia = pedido["lluvia"]

    if peso < 3:
        vehiculo = "Moto"
        prioridad = "alta" if urgencia == "express" else "normal"
        mensajeros = 1
        observaciones = ""

    elif 3 <= peso <= 10:
        if zona == "urbana":
            vehiculo = "Furgoneta"
            prioridad = "alta" if urgencia == "express" else "normal"
            mensajeros = 1
            observaciones = ""
        else:
            if lluvia:
                vehiculo = "Camión pequeño"
                observaciones = "LLuvia en zona rural: Camión pequeño"
            else:
                vehiculo = "Furgoneta"
                observaciones = "Sin lluvia en zona rural: Furgoneta"
            prioridad = "alta" if urgencia == "express" else "normal"
            mensajeros = 1

    else:
        vehiculo = "Camión"
        prioridad = "alta" if urgencia == "express" else "normal"
        mensajeros = 3 if urgencia == "express" else 1
        observaciones = "Envío pesado" + ("+ 2 mensajeros extra" if urgencia == "express" else "")

    return {
        "vehiculo": vehiculo,
        "prioridad": prioridad,
        "mensajeros": mensajeros,
        "observaciones": observaciones
    }
ejemplo_pedido = {
    "peso": 8,
    "zona": "rural",
    "urgencia": "express",
    "lluvia": True
}
print(procesar_pedido(ejemplo_pedido))
