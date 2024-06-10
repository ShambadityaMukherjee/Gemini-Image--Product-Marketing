from dotenv import load_dotenv
load_dotenv() # to load the data from env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Product Description App")

st.header("Marketing Campaign App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the product")

input_prompt="""
You are an expert in Product Marketing campaign where you need to see any product items from the image
               and write the details about the marketing campaign, also provide the process for marketing the product
               is below format

               1. Product Name: [Product Name]
               2. Product Type: [Category of the product, e.g., electronics, software, apparel, etc.]
               3. Price range : [ USD500 - USD10000]
               4. Target Audience: [Demographics, interests, etc.]
               5. Unique Selling Points (USPs): [List of unique features, e.g., innovative design, eco-friendly, advanced technology, etc.]
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)