# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app_ollama

COPY . .

RUN python -m venv .venv

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]