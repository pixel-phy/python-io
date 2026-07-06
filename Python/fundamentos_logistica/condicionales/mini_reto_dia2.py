"""Mini reto del día 2:
    Asignador de prioridad y vehículo para mensajería exprés.

Reglas de negocio:
    Peso            Zona            Urgencia            Asignación
    < 3 kg          CUALQUIERA      normal              moto
    < 3 kg          CUALQUIERA      express             moto + prioridad alta
    3-10 kg         urbana          normal              furgoneta
    3-10 kg         urbana          express             furgoneta + prioridad alta
    3-10 kg         rural           normal              furugoneta solo si no llueve
    3-10 kg         rural           express             camión pequeño (si llueve o no)
    >10 kg          urbana          normal              camión
    >10 kg          urbana          express             camión + 2 mensajeros 
    >10 kg          rural           normal              camión + 4x4
    >10 kg          rural           express             2 camiones + equipo especial

Escribe un programa que:
        1. Pida peso, zona, urgencia, (si aplica: lluvia)
        2. Use múltiples condicionales anidadas (if/elif/else dentro de otros).
        3. Muestre: vehículo + prioridad + pbservaciones especiales
        
Casos borde:
    - Peso exactamente 3 kg.
    - Peso exactamente 10 kg.
    - Zona rural, peso 5 kg, normal, lloviendo.
    - Zona rural, peso 5 kg, express, lloviendo. """
# Peso
try:
    peso = int(input("Ingrese peso: "))
    if peso < 0:
        raise ValueError ("El peso debe ser positivo.")
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Zona
zonas = ["urbana", "rural"]
zona = input("Ingrese Zona (urbana/rural): ").strip().lower()
if zona not in zonas:
    print("Zona debe ser urbana o rural.")
    exit()

# Urgencia
urgencias = ["normal", "express"]
urgencia = input("Ingrese Urgencia (normal/express): ")
if urgencia not in urgencias:
    print("Urgencia debe ser normal/express.")
    exit()

# Asignación
if peso < 3:
    if urgencia == "normal":
        vehiculo = "Moto"
        prioridad = "Ninguna"
        observaciones = "Ninguna"
    else:
        vehiculo = "Moto"
        prioridad = "Alta"
        observaciones = "Ninguna"

elif 3 <= peso <= 10:
    if zona == "urbana":
        if urgencia == "normal":
            vehiculo = "Furgoneta"
            prioridad = "Ninguna"
            observaciones = "Ninguna"
        else:
            vehiculo = "Furgoneta"
            prioridad = "Alta"
            observaciones = "Ninguna"
    else:
        if urgencia == "normal":
            llueve = input("¿Llueve? (si/no): ").strip().lower()
            if llueve == "si":
                vehiculo = "Camión pequeño"
                prioridad = "Ninguna"
                observaciones = "Ninguna"
            else:
                vehiculo = "Furgoneta"
                prioridad = "Ninguna"
                observaciones = "Ninguna"
        else:
            vehiculo = "Furgoneta"
            prioridad = "Alta"
            observaciones = "Ninguna"

elif peso > 10 and zona == "urbana":
    if urgencia == "normal":
        vehiculo = "Camión"
        prioridad = "Ninguna"
        observaciones = "Ninguna"
    else:
        vehiculo = "Camión" 
        prioridad = "Alta"
        observaciones= "Se necesitan 2 mensajeros"

elif peso > 10 and zona == "rural":
    if urgencia == "normal":
        vehiculo = "Camión"
        prioridad = "Ninguna"
        observaciones = "Vehículo debe ser 4x4"
    else:
        vehiculo = "2 Camiones"
        prioridad = "Ninguna"
        observaciones = "Equipo especial"

print(f"Vehículo: {vehiculo}")
print(f"Prioridad: {prioridad}")
print(f"Observaciones: {observaciones}")
