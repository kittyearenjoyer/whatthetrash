import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification

MODEL_NAME = "yangy50/garbage-classification"

st.set_page_config(
    page_title="WASTE_ID.EXE",
    page_icon="☣️",
    layout="wide"
)

# ══════════════ MATRIX BACKGROUND ══════════════

st.markdown("""
<canvas id="matrix"></canvas>

<script>
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const letters = "01アイウエオカキクケコサシスセソABCDEFGHIJKLMNOPQRSTUVWXYZ";
const fontSize = 14;
const columns = canvas.width / fontSize;

const drops = [];

for(let x = 0; x < columns; x++) {
    drops[x] = 1;
}

function draw() {

    ctx.fillStyle = "rgba(0,0,0,0.08)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#00ff41";
    ctx.font = fontSize + "px monospace";

    for(let i = 0; i < drops.length; i++) {

        const text = letters[Math.floor(Math.random() * letters.length)];

        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }

        drops[i]++;
    }
}

setInterval(draw, 35);

window.addEventListener("resize", () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
</script>

<style>

#matrix{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    z-index:-10;
    opacity:0.35;
    pointer-events:none;
}

@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

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

.block-container {
    padding-top: 1.5rem !important;
    max-width: 1100px !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu,
footer,
[data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

/* SCANLINES */

body::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 9999;
    pointer-events: none;

    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,65,0.025) 2px,
        rgba(0,255,65,0.025) 4px
    );

    animation: scanroll 8s linear infinite;
}

@keyframes scanroll {
    0%   { background-position: 0 0; }
    100% { background-position: 0 200px; }
}

/* HERO */

.hero-wrap {

    border: 1px solid #00ff41;
    border-radius: 4px;

    padding: 2rem 2.5rem;

    margin-bottom: 1.5rem;

    position: relative;

    background: linear-gradient(
        135deg,
        rgba(0,255,65,0.05) 0%,
        transparent 60%
    );

    box-shadow:
        0 0 30px rgba(0,255,65,0.15),
        inset 0 0 40px rgba(0,255,65,0.03);

    animation: flicker 6s infinite;
}

@keyframes flicker {

    0%,19%,21%,23%,25%,54%,56%,100% {
        opacity:1;
    }

    20%,22%,24%,55% {
        opacity:0.4;
    }
}

.hero-wrap::before {

    content: "WASTE_ID.EXE v3.0 // NEURAL CLASSIFICATION SYSTEM // READY";

    position: absolute;

    top: -10px;
    left: 20px;

    background: #000;

    padding: 0 8px;

    font-size: 0.6rem;

    color: #00ff41;

    letter-spacing: 2px;
}

.hero-wrap::after {

    content: "[ SECURE CHANNEL ]";

    position: absolute;

    top: -10px;
    right: 20px;

    background: #000;

    padding: 0 8px;

    font-size: 0.6rem;

    color: #007722;

    letter-spacing: 2px;
}

.hero-title {

    font-family: 'Orbitron', monospace !important;

    font-size: clamp(1.8rem, 4vw, 3rem) !important;

    font-weight: 900 !important;

    color: #00ff41 !important;

    letter-spacing: 6px;

    text-shadow:
        0 0 20px #00ff41,
        0 0 40px rgba(0,255,65,0.5),
        0 0 80px rgba(0,255,65,0.2);

    margin-bottom: 0.5rem;
}

.hero-sub {

    color: #00cc33 !important;

    font-size: 0.82rem;

    letter-spacing: 2px;
}

.blink {
    animation: blink 1s step-end infinite;
}

@keyframes blink {
    50% {
        opacity:0;
    }
}

/* TYPEWRITER */

.typewriter {

    overflow: hidden;

    white-space: nowrap;

    border-right: 2px solid #00ff41;

    width: 0;

    animation:
        typing 2.5s steps(40) 0.5s forwards,
        caret 0.8s step-end infinite;
}

@keyframes typing {
    to { width: 100%; }
}

@keyframes caret {
    50% { border-color: transparent; }
}

/* BOOT */

.boot {

    color:#00ff41;

    font-family:'Share Tech Mono', monospace;

    margin-bottom:1rem;

    line-height:1.6;

    animation:flicker 2s infinite;
}

/* STAT GRID */

.stat-grid {

    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:1rem;

    margin-bottom:1.5rem;
}

.stat-box {

    border:1px solid #00ff41;

    border-radius:4px;

    padding:1rem 0.5rem;

    text-align:center;

    background:rgba(0,255,65,0.02);

    box-shadow:0 0 12px rgba(0,255,65,0.08);

    transition:all 0.3s ease;
}

.stat-box:hover {

    background:rgba(0,255,65,0.07);

    box-shadow:0 0 25px rgba(0,255,65,0.25);

    transform:translateY(-2px);
}

.stat-box-label {

    font-size:0.58rem;

    color:#007722;

    letter-spacing:2px;

    margin-bottom:0.4rem;
}

.stat-val {

    font-family:'Orbitron', monospace !important;

    font-size:1.7rem !important;

    color:#00ff41 !important;

    text-shadow:0 0 12px #00ff41;
}

/* PANEL */

.panel {

    border:1px solid #003a15;

    border-radius:4px;

    padding:1.5rem;

    background:rgba(0,255,65,0.015);

    box-shadow:0 0 20px rgba(0,255,65,0.06);

    position:relative;
}

.panel-label {

    position:absolute;

    top:-10px;

    left:16px;

    background:#000;

    padding:0 8px;

    font-size:0.62rem;

    color:#00ff41;

    letter-spacing:3px;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {

    border:2px dashed #00ff41 !important;

    border-radius:8px !important;

    background:rgba(0,255,65,0.03) !important;

    padding:2rem !important;

    transition:all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {

    background:rgba(0,255,65,0.08) !important;

    box-shadow:0 0 25px rgba(0,255,65,0.25) !important;

    transform:scale(1.01);
}

[data-testid="stFileUploaderDropzone"] button {

    background:black !important;

    color:#00ff41 !important;

    border:1px solid #00ff41 !important;

    padding:0.7rem 1.4rem !important;

    border-radius:4px !important;

    font-family:'Share Tech Mono', monospace !important;

    letter-spacing:2px !important;

    transition:all 0.2s ease;
}

[data-testid="stFileUploaderDropzone"] button:hover {

    background:#00ff41 !important;

    color:black !important;

    box-shadow:0 0 20px #00ff41 !important;
}

[data-testid="stFileUploaderDropzone"] label,
[data-testid="stFileUploaderDropzoneInstructions"] {
    display:none !important;
}

/* CAMERA */

[data-testid="stCameraInput"] {

    background:transparent !important;

    border:2px dashed #00ff41 !important;

    border-radius:8px !important;

    padding:1rem !important;
}

[data-testid="stCameraInput"] button {

    background:black !important;

    color:#00ff41 !important;

    border:1px solid #00ff41 !important;

    border-radius:4px !important;

    font-family:'Share Tech Mono', monospace !important;

    letter-spacing:2px !important;
}

[data-testid="stCameraInput"] label {
    display:none !important;
}

/* TABS */

button[data-baseweb="tab"] {

    font-family:'Share Tech Mono', monospace !important;

    font-size:0.78rem !important;

    letter-spacing:2px !important;

    color:#005511 !important;

    background:transparent !important;

    border-bottom:2px solid transparent !important;

    padding-bottom:8px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {

    color:#00ff41 !important;

    border-bottom:2px solid #00ff41 !important;

    text-shadow:0 0 8px #00ff41;
}

/* IMAGE */

[data-testid="stImage"] img {

    border:1px solid #00ff41 !important;

    border-radius:3px !important;

    box-shadow:0 0 25px rgba(0,255,65,0.25) !important;

    filter:brightness(0.92) contrast(1.08) saturate(0.9);
}

/* RESULTS */

.result-wrap {
    margin-top:1.2rem;
}

.result-row {

    border:1px solid;

    border-radius:3px;

    padding:0.75rem 1rem;

    margin-bottom:0.6rem;

    font-size:0.85rem;

    letter-spacing:1px;
}

.result-label {

    border-color:#00ff41;

    color:#00ff41;

    background:rgba(0,255,65,0.04);
}

.result-score {

    border-color:#00ccff;

    color:#00ccff;

    background:rgba(0,204,255,0.03);
}

.result-bin {

    border-color:#ffaa00;

    color:#ffaa00;

    background:rgba(255,170,0,0.03);
}

.result-key {
    opacity:0.5;
    margin-right:0.5rem;
}

/* SCORE BAR */

.score-bar-wrap {

    height:3px;

    background:rgba(0,204,255,0.12);

    border-radius:2px;

    margin-top:6px;
}

.score-bar {

    height:3px;

    background:#00ccff;

    border-radius:2px;

    box-shadow:0 0 8px #00ccff;
}

/* FOOTER */

.footer-line {

    border-top:1px solid #001a08;

    margin-top:2rem;

    padding-top:0.8rem;

    font-size:0.6rem;

    color:#003a15 !important;

    letter-spacing:2px;

    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ══════════════ MUSIC ══════════════

st.markdown("""
<audio autoplay loop>
    <source src="https://files.catbox.moe/8ehw8x.mp3" type="audio/mp3">
</audio>
""", unsafe_allow_html=True)

# ══════════════ LOAD MODEL ══════════════

@st.cache_resource
def load_model():
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return model

model = load_model()

# ══════════════ PREPROCESS ══════════════

def preprocess(image: Image.Image):

    img = image.convert("RGB").resize((224,224), Image.BICUBIC)

    pixels = list(img.getdata())

    tensor = torch.tensor(pixels, dtype=torch.float32) / 255.0

    tensor = (tensor - 0.5) / 0.5

    tensor = tensor.view(224,224,3).permute(2,0,1)

    return tensor.unsqueeze(0)

# ══════════════ DISPOSAL ══════════════

def get_disposal(label: str):

    mapping = {

        "plastic": "GELBE TONNE [YELLOW_BIN]",
        "paper": "BLAUE TONNE [BLUE_BIN]",
        "cardboard": "BLAUE TONNE [BLUE_BIN]",
        "glass": "GLASCONTAINER [BOTTLE_BANK]",
        "metal": "GELBE TONNE [YELLOW_BIN]",
        "trash": "RESTMÜLL [GENERAL_WASTE]"
    }

    for k, v in mapping.items():

        if k in label.lower():
            return v

    return "LOKAL PRÜFEN [CHECK_LOCAL]"

# ══════════════ INFERENCE ══════════════

def run_prediction(image: Image.Image):

    tensor = preprocess(image)

    with torch.no_grad():

        logits = model(pixel_values=tensor).logits

    idx = logits.argmax(-1).item()

    label = model.config.id2label[idx]

    score = torch.softmax(logits, dim=-1)[0][idx].item()

    return label, score

# ══════════════ SHOW RESULTS ══════════════

def show_results(image: Image.Image):

    st.image(image, use_container_width=True)

    with st.spinner("[ RUNNING NEURAL SCAN... ]"):

        label, score = run_prediction(image)

    disposal = get_disposal(label)

    pct = int(score * 100)

    st.markdown(f"""
    <div class="result-wrap">

        <div class="result-row result-label">
            <span class="result-key">CLASS_ID >></span>
            {label.upper()}
        </div>

        <div class="result-row result-score">
            <span class="result-key">CONFIDENCE >></span>
            {score:.1%}

            <div class="score-bar-wrap">
                <div class="score-bar" style="width:{pct}%"></div>
            </div>
        </div>

        <div class="result-row result-bin">
            <span class="result-key">DISPOSAL >></span>
            {disposal}
        </div>

    </div>
    """, unsafe_allow_html=True)

# ══════════════ BOOT SEQUENCE ══════════════

st.markdown("""
<div class="boot">
BOOTING WASTE_ID.EXE...<br>
INITIALIZING NEURAL CORE...<br>
LOADING CLASSIFICATION ENGINE...<br>
ESTABLISHING SECURE CONNECTION...<br>
SYSTEM ONLINE.
</div>
""", unsafe_allow_html=True)

# ══════════════ HERO ══════════════

st.markdown("""
<div class="hero-wrap">

    <div class="hero-title">
        ☣ WASTE_ID.EXE
    </div>

    <div class="hero-sub typewriter">
        > NEURAL WASTE CLASSIFICATION SYSTEM // ONLINE
        <span class="blink">_</span>
    </div>

</div>
""", unsafe_allow_html=True)

# ══════════════ STATS ══════════════

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

# ══════════════ TABS ══════════════

tab1, tab2 = st.tabs([
    "[ FILE_UPLOAD ]",
    "[ WEBCAM_FEED ]"
])

# ══════════════ FILE UPLOAD ══════════════

with tab1:

    st.markdown(
        '<div class="panel"><div class="panel-label">INPUT // FILE_STREAM</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "upload",
        type=["jpg","jpeg","png"],
        label_visibility="hidden"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        show_results(image)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════ CAMERA ══════════════

with tab2:

    st.markdown(
        '<div class="panel"><div class="panel-label">INPUT // LIVE_CAPTURE</div>',
        unsafe_allow_html=True
    )

    camera_image = st.camera_input(
        "camera",
        label_visibility="hidden"
    )

    if camera_image is not None:

        image = Image.open(camera_image)

        show_results(image)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════ FOOTER ══════════════

st.markdown("""
<div class="footer-line">

    WASTE_ID.EXE /// ENGINE: yangy50/garbage-classification
    /// STATUS: ONLINE /// ALL SYSTEMS NOMINAL

</div>
""", unsafe_allow_html=True)
