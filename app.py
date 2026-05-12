import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== EPISCHER MATRIX DESIGN =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background: #000000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* MATRIX CANVAS - SEHR EPISCH */
#matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    opacity: 0.45;
    mix-blend-mode: screen;
}

/* Intensivere Scanlines + Vignette */
body::after {
    content: "";
    position: fixed; inset: 0; z-index: 9998; pointer-events: none;
    background: 
        linear-gradient(rgba(0,255,65,0.03) 50%, transparent 50%),
        repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.06) 2px, rgba(0,255,65,0.06) 4px);
    animation: scanroll 8s linear infinite;
    box-shadow: inset 0 0 150px rgba(0,0,0,0.8);
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 600px; } }

/* Glitch Effect für Titel */
@keyframes glitch {
    0% { text-shadow: 2px 0 #00ff41, -2px 0 #ff00ff; }
    20% { text-shadow: -2px 0 #00ff41, 2px 0 #00ffff; }
    40% { text-shadow: 2px 0 #ff00ff, -2px 0 #00ff41; }
    100% { text-shadow: 2px 0 #00ff41, -2px 0 #ff00ff; }
}

.hero-wrap {
    border: 2px solid #00ff41;
    border-radius: 6px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    background: linear-gradient(135deg, rgba(0,255,65,0.08), rgba(0,20,10,0.9));
    box-shadow: 0 0 50px rgba(0,255,65,0.4),
                inset 0 0 60px rgba(0,255,65,0.1);
    overflow: hidden;
}
.hero-wrap::before {
    content: "SYSTEM ONLINE • NEURAL LINK ESTABLISHED • MATRIX PROTOCOL v3.0";
    position: absolute; top: -12px; left: 30px;
    background: #000; padding: 0 12px;
    font-size: 0.75rem; color: #00ff41; letter-spacing: 3px;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(2.8rem, 6vw, 4.2rem);
    font-weight: 900;
    letter-spacing: 12px;
    text-shadow: 0 0 40px #00ff41,
                 0 0 80px #00ff41,
                 0 0 120px #ff00ff;
    animation: glitch 1.5s infinite;
}
</style>

<canvas id="matrix-canvas"></canvas>

<!-- Musik -->
<audio id="bg-music" loop></audio>

<script>
// EPISCHER MATRIX RAIN
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');

let width, height;
const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZアイウエオカキクケコネオトーキョー$@#%&*█▓▒░";
const fontSize = 16;
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

        if (drops[i] * fontSize > height && Math.random() > 0.96) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}
setInterval(draw, 32);
</script>
""", unsafe_allow_html=True)

# ===================== MODEL (unverändert) =====================
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
    mapping = {"plastic": "GELBE TONNE", "paper": "BLAUE TONNE", "cardboard": "BLAUE TONNE",
               "glass": "GLASCONTAINER", "metal": "GELBE TONNE", "trash": "RESTMÜLL"}
    for k, v in mapping.items():
        if k in label.lower(): return v
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
    with st.spinner("[ NEURAL SCAN RUNNING... ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    
    st.markdown(f"""
    <div style="margin:25px 0; font-size:1.05rem;">
        <div style="border:1px solid #00ff41;color:#00ff41;padding:18px;margin:12px 0;border-radius:6px;background:rgba(0,255,65,0.05)">
            <b>CLASSIFICATION &gt;&gt;</b> {label.upper()}
        </div>
        <div style="border:1px solid #00ffff;color:#00ffff;padding:18px;margin:12px 0;border-radius:6px;background:rgba(0,255,255,0.05)">
            <b>CONFIDENCE &gt;&gt;</b> {score:.1%}
            <div style="height:10px;background:#001a00;margin-top:12px;border-radius:5px;overflow:hidden">
                <div style="height:100%;width:{int(score*100)}%;background:linear-gradient(90deg,#00ff41,#00ffff);box-shadow:0 0 15px #00ffff"></div>
            </div>
        </div>
        <div style="border:1px solid #ffaa00;color:#ffaa00;padding:18px;margin:12px 0;border-radius:6px;background:rgba(255,170,0,0.05)">
            <b>RECOMMENDED DISPOSAL &gt;&gt;</b> {disposal}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== UI =====================
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div style="color:#00ff9d; font-size:1.3rem; letter-spacing:4px; margin-top:10px;">
    CYBERNETIC WASTE IDENTIFICATION SYSTEM
  </div>
</div>
""", unsafe_allow_html=True)

# ===================== MUSIK =====================
st.subheader("🎵 MATRIX AUDIO CONTROL")
music_url = st.text_input("Musik URL (optional)", 
                         value="https://freesound.org/data/previews/612/612095_5674468-lq.mp3",
                         help="Füge hier einen direkten Link zu einer .mp3 Datei ein")

if st.button("▶️ START EPIC MATRIX SOUND", type="primary", use_container_width=True):
    st.markdown(f"""
    <script>
        var audio = document.getElementById('bg-music');
        audio.src = "{music_url}";
        audio.volume = 0.4;
        audio.play();
    </script>
    """, unsafe_allow_html=True)
    st.success("🔊 Matrix Sound aktiviert")

st.markdown("---")

tab1, tab2 = st.tabs(["[ FILE UPLOAD ]", "[ WEBCAM FEED ]"])

with tab1:
    uploaded = st.file_uploader("", type=["jpg","jpeg","png"], label_visibility="collapsed")
    if uploaded:
        show_results(Image.open(uploaded))

with tab2:
    camera = st.camera_input("", label_visibility="collapsed")
    if camera:
        show_results(Image.open(camera))

st.caption("WASTE_ID.EXE v3.0 — FULL MATRIX PROTOCOL ENGAGED")
