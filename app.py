import streamlit as st
from PIL import Image
from transformers import pipeline

# --- CONFIG ---
MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="Trash AI", layout="centered")

st.title("♻️ AI Mülltrenner")
st.write("Lade ein Bild hoch – die KI erkennt den Müll und sagt dir, wo er hin gehört.")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return pipeline("image-classification", model=MODEL_NAME)

classifier = load_model()

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Dein Bild", use_column_width=True)

    # --- INFERENCE ---
    with st.spinner("Analysiere Bild..."):
        results = classifier(image)

    top_result = results[0]
    label = top_result["label"]
    score = top_result["score"]

    st.success(f"Erkannt: **{label}** ({score:.2%})")

    # --- Mülltrennung ---
    disposal_map = {
        "plastic": "Gelbe Tonne 🟡",
        "paper": "Blaue Tonne 🔵",
        "cardboard": "Blaue Tonne 🔵",
        "glass": "Glascontainer 🟢",
        "metal": "Gelbe Tonne 🟡",
        "trash": "Restmüll ⚫",
    }

    lower_label = label.lower()
    found = False

    for key in disposal_map:
        if key in lower_label:
            st.info(f"➡️ Entsorgung: {disposal_map[key]}")
            found = True
            break

    if not found:
        st.warning("Keine klare Entsorgung erkannt – bitte lokal prüfen.")
