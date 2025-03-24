
# 🎓 Generador de Diplomas – Validación Automatizada

Sistema completo para la generación, validación y descarga de certificados académicos (diplomas) desarrollado por el CIEC – Facultad de Ciencias.

---

## 🛠️ ¿Qué hace este sistema?

- Automatiza la creación de certificados en formato `.pptx` personalizados.
- Inserta QR con enlaces públicos a cada PDF validado.
- Convierte automáticamente los `.pptx` a `.pdf` manteniendo el formato original.
- Registra los certificados generados en una hoja de Google Sheets.
- Permite a los usuarios validar y descargar su certificado a través de una app en Streamlit.

---

## 📁 Estructura en Google Drive

```
📁 Generador de Diplomas
├── 📂 Aprobados          ← Archivos Excel por curso
├── 📂 Certificados       ← Archivos .pptx generados
├── 📂 PDF                ← Certificados convertidos a PDF
├── 📂 QR                 ← Códigos QR generados
├── 📑 Plantilla base.pptx
```

---

## 🧾 Hojas de cálculo utilizadas

### 1. [Lista de Cursos y Diplomados](https://docs.google.com/spreadsheets/d/1Uciyv8-Ur611z1wdz38qRBwpviANxWlraaNhg-hb8SM)
Contiene:
- `Nombre del Curso o Diplomado`
- `Código`
- `Duración`
- `Fecha`

### 2. [Aprobados](https://docs.google.com/spreadsheets/d/1prUt0i0EWolsX_LuGl_yKzXPUWmy6CzCxi28zued5BA)
Contiene:
- `Nombre de Archivo` → Ej: `C-01_123456789.pdf`
- `Enlace` → URL pública del certificado PDF

---

## 🖥️ Aplicación en Streamlit

La aplicación:

- Permite seleccionar el curso desde una lista desplegable.
- Solicita la contraseña del participante.
- Verifica si el archivo `{Código}_{Contraseña}.pdf` existe en la hoja `"Aprobados"`.
- Si es válido, muestra el botón para descargar el certificado.

### 🎨 Diseño institucional:
- Logo oficial del CIEC.
- Colores personalizados (dorado y negro).
- Botón de descarga estilizado.

---

## 📦 Requisitos

```txt
streamlit
pandas
gspread
qrcode
python-pptx
google-api-python-client
```

---

## ▶️ Despliegue en Streamlit Cloud

1. Sube este repositorio a tu cuenta de GitHub.
2. Entra a [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Elige como archivo principal: `app.py` o `app_certificados.py`

---

## 🙌 Créditos

Sistema desarrollado por el **CIEC – Facultad de Ciencias**  
Universidad Pedagógica y Tecnológica de Colombia – UPTC  
Implementado con Google Colab + Streamlit

---
