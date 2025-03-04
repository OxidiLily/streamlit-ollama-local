FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
# Install git clone project if public repo
# RUN git clone https://github.com/OxidiLily/streamlit-ollama-local.git .

COPY . .
RUN python -m venv .venv
RUN pip3 install -r requirements.txt
EXPOSE 8501
RUN apt update && apt install nano -y
RUN  mkdir .streamlit && cd .streamlit
# nano secrets.toml  nano config.toml
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
