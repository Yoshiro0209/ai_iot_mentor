import os
import time
from dotenv import load_dotenv
from google import genai
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
        "kamu adalah seorang senior python develoer yang sangat berpengalaman di bidangnya"
        "tugas kamu adalah untuk menganalisis kode python yang dikirmkan oleh user, menemukan bug atau error, memberikan kode perbaikan yang sudah dirapikan, dan mejelaskan letak kesalahannya."
        "dengan bahasa indonesia yang santai, singkat tapi to-the-point, dan mudah dipahami oleh kalanagn pelajar."
    )

    print("=" * 50)
    print("🤖 AI PYTHON CODE MENTOR")
    print("=" * 50)
    print("Tulis pertanyaan ata tempelkan potongan kode python yang bermasalah")
    print("ketik 'exit' atau 'keluar' untuk menghentikan Perintah/program.\n")
    chat_history = []

    while True:
        try:
            user_input = input("Kamu: ")

            if user_input.lower() in ["exit", "keluar", "quit"]:
                print(
                    "\n🤖 AI: Sampai jumpa, Thhar! Tetap semangat ngoding python-nya!"
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
                            "temperature": 0.2,
                        },
                    )
                    break  # Jika berhasil, keluar dari loop retry
                except Exception as api_err:
                    if "503" in str(api_err) and attempt < max_retries - 1:
                        print(
                            f"Server lagi sibuk, nih (percobaan {attempt + 1}), mencoba ualng dalam 3 detik..."
                        )
                        time.sleep(3)  # Tunggu 3 detik sebelum mencoba lagi
                    else:
                        raise api_err
            if response:
                ai_reply = response.text
                print(f"AI Python Solver:\n{ai_reply}")
                print("-" * 50)

                chat_history.append(f"User: {user_input}")
                chat_history.append(f"AI: {ai_reply}")

        except KeyboardInterrupt:
            print("\n\n AI: Program dihentikan secara manual oleh pengguna. Sampai ketemu lagi...")
            break
        except Exception as e:
            print(f" Terjadi Kesalahan: {e}\n")

if __name__ == "__main__":
    main()