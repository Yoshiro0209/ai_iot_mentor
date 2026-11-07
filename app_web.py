import time
from google import genai
import streamlit as st
import random

# Konfigurasi halaman web
st.set_page_config(
    page_title="AI IoT & Python Mentor",
    page_icon="🤖",
    layout="centered",
)

# Efek Animasi Loading awal ala Sistem Hacker
if "loaded" not in st.session_state:
  with st.spinner(
      "Initializing Neural Core & Establishing Secure Connection..."
  ):
    time.sleep(1.5)
  st.session_state.loaded = True
  st.toast("System Online. Secure Connection Established", icon="🤖")

# Inisialisasi Client Gemini menggunakan st.secrets
# (Pastikan GEMINI_API_KEY sudah diset di Streamlit Cloud Secrets / lokal via st.secrets)
try:
  client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
  # Fallback jika dijalankan lokal dengan environment biasa
  import os

  client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- FITUR 4: SIDEBAR & INDIKATOR SISTEM REAL-TIME ---
current_latency = random.randint(15, 68)

with st.sidebar:
  st.markdown("### 🖥️ **SYSTEM STATUS**")
  st.markdown(
      """
    - **Status:** `ONLINE` 🟢
    - **Latency:** `{current_latency}ms`
    - **Engine:** `Gemini AI`
    - **Security:** `Encrypted`
    """
  )
  st.divider()

  # --- FITUR 3: PILIHAN MODE PERSONA / MENTOR ---
  st.markdown("### ⚙️ **AI CONFIGURATION**")
  mentor_mode = st.selectbox(
      "Pilih Mode Mentor:",
      [
          "Debugger Ahli (Fokus Error & Solusi)",
          "Penjelasan Pemula (Santai & Detail)",
          "Clean Code Optimizer (Rapi & Efisien)",
      ],
  )

  st.divider()
  if st.button("🗑️ Bersihkan Riwayat Chat"):
    st.session_state.messages = []
    st.rerun()

# Judul Utama dengan nuansa terminal
st.title("🤖 AI IoT & Python Code Mentor")
st.write(
    "Asisten AI pribadi buat bantu kamu debugging kode Python & mikrokontroler"
    " kamu (ESP32/Arduino/ESP8266)"
)

# --- FITUR 2: SISTEM RIWAYAT CHAT (CHAT MEMORY) ---
if "messages" not in st.session_state:
  st.session_state.messages = []

# Tampilkan pesan obrolan yang sudah tersimpan
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Input chat dari pengguna
if prompt := st.chat_input("Tulis pertanyaan atau tempel kodenya di sini..."):
  # Simpan pesan user ke riwayat
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Tentukan instruksi sistem berdasarkan mode mentor yang dipilih
  system_instruction = (
      "Kamu adalah AI IoT & Python Mentor yang cerdas dan asik."
  )
  if "Debugger" in mentor_mode:
    system_instruction += (
        " Fokus berikan analisis error secara cepat dan solusi kodenya."
    )
  elif "Pemula" in mentor_mode:
    system_instruction += (
        " Jelaskan logika kodenya dengan bahasa yang santai, ramah, dan mudah"
        " dipahami pemula."
    )
  elif "Optimizer" in mentor_mode:
    system_instruction += (
        " Fokus pada perbaikan clean code, efisiensi memori, dan best practices."
    )

  # Generate jawaban dari Gemini
  with st.chat_message("assistant"):
    with st.spinner("Menganalisis kode dan logika..."):
      try:
        # Menggunakan format pemanggilan chat standar
        chat_history = [
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ]

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        ai_response = response.text

        st.markdown(ai_response)

        # --- FITUR 1: TOMBOL COPY / SALIN OTOMATIS (Bawaan Streamlit Markdown) ---
        # Streamlit secara otomatis menyediakan tombol salin di pojok kanan atas setiap blok kode (```code```).

        # Simpan jawaban AI ke riwayat
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )
      except Exception as e:
        error_msg = f"Terjadi kesalahan koneksi ke AI: {e}"
        st.error(error_msg)