import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== ULTIMATIVE CYBERPUNK REVOLUTION =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background: #000000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* === DOUBLE MATRIX RAIN === */
#matrix-canvas, #matrix-canvas2 {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2; opacity: 0.6; mix-blend-mode: screen;
}
#matrix-canvas2 { z-index: -1; opacity: 0.3; }

/* CRT + Vignette + Scanlines */
body::before {
    content: ""; position: fixed; inset: 0; z-index: 9996; pointer-events: none;
    background: radial-gradient(circle at center, transparent 40%, rgba(0,0,0,0.85) 100%);
    box-shadow: inset 0 0 300px rgba(0,0,0,0.9);
}

body::after {
    content: ""; position: fixed; inset: 0; z-index: 9997; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 4px, rgba(0,255,65,0.15) 4px, rgba(0,255,65,0.15) 8px);
    animation: scanroll 4.5s linear infinite;
    filter: contrast(1.2) brightness(1.15);
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 1200px; } }

/* EPIC GLITCH */
@keyframes glitch {
    0% { text-shadow: 5px 0 #ff00ff, -5px 0 #00ffff; transform: skew(2deg); }
    25% { text-shadow: -5px 0 #00ff41, 5px 0 #ffff00; }
    50% { text-shadow: 5px 0 #00ffff, -5px 0 #ff00ff; }
    100% { text-shadow: 5px 0 #ff00ff, -5px 0 #00ffff; }
}

.hero-container {
    border: 5px solid #00ff41;
    border-radius: 12px;
    padding: 2.5rem 3rem;
    margin: 1.5rem 0 2.5rem 0;
    position: relative;
    background: linear-gradient(135deg, rgba(0,255,65,0.18), rgba(0,15,8,0.97));
    box-shadow: 0 0 100px #00ff41,
                0 0 200px rgba(255,0,255,0.4),
                inset 0 0 120px rgba(0,255,65,0.3);
    overflow: hidden;
}
.hero-container::before {
    content: "WASTE_ID.EXE v5.1 // NEURAL MATRIX CORE ONLINE // DO NOT TRUST THE SYSTEM";
    position: absolute; top: -18px; left: 50%; transform: translateX(-50%);
    background: #000; padding: 8px 25px;
    font-size: 0.9rem; color: #ff0044; letter-spacing: 6px;
    border: 2px solid #ff0044; white-space: nowrap;
    box-shadow: 0 0 20px #ff0044;
}
.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(3.5rem, 9vw, 6rem);
    font-weight: 900;
    letter-spacing: 20px;
    text-transform: uppercase;
    animation: glitch 0.6s infinite;
    text-shadow: 0 0 80px #00ff41,
                 0 0 160px #ff00ff,
                 0 0 220px #00ffff;
    margin-bottom: 0.8rem;
}
.biohazard {
    font-size: 4.5rem;
    filter: drop-shadow(0 0 25px #00ff41);
    margin-right: 20px;
}
</style>

<canvas id="matrix-canvas"></canvas>
<canvas id="matrix-canvas2"></canvas>

<script>
// === ULTRA MATRIX RAIN ===
const c1 = document.getElementById('matrix-canvas');
const ctx1 = c1.getContext('2d');
const c2 = document.getElementById('matrix-canvas2');
const ctx2 = c2.getContext('2d');

let w, h;
const chars = "01アイウエオカキクケコネオトーキョー0123456789$@#%&*█▓▒░";
const fs = 17;
let drops1 = [], drops2 = [];

function resize() {
    w = window.innerWidth; h = window.innerHeight;
    c1.width = c2.width = w; c1.height = c2.height = h;
    drops1 = Array(Math.floor(w/fs)).fill(1);
    drops2 = Array(Math.floor(w/fs)).fill(1);
}
resize();
window.addEventListener('resize', resize);

function draw1() {
    ctx1.fillStyle = 'rgba(0,0,0,0.06)';
    ctx1.fillRect(0,0,w,h);
    ctx1.fillStyle = '#00ff41';
    ctx1.font = `${fs}px monospace`;
    for (let i = 0; i < drops1.length; i++) {
        ctx1.fillText(chars[Math.random()*chars.length|0], i*fs, drops1[i]*fs);
        if (drops1[i]*fs > h && Math.random() > 0.96) drops1[i] = 0;
        drops1[i]++;
    }
}
function draw2() {
    ctx2.fillStyle = 'rgba(0,0,0,0.1)';
    ctx2.fillRect(0,0,w,h);
    ctx2.fillStyle = '#00ff88';
    ctx2.font = `${fs*0.85}px monospace`;
    for (let i = 0; i < drops2.length; i++) {
        ctx2.fillText(chars[Math.random()*chars.length|0], i*fs, drops2[i]*fs);
        if (drops2[i]*fs > h && Math.random() > 0.93) drops2[i] = 0;
        drops2[i]++;
    }
}
setInterval(draw1, 28);
setInterval(draw2, 40);
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
    with st.spinner("[ NEURAL CORE OVERDRIVE... SCANNING ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    
    st.markdown(f"""
    <div style="margin:30px 0">
        <div style="border:3px solid #00ff41;color:#00ff41;padding:25px;border-radius:12px;background:rgba(0,60,30,0.8);box-shadow:0 0 35px #00ff41;">
            <b>CLASS &gt;&gt;</b> {label.upper()}
        </div>
        <div style="border:3px solid #00ffff;color:#00ffff;padding:25px;margin:18px 0;border-radius:12px;background:rgba(0,45,55,0.8);box-shadow:0 0 35px #00ffff;">
            <b>CONFIDENCE &gt;&gt;</b> {score:.1%}
            <div style="height:16px;background:#001a00;margin-top:16px;border-radius:8px;overflow:hidden">
                <div style="height:100%;width:{int(score*100)}%;background:linear-gradient(90deg,#00ff41,#00ffff);box-shadow:0 0 30px #00ffff"></div>
            </div>
        </div>
        <div style="border:3px solid #ffaa00;color:#ffaa00;padding:25px;border-radius:12px;background:rgba(70,40,0,0.8);box-shadow:0 0 35px #ffaa00;">
            <b>DISPOSAL PROTOCOL &gt;&gt;</b> {disposal}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== EPIC HERO =====================
st.markdown("""
<div class="hero-container">
  <div style="display:flex; align-items:center; justify-content:center; flex-wrap:wrap;">
    <span class="biohazard">☣</span>
    <div class="hero-title">WASTE_ID.EXE</div>
  </div>
  <div style="text-align:center; color:#00ff9d; font-size:1.6rem; letter-spacing:8px; margin-top:15px;">
    REVOLUTIONARY NEURAL WASTE SYSTEM
  </div>
</div>
""", unsafe_allow_html=True)

# ===================== TABS =====================
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
<div style="text-align:center; margin:60px 0 30px 0; color:#002200; font-size:1.1rem; letter-spacing:5px;">
    WASTE_ID.EXE v5.1 — THE MATRIX REVOLUTION IS HERE<br>
    YOU CANNOT ESCAPE THE SYSTEM
</div>
""", unsafe_allow_html=True)
