FROM python:3.9.1
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y poppler-utils tesseract-ocr
RUN pip install -r requirements.txt
EXPOSE $PORT
CMD streamlit run --server.port $PORT squad.py
