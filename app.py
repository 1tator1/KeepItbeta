import streamlit as st
from transformers import pipeline  
import docx   

# Carga el modelo de preguntas y respuestas de Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Función para extraer el texto de un documento .docx
def extraer_texto_docx(archivo_subido):
    documento = docx.Document(archivo_subido)
    texto = '\n'.join([p.text for p in documento.paragraphs if p.text.strip() != ""])
    return texto

# Título de la app
st.title("📄 Pregunta a tu documento: Rehabilitación de Cadera")

# Carga de archivo
archivo = st.file_uploader("Sube un archivo .docx", type=["docx"])
texto_documento = ""

# Procesamiento del archivo cargado
if archivo:
    texto_documento = extraer_texto_docx(archivo)
    with st.expander("📘 Ver contenido del documento"):
        st.write(texto_documento)

# Campo para escribir la pregunta y mostrar la respuesta
if texto_documento:
    pregunta = st.text_input("Escribe tu pregunta sobre el documento:")
    if pregunta:
        resultado = qa_pipeline({
            "context": texto_documento,
            "question": pregunta
        })
        st.success(f"✅ Respuesta: {resultado['answer']}")
