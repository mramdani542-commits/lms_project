import os
import django
import json
from django.core.serializers import serialize

# --- Konfigurasi Django ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_project.settings")  # ganti dengan nama projectmu
django.setup()

from django.apps import apps

def export_clean_data():
    data = {}
    for model in apps.get_models():
        try:
            # Serialize semua data di tabel model ini
            serialized = serialize("json", model.objects.all())
            
            # Parse ke Python dict lalu bersihkan karakter rusak
            parsed = json.loads(serialized)
            clean_data = json.dumps(parsed, indent=2, ensure_ascii=False)

            # Simpan ke dictionary dengan nama model
            data[model.__name__] = parsed
            print(f"✅ Berhasil export {model.__name__}, total {len(parsed)} records")

        except Exception as e:
            print(f"⚠️ Gagal export {model.__name__}: {e}")

    # Simpan hasil ke file JSON
    with open("database_dump.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\n🎉 Export selesai! File tersimpan di database_dump.json")

if __name__ == "__main__":
    export_clean_data()
