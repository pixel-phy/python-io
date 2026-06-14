""" Ejercicio 01:
    Una paquetería asigna vehículo solo por peso.
    Reglas:
    - Menos de 5 kg: "moto".
    - De 5 a 10 kg: "furgoneta".
    - Más de 20 kg: "camión".

    Escribe un if/elif/else que asigne el vehículo según peso variable.
    ¿Qué pasa si peso = 20? En qué categoría cae? """

peso = 20

if peso < 5:
    print("Paquete asignado a moto.")
elif peso <= 20:
    print("Paquete asignado a furgoneta.")
else:
    print("Paquete asignado a camión.")
    
