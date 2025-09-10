# streamlit-ollama-local

Integrasi [Streamlit](https://streamlit.io/) dengan [Ollama](https://ollama.com/) untuk menjalankan model AI lokal secara mudah melalui antarmuka web interaktif.

## Fitur

- **Antarmuka Streamlit**: Mudah digunakan untuk mengakses dan mengelola model AI lokal.
- **Integrasi Ollama**: Jalankan dan interaksikan model seperti Llama, Mistral, dan lainnya secara lokal.
- **Konfigurasi Sederhana**: Deploy cepat tanpa konfigurasi rumit.
- **Dukungan Docker**: Jalankan aplikasi dalam container untuk kemudahan deployment.

## Instalasi

### 1. Clone repository

```bash
git clone https://github.com/OxidiLily/streamlit-ollama-local.git
cd streamlit-ollama-local
```

### 2. Install dependencies

Pastikan Python 3.8+ sudah terinstall.

```bash
pip install -r requirements.txt
```

### 3. Jalankan Ollama

Pastikan Ollama sudah terinstall dan model sudah di-pull:

```bash
ollama run llama2
```

### 4. Jalankan Streamlit

```bash
streamlit run app.py
```

## Menjalankan dengan Docker

```bash
docker build -t streamlit-ollama-local .
docker run -p 8501:8501 streamlit-ollama-local
```

## Penggunaan

- Akses aplikasi melalui browser di `http://localhost:8501`
- Masukkan prompt dan interaksikan dengan model AI lokal

## Struktur Project

```
.
├── app.py                # Main Streamlit app
├── requirements.txt      # Daftar dependensi Python
├── Dockerfile            # Docker build file
└── README.md             # Dokumentasi ini
```

## Kontribusi

Kontribusi sangat terbuka! Silakan buka issue atau pull request.

---

Dibuat oleh [OxidiLily](https://oxidilily.com/)
