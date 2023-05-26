FROM python:3.9.1
COPY . /app
WORKDIR /app

# Add these lines
RUN apt-get update \
    && apt-get install -y poppler-utils \
    && apt-get install -y tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \

RUN pip install -r requirements.txt
EXPOSE $PORT
CMD streamlit run --server.port $PORT chat.py