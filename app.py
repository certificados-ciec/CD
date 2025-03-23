import streamlit as st
import pandas as pd

st.set_page_config(page_title="Validación de Certificados", page_icon="🎓")

st.title("🎓 Validación de Certificados")
st.markdown("Seleccione el curso e ingrese su contraseña para validar y descargar su certificado.")

# 🔗 URLs públicas de las hojas (formato CSV)
URL_LISTA_CURSOS = "https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM/gviz/tq?tqx=out:csv"
URL_APROBADOS = "https://docs.google.com/spreadsheets/d/1tcJDdUtLYpXxHab7nPFNd4f910dQ4OdcF0T_s51gVTM/gviz/tq?tqx=out:csv"

# 🔄 Cargar datos
@st.cache_data
def cargar_datos():
    df_cursos = pd.read_csv(URL_LISTA_CURSOS, dtype=str).fillna("")
    df_aprobados = pd.read_csv(URL_APROBADOS, dtype=str).fillna("")
    return df_cursos, df_aprobados

try:
    df_cursos, df_aprobados = cargar_datos()
except Exception as e:
    st.error("❌ Error al cargar las hojas de cálculo. Verifica que los enlaces estén públicos y sean correctos.")
    st.stop()

# 🔽 Lista desplegable con los nombres de curso
nombre_curso = st.selectbox("Seleccione el curso o diplomado", df_cursos["Nombre del Curso o Diplomado"].unique())

# 🔒 Campo para contraseña
contraseña = st.text_input("Ingrese su contraseña", type="password")

# 🔍 Al hacer clic en "Validar"
if st.button("Validar"):
    fila_curso = df_cursos[df_cursos["Nombre del Curso o Diplomado"] == nombre_curso]

    if fila_curso.empty:
        st.error("❌ Curso no encontrado.")
    else:
        codigo = fila_curso.iloc[0]["Código"]
        nombre_archivo = f"{codigo}_{contraseña}.pdf"

        fila_archivo = df_aprobados[df_aprobados["Nombre de Archivo"] == nombre_archivo]

        if not fila_archivo.empty:
            enlace = fila_archivo.iloc[0]["Enlace"]
            st.success("✅ Certificado encontrado.")
            st.markdown(f"[📄 Descargar certificado]({enlace})", unsafe_allow_html=True)
        else:
            st.error("❌ Contraseña inválida o revise si el curso es correcto.")
