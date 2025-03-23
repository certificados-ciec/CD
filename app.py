import streamlit as st
import pandas as pd
import requests

# CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="Validación de Certificados", page_icon="🎓", layout="centered")

st.title("🎓 Validación de Certificados")
st.markdown("Seleccione el curso y digite su contraseña para descargar su certificado.")

# 📥 URL pública de la hoja de cálculo (en formato CSV exportable)
# Reemplaza con el ID real de tu Google Sheets si cambia
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM/export?format=csv"

# 📂 Carpeta pública de certificados PDF
PDF_PUBLIC_FOLDER = "https://drive.google.com/uc?export=download&id="  # Usaremos el ID del archivo más adelante
PDF_FOLDER_VIEW = "https://drive.google.com/drive/folders/1-2jydDm0CIbLoGVR7J6IeXxPJKgVq7-n"

# 🔄 Función para obtener el listado de cursos y códigos
@st.cache_data
def cargar_cursos():
    df = pd.read_csv(SHEET_CSV_URL)
    cursos = df["Nombre del Curso o Diplomado"].tolist()
    codigos = df.set_index("Nombre del Curso o Diplomado")["Código"].to_dict()
    return cursos, codigos

# 🔍 Buscar archivo en la carpeta pública
def validar_certificado(codigo, contraseña):
    archivo_nombre = f"{codigo}_{contraseña}.pdf"
    url = f"https://drive.google.com/file/d/{archivo_nombre}/view?usp=sharing"
    response = requests.get(url)
    return url if response.status_code == 200 else None

# CARGA DE DATOS
cursos, codigos = cargar_cursos()

# INTERFAZ
curso_seleccionado = st.selectbox("Seleccione el curso o diplomado", cursos)
password_input = st.text_input("Ingrese su contraseña", type="password")

if st.button("Validar"):
    codigo = codigos.get(curso_seleccionado)
    if not codigo:
        st.error("Curso no válido. Intente de nuevo.")
    else:
        archivo_nombre = f"{codigo}_{password_input}.pdf"
        pdf_url = f"https://drive.google.com/uc?export=download&id={archivo_nombre}"

        # Verificar si existe el archivo por su URL directa
        test_url = f"https://drive.google.com/file/d/{archivo_nombre}/view"
        response = requests.get(test_url)

        if response.status_code == 200:
            st.success("✅ Validación exitosa.")
            st.markdown(f"[📄 Descargar certificado]({pdf_url})", unsafe_allow_html=True)
        else:
            st.error("❌ Contraseña inválida o revise si el curso o diplomado es correcto.")
