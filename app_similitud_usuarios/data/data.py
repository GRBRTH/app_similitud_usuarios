import pandas as pd

#Lectura de respuestas por usuario
def cargar_respuestas(ruta_archivo):
    df = pd.read_excel(ruta_archivo, sheet_name="Respuestas")
    diccionario = {}

    for index, row in df.iterrows():
        nombre = row["Usuario"]
        respuestas = [row["P1"], row["P2"], row["P3"], row["P4"]]
        diccionario[nombre] = respuestas

    return diccionario

#Lectura de datos personales por usuario
def cargar_informacion(ruta_archivo):
    df = pd.read_excel(ruta_archivo, sheet_name="Informacion")
    diccionario = {}

    for index, row in df.iterrows():
        nombre = row["Usuario"]
        info = {
            "Género": row["Género"],
            "Edad": row["Edad"],
            "Ciudad": row["Ciudad"]
        }
        diccionario[nombre] = info

    return diccionario

# Ruta relativa desde la raíz del proyecto
ruta = "data/base_datos.xlsx"

# Diccionarios disponibles para importar
data = cargar_respuestas(ruta)
info_personal = cargar_informacion(ruta)

# Verificación
#print(data)
#print(info_personal)


