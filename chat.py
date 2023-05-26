import streamlit as st
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile
import openai
import os
from streamlit_chat import message
import pandas as pd

openai.api_key = os.getenv("OPENAI_KEY")

def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://raw.githubusercontent.com/AxelDucamp/Bayesian_Network_Deployement/340bd83a8d2cc5622657d984bc292c8e314d8b91/wallpapertmp.png");
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
        #question = st.text_input("Enter your question here : ")
        #if st.button("Submit !"):
        #    with st.spinner('Wait for it...'):
        #        response = openai.ChatCompletion.create(
        #            model="gpt-4",
        #            messages=[
        #                {"role": "system",
        #                 "content": "You are an assistant looking for information in documents. Your task is to answer questions about the given text. French only"},
        #                {"role": "user", "content": "Information about the document : " + st.session_state["text"] + ". The question is : " + question},
        #            ]
        #        )

        #    st.write(response["choices"][0]["message"]["content"])

        # Initialisation des variables de session
        if 'key' not in st.session_state:
            st.session_state['key'] = 0
            try:
                os.remove("chat.csv")
            except:
                pass
        if 'bot_key' not in st.session_state:
            st.session_state['bot_key'] = 0
        if 'check2' not in st.session_state:
            st.session_state['check2'] = False
        if 'chat_resume' not in st.session_state:
            st.session_state['chat_resume'] = []

        # Chargement ou création du fichier CSV contenant les messages
        try:
            df = pd.read_csv("chat.csv")
        except FileNotFoundError:
            data = {
                "bot": ["Bonjour je vous écoute ! 🐵"],
                "user": [""]
            }
            st.session_state['chat_resume'].append("Bonjour je vous écoute ! 🐵")
            df = pd.DataFrame(data)
            df.to_csv("chat.csv", index=False)

        placeholder = st.empty()
        input_ = st.text_input("you:")

        # Enregistrement du message de l'utilisateur
        if input_:
            df.loc[st.session_state['key'], "user"] = input_
            st.session_state['key'] += 1
            st.session_state['chat_resume'].append(input_)

        # Génération et enregistrement de la réponse du chatbot
        if st.session_state['bot_key'] != st.session_state['key']:
            df.to_csv("chat.csv", index=False)
            if not st.session_state['check2']:
                with st.spinner('Wait for it...'):
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system",
                             "content": "You are an assistant looking for information in documents. Your task is to answer questions about the given text. French only. The document : " + st.session_state["text"]},
                            {"role": "user", "content": " ".join(
                                st.session_state['chat_resume'])},
                        ]
                    )
                bot_response = response["choices"][0]["message"]["content"]
            if bot_response:
                st.session_state['chat_resume'].append(bot_response)
                data = {
                    "bot": [bot_response],
                    "user": [""]
                }
                df_tmp = pd.DataFrame(data)
                df = pd.concat([df, df_tmp], axis=0)
                df.to_csv("chat.csv", index=False)
                st.session_state['bot_key'] += 1
                # st.experimental_rerun()
                st.session_state['check2'] = True

        # Affichage de l'historique des messages
        with placeholder.container():
            for message_ in range(len(df)):
                if message_ != 0:
                    try:
                        message(df["user"].iloc[message_ - 1], is_user=True)
                        message(df["bot"].iloc[message_])
                        st.session_state['check2'] = False

                        # st.experimental_rerun()
                    except:
                        # os.remove("chat.csv")
                        pass
                else:
                    message(df["bot"].iloc[message_])


if __name__ == '__main__':
    main()
