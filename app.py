from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    # Custom prompt template for medical document analysis
    prompt_template = "Analyze this medical document and provide a concise summary of the key findings, diagnosis, treatment plan, or any relevant information. Please use plain language for easy understanding."

    response = model.generate_content([prompt_template, image])
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="💡 Medical Description Analyzer 📄")

st.header("Medical Descriptions Extracter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "pdf"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Analyze this Document")

## If ask button is clicked

if submit:
    if image:
        response = get_gemini_response(image)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("Please upload an image first.")
