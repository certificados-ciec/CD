import streamlit as st
import pandas as pd

# CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="Validación de Certificados", page_icon="📄", layout="centered")

# PERSONALIZA AQUÍ 🎨
LOGO_URL = "https://raw.githubusercontent.com/certificados-ciec/CD/main/Logo.png"

COLOR_FONDO = "#FFFFFF"
COLOR_TEXTO = "#000000"
COLOR_TITULO = "#f0b124"   # Dorado fuerte
COLOR_BOTON = "#f3d027"    # Dorado claro
COLOR_LINEA = "#dcdcda"    # Gris claro

st.markdown(f"""
    <div style="background-color:{COLOR_FONDO}; padding:20px; text-align:center; border-radius:10px;">
        <img src="{LOGO_URL}" width="200" style="margin-bottom:10px;">
        <h1 style="color:{COLOR_TITULO}; margin-bottom:0;">Validación de Certificados</h1>
        <p style="font-size:18px; color:{COLOR_TEXTO}; margin-top:5px;">
            Ingrese su curso y contraseña para validar su certificado en PDF.
        </p>
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
                        <button style="background-color:{COLOR_BOTON}; color:{COLOR_TEXTO}; padding:10px 20px; border:none; border-radius:5px; font-size:16px; font-weight:bold; cursor:pointer;">
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
