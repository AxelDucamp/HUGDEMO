import requests
import os

def download_pdf_with_url(url : str):

    if "TMP.pdf" is in os.listdir():
        os.remove("TMP.pdf")

    req = requests.get(url)

    with open('TMP.pdf', 'wb') as f:
        f.write(req.content)

    return req