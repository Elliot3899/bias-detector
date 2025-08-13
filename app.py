import streamlit as st
import requests
import os

# ========================
# CONFIGURATION
# ========================
API_URL = "https://api.openai.com/v1/chat/completions"  # Change if using another API
API_KEY = os.getenv("OPENAI_API_KEY")  # Store key in environment variable

# ========================
# STREAMLIT APP
# ========================
st.set_page_config(page_title="Bias & Persuasion Detector", layout="centered")

st.title("Bias & Persuasion Detector")
st.write("Enter your text and let the AI analyze it.")

user_text = st.text_area("Text to analyze:")

if st.button("Analyze"):
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",  # Or your chosen model
            "messages": [
                {"role": "system", "content": "You are an AI that detects bias and persuasion techniques in text."},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0
        }

        try:
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                output = result['choices'][0]['message']['content']
                st.success(output)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
