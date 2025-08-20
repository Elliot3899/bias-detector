import streamlit as st
import requests
import os

# ========================
# CONFIGURATION
# ========================
API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")  # set this in your host's env vars

# ========================
# STREAMLIT PAGE SETUP
# ========================
st.set_page_config(page_title="Bias & Persuasion Detector", layout="centered")

# Hide Streamlit's default footer, hamburger menu, and badge
st.markdown("""
<style>
#MainMenu {visibility: hidden;}               /* Hide top-right menu */
div[role="contentinfo"] {visibility: hidden;} /* Hide footer */
a[data-testid="stBadge"] {visibility: hidden;}/* Hide "Made with Streamlit" badge */
</style>
""", unsafe_allow_html=True)

# ========================
# THEME HELPERS
# ========================
DARK = {
    "bg": "#0e1117",
    "bg2": "#161b22",
    "text": "#e6edf3",
    "accent": "#8ab4f8",
    "border": "#30363d",
}
LIGHT = {
    "bg": "#ffffff",
    "bg2": "#f6f8fa",
    "text": "#0b0f17",
    "accent": "#1f6feb",
    "border": "#d0d7de",
}

def apply_theme(theme, is_dark: bool):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {theme["bg"]};
            color: {theme["text"]};
        }}
        [data-testid="stHeader"] {{
            background: {theme["bg"]};
        }}

        /* Inputs/Textareas */
        .stTextInput textarea, .stTextArea textarea {{
            background: {theme["bg2"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
        }}

        /* Button — strong contrast in both themes */
        .stButton>button {{
            background: {"#238636" if is_dark else "#1f6feb"}; /* green for dark, blue for light */
            color: white !important;
            border: 1px solid {theme["border"]};
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1rem;
            cursor: pointer;
        }}
        .stButton>button:hover {{ filter: brightness(1.06); }}
        .stButton>button:focus {{
            outline: 3px solid rgba(255,255,255,0.35);
            outline-offset: 2px;
        }}

        /* Alert containers */
        .stSuccess, .stWarning, .stError {{
            background: {theme["bg2"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]};
        }}

        /* Links */
        a, .stMarkdown a {{ color: {theme["accent"]} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ========================
# UI
# ========================
# Sidebar theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
with st.sidebar:
    st.markdown("### Appearance")
    st.session_state.theme = st.toggle("Dark mode", value=True, key="__dark") and "Dark" or "Light"

is_dark = st.session_state.theme == "Dark"
current = DARK if is_dark else LIGHT
apply_theme(current, is_dark)

st.title("Bias & Persuasion Detector")
st.write("Enter your text and let the AI analyze it.")

user_text = st.text_area("Text to analyze:")

if st.button("Analyze", use_container_width=True):
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        if not API_KEY:
            st.error("OPENAI_API_KEY is not set on the server/environment.")
        else:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",  # or another available chat model
                "messages": [
                    {"role": "system", "content": "You are an AI that detects bias and persuasion techniques in text."},
                    {"role": "user", "content": user_text}
                ],
                "temperature": 0
            }
            try:
                response = requests.post(API_URL, headers=headers, json=data, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    output = result['choices'][0]['message']['content']
                    st.success(output)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")



