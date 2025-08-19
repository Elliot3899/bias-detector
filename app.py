import streamlit as st
import requests
import os

# ========================
# CONFIGURATION
# ========================
API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")

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

def apply_theme(theme):
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
        .stTextInput textarea, .stTextArea textarea {{
            background: {theme["bg2"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]} !important;
        }}
        .stButton>button {{
            border-radius: 10px;
            border: 1px solid {theme["border"]};
        }}
        .stSuccess, .stWarning, .stError {{
            background: {theme["bg2"]} !important;
            color: {theme["text"]} !important;
            border: 1px solid {theme["border"]};
        }}
        a, .stMarkdown a {{
            color: {theme["accent"]} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ========================
# STREAMLIT APP
# ========================
st.set_page_config(page_title="Bias & Persuasion Detector", layout="centered")

# Sidebar theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
with st.sidebar:
    st.markdown("### Appearance")
    st.session_state.theme = st.toggle("Dark mode", value=True, key="__dark") and "Dark" or "Light"

current = DARK if st.session_state.theme == "Dark" else LIGHT
apply_theme(current)

st.title("Bias & Persuasion Detector")
st.write("Enter your text and let the AI analyze it.")

user_text = st.text_area("Text to analyze:")

if st.button("Analyze"):
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
                "model": "gpt-3.5-turbo",
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


