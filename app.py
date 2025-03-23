import streamlit as st
import pandas as pd

# 🎨 Configuración general
st.set_page_config(page_title="Validación de Certificados", page_icon="📄", layout="centered")

# 🎓 Encabezado con estilo
st.markdown("""
    <div style="text-align:center">
        <h1 style="color:#2c3e50;">🔍 Validación de Certificados</h1>
        <p style="font-size:18px;">Seleccione su curso e ingrese su contraseña para descargar el certificado en PDF.</p>
    </div>
""", unsafe_allow_html=True)

# 📄 URLs de las hojas de cálculo
URL_LISTA_CURSOS = "https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM/gviz/tq?tqx=out:csv"
URL_APROBADOS = "https://docs.google.com/spreadsheets/d/1tcJDdUtLYpXxHab7nPFNd4f910dQ4OdcF0T_s51gVTM/gviz/tq?tqx=out:csv"

# 🔄 Carga de datos con caché
@st.cache_data
def cargar_datos():
    df_cursos = pd.read_csv(URL_LISTA_CURSOS, dtype=str).fillna("")
    df_aprobados = pd.read_csv(URL_APROBADOS, dtype=str).fillna("")
    return df_cursos, df_aprobados

try:
    df_cursos, df_aprobados = cargar_datos()
except:
    st.error("❌ No se pudo cargar la información. Verifica los enlaces o permisos de las hojas.")
    st.stop()

# 🧾 Interfaz principal
st.markdown("### 📘 Curso o diplomado tomado:")
nombre_curso = st.selectbox("", df_cursos["Nombre del Curso o Diplomado"].unique())

st.markdown("### 🔐 Contraseña del certificado:")
contraseña = st.text_input("", type="password", placeholder="Ingrese su contraseña aquí")

# 🎯 Botón de validación con estilo
if st.button("✅ Validar certificado"):
    fila_curso = df_cursos[df_cursos["Nombre del Curso o Diplomado"] == nombre_curso]

    if fila_curso.empty:
        st.warning("⚠️ Curso no encontrado.")
    else:
        codigo = fila_curso.iloc[0]["Código"]
        nombre_archivo = f"{codigo}_{contraseña}.pdf"

        fila_archivo = df_aprobados[df_aprobados["Nombre de Archivo"] == nombre_archivo]

        if not fila_archivo.empty:
            enlace = fila_archivo.iloc[0]["Enlace"]
            st.success("✅ ¡Certificado encontrado!")
            st.markdown(f"""
                <a href="{enlace}" target="_blank" style="text-decoration:none;">
                    <button style='padding:10px 20px; background-color:#27ae60; color:white; border:none; border-radius:5px; font-size:16px;'>📄 Descargar Certificado</button>
                </a>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Contraseña inválida o verifique si el curso o diplomado es el correcto.")

# 📌 Pie de página
st.markdown("""
    <hr>
    <div style="text-align:center; font-size:14px; color:gray;">
        Aplicación desarrollada para validar certificados digitales.
    </div>
""", unsafe_allow_html=True)
