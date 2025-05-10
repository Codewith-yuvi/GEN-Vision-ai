from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import json
import requests
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Function to get Gemini response
def get_gemini_response(input_text, image):
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content([image])
    return response.text

# Streamlit page config
st.set_page_config(page_title="GEN Vision AI Assistant")

# Function to load Lottie animation from file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Function to load Lottie animation from URL
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error loading Lottie URL: {e}")
        return None

# Load animations
lottie_intro = load_lottieurl("https://lottie.host/4a9c4bed-592d-44c5-961c-c1bae9e8474a/OqhE1lQo6r.lottie")
lottie_coding = load_lottiefile("coding.json")  # Ensure file exists
lottie_spinner = load_lottiefile("spinner.json")

# Page header
st.title("GEN Vision AI Assistant")
st.subheader("See the better future with GEN-Vision")

# Intro animation
st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="High",
    height=250,
    width=250,
    key="coding_lottie"
)

if lottie_intro is not None:
    st_lottie(lottie_intro, key="intro_animation")

# Prompt input with larger input box
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        height: 60px;  /* Increased height */
        font-size: 18px;  /* Increased font size */
        padding: 8px;  /* Increased padding */
        border-radius: 8px;  /* Rounded corners */
    }
    </style>
""", unsafe_allow_html=True)

# Text input
input_text = st.text_input("Input prompt:", key="input")

# Image uploader with custom CSS for purple background
st.markdown("""
    <style>
    div.stFileUploader > div {
        background-color: #8e44ad;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stFileUploader > div:hover {
        background-color: #732d91;
    }
    div.stButton > button:first-child {
        background-color: #8e44ad;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #732d91;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

# Submit button
submit = st.button("Submit")

if submit:
    placeholder = st.empty()

    # Show animated spinner while generating
    with placeholder.container():
        if lottie_spinner is not None:
            st_lottie(
                lottie_spinner,
                speed=0.1,
                reverse=False,
                loop=True,
                quality="medium",
                height=200,
                width=200,
                key="loading_spinner"
            )
            st.markdown("<h5 style='text-align: center;'>Generating response...</h5>", unsafe_allow_html=True)
        else:
            st.info("Generating response...")

    # Generate the response
    response = get_gemini_response(input_text, image)

    # Remove spinner
    placeholder.empty()

    # Show result with gray background
    st.header("The Response is:")
    st.markdown(
        f"""
        <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px; font-size: 16px;">
            {response}
        </div>
        """,
        unsafe_allow_html=True
    )
