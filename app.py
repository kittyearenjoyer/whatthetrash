import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

# --- CONFIG ---
MODEL_NAME = "tahzaya/trash-sorter-ai"

st.set_page_config(page_title="Trash AI", layout="centered")

st.title("♻️ AI Mülltrenner")
st.write("Lade ein Bild hoch – die KI sagt dir, was es ist und wie du es entsorgen solltest.")

# --- LOAD MODEL (cached) ---
@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    return processor, model

processor, model = load_model()

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Dein Bild", use_column_width=True)

    # --- PREPROCESS ---
    inputs = processor(images=image, return_tensors="pt")

    # --- INFERENCE ---
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()

    label = model.config.id2label[predicted_class_id]

    # --- OUTPUT ---
    st.success(f"Erkannt: **{label}**")

    # Optional einfache Müll-Logik
    disposal_map = {
        "plastic": "Gelbe Tonne 🟡",
        "paper": "Blaue Tonne 🔵",
        "glass": "Glascontainer 🟢",
        "metal": "Gelbe Tonne 🟡",
        "organic": "Biotonne 🟤",
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
