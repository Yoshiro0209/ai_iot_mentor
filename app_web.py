import os
import time
import streamlit as st
from google import genai

# Memuat API Key dari file .env

# Konfigurasi halaman web
st.set_page_config(
    page_title="AI IoT & Python Mentor", page_icon="🤖", layout="centered"
)

if "loaded" not in st.session_state:
  with st.spinner(
    "Initilalizing Neural Core & Establishing Secure Connection..."
  ):
    time.sleep(1.5)
  st.session_state.loaded = True
  st.toast("System Online. Secure Connection Established", icons="🤖")

st.title("🤖 AI IoT & Python Code Mentor")
st.write(
    "Asisten AI pribadi buat bantu kamu debugging kode Python & mikrokontroler"
    " kamu (ESP32/Arduino/ESP8266)"
)


# 1. Inisialisasi Client Gemini (mengambil API key dari environment variable)
try:
  client = genai.Client()
except Exception as e:
  st.error(
      f"❌ Error inisialisasi client: {e}. Pastikan GEMINI_API_KEY sudah benar"
      " di file .env"
  )

# 2. Inisialisasi Session State UNTUK PERTAMA KALI (Paling penting!)
if "messages" not in st.session_state:
  st.session_state.messages = []

# System Instruction
system_instruction = (
    "Kamu adalah AI Senior Embedded Systems & Python Developer yang ahli dalam"
    " C++, Arduino IDE, ESP32, ESP8266, dan Python. Tugasmu adalah membantu"
    " seorang pelajar teknik elektronika untuk mendiagnosis bug, merancang"
    " logika non-blocking (menggunakan millis alih-alih delay), dan"
    " memberikan kode perbaikan (clean code) dengan bahasa Indonesia yang"
    " santai, suportif, dan mudah dipahami."
)

# 3. Tampilkan riwayat obrolan di layar web
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# 4. Kotak input chat di bagian bawah
if user_input := st.chat_input(
    "Tulis pertanyaan atau tempel kodenya di sini..."
):
  # Simpan & tampilkan pesan user
  st.session_state.messages.append({"role": "user", "content": user_input})
  with st.chat_message("user"):
    st.markdown(user_input)

  # Proses AI
  with st.chat_message("assistant"):
    with st.spinner("AI sedang berpikir..."):
      try:
        # Susun riwayat obrolan untuk konteks
        chat_context = ""
        for msg in st.session_state.messages:
          chat_context += f"{msg['role']}: {msg['content']}\n"

        # Panggil Gemini API (Gunakan gemini-2.5-flash)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=chat_context,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.3,
            },
        )

        ai_reply = response.text
        st.markdown(ai_reply)

        # Simpan respons AI ke riwayat
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

      except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil AI: {e}")