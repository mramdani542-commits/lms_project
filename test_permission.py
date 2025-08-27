import os
from pathlib import Path

# Skrip ini akan meniru apa yang Django coba lakukan: menulis file ke folder media.

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TEST_FILE_PATH = os.path.join(MEDIA_ROOT, 'test.txt')

print(f"Mencoba menulis file ke: {TEST_FILE_PATH}")

try:
    # Pertama, pastikan folder 'media' memang ada
    if not os.path.exists(MEDIA_ROOT):
        print(f"\n!!! ERROR: Folder 'media' tidak ditemukan di '{MEDIA_ROOT}'")
        print("!!! Pastikan Anda sudah membuat folder 'media' di sebelah file manage.py")
    else:
        # Coba buka file dalam mode tulis ('w') dan buat filenya
        with open(TEST_FILE_PATH, 'w') as f:
            f.write('Jika file ini ada, maka izin folder sudah benar.')
        
        print("\n===============================================")
        print(">>> SUKSES! File 'test.txt' berhasil dibuat di dalam folder media.")
        print(">>> Ini membuktikan TIDAK ADA masalah izin folder.")
        print("===============================================")

except PermissionError:
    print("\n==============================================================")
    print(">>> GAGAL: PermissionError!")
    print(">>> Ini 100% membuktikan ada MASALAH IZIN FOLDER.")
    print(">>> Python/Django tidak diizinkan oleh Windows untuk menyimpan file di sana.")
    print(">>> Silakan periksa kembali langkah-langkah 'Security Properties' pada folder media.")
    print("==============================================================")

except Exception as e:
    print(f"\n>>> GAGAL dengan error tak terduga: {e}")