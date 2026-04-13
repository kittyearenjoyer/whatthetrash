import streamlit as st
from PIL import Image
import torch
import torchvision.transforms as transforms
from transformers import AutoModelForImageClassification

# --- CONFIG ---
MODEL_NAME = "tahzaya/trash-sorter-ai"

st.set_page_config(page_title="Trash AI", layout="centered")

st.title("♻️ AI Mülltrenner")
st.write("Lade ein Bild hoch – die KI erkennt den Müll und sagt dir, wo er hin gehört.")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()

    # Manuelles Preprocessing (kein HF Processor nötig)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    return model, transform

model, transform = load_model()

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Dein Bild", use_column_width=True)

    # --- PREPROCESS ---
    img_tensor = transform(image).unsqueeze(0)

    # --- INFERENCE ---
    with torch.no_grad():
        outputs = model(img_tensor)
        logits = outputs.logits
        predicted_class_id = logits.argmax(-1).item()

    label = model.config.id2label[predicted_class_id]

    # --- OUTPUT ---
    st.success(f"Erkannt: **{label}**")

    # --- Mülltrennung (simple Logik) ---
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
