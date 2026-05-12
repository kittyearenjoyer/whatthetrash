import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(page_title="WASTE_ID.EXE", page_icon="☣️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main, section.main,
[data-testid="stMainBlockContainer"],
.block-container {
    background: #000 !important;
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.block-container { padding-top: 1.5rem !important; max-width: 1100px !important; }

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer,
[data-testid="stStatusWidget"] { display: none !important; visibility: hidden !important; }

/* ── SCANLINES ── */
body::after {
    content: "";
    position: fixed; inset: 0; z-index: 9999; pointer-events: none;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,255,65,0.025) 2px, rgba(0,255,65,0.025) 4px
    );
    animation: scanroll 8s linear infinite;
}
@keyframes scanroll {
    0%   { background-position: 0 0; }
    100% { background-position: 0 200px; }
}

/* ── FLICKER ON LOAD ── */
@keyframes flicker {
    0%,19%,21%,23%,25%,54%,56%,100% { opacity: 1; }
    20%,22%,24%,55% { opacity: 0.4; }
}
.hero-wrap { animation: flicker 6s infinite; }

/* ── HERO ── */
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
.hero-wrap::after {
    content: "[ SECURE CHANNEL ]";
    position: absolute; top: -10px; right: 20px;
    background: #000; padding: 0 8px;
    font-size: 0.6rem; color: #007722; letter-spacing: 2px;
}
.hero-title {
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(1.8rem, 4vw, 3rem) !important;
    font-weight: 900 !important;
    color: #00ff41 !important;
    letter-spacing: 6px;
    text-shadow: 0 0 20px #00ff41, 0 0 40px rgba(0,255,65,0.5), 0 0 80px rgba(0,255,65,0.2);
    margin-bottom: 0.5rem;
}
.hero-sub {
    color: #00cc33 !important;
    font-size: 0.82rem;
    letter-spacing: 2px;
}
.blink { animation: blink 1s step-end infinite; }
@keyframes blink { 50% { opacity: 0; } }

/* ── TYPING ANIMATION ── */
.typewriter {
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid #00ff41;
    width: 0;
    animation: typing 2.5s steps(40) 0.5s forwards, caret 0.8s step-end infinite;
}
@keyframes typing  { to { width: 100%; } }
@keyframes caret   { 50% { border-color: transparent; } }

/* ── STAT GRID ── */
.stat-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 1rem; margin-bottom: 1.5rem;
}
.stat-box {
    border: 1px solid #00ff41; border-radius: 4px; padding: 1rem 0.5rem;
    text-align: center;
    background: rgba(0,255,65,0.02);
    box-shadow: 0 0 12px rgba(0,255,65,0.08);
    position: relative;
    transition: box-shadow 0.3s, background 0.3s;
}
.stat-box:hover {
    background: rgba(0,255,65,0.07);
    box-shadow: 0 0 25px rgba(0,255,65,0.25);
}
.stat-box-label {
    font-size: 0.58rem; color: #007722; letter-spacing: 2px; margin-bottom: 0.4rem;
}
.stat-val {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.7rem !important;
    color: #00ff41 !important;
    text-shadow: 0 0 12px #00ff41;
}

/* ── CORNER BRACKETS ── */
.bracket-box {
    position: relative;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.bracket-box::before,
.bracket-box::after,
.bracket-box .br-br::before,
.bracket-box .br-br::after {
    content: ""; position: absolute;
    width: 16px; height: 16px;
    border-color: #00ff41; border-style: solid;
}
.bracket-box::before  { top:0; left:0;  border-width: 2px 0 0 2px; }
.bracket-box::after   { top:0; right:0; border-width: 2px 2px 0 0; }
.bracket-box .br-br::before { bottom:0; left:0;  border-width: 0 0 2px 2px; }
.bracket-box .br-br::after  { bottom:0; right:0; border-width: 0 2px 2px 0; }

/* ── PANEL ── */
.panel {
    border: 1px solid #003a15;
    border-radius: 4px;
    padding: 1.5rem;
    background: rgba(0,255,65,0.015);
    box-shadow: 0 0 20px rgba(0,255,65,0.06);
    position: relative;
}
.panel-label {
    position: absolute; top: -10px; left: 16px;
    background: #000; padding: 0 8px;
    font-size: 0.62rem; color: #00ff41; letter-spacing: 3px;
}

/* ── FILE UPLOADER: hide default label & fix button ── */
[data-testid="stFileUploaderDropzone"] label,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span:not(.st-emotion-cache-9ycgxx) {
    display: none !important;
}
/* The actual "Browse files" button inside uploader */
[data-testid="stFileUploaderDropzone"] button {
    font-family: 'Share Tech Mono', monospace !important;
    background: transparent !important;
    border: 1px solid #00ff41 !important;
    color: #00ff41 !important;
    border-radius: 3px !important;
    letter-spacing: 2px !important;
    font-size: 0.75rem !important;
    padding: 0.4rem 1rem !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: rgba(0,255,65,0.1) !important;
    box-shadow: 0 0 12px rgba(0,255,65,0.4) !important;
}
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: 1px dashed #003a15 !important;
    border-radius: 4px !important;
    padding: 1rem !important;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00ff41 !important;
    box-shadow: 0 0 15px rgba(0,255,65,0.15) !important;
}
/* file name after upload */
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p {
    color: #00aa22 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
}
/* hide ALL labels inside the uploader section except our custom one */
[data-testid="stFileUploaderDropzoneInstructions"] { display: none !important; }

/* ── CAMERA ── */
[data-testid="stCameraInput"] {
    background: transparent !important;
    border: 1px dashed #003a15 !important;
    border-radius: 4px !important;
}
[data-testid="stCameraInput"] button {
    font-family: 'Share Tech Mono', monospace !important;
    background: transparent !important;
    border: 1px solid #00ff41 !important;
    color: #00ff41 !important;
    border-radius: 3px !important;
    letter-spacing: 2px !important;
}
[data-testid="stCameraInput"] label { display: none !important; }

/* ── TABS ── */
button[data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.78rem !important; letter-spacing: 2px !important;
    color: #005511 !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    padding-bottom: 8px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #00ff41 !important;
    border-bottom: 2px solid #00ff41 !important;
    text-shadow: 0 0 8px #00ff41;
}
[role="tablist"] { border-bottom: 1px solid #002a0a !important; }

/* ── IMAGE ── */
[data-testid="stImage"] img {
    border: 1px solid #00ff41 !important;
    border-radius: 3px !important;
    box-shadow: 0 0 25px rgba(0,255,65,0.25) !important;
    filter: brightness(0.92) contrast(1.08) saturate(0.9);
    animation: imgfadein 0.5s ease;
}
@keyframes imgfadein { from { opacity:0; filter: brightness(2); } to { opacity:1; } }

/* ── RESULTS ── */
.result-wrap { margin-top: 1.2rem; }
.result-row {
    border: 1px solid;
    border-radius: 3px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.85rem;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
    animation: slidein 0.4s ease both;
}
.result-row:nth-child(1) { animation-delay: 0.05s; }
.result-row:nth-child(2) { animation-delay: 0.15s; }
.result-row:nth-child(3) { animation-delay: 0.25s; }
@keyframes slidein {
    from { opacity:0; transform: translateX(-12px); }
    to   { opacity:1; transform: translateX(0); }
}
.result-row::before {
    content:""; position:absolute; left:0; top:0; bottom:0;
    width:3px;
}
.result-label { border-color:#00ff41; color:#00ff41; background:rgba(0,255,65,0.04); }
.result-label::before { background:#00ff41; box-shadow:0 0 8px #00ff41; }
.result-score { border-color:#00ccff; color:#00ccff; background:rgba(0,204,255,0.03); }
.result-score::before { background:#00ccff; box-shadow:0 0 8px #00ccff; }
.result-bin   { border-color:#ffaa00; color:#ffaa00; background:rgba(255,170,0,0.03); }
.result-bin::before { background:#ffaa00; box-shadow:0 0 8px #ffaa00; }
.result-key   { opacity:0.5; margin-right:0.5rem; }

/* animated score bar */
.score-bar-wrap { height:3px; background:rgba(0,204,255,0.12); border-radius:2px; margin-top:6px; }
.score-bar {
    height:3px; background:#00ccff; border-radius:2px;
    box-shadow:0 0 8px #00ccff;
    animation: growbar 0.8s ease 0.3s both;
    transform-origin: left;
}
@keyframes growbar { from { width:0 !important; } }

/* ── SPINNER ── */
[data-testid="stSpinner"] p,
[data-testid="stSpinner"] span {
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 2px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:#000; }
::-webkit-scrollbar-thumb { background:#003a15; border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:#00ff41; }

/* ── FOOTER ── */
.footer-line {
    border-top: 1px solid #001a08;
    margin-top: 2rem; padding-top: 0.8rem;
    font-size: 0.6rem; color: #003a15 !important;
    letter-spacing: 2px; text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD MODEL ──
@st.cache_resource
def load_model():
    m = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    m.eval()
    return m

model = load_model()

# ── INFERENCE ──
def preprocess(image: Image.Image) -> torch.Tensor:
    img = image.convert("RGB").resize((224, 224), Image.BICUBIC)
    pixels = list(img.getdata())
    t = torch.tensor(pixels, dtype=torch.float32) / 255.0
    t = (t - 0.5) / 0.5
    t = t.view(224, 224, 3).permute(2, 0, 1)
    return t.unsqueeze(0)

def get_disposal(label: str) -> str:
    m = {
        "plastic":   "GELBE TONNE  &nbsp;[RECYCLING_BIN_YELLOW]",
        "paper":     "BLAUE TONNE  &nbsp;[RECYCLING_BIN_BLUE]",
        "cardboard": "BLAUE TONNE  &nbsp;[RECYCLING_BIN_BLUE]",
        "glass":     "GLASCONTAINER [BOTTLE_BANK]",
        "metal":     "GELBE TONNE  &nbsp;[RECYCLING_BIN_YELLOW]",
        "trash":     "RESTMÜLL     &nbsp;[GENERAL_WASTE]",
    }
    for k, v in m.items():
        if k in label.lower(): return v
    return "LOKAL PRÜFEN  [CHECK_LOCAL_REGULATIONS]"

def run_prediction(image: Image.Image):
    t = preprocess(image)
    with torch.no_grad():
        logits = model(pixel_values=t).logits
    idx   = logits.argmax(-1).item()
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
      <div class="result-row result-label">
        <span class="result-key">CLASS_ID &nbsp;&gt;&gt;</span>{label.upper()}
      </div>
      <div class="result-row result-score">
        <span class="result-key">CONFIDENCE&gt;&gt;</span>{score:.1%}
        <div class="score-bar-wrap"><div class="score-bar" style="width:{pct}%"></div></div>
      </div>
      <div class="result-row result-bin">
        <span class="result-key">DISPOSAL &nbsp;&gt;&gt;</span>{disposal}
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════ RENDER ══════════════

# HERO
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">☣ WASTE_ID.EXE</div>
  <div class="hero-sub typewriter">&gt; NEURAL WASTE CLASSIFICATION SYSTEM // ONLINE<span class="blink">_</span></div>
</div>
""", unsafe_allow_html=True)

# STATS
st.markdown("""
<div class="stat-grid">
  <div class="stat-box">
    <div class="stat-box-label">// WASTE CLASSES</div>
    <div class="stat-val">06</div>
  </div>
  <div class="stat-box">
    <div class="stat-box-label">// MODEL ENGINE</div>
    <div class="stat-val">ViT</div>
  </div>
  <div class="stat-box">
    <div class="stat-box-label">// INPUT MODES</div>
    <div class="stat-val">02</div>
  </div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2 = st.tabs(["[ FILE_UPLOAD ]", "[ WEBCAM_FEED ]"])

with tab1:
    st.markdown('<div class="panel"><div class="panel-label">INPUT // FILE_STREAM</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("x", type=["jpg","jpeg","png"], label_visibility="hidden")
    if uploaded_file is not None:
        show_results(Image.open(uploaded_file))
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="panel"><div class="panel-label">INPUT // LIVE_CAPTURE</div>', unsafe_allow_html=True)
    camera_image = st.camera_input("x", label_visibility="hidden")
    if camera_image is not None:
        show_results(Image.open(camera_image))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-line">
  WASTE_ID.EXE &nbsp;///&nbsp; ENGINE: yangy50/garbage-classification
  &nbsp;///&nbsp; STATUS: ONLINE &nbsp;///&nbsp; ALL SYSTEMS NOMINAL
</div>
""", unsafe_allow_html=True)
