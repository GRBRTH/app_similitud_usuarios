import streamlit as st
from backend.core import lista_usuarios, matriz_similitud, vecinos_mas_similares, dic_vectores, codificaciones
from data.data import data, info_personal 

# --- Título ---
st.title("🔍 Buscador de perfiles similares")

#Diseño estético con HTML
#-------------------------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general */
    .main {
        background-color: #f9f9f9;
    }

    /* Títulos principales */
    h1 {
        color: #1a237e;
        font-size: 36px;
        text-align: center;
    }

    /* Subtítulos */
    h3 {
        color: #333333;
        font-size: 24px;
        margin-top: 1em;
    }

    /* Botones con color del slider */
    .stButton>button {
        background-color: #F44336; /* Color igual al del slider */
        color: white;
        font-weight: bold;
        padding: 0.6em 1.2em;
        border: none;
        border-radius: 8px;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #D32F2F; /* Un poco más oscuro al hacer hover */
    }

    /* Tablas */
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        padding: 1em;
    }

    /* Texto general */
    p {
        font-size: 16px;
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

#-------------------------------------------------------------------------------------------------

# --- Selección de modo ---
modo = st.radio("¿Qué deseas hacer?", ["Seleccionar perfil existente", "Ingresar nuevo perfil"])

# --- Seleccionar perfil existente ---
if modo == "Seleccionar perfil existente":
    perfil_objetivo = st.selectbox("Selecciona un perfil", lista_usuarios)
    k = st.slider("Cantidad de vecinos similares", 1, len(lista_usuarios)-1, 3)

    if st.button("Buscar vecinos similares"):
        resultado = vecinos_mas_similares(perfil_objetivo, k, lista_usuarios, matriz_similitud)

        #--------------------------------------------------------------------------------------
        #st.subheader(f"Perfiles más similares a **{perfil_objetivo}**:")
        #for nombre, similitud in resultado:
        #    st.write(f"- {nombre} (similitud: {similitud})")
        #--------------------------------------------------------------------------------------

        st.markdown(f"### 🤝 Los {k} perfiles más semejantes a {perfil_objetivo} son:")

        for vecino, similitud in resultado:
            info = info_personal.get(vecino, {"Género": "Desconocido", "Edad": "?", "Ciudad": "?"})
            
            st.markdown(f"""
            <div style="background-color:#ffffff;padding:10px 15px;border-radius:10px;
                        margin-bottom:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);">
                <strong>{vecino}</strong> (🔗 Similitud: <strong>{similitud:.2f}</strong>)<br>
                🧑 <strong>Género:</strong> {info['Género']}<br>
                🎂 <strong>Edad:</strong> {info['Edad']} años<br>
                📍 <strong>Ciudad:</strong> {info['Ciudad']}
            </div>
            """, unsafe_allow_html=True)

        # Gráfico de barras ---------------------------
        import matplotlib.pyplot as plt
        nombres = [nombre for nombre, _ in resultado]
        valores = [sim for _, sim in resultado]
        fig, ax = plt.subplots()
        ax.barh(nombres, valores, color='green')
        ax.set_xlabel("Similitud")
        ax.set_title(f"Similitud con {perfil_objetivo}")
        ax.invert_yaxis()
        st.subheader(f"📊 Perfiles más similares a {perfil_objetivo}")
        st.pyplot(fig)
        # ----------------------------------------------

        # Tabla comparativa -----------------------------------------------------
        import pandas as pd
        preguntas = ["P1", "P2", "P3", "P4"]
        res_objetivo = data[perfil_objetivo]

        # Fila del perfil objetivo
        datos_tabla = [{
            "Usuario": perfil_objetivo,
            **{pregunta: r for pregunta, r in zip(preguntas, res_objetivo)},
            "Similitud": 1.0,
            **info_personal.get(perfil_objetivo, {"Género": "N/A", "Edad": "N/A", "Ciudad": "N/A"})
        }]

        for nombre, sim in resultado:
            respuestas = data[nombre]
            fila = {
                "Usuario": nombre,
                **{pregunta: r for pregunta, r in zip(preguntas, respuestas)},
                "Similitud": sim,
                **info_personal.get(nombre, {"Género": "N/A", "Edad": "N/A", "Ciudad": "N/A"})
            }
            datos_tabla.append(fila)

        df_tabla = pd.DataFrame(datos_tabla)
        st.subheader("📋 Tabla comparativa de respuestas y datos personales")
        st.dataframe(df_tabla)
        # ---------------------------------------------------------------------------

        # --- Gráficos demográficos de vecinos --------------------------------------
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd

        # Obtener los nombres de los vecinos (sin incluir al perfil objetivo)
        nombres_vecinos = [nombre for nombre, _ in resultado]

        # Obtener su información personal
        datos_info = [info_personal.get(nombre, {"Género": "N/A", "Edad": None, "Ciudad": "N/A"}) for nombre in nombres_vecinos]
        df_info = pd.DataFrame(datos_info)
        df_info["Usuario"] = nombres_vecinos

        # Asegurarse de que Edad sea numérica
        df_info["Edad"] = pd.to_numeric(df_info["Edad"], errors="coerce")

        # Crear columnas
        col1, col2, col3 = st.columns(3)

        # 1. Gráfico de torta - Género
        with col1:
            st.subheader("👨👩 Género")
            genero_counts = df_info["Género"].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(genero_counts, labels=genero_counts.index, autopct="%1.1f%%", startangle=90)
            ax1.axis("equal")
            st.pyplot(fig1)

        # 2. Gráfico de barras - Edad
        with col2:
            st.subheader("🪪 Edad")
            bins = [15, 25, 35, 45, 60]
            labels = ["16–25", "26–35", "36–45", "46–60"]
            df_info["Rango Edad"] = pd.cut(df_info["Edad"], bins=bins, labels=labels)
            edad_counts = df_info["Rango Edad"].value_counts().sort_index()
            fig2, ax2 = plt.subplots()
            sns.barplot(x=edad_counts.index, y=edad_counts.values, palette="crest", ax=ax2)
            ax2.set_xlabel("Rango")
            ax2.set_ylabel("Cantidad")
            st.pyplot(fig2)

        # 3. Gráfico de barras - Ciudad
        with col3:
            st.subheader("🏙️🌆 Ciudad")
            ciudad_counts = df_info["Ciudad"].value_counts()
            fig3, ax3 = plt.subplots()
            sns.barplot(x=ciudad_counts.index, y=ciudad_counts.values, palette="Set2", ax=ax3)
            ax3.set_xlabel("Ciudad")
            ax3.set_ylabel("Cantidad")
            ax3.tick_params(axis='x', rotation=45)
            st.pyplot(fig3)

        #----------------------------------------------------------------------------------


# --- Ingresar nuevo perfil ---
else:
    nombre_nuevo = st.text_input("Nombre del nuevo usuario")

    if nombre_nuevo in data:
        st.error("Ese nombre ya existe. Elige otro.")
    elif nombre_nuevo:
        p1 = st.selectbox("¿Qué comida del día prefieres?", ["Cena", "Almuerzo", "Desayuno"])
        p2 = st.selectbox("¿Cuál es tu deporte favorito?", ["Baloncesto", "Fútbol", "Tennis"])
        p3 = st.selectbox("¿Cuál es tu libro favorito?", ["Don Quijote de la Mancha", "La casa de los espíritus", "Crónica de una muerte anunciada"])
        p4 = st.selectbox("¿Qué serie te gusta más?", ["Juego de Tronos", "Breaking Bad", "Peaky Blinders"])
        k = st.slider("Cantidad de vecinos similares", 1, len(lista_usuarios), 3)

        if st.button("Buscar vecinos similares"):
            nuevo_data = data.copy()
            nuevo_data[nombre_nuevo] = [p1, p2, p3, p4]

            from backend.core import convertir_a_vectores, calcular_matriz_distancias, calcular_matriz_similitud

            nuevos_vectores = convertir_a_vectores(nuevo_data, codificaciones)
            nueva_lista_usuarios = list(nuevo_data.keys())
            nueva_matriz_distancias = calcular_matriz_distancias(nueva_lista_usuarios, nuevos_vectores)
            nueva_matriz_similitud = calcular_matriz_similitud(nueva_matriz_distancias)

            resultado = vecinos_mas_similares(nombre_nuevo, k, nueva_lista_usuarios, nueva_matriz_similitud)

            #------------------------------------------------------------------------
            #st.subheader(f"Perfiles más similares a **{nombre_nuevo}**:")
            #for nombre, similitud in resultado:
            #    st.write(f"- {nombre} (similitud: {similitud})")
            #------------------------------------------------------------------------

            st.markdown(f"### 🤝 Los {k} perfiles más semejantes a {nombre_nuevo} son:")

            for vecino, similitud in resultado:
                info = info_personal.get(vecino, {"Género": "Desconocido", "Edad": "?", "Ciudad": "?"})
                
                st.markdown(f"""
                <div style="background-color:#ffffff;padding:10px 15px;border-radius:10px;
                            margin-bottom:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);">
                    <strong>{vecino}</strong> (🔗 Similitud: <strong>{similitud:.2f}</strong>)<br>
                    🧑 <strong>Género:</strong> {info['Género']}<br>
                    🎂 <strong>Edad:</strong> {info['Edad']} años<br>
                    📍 <strong>Ciudad:</strong> {info['Ciudad']}
                </div>
                """, unsafe_allow_html=True)

            # Gráfico
            import matplotlib.pyplot as plt
            nombres = [nombre for nombre, _ in resultado]
            valores = [sim for _, sim in resultado]
            fig, ax = plt.subplots()
            ax.barh(nombres, valores, color='blue')
            ax.set_xlabel("Similitud")
            ax.set_title(f"Similitud con {nombre_nuevo}")
            ax.invert_yaxis()
            st.subheader(f"📊 Perfiles más similares a {nombre_nuevo}")
            st.pyplot(fig)
            # ------------------------------------------------------------------------

            # Tabla comparativa ------------------------------------------------------
            import pandas as pd
            preguntas = ["P1", "P2", "P3", "P4"]
            res_objetivo = [p1, p2, p3, p4]

            datos_tabla = [{
                "Usuario": nombre_nuevo,
                **{pregunta: r for pregunta, r in zip(preguntas, res_objetivo)},
                "Similitud": 1.0,
                "Género": "N/A",
                "Edad": "N/A",
                "Ciudad": "N/A"
            }]

            for nombre, sim in resultado:
                respuestas = nuevo_data[nombre]
                fila = {
                    "Usuario": nombre,
                    **{pregunta: r for pregunta, r in zip(preguntas, respuestas)},
                    "Similitud": sim,
                    **info_personal.get(nombre, {"Género": "N/A", "Edad": "N/A", "Ciudad": "N/A"})
                }
                datos_tabla.append(fila)

            df_tabla = pd.DataFrame(datos_tabla)
            st.subheader("📋 Tabla comparativa de respuestas y datos personales")
            st.dataframe(df_tabla)
            #--------------------------------------------------------------------------------

            # --- Gráficos demográficos de vecinos ---
            import matplotlib.pyplot as plt
            import seaborn as sns
            import pandas as pd

            # Obtener los nombres de los vecinos (sin incluir al perfil objetivo)
            nombres_vecinos = [nombre for nombre, _ in resultado]

            # Obtener su información personal
            datos_info = [info_personal.get(nombre, {"Género": "N/A", "Edad": None, "Ciudad": "N/A"}) for nombre in nombres_vecinos]
            df_info = pd.DataFrame(datos_info)
            df_info["Usuario"] = nombres_vecinos

            # Asegurarse de que Edad sea numérica
            df_info["Edad"] = pd.to_numeric(df_info["Edad"], errors="coerce")

            # Crear columnas
            col1, col2, col3 = st.columns(3)

            # 1. Gráfico de torta - Género
            with col1:
                st.subheader("👨👩 Género")
                genero_counts = df_info["Género"].value_counts()
                fig1, ax1 = plt.subplots()
                ax1.pie(genero_counts, labels=genero_counts.index, autopct="%1.1f%%", startangle=90)
                ax1.axis("equal")
                st.pyplot(fig1)

            # 2. Gráfico de barras - Edad
            with col2:
                st.subheader("🪪 Edad")
                bins = [15, 25, 35, 45, 60]
                labels = ["16–25", "26–35", "36–45", "46–60"]
                df_info["Rango Edad"] = pd.cut(df_info["Edad"], bins=bins, labels=labels)
                edad_counts = df_info["Rango Edad"].value_counts().sort_index()
                fig2, ax2 = plt.subplots()
                sns.barplot(x=edad_counts.index, y=edad_counts.values, palette="crest", ax=ax2)
                ax2.set_xlabel("Rango")
                ax2.set_ylabel("Cantidad")
                st.pyplot(fig2)

            # 3. Gráfico de barras - Ciudad
            with col3:
                st.subheader("🏙️🌆 Ciudad")
                ciudad_counts = df_info["Ciudad"].value_counts()
                fig3, ax3 = plt.subplots()
                sns.barplot(x=ciudad_counts.index, y=ciudad_counts.values, palette="Set2", ax=ax3)
                ax3.set_xlabel("Ciudad")
                ax3.set_ylabel("Cantidad")
                ax3.tick_params(axis='x', rotation=45)
                st.pyplot(fig3)



            


