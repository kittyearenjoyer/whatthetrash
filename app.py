import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

# ===================== FULL CSS + MATRIX =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
    background: transparent !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* MATRIX CANVAS */
#matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -1;
    opacity: 0.22;
    pointer-events: none;
    mix-blend-mode: screen;
}

/* Dein originales CSS (leicht optimiert) */
.block-container { padding-top: 1.5rem !important; max-width: 1100px !important; }

[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }

/* SCANLINES */
body::after {
    content: "";
    position: fixed; inset: 0; z-index: 9999; pointer-events: none;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,255,65,0.03) 2px, rgba(0,255,65,0.03) 4px
    );
    animation: scanroll 8s linear infinite;
}
@keyframes scanroll { 0% { background-position: 0 0; } 100% { background-position: 0 200px; } }

/* HERO */
.hero-wrap {
    border: 1px solid #00ff41;
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    background: linear-gradient(135deg, rgba(0,255,65,0.05) 0%, transparent 60%);
    box-shadow: 0 0 30px rgba(0,255,65,0.15), inset 0 0 40px rgba(0,255,65,0.03);
}
.hero-wrap::before {
    content: "WASTE_ID.EXE v2.4.1 // NEURAL CLASSIFICATION SYSTEM // READY";
    position: absolute; top: -10px; left: 20px;
    background: #000; padding: 0 8px;
    font-size: 0.6rem; color: #00ff41; letter-spacing: 2px;
}
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1.8rem, 4vw, 3rem) !important;
    font-weight: 900 !important;
    color: #00ff41 !important;
    letter-spacing: 6px;
    text-shadow: 0 0 20px #00ff41, 0 0 40px rgba(0,255,65,0.5);
}

/* Weitere Styles (verkürzt - dein Original bleibt erhalten) */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-box {
    border: 1px solid #00ff41; border-radius: 4px; padding: 1rem 0.5rem;
    text-align: center; background: rgba(0,255,65,0.02);
}
.stat-val { font-family: 'Orbitron', monospace !important; font-size: 1.7rem !important; color: #00ff41 !important; }

.result-row {
    border: 1px solid; border-radius: 3px; padding: 0.75rem 1rem;
    margin-bottom: 0.6rem; animation: slidein 0.4s ease both;
}
@keyframes slidein { from { opacity:0; transform: translateX(-12px); } to { opacity:1; transform: translateX(0); } }
</style>

<canvas id="matrix-canvas"></canvas>

<!-- Hintergrundmusik (Cyberpunk / Matrix Style) -->
<audio id="bg-music" loop autoplay>
    <source src="https://freesound.org/data/previews/612/612095_5674468-lq.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
</audio>

<script>
// === MATRIX RAIN ===
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');

let width, height;
const chars = "01アイウエオカキクケコ123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$@#%&*";
const fontSize = 13;
let drops = [];

function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    drops = Array(Math.floor(width / fontSize)).fill(1);
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.06)';
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
setInterval(draw, 35);

// Music fallback
document.addEventListener('click', function() {
    const audio = document.getElementById('bg-music');
    if (audio.paused) audio.play();
}, { once: true });
</script>
""", unsafe_allow_html=True)

# ===================== MODEL =====================
@st.cache_resource
def load_model():
    m = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    m.eval()
    return m

model = load_model()

def preprocess(image: Image.Image) -> torch.Tensor:
    img = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    pixels = list(img.getdata())
    t = torch.tensor(pixels, dtype=torch.float32) / 255.0
    t = (t - 0.5) / 0.5
    t = t.view(224, 224, 3).permute(2, 0, 1)
    return t.unsqueeze(0)

def get_disposal(label: str) -> str:
    m = {
        "plastic": "GELBE TONNE [RECYCLING_BIN_YELLOW]",
        "paper": "BLAUE TONNE [RECYCLING_BIN_BLUE]",
        "cardboard": "BLAUE TONNE [RECYCLING_BIN_BLUE]",
        "glass": "GLASCONTAINER [BOTTLE_BANK]",
        "metal": "GELBE TONNE [RECYCLING_BIN_YELLOW]",
        "trash": "RESTMÜLL [GENERAL_WASTE]",
    }
    for k, v in m.items():
        if k in label.lower(): return v
    return "LOKAL PRÜFEN [CHECK_LOCAL_REGULATIONS]"

def run_prediction(image: Image.Image):
    t = preprocess(image)
    with torch.no_grad():
        logits = model(pixel_values=t).logits
    idx = logits.argmax(-1).item()
    label = model.config.id2label[idx]
    score = torch.softmax(logits, dim=-1)[0][idx].item()
    return label, score

def show_results(image: Image.Image):
    st.image(image, use_container_width=True)
    with st.spinner("[ RUNNING NEURAL SCAN... PLEASE WAIT ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    pct = int(score * 100)
    
    st.markdown(f"""
    <div class="result-wrap">
      <div class="result-row" style="border-color:#00ff41; color:#00ff41;">
        <b>CLASS_ID &gt;&gt;</b> {label.upper()}
      </div>
      <div class="result-row" style="border-color:#00ccff; color:#00ccff;">
        <b>CONFIDENCE &gt;&gt;</b> {score:.1%} 
        <div style="height:3px; background:rgba(0,204,255,0.2); margin-top:6px;">
          <div style="height:3px; width:{pct}%; background:#00ccff; box-shadow:0 0 8px #00ccff;"></div>
        </div>
      </div>
      <div class="result-row" style="border-color:#ffaa00; color:#ffaa00;">
        <b>DISPOSAL &gt;&gt;</b> {disposal}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== UI =====================
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div class="hero-sub typewriter">&gt; NEURAL WASTE CLASSIFICATION SYSTEM // ONLINE<span class="blink">_</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-grid">
  <div class="stat-box"><div style="font-size:0.58rem; color:#007722;">WASTE CLASSES</div><div style="font-size:1.8rem;">06</div></div>
  <div class="stat-box"><div style="font-size:0.58rem; color:#007722;">MODEL ENGINE</div><div style="font-size:1.8rem;">ViT</div></div>
  <div class="stat-box"><div style="font-size:0.58rem; color:#007722;">MATRIX PROTOCOL</div><div style="font-size:1.8rem;">ACTIVE</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["[ FILE_UPLOAD ]", "[ WEBCAM_FEED ]"])

with tab1:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"], label_visibility="hidden")
    if uploaded_file is not None:
        show_results(Image.open(uploaded_file))

with tab2:
    camera_image = st.camera_input("Take Photo", label_visibility="hidden")
    if camera_image is not None:
        show_results(Image.open(camera_image))

st.markdown("""
<div style="text-align:center; margin-top:2rem; color:#003a15; font-size:0.7rem; letter-spacing:2px;">
  WASTE_ID.EXE &nbsp;///&nbsp; MATRIX PROTOCOL ACTIVE &nbsp;///&nbsp; ALL SYSTEMS NOMINAL
</div>
""", unsafe_allow_html=True)
