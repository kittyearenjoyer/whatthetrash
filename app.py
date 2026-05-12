import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== REVOLUTIONÄRES EPIC DESIGN =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background: #000000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* === REVOLUTIONÄRER MATRIX BACKGROUND === */
#matrix-canvas {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -3; opacity: 0.6; mix-blend-mode: screen;
}
#matrix-canvas2 {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2; opacity: 0.25; mix-blend-mode: screen;
}

/* Intensive Scanlines + Vignette + CRT Effect */
body::before {
    content: ""; position: fixed; inset: 0; z-index: 9997; pointer-events: none;
    background: radial-gradient(circle at center, rgba(0,255,65,0.08) 0%, transparent 70%);
    box-shadow: inset 0 0 250px rgba(0,0,0,0.95);
}

body::after {
    content: ""; position: fixed; inset: 0; z-index: 9998; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,65,0.12) 3px, rgba(0,255,65,0.12) 6px);
    animation: scanroll 5s linear infinite;
    filter: contrast(1.15) brightness(1.1);
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 1000px; } }

/* Ultra Glitch */
@keyframes glitch {
    0% { text-shadow: 4px 0 #ff00ff, -4px 0 #00ffff, 0 0 20px #00ff41; }
    20% { text-shadow: -4px 0 #00ff41, 4px 0 #ffff00, 0 0 30px #ff00ff; }
    40% { text-shadow: 4px 0 #00ffff, -4px 0 #ff00ff, 0 0 25px #00ff41; }
    100% { text-shadow: 4px 0 #ff00ff, -4px 0 #00ffff, 0 0 20px #00ff41; }
}

.hero-wrap {
    border: 4px solid #00ff41;
    border-radius: 12px;
    padding: 3.5rem 4rem;
    margin: 2rem 0;
    position: relative;
    background: linear-gradient(135deg, rgba(0,255,65,0.15), rgba(0,20,10,0.98));
    box-shadow: 0 0 80px rgba(0,255,65,0.7),
                0 0 160px rgba(255,0,255,0.3),
                inset 0 0 100px rgba(0,255,65,0.25);
    overflow: hidden;
}
.hero-wrap::before {
    content: "WASTE_ID.EXE v5.0 // NEURAL MATRIX CORE ONLINE // DO NOT TRUST THE SYSTEM";
    position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
    background: #000; padding: 6px 20px;
    font-size: 0.85rem; color: #ff0044; letter-spacing: 5px;
    border: 1px solid #ff0044; white-space: nowrap;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(3.2rem, 8vw, 5.5rem);
    font-weight: 900;
    letter-spacing: 18px;
    text-transform: uppercase;
    animation: glitch 0.7s infinite;
    text-shadow: 0 0 70px #00ff41,
                 0 0 140px #ff00ff;
}
</style>

<canvas id="matrix-canvas"></canvas>
<canvas id="matrix-canvas2"></canvas>

<script>
// === REVOLUTIONÄRER DOUBLE LAYER MATRIX RAIN ===
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
const canvas2 = document.getElementById('matrix-canvas2');
const ctx2 = canvas2.getContext('2d');

let w, h;
const chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZアイウエオカキクケコネオトーキョー$@#%&*█▓▒░";
const fontSize = 16;
let drops = [], drops2 = [];

function resize() {
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = canvas2.width = w;
    canvas.height = canvas2.height = h;
    drops = Array(Math.floor(w / fontSize)).fill(1);
    drops2 = Array(Math.floor(w / fontSize)).fill(1);
}
resize();
window.addEventListener('resize', resize);

function drawLayer1() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.07)';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#00ff41';
    ctx.font = `${fontSize}px monospace`;

    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > h && Math.random() > 0.96) drops[i] = 0;
        drops[i]++;
    }
}

function drawLayer2() {
    ctx2.fillStyle = 'rgba(0, 0, 0, 0.12)';
    ctx2.fillRect(0, 0, w, h);
    ctx2.fillStyle = '#00ff88';
    ctx2.font = `${fontSize * 0.9}px monospace`;

    for (let i = 0; i < drops2.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx2.fillText(text, i * fontSize, drops2[i] * fontSize * 0.9);
        if (drops2[i] * fontSize > h && Math.random() > 0.94) drops2[i] = 0;
        drops2[i]++;
    }
}

setInterval(drawLayer1, 30);
setInterval(drawLayer2, 42);
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
    with st.spinner("[ NEURAL CORE OVERDRIVE ACTIVATED... ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    
    st.markdown(f"""
    <div style="margin:30px 0;">
        <div style="border:3px solid #00ff41;color:#00ff41;padding:22px;border-radius:10px;background:rgba(0,50,30,0.7);box-shadow:0 0 30px #00ff41;">
            <b>NEURAL CLASSIFICATION &gt;&gt;</b> {label.upper()}
        </div>
        <div style="border:3px solid #00ffff;color:#00ffff;padding:22px;margin:15px 0;border-radius:10px;background:rgba(0,40,50,0.7);box-shadow:0 0 30px #00ffff;">
            <b>CONFIDENCE LEVEL &gt;&gt;</b> {score:.1%}
            <div style="height:14px;background:#001a00;margin-top:14px;border-radius:7px;overflow:hidden">
                <div style="height:100%;width:{int(score*100)}%;background:linear-gradient(90deg,#00ff41,#00ffff);box-shadow:0 0 25px #00ffff"></div>
            </div>
        </div>
        <div style="border:3px solid #ffaa00;color:#ffaa00;padding:22px;border-radius:10px;background:rgba(60,35,0,0.7);box-shadow:0 0 30px #ffaa00;">
            <b>DISPOSAL PROTOCOL &gt;&gt;</b> {disposal}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== UI =====================
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div style="color:#00ff9d; font-size:1.5rem; letter-spacing:8px; text-align:center; margin-top:20px;">
    REVOLUTIONARY NEURAL WASTE SYSTEM
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["[ TARGET UPLOAD ]", "[ LIVE NEURAL CAPTURE ]"])

with tab1:
    uploaded = st.file_uploader("", type=["jpg","jpeg","png"], label_visibility="collapsed")
    if uploaded:
        show_results(Image.open(uploaded))

with tab2:
    camera = st.camera_input("", label_visibility="collapsed")
    if camera:
        show_results(Image.open(camera))

st.markdown("""
<div style="text-align:center; margin:50px 0; color:#003300; font-size:1rem; letter-spacing:4px;">
    WASTE_ID.EXE v5.0 — MATRIX REVOLUTION PROTOCOL ENGAGED<br>
    ALL SYSTEMS NOMINAL • YOU ARE BEING WATCHED
</div>
""", unsafe_allow_html=True)
