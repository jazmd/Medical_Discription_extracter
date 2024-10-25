from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables and configure API
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Please add your Google API key to the .env file!")
else:
    genai.configure(api_key=api_key)

def analyze_medical_document(image, prompt):
    """Analyze medical document using Google's Gemini AI"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def main():
    # Page setup
    st.set_page_config(page_title="Medical Document Analyzer")
    
    # Header
    st.title("🏥 Medical Document Analyzer")
    st.write("Upload a medical document image to get an analysis")

    # Default prompt template
    default_prompt = """
    Please analyze this medical document and provide:
    1. Key findings
    2. Diagnosis (if any)
    3. Treatment recommendations
    4. Important notes
    
    Please explain in simple, easy-to-understand language.
    """

    # Input section
    custom_prompt = st.text_area(
        "Customize your analysis request (optional):",
        value=default_prompt,
        height=150
    )

    # File upload
    uploaded_file = st.file_uploader(
        "Upload medical document image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your medical document"
    )

    # Display and analyze image
    if uploaded_file:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Document", use_column_width=True)

            # Analyze button
            if st.button("📋 Analyze Document", type="primary"):
                with st.spinner("Analyzing document..."):
                    # Get analysis
                    analysis = analyze_medical_document(image, custom_prompt)
                    
                    # Display results
                    st.success("Analysis Complete!")
                    st.markdown("### Analysis Results")
                    st.markdown(analysis)

                    # Add download option for analysis
                    st.download_button(
                        "📥 Download Analysis",
                        analysis,
                        file_name="medical_analysis.txt",
                        mime="text/plain"
                    )
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()
