import streamlit as st
import pytesseract
from PIL import Image
import base64

st.title("Detector de Juegos Enigma")
st.write("Subí una imagen o escribí texto para analizar posibles pistas ocultas.")

# Subida de imagen
uploaded_file = st.file_uploader("Subí una imagen del perfil", type=["jpg", "png", "jpeg"])
text_input = st.text_area("O pegá texto directamente")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    with st.spinner("Analizando texto en la imagen..."):
        extracted_text = pytesseract.image_to_string(image)
        st.subheader("Texto detectado:")
        st.code(extracted_text)

        text_input += "\n" + extracted_text

# Función simple para detectar patrones
def detect_patterns(text):
    hints = []
    if any(char.isdigit() for char in text):
        hints.append("Contiene números (¿clave numérica?)")
    if any(char.isupper() for char in text) and any(char.islower() for char in text):
        hints.append("Tiene mayúsculas y minúsculas mezcladas (¿clave oculta?)")
    if "==" in text or "/" in text:
        hints.append("Parece Base64")
    if len(set(text)) < len(text) / 2:
        hints.append("Repite muchas letras (¿Vigenère?)")
    return hints

if text_input:
    st.subheader("Posibles pistas encontradas:")
    for hint in detect_patterns(text_input):
        st.write("• " + hint)

    st.subheader("Intento de decodificación básica (Base64):")
    try:
        decoded = base64.b64decode(text_input.strip()).decode("utf-8")
        st.code(decoded)
    except:
        st.write("No parece estar en Base64.")

# Espacio para conectar con una IA
st.subheader("¿Querés ayuda de la IA?")
if st.button("Enviar texto a ChatGPT"):
    st.write("Copiá el texto y pegalo en ChatGPT (próxima versión lo hará automáticamente).")