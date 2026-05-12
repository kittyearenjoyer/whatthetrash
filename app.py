import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== CSS + MATRIX =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container {
    background: #000000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

#matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    opacity: 0.25;
    mix-blend-mode: screen;
}

/* Scanlines */
body::after {
    content: "";
    position: fixed; inset: 0; z-index: 9999; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.035) 2px, rgba(0,255,65,0.035) 4px);
    animation: scanroll 10s linear infinite;
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 300px; } }

/* Hero & andere Styles */
.hero-wrap {
    border: 1px solid #00ff41;
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    background: rgba(0,255,65,0.03);
    box-shadow: 0 0 30px rgba(0,255,65,0.2);
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 900;
    letter-spacing: 8px;
    text-shadow: 0 0 25px #00ff41;
}
</style>

<canvas id="matrix-canvas"></canvas>

<!-- Hintergrundmusik -->
<audio id="bg-music" loop>
    <source src="https://freesound.org/data/previews/612/612095_5674468-lq.mp3" type="audio/mpeg">
</audio>

<script>
// MATRIX RAIN - starke Zahlen-Version
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');

let width, height;
const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ01アイウエオ123456789";
const fontSize = 14;
let drops = [];

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    drops = Array(Math.floor(width / fontSize)).fill(1);
}
resize();
window.addEventListener('resize', resize);

function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.07)';
    ctx.fillRect(0, 0, width, height);
    
    ctx.fillStyle = '#00ff41';
    ctx.font = `${fontSize}px monospace`;

    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}
setInterval(draw, 33);
</script>
""", unsafe_allow_html=True)

# ===================== MODEL =====================
@st.cache_resource
def load_model():
    return AutoModelForImageClassification.from_pretrained(MODEL_NAME).eval()

model = load_model()

def preprocess(image: Image.Image):
    img = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    pixels = list(img.getdata())
    t = torch.tensor(pixels, dtype=torch.float32) / 255.0
    t = (t - 0.5) / 0.5
    t = t.view(224, 224, 3).permute(2, 0, 1).unsqueeze(0)
    return t

def get_disposal(label):
    mapping = {
        "plastic": "GELBE TONNE [YELLOW BIN]",
        "paper": "BLAUE TONNE [BLUE BIN]",
        "cardboard": "BLAUE TONNE [BLUE BIN]",
        "glass": "GLASCONTAINER",
        "metal": "GELBE TONNE [YELLOW BIN]",
        "trash": "RESTMÜLL"
    }
    for key, val in mapping.items():
        if key in label.lower():
            return val
    return "LOKAL PRÜFEN"

def run_prediction(image):
    t = preprocess(image)
    with torch.no_grad():
        logits = model(pixel_values=t).logits
    idx = logits.argmax(-1).item()
    label = model.config.id2label[idx]
    score = torch.softmax(logits, dim=-1)[0][idx].item()
    return label, score

def show_results(image):
    st.image(image, use_container_width=True)
    with st.spinner("[ RUNNING NEURAL SCAN... ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    
    st.markdown(f"""
    <div style="margin-top:1.5rem;">
        <div style="border:1px solid #00ff41; color:#00ff41; padding:12px; margin:8px 0; border-radius:3px;">
            <b>CLASS &gt;&gt;</b> {label.upper()}
        </div>
        <div style="border:1px solid #00ccff; color:#00ccff; padding:12px; margin:8px 0; border-radius:3px;">
            <b>CONFIDENCE &gt;&gt;</b> {score:.1%}<br>
            <div style="background:#002200; height:6px; margin-top:8px; border-radius:3px;">
                <div style="width:{int(score*100)}%; background:#00ff41; height:100%; box-shadow:0 0 10px #00ff41;"></div>
            </div>
        </div>
        <div style="border:1px solid #ffaa00; color:#ffaa00; padding:12px; margin:8px 0; border-radius:3px;">
            <b>DISPOSAL &gt;&gt;</b> {disposal}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== UI =====================
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div style="color:#00cc33; letter-spacing:3px;">NEURAL WASTE CLASSIFICATION SYSTEM // MATRIX PROTOCOL ACTIVE</div>
</div>
""", unsafe_allow_html=True)

# Musik Control
col1, col2 = st.columns([4,1])
with col2:
    if st.button("▶️ PLAY MATRIX SOUND", help="Hintergrundmusik starten"):
        st.markdown("""
        <script>
            document.getElementById('bg-music').play();
        </script>
        """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["[ FILE UPLOAD ]", "[ WEBCAM ]"])

with tab1:
    uploaded = st.file_uploader("Bild hochladen", type=["jpg","jpeg","png"], label_visibility="collapsed")
    if uploaded:
        show_results(Image.open(uploaded))

with tab2:
    cam = st.camera_input("Foto aufnehmen", label_visibility="collapsed")
    if cam:
        show_results(Image.open(cam))

st.caption("WASTE_ID.EXE v2.5 — MATRIX PROTOCOL ACTIVE")
