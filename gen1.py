from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import json
import requests
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from streamlit_lottie import st_lottie
import time

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
def load_lottieurl(url: str, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            r = requests.get(url)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                print("Max retries reached.")
                return None

# Load animations
lottie_intro = load_lottieurl("https://lottie.host/4a9c4bed-592d-44c5-961c-c1bae9e8474a/OqhE1lQo6r.lottie")
lottie_coding = load_lottiefile("coding.json")  # Make sure this file exists
lottie_spinner = load_lottiefile("spinner.json")

# Page header
st.title("GEN Vision AI Assistant")
st.subheader("See the better future with GEN-Vision")

# Intro animation
st_lottie(
    lottie_coding,
    speed=2,
    reverse=False,
    loop=True,
    quality="low",
    height=250,
    width=250,
    key="coding_lottie"
)

if lottie_intro is not None:
    st_lottie(lottie_intro, key="intro_animation")

# Prompt input
input_text = st.text_input("Input prompt:", key="input")

# Image uploader
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
                speed=1,
                reverse=False,
                loop=True,
                quality="low",
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

    # Show result
    st.header("The Response is:")
    st.write(response)
