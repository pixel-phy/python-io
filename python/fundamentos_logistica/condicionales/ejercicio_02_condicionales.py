"""Ejercicio 2:
    Mismo peso + Zona de envío (Urbana/Rural)
    Reglas:
    - Moto: peso < 5 kg
    - Furgoneta: 5-20 kg, peso si es ZONA RURAL - Resticción adicional: solo si no llueve.
    - Camión > 20 kg (Siempre disponible).
        Escribir código que use if/elif/else y pregunte:
    1. ¿Peso del paquete?
    2. ¿Zona (urbana/rural)?
    3. Si es rural y furgoneta: ¿Está lloviendo? (sí/no)
    El vehículo asignado o un mensaje de "No disponible".
    """

peso = input("¿Peso del paquete?: ")
try:
    int_peso = int(peso)
    if int_peso < 0:
        raise ValueError("El peso debe ser un número positivo.")
except ValueError as e:
    print(f"Error: {e}")
    exit()

if int_peso < 5:
    vehiculo = "Moto"
elif int_peso <= 20:
    vehiculo = "Furgoneta"
else:
    vehiculo = "Camión"

zona = input("Zona (urbana/rural): ").strip().lower()
zonas = ["urbana", "rural"]
if zona not in zonas:
    print("Ingrese una zona válida.")
    exit()

llueve = False
if zona == "rural" and vehiculo == "Furgoneta":
    clima = input("¿Está lloviendo? (si/no): ")
    llueve = (clima == 'si')

print("\nRESUMEN PEDIDO:")
print(f"Peso paquete: {int_peso} kg")
print(f"Zona: {zona}.")
if llueve:
    print(f"{vehiculo} No disponible por condiciones climáticas.")
else:
    print(f"Vehículo ({vehiculo}) asignado exitosamente.")


