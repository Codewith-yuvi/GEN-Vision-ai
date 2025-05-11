from dotenv import load_dotenv
load_dotenv()

import json
import requests
import streamlit as st
import os
import re
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def get_gemini_response(input_text, image):
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content([image])
    return response.text

# Load Lottie animations
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Page config
st.set_page_config(page_title="GEN Vision AI Assistant")

# Load local Lottie background animation (replace "bg_animation.json" with your actual file path)
lottie_bg = load_lottiefile("bg_animation.json")  # Make sure this file exists in your project directory

# Add background animation with CSS styling
if lottie_bg:
    st.markdown("""
        <style>
        .lottie-bg-container {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            opacity: 0.3;  /* Make background a bit transparent */
            overflow: hidden;
            pointer-events: none;
        }
        </style>
        <div class="lottie-bg-container">
    """, unsafe_allow_html=True)

    # Display the Lottie animation for background
    st_lottie(lottie_bg, speed=1, loop=True, height=900, width=1600, key="background", quality="high")

    st.markdown("</div>", unsafe_allow_html=True)

# Load other Lottie animations (for intro, spinner, etc.)
lottie_intro = load_lottiefile("intro.json")  # Adjust path to your intro Lottie file
lottie_coding = load_lottiefile("coding.json")  # Adjust path to your coding Lottie file
lottie_spinner = load_lottiefile("spinner.json")  # Adjust path to your spinner Lottie file

# App title and subtitle
st.title("GEN Vision AI Assistant")
st.subheader("See the better future with GEN-Vision")

# Lottie animation for coding
st_lottie(lottie_coding, speed=0.1, loop=True, height=100, width=100, key="coding_lottie")
if lottie_intro is not None:
    st_lottie(lottie_intro, key="intro_animation")

# Custom CSS styling for other elements
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        height: 60px;
        font-size: 18px;
        padding: 8px;
        border-radius: 8px;
    }
    div.stFileUploader > div {
        background-color: #3CE37C;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    div.stFileUploader > div:hover {
        background-color: #732d91;
    }
    div.stButton > button:first-child {
        background-color:#3CE37C;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #E501FF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Input fields
input_text = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

# Submit logic
submit = st.button("Submit")

if submit:
    placeholder = st.empty()
    with placeholder.container():
        if lottie_spinner:
            st_lottie(lottie_spinner, speed=0.1, loop=True, height=100, width=100, key="loading_spinner")
            st.markdown("<h5 style='text-align: center;'>Ideas Catching Fire... 🔥</h5>", unsafe_allow_html=True)
        else:
            st.info("Generating response...")

    # Get Gemini response
    raw_response = get_gemini_response(input_text, image)

    # Clean unwanted closing tags from response
    cleaned_response = re.sub(r'</div>\s*$', '', raw_response.strip(), flags=re.IGNORECASE)

    # Remove spinner
    placeholder.empty()

    # Show result
    st.header("The Response is:")
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; font-size: 16px;">
            {cleaned_response}
        </div>
        """,
        unsafe_allow_html=True
    )

