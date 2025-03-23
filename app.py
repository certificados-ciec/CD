import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="Validación de Certificados", page_icon="📄", layout="centered")

# PERSONALIZA AQUÍ 🎨
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Empty.png/200px-Empty.png"  # Reemplaza con tu logo
COLOR_PRIMARIO = "#1E88E5"  # Azul institucional
COLOR_BOTON = "#43A047"     # Verde tipo éxito

# ENCABEZADO CON LOGO
st.markdown(f"""
    <div style="text-align:center;">
        <img src="{LOGO_URL}" width="120">
        <h1 style="color:{COLOR_PRIMARIO}; margin-bottom: 0;">Validación de Certificados</h1>
        <p style="font-size:18px;">Ingrese su curso y contraseña para validar su certificado.</p>
    </div>
""", unsafe_allow_html=True)

# URL de hojas de cálculo
URL_LISTA_CURSOS = "https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM/gviz/tq?tqx=out:csv"
URL_APROBADOS = "https://docs.google.com/spreadsheets/d/1tcJDdUtLYpXxHab7nPFNd4f910dQ4OdcF0T_s51gVTM/gviz/tq?tqx=out:csv"

# Cargar datos
@st.cache_data
def cargar_datos():
    df_cursos = pd.read_csv(URL_LISTA_CURSOS, dtype=str).fillna("")
    df_aprobados = pd.read_csv(URL_APROBADOS, dtype=str).fillna("")
    return df_cursos, df_aprobados

try:
    df_cursos, df_aprobados = cargar_datos()
except:
    st.error("❌ Error al cargar las hojas de cálculo.")
    st.stop()

# CURSO Y CONTRASEÑA
nombre_curso = st.selectbox("📘 Curso tomado", df_cursos["Nombre del Curso o Diplomado"].unique())
contraseña = st.text_input("🔐 Contraseña", type="password", placeholder="Ingrese su contraseña")

# BOTÓN DE VALIDACIÓN
if st.button("✅ Validar"):
    fila_curso = df_cursos[df_cursos["Nombre del Curso o Diplomado"] == nombre_curso]
    if fila_curso.empty:
        st.warning("⚠️ Curso no encontrado.")
    else:
        codigo = fila_curso.iloc[0]["Código"]
        nombre_archivo = f"{codigo}_{contraseña}.pdf"
        fila_archivo = df_aprobados[df_aprobados["Nombre de Archivo"] == nombre_archivo]

        if not fila_archivo.empty:
            enlace = fila_archivo.iloc[0]["Enlace"]
            st.success("✅ Certificado encontrado.")
            st.markdown(f"""
                <div style="text-align:center; margin-top:20px;">
                    <a href="{enlace}" target="_blank">
                        <button style="background-color:{COLOR_BOTON}; color:white; padding:10px 20px; border:none; border-radius:5px; font-size:16px;">
                            📄 Descargar Certificado
                        </button>
                    </a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Contraseña inválida o curso incorrecto.")

# PIE DE PÁGINA
st.markdown("""
    <hr style="margin-top:40px;">
    <div style="text-align:center; font-size:13px; color:gray;">
        Aplicación desarrollada para la validación automática de certificados académicos.
    </div>
""", unsafe_allow_html=True)
