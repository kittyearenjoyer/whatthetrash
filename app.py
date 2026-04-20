import streamlit as st
from PIL import Image
from transformers import pipeline

# --- CONFIG ---
MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="Trash AI", layout="centered")

st.title("♻️ Trash AI")
st.write("Bild hochladen oder Webcam nutzen.")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return pipeline("image-classification", model=MODEL_NAME)

classifier = load_model()

# --- Prediction Function ---
def predict_image(image):
    results = classifier(image)
    top = results[0]

    label = top["label"]
    score = top["score"]

    st.success(f"Erkannt: **{label}** ({score:.1%})")

    disposal_map = {
        "plastic": "Gelbe Tonne 🟡",
        "paper": "Blaue Tonne 🔵",
        "cardboard": "Blaue Tonne 🔵",
        "glass": "Glascontainer 🟢",
        "metal": "Gelbe Tonne 🟡",
        "trash": "Restmüll ⚫",
    }

    found = False
    for key in disposal_map:
        if key in label.lower():
            st.info(f"➡️ Entsorgung: {disposal_map[key]}")
            found = True
            break

    if not found:
        st.warning("Bitte lokal prüfen.")

# --- TABS ---
tab1, tab2 = st.tabs(["📁 Upload", "📷 Webcam"])

# ---------- Upload ----------
with tab1:
    uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Dein Bild", use_column_width=True)

        with st.spinner("Analysiere..."):
            predict_image(image)

# ---------- Webcam ----------
with tab2:
    camera_image = st.camera_input("Foto machen")

    if camera_image:
        image = Image.open(camera_image).convert("RGB")
        st.image(image, caption="Webcam Bild", use_column_width=True)

        with st.spinner("Analysiere..."):
            predict_image(image)
