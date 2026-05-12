import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== EPIC MATRIX DESIGN =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background: #000000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

#matrix-canvas {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    z-index: -2; opacity: 0.52; mix-blend-mode: screen;
}

body::after {
    content: ""; position: fixed; inset: 0; z-index: 9998; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.085) 2px, rgba(0,255,65,0.085) 4px);
    animation: scanroll 6.5s linear infinite;
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 800px; } }

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 900;
    letter-spacing: 16px;
    text-shadow: 0 0 60px #00ff41, 0 0 110px #00ff41;
    animation: glitch 0.9s infinite;
}
@keyframes glitch {
    0%,100% { text-shadow: 4px 0 #ff00ff, -4px 0 #00ffff; }
    50% { text-shadow: -4px 0 #00ff41, 4px 0 #ffff00; }
}
</style>

<canvas id="matrix-canvas"></canvas>
<audio id="bg-music" loop preload="auto"></audio>

<script>
// Matrix Rain
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');
let w, h, drops = [];
const chars = "01アイウエオカキクケコ0123456789$@#%&*█";

function resize() {
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = w; canvas.height = h;
    drops = Array(Math.floor(w / 15)).fill(1);
}
resize();
window.addEventListener('resize', resize);

function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.075)';
    ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#00ff41';
    ctx.font = '16px monospace';
    for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i*15, drops[i]*15);
        if (drops[i]*15 > h && Math.random() > 0.975) drops[i] = 0;
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
    <div style="margin:25px 0">
        <div style="border:2px solid #00ff41;color:#00ff41;padding:18px;border-radius:8px;background:rgba(0,40,20,0.6)">
            <b>CLASS &gt;&gt;</b> {label.upper()}
        </div>
        <div style="border:2px solid #00ffff;color:#00ffff;padding:18px;margin:12px 0;border-radius:8px;background:rgba(0,30,40,0.6)">
            <b>CONFIDENCE &gt;&gt;</b> {score:.1%}
            <div style="height:10px;background:#001a00;margin-top:10px;border-radius:5px">
                <div style="width:{int(score*100)}%;height:100%;background:#00ff41;box-shadow:0 0 15px #00ff41"></div>
            </div>
        </div>
        <div style="border:2px solid #ffaa00;color:#ffaa00;padding:18px;border-radius:8px;background:rgba(50,25,0,0.6)">
            <b>DISPOSAL &gt;&gt;</b> {disposal}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== UI + NEUER MUSIK LINK =====================
st.markdown("""
<div style="border:3px solid #00ff41;padding:3rem;text-align:center;background:rgba(0,255,65,0.08);box-shadow:0 0 70px #00ff41">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div style="color:#00ff9d;letter-spacing:6px;margin-top:15px">MATRIX PROTOCOL v4.4</div>
</div>
""", unsafe_allow_html=True)

st.subheader("🎵 MATRIX AUDIO")

col1, col2 = st.columns([3,1])
with col1:
    music_url = st.text_input(
        "Musik-Link (MP3)",
        value="https://archive.org/download/cyberpunk-ambient-rainy-night-walks/Cyberpunk%20Ambient%20-%20Rainy%20Night%20Walks.mp3",
        help="Neuer Link: Cyberpunk Rainy Night Walks"
    )

with col2:
    volume = st.slider("Lautstärke", 0.0, 1.0, 0.40, 0.05)

if st.button("▶️ START MATRIX SOUND", type="primary", use_container_width=True):
    st.markdown(f"""
    <script>
        var audio = document.getElementById('bg-music');
        audio.src = "{music_url}";
        audio.volume = {volume};
        audio.play().catch(err => {{
            console.error(err);
            alert("Audio konnte nicht gestartet werden. Versuche einen anderen Browser oder klicke nochmal.");
        }});
    </script>
    """, unsafe_allow_html=True)
    st.success("Matrix Sound gestartet")

if st.button("⏹ STOP SOUND", use_container_width=True):
    st.markdown("""
    <script>
        document.getElementById('bg-music').pause();
    </script>
    """, unsafe_allow_html=True)
    st.info("Sound gestoppt")

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

st.caption("WASTE_ID.EXE — FULL CYBER IMMERSION")
