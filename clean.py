# clean.py — Nettoyage des fichiers NOAA (raw + finaux)

import os
import glob

def clean_noaa_files(data_dir="data"):
    print("🔍 Recherche et suppression des fichiers NOAA...")

    patterns = [
        "noaa_station1_*.csv",
        "noaa_station2_*.csv",
        "raw_noaa_station1_*.csv",
        "raw_noaa_station2_*.csv",
    ]

    deleted_files = []

    for pattern in patterns:
        search_path = os.path.join(data_dir, "*", pattern)
        for filepath in glob.glob(search_path):
            try:
                os.remove(filepath)
                deleted_files.append(filepath)
            except Exception as e:
                print(f"⚠️ Erreur lors de la suppression de {filepath} : {e}")

    print(f"🧹 {len(deleted_files)} fichier(s) supprimé(s).")
    for f in deleted_files:
        print("   -", f)

if __name__ == "__main__":
    clean_noaa_files()
