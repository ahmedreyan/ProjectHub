import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set Google API key directly
api_key = "AIzaSyB7enEUG7tIl-cfBtYHx_8ZW2DCpPEsgb8"  # Replace 'YOUR_API_KEY_HERE' with your actual API key
genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
def get_gemini_response(input_prompt, image=None):
    try:
        if image:
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([input_prompt, image])
            return response.text
        else:
            return "Please insert an image first."
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# User input
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to ask about the image
submit_button = st.button("Ask the question")

# When the button is clicked
if submit_button:
    if input_prompt or image:
        response = get_gemini_response(input_prompt, image)
        st.subheader("The Answer of your question is:")
        st.write(response)
    else:
        if not input_prompt and not image:
            st.error("Please provide an input prompt or upload an image.")
        elif not input_prompt:
            st.warning("Please provide an input prompt.")
        elif not image:
            st.warning("Please upload an image.")