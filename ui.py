import streamlit as st
import requests
import time
from datetime import datetime

# ================= CONFIG =================
BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="CHATBOT",
    page_icon="💬",
    layout="wide"
)

# ================= TOPIC CLASSIFICATION =================
def classify_topic(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["who is", "born", "biography", "leader", "actor", "cricketer"]):
        return "🧑 Person"
    elif any(k in q for k in ["where is", "located", "city", "country", "tower", "temple"]):
        return "📍 Place"
    elif any(k in q for k in ["technology", "ai", "computer", "software", "machine learning"]):
        return "💻 Technology"
    elif any(k in q for k in ["cricket", "football", "player", "match", "sports"]):
        return "🏏 Sports"
    elif any(k in q for k in ["define", "explain", "what is", "theory", "concept"]):
        return "📘 Education"
    else:
        return "💬 General"

# ================= PREMIUM BACKGROUND + UI =================
st.markdown("""
<style>
/* FULL SCREEN BACKGROUND FIX */
html, body, [data-testid="stAppViewContainer"], .stApp {
    height: 100%;
    background:
        linear-gradient(rgba(5,8,20,0.88), rgba(5,8,20,0.88)),
        url("https://images.unsplash.com/photo-1674027444485-cec3da58eef4?auto=format&fit=crop&w=2000&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Remove white gaps */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stFooter"] {
    background: transparent !important;
}

/* Main app padding fix */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Glass container */
.glass {
    background: rgba(28, 28, 40, 0.75);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 0 40px rgba(0,0,0,0.6);
    margin-bottom: 22px;
}

/* User bubble */
.user {
    background: linear-gradient(135deg,#6f7cff,#00ffd5);
    color: #000;
    padding: 14px 18px;
    border-radius: 18px;
    font-weight: 600;
    text-align: right;
    margin: 12px 0;
}

/* Bot text */
.bot {
    color: #eaeaea;
    line-height: 1.75;
    font-size: 16px;
}

/* Topic badge */
.badge {
    color: #00ffd5;
    font-size: 14px;
    margin-bottom: 6px;
}

/* Timestamp */
.time {
    font-size: 12px;
    color: #9aa4b2;
    margin-top: 6px;
}

/* Hide Streamlit footer text */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div style="text-align:center;margin-top:10px;">
    <h1 style="color:#00ffd5;">💬 CHATBOT</h1>
    <p style="color:#b5c7d3;">Smart • Topic-Aware • Gen-Z AI Assistant</p>
    <span style="color:#4cff4c;">● Online</span>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.header("⚙ Controls")
    if st.button("🗑 Clear Chat"):
        st.session_state.chat = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Theme:** AI Glass Dark")
    st.markdown("**Mode:** Text-Only Smart Chat")
    st.markdown("**Status:** 🟢 Connected")

# ================= MEMORY =================
if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= TYPING EFFECT =================
def typing_effect(text):
    box = st.empty()
    out = ""
    for ch in text:
        out += ch
        box.markdown(f"<div class='bot'>{out}</div>", unsafe_allow_html=True)
        time.sleep(0.003)

# ================= CHAT AREA =================
container = st.container()

with container:
    if not st.session_state.chat:
        st.markdown("""
        <div class="glass" style="text-align:center;">
            <h3 style="color:#00ffd5;">👋 Welcome!</h3>
            <p class="bot">Ask anything to start the conversation.</p>
        </div>
        """, unsafe_allow_html=True)

    for item in st.session_state.chat:
        st.markdown(f"<div class='user'>{item['q']}</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown(f"<div class='badge'>{item['topic']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot'>{item['a']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='time'>🕒 {item['time']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= INPUT =================
query = st.chat_input("Ask anything…")

if query:
    topic = classify_topic(query)
    timestamp = datetime.now().strftime("%I:%M %p")

    st.markdown(f"<div class='user'>{query}</div>", unsafe_allow_html=True)

    with st.spinner("🤖 Thinking..."):
        res = requests.post(
            BACKEND_URL,
            json={"message": query},
            timeout=60
        )
        try:
            answer = res.json().get("reply", "No response")
        except:
            answer = "Error getting response"

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown(f"<div class='badge'>{topic}</div>", unsafe_allow_html=True)
    typing_effect(answer)
    st.markdown(f"<div class='time'>🕒 {timestamp}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.chat.append({
        "q": query,
        "a": answer,
        "topic": topic,
        "time": timestamp
    })
