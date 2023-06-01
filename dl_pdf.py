import requests


def download_pdf_with_url(url : str):

    req = requests.get(url)

    with open('TMP.pdf', 'wb') as f:
        f.write(req.content)

    return req