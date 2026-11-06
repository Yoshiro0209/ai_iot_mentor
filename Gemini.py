import argparse
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# Memuat konfigurasi dari file .env
load_dotenv()


def get_language_name(file_extension):
  """Fungsi untuk memetakan ekstensi file ke nama bahasa pemrograman"""
  mapping = {
      ".py": "Python",
      ".js": "JavaScript",
      ".ts": "TypeScript",
      ".cpp": "C++",
      ".ino": "Arduino (C++)",
      ".c": "C",
      ".html": "HTML",
      ".css": "CSS",
      ".java": "Java",
      ".json": "JSON",
      ".sh": "Bash Shell Script",
  }
  return mapping.get(file_extension.lower(), "Kode / Teks Umum")


def save_report_to_markdown(file_path, detected_language, ai_response_text):
  """Fungsi baru untuk menyimpan hasil review ke dalam file .md otomatis"""
  # Membuat folder 'reports' jika belum ada
  os.makedirs("reports", exist_ok=True)

  # Menyiapkan nama file laporan berdasarkan nama file asli dan waktu
  base_name = os.path.basename(file_path)
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  report_filename = f"reports/review_{base_name}_{timestamp}.md"

  # Menyusun format isi file Markdown
  markdown_content = f"""# Laporan AI Code Review

- **File yang Direview:** `{file_path}`
- **Bahasa Pemrograman:** `{detected_language}`
- **Waktu Analisis:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`

---

## 🤖 Hasil Analisis
{ai_response_text}
"""

  # Menulis ke file
  try:
    with open(report_filename, "w", encoding="utf-8") as f:
      f.write(markdown_content)
    print(f"\n📁 Laporan berhasil disimpan otomatis ke: `{report_filename}`")
  except Exception as e:
    print(f"❌ Gagal menyimpan laporan: {e}")


def review_code(file_path):
  if not os.path.exists(file_path):
    print(f"❌ Error: File '{file_path}' tidak ditemukan!")
    return

  _, ext = os.path.splitext(file_path)
  detected_language = get_language_name(ext)

  try:
    with open(file_path, "r", encoding="utf-8") as f:
      code_content = f.read()
  except Exception as e:
    print(f"❌ Error saat membaca file: {e}")
    return

  try:
    client = genai.Client()
  except Exception as e:
    print(
        "❌ Error inisialisasi client. Pastikan GEMINI_API_KEY sudah diisi"
        " dengan benar di file .env"
    )
    return

  system_instruction = (
      "Kamu adalah seorang Senior Software Engineer yang teliti, ramah, handal"
      " dan suportif. Tugasmu adalah menganalisis kode yang dikirimkan,"
      " mendeteksi potensi bug, memberikan saran optimasi yang sesuai dengan"
      " standar bahasa pemrograman tersebut, dan menjelaskan cara kerjanya"
      " dengan bahasa Indonesia yang santai dan mudah dipahami oleh orang yang baru belajar atau menyelam di dunia koding."
  )

  prompt = f"""
    Tolong review kode berikut ini:
    
    - **File:** {file_path}
    - **Bahasa Pemrograman Terdeteksi:** {detected_language}
    
    ```
    {code_content}
    ```
    
    Berikan analisis dengan format rapi seperti berikut:
    1. **Ringkasan Fungsi:** Apa fungsi utama dari kode ini.
    2. **Analisis & Potensi Bug:** Apakah ada bagian yang rawan error, *best practices* yang terlewat, atau kurang efektif untuk bahasa {detected_language}.
    3. **Saran Perbaikan:** Cara membuat kode ini lebih bersih, aman, atau optimal.
    """

  print(
      f"🔍 Mendeteksi bahasa: `{detected_language}`"
      f" ({ext if ext else 'tanpa ekstensi'})"
  )
  print(
      f"🔍 Sedang menganalisis file `{file_path}` menggunakan AI... Mohon"
      " tunggu sebentar.\n"
  )

  try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.3,
        },
    )

    print("=" * 40)
    print(f"🤖 HASIL REVIEW AI ({detected_language})")
    print("=" * 40)
    print(response.text)
    print("=" * 40)

    # Memanggil fungsi simpan otomatis
    save_report_to_markdown(file_path, detected_language, response.text)

  except Exception as e:
    print(f"❌ Terjadi kesalahan saat memanggil API: {e}")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Smart CLI Code Reviewer dengan Auto-Save Markdown"
  )
  parser.add_argument("file", help="Path ke file kode yang ingin direview")
  args = parser.parse_args()

  review_code(args.file)