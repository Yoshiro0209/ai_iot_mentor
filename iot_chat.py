import os
import time
from dotenv import load_dotenv
from google import genai

# Memuat API Key dari file .env
load_dotenv()


def main():
  try:
    client = genai.Client()
  except Exception as e:
    print(
        "❌ Error inisialisasi client. Pastikan GEMINI_API_KEY sudah diisi"
        " dengan benar di file .env"
    )
    return

  system_instruction = (
      "Kamu adalah AI Senior Embedded Systems Engineer yang ahli dalam C++,"
      " Arduino IDE, ESP32, ESP8266, dan protokol IoT (seperti MQTT, HTTP, Blynk,"
      " atau Wokwi). Tugasmu adalah membantu seorang pelajar teknik elektronika"
      " untuk mendiagnosis bug, merancang logika non-blocking (menggunakan millis"
      " alih-alih delay), dan memberikan saran wiring sensor yang aman dengan"
      " bahasa Indonesia yang santai, suportif, dan mudah dipahami."
  )

  print("=" * 50)
  print("🤖 AI IOT CODE MENTOR (ESP32 / ESP8266 / Arduino)")
  print("=" * 50)
  print("Ketikkan 'exit' atau 'keluar' untuk menghentikan program.\n")

  chat_history = []

  while True:
    try:
      user_input = input("Kamu: ")

      if user_input.lower() in ["exit", "keluar", "quit"]:
        print(
            "\n🤖 AI: Sampai jumpa, Thhar! Tetap semangat ngoding ESP32-nya!"
            " 👋"
        )
        break

      if not user_input.strip():
        continue

      print("⏳ AI Sedang Berpikir, Bentar ya....")

      current_prompt = (
          f"Riwayat obrolan:\n{chat_history}\n\nPertanyaan baru: {user_input}"
      )

      # Mekanisme Retry Otomatis jika terjadi error 503 / Sibuk
      max_retries = 3
      response = None

      for attempt in range(max_retries):
        try:
          response = client.models.generate_content(
              model="gemini-3.5-flash",
              contents=current_prompt,
              config={
                  "system_instruction": system_instruction,
                  "temperature": 0.4,
              },
          )
          break  # Kalau berhasil, keluar dari perulangan retry
        except Exception as api_err:
          if "503" in str(api_err) and attempt < max_retries - 1:
            print(
                f"⚠️ Server sedang sibuk (Percobaan {attempt + 1}), mencoba"
                " ulang dalam 3 detik..."
            )
            time.sleep(3)
          else:
            raise api_err  # Kalau error lain atau sudah 3x gagal, lempar errornya

      if response:
        ai_reply = response.text
        print(f"\n🤖 AI Mentor:\n{ai_reply}")
        print("-" * 50)

        chat_history.append(f"User: {user_input}")
        chat_history.append(f"AI: {ai_reply}")

    except KeyboardInterrupt:
      print(
          "\n\n🤖 AI: Program dihentikan secara manual. Selamat beristirahat,"
          " Thhar!"
      )
      break
    except Exception as e:
      print(f"\n❌ Terjadi kesalahan: {e}\n")


if __name__ == "__main__":
  main()