# Importamos las librerías necesarias
import streamlit as st                       # Para crear la interfaz web
from transformers import pipeline            # Para cargar el modelo de preguntas y respuestas
import docx                                  # Para leer archivos de Word (.docx)

# Cargamos el modelo de lenguaje que responde preguntas usando Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Función para leer el contenido del archivo DOCX
def extraer_texto_docx(archivo_subido):
    documento = docx.Document(archivo_subido)                  # Abrimos el archivo de Word
    texto = '\n'.join([p.text for p in documento.paragraphs   # Unimos los párrafos con salto de línea
                       if p.text.strip() != ""])              # Ignoramos líneas vacías
    return texto

# Título de la aplicación
st.title("📄 KeepIt: PREGUNTA TUS DUDAS")

# Paso 1: El usuario sube el archivo
archivo = st.file_uploader("Sube un archivo .docx", type=["docx"])

# Variable para almacenar el texto del documento
texto_documento = ""

# Si el usuario ha subido un archivo
if archivo:
    texto_documento = extraer_texto_docx(archivo)   # Extraemos el texto del archivo
    # Mostramos el texto extraído si el usuario quiere verlo
    with st.expander("📘 Ver contenido del documento"):
        st.write(texto_documento)

# Paso 2: El usuario hace una pregunta
if texto_documento:
    pregunta = st.text_input("Escribe tu pregunta sobre el documento:")

    # Si hay una pregunta, generamos una respuesta
    if pregunta:
        resultado = qa_pipeline({
            "context": texto_documento,     # El texto del documento
            "question": pregunta            # La pregunta del usuario
        })

        # Mostramos la respuesta encontrada
        st.success(f"✅ Respuesta: {resultado['answer']}")
