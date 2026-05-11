import io
import os
import tempfile

import streamlit as st
from PIL import Image
from transformers import pipeline

# ---------------- CONFIG ----------------
MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(
    page_title="What the Trash",
    page_icon="♻️",
    layout="wide",
)

# ---------------- MODERN UI CSS ----------------
st.markdown("""
<style>

/* ---------- Hintergrund ---------- */
.main {
    background: linear-gradient(180deg, #f8fafc 0%, #e5e7eb 100%);
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

/* ---------- Alle Texte schwarz ---------- */
html, body, p, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: black !important;
}

/* ---------- Hero ---------- */
.hero-box {
    padding: 2.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, #22c55e, #86efac);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    margin-bottom: 1.5rem;
}

/* ---------- Cards ---------- */
.glass-card {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 22px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.metric-box {
    background: rgba(255,255,255,0.7);
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(0,0,0,0.08);
}

.small-text {
    font-size: 0.95rem;
}

/* ---------- Buttons ---------- */
.stButton>button {
    width: 100%;
    border-radius: 14px;
    height: 3rem;
    border: none;
    font-weight: 700;
    color: black !important;
}

/* ---------- Upload + Kamera ---------- */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    padding: 1rem;
    border-radius: 18px;
}

[data-testid="stCameraInput"] {
    background: rgba(255,255,255,0.65);
    padding: 1rem;
    border-radius: 18px;
}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
    color: black !important;
    padding-bottom: 10px;
}

div[data-testid="stTabs"] {
    margin-bottom: -12px;
}

/* ---------- Weiße leere Box entfernen ---------- */
div[data-testid="stTabs"] + div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    min-height: 0 !important;
}

/* ---------- Allgemein unnötige weiße Flächen killen ---------- */
section.main > div {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    clf = pipeline(
        "image-classification",
        model=MODEL_NAME,
        device=-1,
        framework="pt",
    )
    return clf

classifier = load_model()

# ---------------- HELPERS ----------------
def get_disposal(label: str) -> str:
    disposal_map = {
        "plastic":   "Gelbe Tonne 🟡",
        "paper":     "Blaue Tonne 🔵",
        "cardboard": "Blaue Tonne 🔵",
        "glass":     "Glascontainer 🟢",
        "metal":     "Gelbe Tonne 🟡",
        "trash":     "Restmüll ⚫",
    }
    for key, value in disposal_map.items():
        if key in label.lower():
            return value
    return "Lokal prüfen 📍"


def run_prediction(image: Image.Image):
    # transformers 4.41.2 load_image() only accepts: PIL.Image, str path, or URL.
    # Save to a temp file and pass the path — most reliable across all versions.
    img = image.convert("RGB")
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        img.save(tmp, format="JPEG")
        tmp_path = tmp.name
    try:
        results = classifier(tmp_path)
    finally:
        os.unlink(tmp_path)
    top = results[0]
    return top["label"], top["score"]


def show_results(image: Image.Image):
    """Display image + prediction results."""
    st.image(image, use_container_width=True)
    with st.spinner("KI analysiert Bild..."):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    st.success(f"Erkannt: **{label}**")
    st.info(f"Sicherheit: {score:.1%}")
    st.warning(f"Entsorgung: {disposal}")


# ---------------- HERO ----------------
st.markdown("""
<div class="hero-box">
    <h1 style="margin-bottom:0.4rem;">♻️ What the Trash</h1>
    <p style="font-size:1.15rem; margin-bottom:0;">
        KI erkennt deinen Müll per Upload oder Webcam.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- STATS ----------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-box"><h3>6+</h3><div class="small-text">Kategorien</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-box"><h3>AI</h3><div class="small-text">Bildanalyse</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-box"><h3>Webcam</h3><div class="small-text">Live Nutzung</div></div>', unsafe_allow_html=True)

st.write("")

# ---------------- INPUT AREA ----------------
tab1, tab2 = st.tabs(["📁 Upload", "📷 Webcam"])

# -------- Upload --------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        show_results(image)
    st.markdown('</div>', unsafe_allow_html=True)

# -------- Webcam --------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    camera_image = st.camera_input("Foto aufnehmen")
    if camera_image is not None:
        image = Image.open(camera_image).convert("RGB")
        show_results(image)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.write("")
st.caption("What the Trash • AI Waste Classifier")
