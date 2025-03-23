import streamlit as st
import pandas as pd
import requests

# CONFIGURACIÓN DE LA APP
st.set_page_config(page_title="Validación de Certificados", page_icon="🎓", layout="centered")

st.title("🎓 Validación de Certificados")
st.markdown("Seleccione el curso y digite su contraseña para descargar su certificado.")

# 📥 URL pública de la hoja de cálculo (formato CSV seguro)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM/gviz/tq?tqx=out:csv"

# 📂 Carpeta pública de certificados PDF
CARPETA_DRIVE_PUBLICA = "https://drive.google.com/drive/folders/1-2jydDm0CIbLoGVR7J6IeXxPJKgVq7-n"
URL_BASE_VISUALIZACION = "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
URL_BASE_DESCARGA_NOMBRE = "https://drive.google.com/uc?export=download&id=FILE_ID"

# 🔄 Función para obtener el listado de cursos y códigos
@st.cache_data
def cargar_cursos():
    df = pd.read_csv(SHEET_CSV_URL)
    cursos = df["Nombre del Curso o Diplomado"].dropna().tolist()
    codigos = df.set_index("Nombre del Curso o Diplomado")["Código"].to_dict()
    return cursos, codigos

# CARGA DE DATOS
try:
    cursos, codigos = cargar_cursos()
except Exception as e:
    st.error("❌ No se pudo cargar la lista de cursos. Verifique si la hoja es pública.")
    st.stop()

# INTERFAZ
curso_seleccionado = st.selectbox("Seleccione el curso o diplomado", cursos)
password_input = st.text_input("Ingrese su contraseña", type="password")

# FUNCIÓN PARA CONSTRUIR URL DE PRUEBA
def construir_url_descarga(nombre_archivo):
    # Se usa para verificar si el archivo existe
    return f"https://drive.google.com/file/d/{nombre_archivo}/view?usp=sharing"

# FUNCIÓN PARA VERIFICAR SI EXISTE ARCHIVO
def archivo_existe(nombre_archivo):
    # Esto solo funciona si el archivo es públicamente accesible con nombre conocido
    try:
        response = requests.get(construir_url_descarga(nombre_archivo))
        return response.status_code == 200
    except:
        return False

if st.button("Validar"):
    codigo = codigos.get(curso_seleccionado)
    if not codigo:
        st.error("❌ Curso no válido. Intente de nuevo.")
    else:
        # Construir nombre esperado del archivo
        nombre_archivo = f"{codigo}_{password_input}"
        url_visualizacion = f"https://drive.google.com/file/d/{nombre_archivo}/view?usp=sharing"
        url_descarga_directa = f"https://drive.google.com/uc?export=download&id={nombre_archivo}"

        # Intentamos validar por nombre directo (solo si sabes que los nombres coinciden con los IDs)
        existe = archivo_existe(nombre_archivo)

        if existe:
            st.success("✅ Validación exitosa.")
            st.markdown(f"[📄 Descargar certificado]({url_descarga_directa})", unsafe_allow_html=True)
        else:
            st.error("❌ Contraseña inválida o revise si el curso o diplomado es correcto.")
