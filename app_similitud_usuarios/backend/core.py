from data.data import data
import math


#Obtener los nombres de los usuarios
lista_usuarios = list(data.keys())
#Obtener las respuestas de los usuarios
lista_respuestas = list(data.values())

# Paso 2: Asignar valores numéricos a cada respuesta (una codificación simple)
# Creamos un diccionario con un mapping de pregunta -> respuesta -> número
def codificar_respuestas(data):
    preguntas = zip(*data.values())  # Transpone la lista de respuestas
    codificaciones = []

    for i, respuestas in enumerate(preguntas):
        respuestas_unicas = list(sorted(set(respuestas)))
        codificacion = {respuesta: idx for idx, respuesta in enumerate(respuestas_unicas)}
        codificaciones.append(codificacion)

    return codificaciones

codificaciones = codificar_respuestas(data) #Aquí se extraen los resultados de las codificaciones

# Paso 3: Convertir perfiles a vectores numéricos
def convertir_a_vectores(data, codificaciones):
    vectores = {}
    for usuario, respuestas in data.items():
        vector = [codificaciones[i][respuesta] for i, respuesta in enumerate(respuestas)]
        vectores[usuario] = vector
    return vectores

dic_vectores = convertir_a_vectores(data, codificaciones)

# Paso 4: Calcular matriz de distancias euclidianas
def calcular_matriz_distancias(usuarios, vectores):
    matriz = []
    for u1 in usuarios:
        fila = []
        for u2 in usuarios:
            v1 = vectores[u1]
            v2 = vectores[u2]
            if u1 == u2:
                distancia = 0.0
            else:
                suma_cuadrados = sum((a - b) ** 2 for a, b in zip(v1, v2))
                distancia = math.sqrt(suma_cuadrados)
            fila.append(round(distancia, 2))
        matriz.append(fila)
    return matriz

matriz_distancias = calcular_matriz_distancias(lista_usuarios, dic_vectores)

# Paso 5: Calcular matriz de similitud
def calcular_matriz_similitud(matriz_distancias):
    max_dist = max(max(fila) for fila in matriz_distancias if max(fila) != 0)
    matriz_similitud = []
    for fila in matriz_distancias:
        nueva_fila = [round(1 - (d / max_dist), 2) if d != 0 else 1.0 for d in fila]
        matriz_similitud.append(nueva_fila)
    return matriz_similitud

matriz_similitud = calcular_matriz_similitud(matriz_distancias)

# Paso 6: Buscar vecinos más similares
def vecinos_mas_similares(nombre_objetivo, k, usuarios, matriz_similitud):
    if nombre_objetivo not in usuarios:
        raise ValueError("Usuario no encontrado.")

    i = usuarios.index(nombre_objetivo)
    similitudes = matriz_similitud[i]

    vecinos = []
    for j, sim in enumerate(similitudes):
        if j != i:
            vecinos.append((usuarios[j], sim))

    vecinos.sort(key=lambda x: x[1], reverse=True)
    return vecinos[:k]
