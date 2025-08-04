# 🧠 Aplicación de Similitud entre Usuarios

Aplicación web desarrollada con **Streamlit** que recomienda perfiles similares utilizando la técnica de **k vecinos más cercanos (k-NN)**. Basada en las respuestas de un cuestionario, permite identificar usuarios afines, ideal para:

- Matchmaking personalizado
- Análisis de afinidad
- Segmentación de usuarios

---

## 🧩 Problemática a Abordar

Hoy en día, muchas plataformas requieren ofrecer contenido personalizado. Ya sea para entretenimiento, e-commerce o redes sociales, es clave identificar patrones comunes entre usuarios.

Este proyecto aborda cómo detectar usuarios con gustos o respuestas similares de manera automatizada, utilizando ciencia de datos.

---

## 🚀 Solución Propuesta

Se utilizó el algoritmo **k-Nearest Neighbors (KNN)** para comparar perfiles en base a sus respuestas vectorizadas. Las distancias euclidianas permiten determinar qué usuarios son más parecidos entre sí.

---

## 🛠️ Herramientas y Librerías

- **Python**: lenguaje principal
- **Streamlit**: interfaz web interactiva
- **Pandas**: manipulación de datos
- **NumPy**: operaciones matemáticas
- **Matplotlib**: visualización de resultados
- **scikit-learn**: cálculo de distancias y análisis KNN
- **Openpyxl**: lectura de archivos Excel

> Las dependencias están listadas en el archivo [`requirements.txt`](./requirements.txt)

---

## 🗂️ Estructura del Proyecto

app_similitud_usuarios/

├── backend/ # Lógica del análisis y procesamiento

├── data/ # Datos base (Excel, codificación, etc.)

├── frontend/ # Visualización HTML (Streamlit)

├── notebooks/ # Análisis exploratorio y desarrollo previo (Colab)

├── main.py # Archivo principal que ejecuta la app

├── README.md # Este archivo

├── requirements.txt # Dependencias del proyecto


---

## 📈 Proceso General

1. **Creación del dataset**: se define una tabla de usuarios con respuestas a 4 preguntas.
2. **Codificación**: respuestas categóricas son convertidas a valores numéricos.
3. **Vectorización**: cada perfil es representado como un vector.
4. **Cálculo de distancias**: se mide la similitud con otros usuarios.
5. **Recomendación**: se muestran los `k` perfiles más similares.

---

## 🧪 Cómo Ejecutar la App
--
1. Clona el repositorio:
---
bash

git clone https://github.com/tu_usuario/app_similitud_usuarios.git
---
cd app_similitud_usuarios
--
Instala las dependencias:
---
bash

pip install -r requirements.txt
--
Ejecuta la app:
---
bash

streamlit run main.py
--
📓 Notebooks:

El análisis completo, pruebas, codificación y lógica KNN están en la carpeta /notebooks.
--
Informe del proyecto:

El informe que detalla el contenido teórico del proyecto se encuentra en el archivo Informe.md
--
🏁 Conclusión:

Este proyecto demuestra cómo aplicar técnicas de ciencia de datos para personalización basada en afinidad entre usuarios. Su diseño modular permite escalarlo fácilmente a nuevos contextos como:
-Motores de recomendación
-Segmentación de audiencias
-Matching en redes sociales o sitios de citas
