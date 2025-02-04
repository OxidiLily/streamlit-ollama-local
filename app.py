import streamlit as st
import requests
import json
import os
import re
from datetime import datetime

# Judul aplikasi
st.set_page_config(page_title="Ollama WebUI", page_icon="🤖", layout="wide",menu_items={
        'About': "About Me? "+"\n\n https://oxidilily.my.id/"
    })

# Direktori untuk menyimpan file chat
CHAT_DIR = "saved_chats"
os.makedirs(CHAT_DIR, exist_ok=True)

# Path untuk file penyimpanan riwayat chat sementara
CURRENT_CHAT_FILE = os.path.join(CHAT_DIR, "current_chat.json")

# Fungsi untuk mendapatkan daftar model dari Ollama
def get_ollama_models():
    url = st.secrets["API"]["tags"]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("API Response:", data)  # Debugging
            if isinstance(data, dict) and "models" in data:
                return [model["name"] for model in data["models"]]
            elif isinstance(data, list):
                return [model["name"] for model in data]
            else:
                st.error("Format respons tidak sesuai.")
                return []
        else:
            st.error(f"Gagal mendapatkan Daftar Model dari Ollama: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Terjadi Kesalahan dalam mendapatkan Daftar Model")
        return []

# Fungsi untuk membaca riwayat chat dari file
def load_chat_history(file_name):
    file_path = os.path.join(CHAT_DIR, file_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.error(f"File '{file_name}' rusak. Menggunakan riwayat kosong.")
            return {}
    return {}

# Fungsi untuk menyimpan riwayat chat ke file
def save_chat_history(chat_history, file_name):
    file_path = os.path.join(CHAT_DIR, file_name)
    with open(file_path, "w") as file:
        json.dump(chat_history, file)

# Fungsi untuk menghapus file chat
def delete_chat(file_name):
    file_path = os.path.join(CHAT_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"Chat '{file_name}' berhasil dihapus!")
    else:
        st.error(f"File '{file_name}' tidak ditemukan.")

# Fungsi untuk membersihkan <think> dari respons
def clean_response(response):
    cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    cleaned_response = cleaned_response.strip()
    return cleaned_response

# Simpan riwayat chat ke session state dan file sementara
def save_chat_to_session_and_file(chat_history):
    # Simpan ke session state
    st.session_state.chat_history = chat_history
    
    # Simpan ke file sementara
    with open(CURRENT_CHAT_FILE, "w") as file:
        json.dump(chat_history, file)

# Inisialisasi session state untuk menyimpan riwayat percakapan
if "chat_history" not in st.session_state:
    # Muat riwayat chat dari file sementara jika ada
    if os.path.exists(CURRENT_CHAT_FILE):
        try:
            with open(CURRENT_CHAT_FILE, "r") as file:
                st.session_state.chat_history = json.load(file)
        except json.JSONDecodeError:
            st.session_state.chat_history = {}
    else:
        st.session_state.chat_history = {}

# Sidebar untuk pengaturan
with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    # Ambil daftar model dari Ollama
    available_models = get_ollama_models()
    
    if not available_models:
        st.warning("Tidak ada model yang tersedia.")
        selected_model = None
    else:
        # Tampilkan selectbox untuk memilih model
        selected_model = st.selectbox("Pilih Model", available_models)

   # Daftar chat yang tersimpan
    saved_chats = [f for f in os.listdir(CHAT_DIR) if f.endswith(".json")]
    if saved_chats:
        st.subheader("Chat Tersimpan")
        selected_chat = st.selectbox("Pilih Chat untuk Dilanjutkan atau Dihapus", [""] + saved_chats)
        
        if selected_chat:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Lanjutkan Chat"):
                    st.session_state.chat_history = load_chat_history(selected_chat)
                    save_chat_to_session_and_file(st.session_state.chat_history)  # Simpan ke file sementara
                    st.success(f"Chat '{selected_chat}' berhasil dimuat!")
                    st.rerun()
            with col2:
                if st.button("Hapus Chat"):
                    delete_chat(selected_chat)
                    st.rerun()

    # Tombol untuk menyimpan chat
    if st.button("Simpan Chat"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"chat_{timestamp}.json"
        save_chat_history(dict(st.session_state.chat_history), file_name)
        st.success(f"Chat berhasil disimpan sebagai '{file_name}'!")

    # Tombol untuk memulai chat baru
    if st.button("Mulai Chat Baru"):
        st.session_state.chat_history = {}
        if os.path.exists(CURRENT_CHAT_FILE):
            os.remove(CURRENT_CHAT_FILE)  # Hapus file sementara
        st.success("Chat baru dimulai!")
        st.rerun()

# Header utama
st.title("🤖 Ollama WebUI")

# Inisialisasi riwayat chat untuk model yang dipilih
if selected_model:
    if selected_model not in st.session_state.chat_history:
        st.session_state.chat_history[selected_model] = []
    messages = st.session_state.chat_history[selected_model]

    # Tampilkan riwayat percakapan untuk model yang dipilih
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dari pengguna
    if prompt := st.chat_input("Ketik pesan Anda..."):
        # Simpan pesan pengguna ke riwayat percakapan
        messages.append({"role": "user", "content": prompt})
        save_chat_to_session_and_file(st.session_state.chat_history)  # Simpan ke session state dan file sementara
        
        # Tampilkan pesan pengguna
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Dapatkan respons dari Ollama
        def query_ollama(prompt, model):
            url = st.secrets["API"]["generate"] 
            headers = {"Content-Type": "application/json"}
            data = {
                "model": model,
                "prompt": prompt
            }
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                if response.status_code == 200:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            try:
                                json_data = json.loads(decoded_line)
                                full_response += json_data.get("response", "")
                            except json.JSONDecodeError:
                                st.error(f"Gagal mendapatkan respons dari Ollama")
                    return full_response
                else:
                    st.error("Terjadi kesalahan dalam mendapatkan respons dari Ollama")

        with st.spinner("Memproses..."):
            response = query_ollama(prompt, selected_model)
        
        # Bersihkan respons dari tag <think>
        cleaned_response = clean_response(response)
        
        # Simpan respons Ollama ke riwayat percakapan
        messages.append({"role": "assistant", "content": cleaned_response})
        save_chat_to_session_and_file(st.session_state.chat_history)  # Simpan ke session state dan file sementara
        
        # Tampilkan respons Ollama
        with st.chat_message("assistant"):
            st.markdown(cleaned_response)
