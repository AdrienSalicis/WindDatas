# cleanup_old_noaa_files.py

import os
import re

def delete_old_noaa_files(data_folder="data"):
    """
    Supprime les fichiers NOAA ISD anciens (nommés noaa_isd_<site>_<station>.csv)
    conservés depuis une ancienne version du fetcher.
    """
    print("[🧹] Recherche des fichiers NOAA ISD anciens à supprimer...")
    pattern = re.compile(r"noaa_isd_[^_]+_\d+\.csv")

    count = 0
    for root, _, files in os.walk(data_folder):
        for file in files:
            if pattern.match(file):
                full_path = os.path.join(root, file)
                os.remove(full_path)
                print(f"[✅] Supprimé : {full_path}")
                count += 1

    if count == 0:
        print("[ℹ️] Aucun fichier ancien à supprimer.")
    else:
        print(f"[✔] {count} fichiers supprimés.")

if __name__ == "__main__":
    delete_old_noaa_files()