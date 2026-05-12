import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

# ---------------- CONFIG ----------------
MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(
    page_title="WASTE_ID.EXE",
    page_icon="☣️",
    layout="wide",
)

# ---------------- HACKER CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

/* ── BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.main, section.main { background: #000 !important; }

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1100px !important;
    background: transparent !important;
}

/* kill white streamlit surfaces */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] { background: transparent !important; display:none !important; }

/* ── SCANLINE OVERLAY ── */
body::after {
    content: "";
    position: fixed; inset: 0; z-index: 9999;
    pointer-events: none;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,65,0.03) 2px,
        rgba(0,255,65,0.03) 4px
    );
}

/* ── HERO ── */
.hero-wrap {
    border: 1px solid #00ff41;
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    background: linear-gradient(135deg, rgba(0,255,65,0.05) 0%, transparent 60%);
    box-shadow: 0 0 30px rgba(0,255,65,0.15), inset 0 0 30px rgba(0,255,65,0.04);
}
.hero-wrap::before {
    content: "WASTE_ID.EXE v2.4.1 // NEURAL CLASSIFICATION SYSTEM";
    position: absolute; top: -11px; left: 20px;
    background: #000; padding: 0 8px;
    font-size: 0.65rem; color: #00ff41; letter-spacing: 2px;
}
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1.6rem, 4vw, 2.8rem) !important;
    font-weight: 900 !important;
    color: #00ff41 !important;
    letter-spacing: 4px;
    text-shadow: 0 0 20px #00ff41, 0 0 40px rgba(0,255,65,0.4);
    margin: 0 0 0.4rem 0;
}
.hero-sub {
    color: #00cc33 !important;
    font-size: 0.85rem;
    letter-spacing: 1px;
    margin: 0;
}
.blink { animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }

/* ── STAT GRID ── */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-box {
    border: 1px solid #00ff41;
    border-radius: 4px;
    padding: 1rem;
    text-align: center;
    background: rgba(0,255,65,0.03);
    position: relative;
    box-shadow: 0 0 10px rgba(0,255,65,0.1);
}
.stat-box::after {
    content: attr(data-label);
    position: absolute; bottom: -10px; left: 50%; transform: translateX(-50%);
    background: #000; padding: 0 6px;
    font-size: 0.6rem; color: #00aa22; letter-spacing: 2px; white-space: nowrap;
}
.stat-val {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.6rem !important;
    color: #00ff41 !important;
    text-shadow: 0 0 10px #00ff41;
}

/* ── PANEL ── */
.panel {
    border: 1px solid #00ff41;
    border-radius: 4px;
    padding: 1.5rem;
    background: rgba(0,255,65,0.02);
    box-shadow: 0 0 20px rgba(0,255,65,0.08);
    position: relative;
}
.panel-label {
    position: absolute; top: -11px; left: 16px;
    background: #000; padding: 0 8px;
    font-size: 0.65rem; color: #00ff41; letter-spacing: 2px;
}

/* ── RESULT BOXES ── */
.result-wrap { margin-top: 1.2rem; }
.result-row {
    border: 1px solid;
    border-radius: 3px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
}
.result-row::before {
    content: "";
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px;
}
.result-label  { border-color: #00ff41; color: #00ff41; background: rgba(0,255,65,0.05); }
.result-label::before  { background: #00ff41; box-shadow: 0 0 8px #00ff41; }
.result-score  { border-color: #00ccff; color: #00ccff; background: rgba(0,204,255,0.04); }
.result-score::before  { background: #00ccff; box-shadow: 0 0 8px #00ccff; }
.result-bin    { border-color: #ffaa00; color: #ffaa00; background: rgba(255,170,0,0.04); }
.result-bin::before    { background: #ffaa00; box-shadow: 0 0 8px #ffaa00; }

.result-key { color: #007722; margin-right: 0.5rem; }

/* progress bar for score */
.score-bar-wrap { height: 4px; background: rgba(0,204,255,0.15); border-radius: 2px; margin-top: 6px; }
.score-bar { height: 4px; background: #00ccff; border-radius: 2px;
    box-shadow: 0 0 8px #00ccff; transition: width 0.8s ease; }

/* ── TABS ── */
button[data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 2px !important;
    color: #007722 !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 8px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #00ff41 !important;
    border-bottom: 2px solid #00ff41 !important;
    text-shadow: 0 0 8px #00ff41;
}
[data-testid="stTabs"] { margin-bottom: 0; }
[role="tablist"] { border-bottom: 1px solid #003311 !important; }

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(0,255,65,0.02) !important;
    border: 1px dashed #007722 !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] * { color: #00aa22 !important; font-family: 'Share Tech Mono', monospace !important; }
[data-testid="stFileUploaderDropzone"] { background: transparent !important; border: none !important; }

/* ── CAMERA ── */
[data-testid="stCameraInput"] {
    background: rgba(0,255,65,0.02) !important;
    border: 1px dashed #007722 !important;
    border-radius: 4px !important;
}
[data-testid="stCameraInput"] * { color: #00aa22 !important; font-family: 'Share Tech Mono', monospace !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Share Tech Mono', monospace !important;
    background: transparent !important;
    border: 1px solid #00ff41 !important;
    color: #00ff41 !important;
    letter-spacing: 2px !important;
    border-radius: 3px !important;
}
.stButton > button:hover {
    background: rgba(0,255,65,0.1) !important;
    box-shadow: 0 0 12px rgba(0,255,65,0.4) !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] * { color: #00ff41 !important; font-family: 'Share Tech Mono', monospace !important; }

/* ── IMAGE ── */
[data-testid="stImage"] img {
    border: 1px solid #00ff41 !important;
    border-radius: 3px !important;
    box-shadow: 0 0 20px rgba(0,255,65,0.2) !important;
    filter: brightness(0.95) contrast(1.05) hue-rotate(0deg);
}

/* ── FOOTER ── */
.footer-line {
    border-top: 1px solid #003311;
    margin-top: 2rem;
    padding-top: 0.8rem;
    font-size: 0.65rem;
    color: #005511 !important;
    letter-spacing: 2px;
    text-align: center;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, [data-testid="stStatusWidget"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return model

model = load_model()

# ---------------- INFERENCE ----------------
def preprocess(image: Image.Image) -> torch.Tensor:
    img = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    pixels = list(img.getdata())
    t = torch.tensor(pixels, dtype=torch.float32)
    t = t / 255.0
    t = (t - 0.5) / 0.5
    t = t.view(224, 224, 3).permute(2, 0, 1)
    return t.unsqueeze(0)

def get_disposal(label: str) -> str:
    disposal_map = {
        "plastic":   "GELBE TONNE  [RECYCLING_BIN_YELLOW]",
        "paper":     "BLAUE TONNE  [RECYCLING_BIN_BLUE]",
        "cardboard": "BLAUE TONNE  [RECYCLING_BIN_BLUE]",
        "glass":     "GLASCONTAINER [BOTTLE_BANK]",
        "metal":     "GELBE TONNE  [RECYCLING_BIN_YELLOW]",
        "trash":     "RESTMÜLL     [GENERAL_WASTE]",
    }
    for key, value in disposal_map.items():
        if key in label.lower():
            return value
    return "LOKAL PRÜFEN [CHECK_LOCAL_REGULATIONS]"

def run_prediction(image: Image.Image):
    tensor = preprocess(image)
    with torch.no_grad():
        logits = model(pixel_values=tensor).logits
    idx   = logits.argmax(-1).item()
    label = model.config.id2label[idx]
    score = torch.softmax(logits, dim=-1)[0][idx].item()
    return label, score

def show_results(image: Image.Image):
    st.image(image, use_container_width=True)
    with st.spinner("[ RUNNING NEURAL SCAN... ]"):
        label, score = run_prediction(image)
    disposal = get_disposal(label)
    pct = int(score * 100)
    st.markdown(f"""
    <div class="result-wrap">
      <div class="result-row result-label">
        <span class="result-key">CLASS_ID  &gt;&gt;</span> {label.upper()}
      </div>
      <div class="result-row result-score">
        <span class="result-key">CONFIDENCE&gt;&gt;</span> {score:.1%}
        <div class="score-bar-wrap"><div class="score-bar" style="width:{pct}%"></div></div>
      </div>
      <div class="result-row result-bin">
        <span class="result-key">DISPOSAL  &gt;&gt;</span> {disposal}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════
#  RENDER
# ══════════════════════════════════════════

# ── HERO ──
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <p class="hero-sub">&gt; NEURAL WASTE CLASSIFICATION SYSTEM // ONLINE<span class="blink">_</span></p>
</div>
""", unsafe_allow_html=True)

# ── STATS ──
st.markdown("""
<div class="stat-grid">
  <div class="stat-box" data-label="WASTE CLASSES">
    <div class="stat-val">6+</div>
  </div>
  <div class="stat-box" data-label="ENGINE">
    <div class="stat-val">ViT</div>
  </div>
  <div class="stat-box" data-label="INPUT MODE">
    <div class="stat-val">CAM</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2 = st.tabs(["[ FILE_UPLOAD ]", "[ WEBCAM_FEED ]"])

with tab1:
    st.markdown('<div class="panel"><div class="panel-label">INPUT // FILE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("DROP TARGET FILE", type=["jpg", "jpeg", "png"], label_visibility="visible")
    if uploaded_file is not None:
        show_results(Image.open(uploaded_file))
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="panel"><div class="panel-label">INPUT // LIVE CAPTURE</div>', unsafe_allow_html=True)
    camera_image = st.camera_input("CAPTURE FRAME", label_visibility="visible")
    if camera_image is not None:
        show_results(Image.open(camera_image))
    st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer-line">
  WASTE_ID.EXE &nbsp;|&nbsp; NEURAL ENGINE: yangy50/garbage-classification &nbsp;|&nbsp;
  STATUS: ONLINE &nbsp;|&nbsp; ALL RIGHTS RESERVED © 2024
</div>
""", unsafe_allow_html=True)
