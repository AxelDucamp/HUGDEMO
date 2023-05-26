import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile
import openai
import os

#openai.api_key = os.getenv("OPENAI_KEY")
openai.api_key = "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"

def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://raw.githubusercontent.com/AxelDucamp/Bayesian_Network_Deployement/ab6ff7d681c9f6d692dfb1e9cde34aacd61f3fc6/img.png");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


add_bg_from_url()

# Function to convert PDF to images
def pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)

# Function to convert Images to Text
def ocr_core(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

if 'text' not in st.session_state.keys():
    st.session_state["text"] = ""

if "check" not in st.session_state.keys():
    st.session_state["check"] = False

def main():
    st.title("HUG Demo 02/06/2023")

    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if pdf_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(pdf_file.getvalue())
            result = pdf_to_img(f.name)
        if st.button('Convert to Text'):
            st.session_state["check"] = True
            if result:
                st.write('Extracting Text from PDF...')
                extracted_text = ocr_core(result)
                st.write('Done.')
                st.session_state["text"] = extracted_text
                st.text_area("Extracted Text:", extracted_text, height=200)

        elif st.session_state["text"] != "":
            st.text_area("Extracted Text:", st.session_state["text"], height=200)

    if st.session_state["check"] == True:
        question = st.text_input("Enter your question here : ")
        if st.button("Submit !"):
            with st.spinner('Wait for it...'):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system",
                         "content": "You are an assistant looking for information in documents. Your task is to answer questions about the given text. French only"},
                        {"role": "user", "content": "Information about the document : " + st.session_state["text"] + ". The question is : " + question},
                    ]
                )

            st.write(response["choices"][0]["message"]["content"])


if __name__ == '__main__':
    main()
