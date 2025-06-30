import os

def nettoyer_openmeteo_files(root_folder="data"):
    print(f"[🧹] Nettoyage des fichiers OpenMeteo dans {root_folder}")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().startswith("openmeteo_") and filename.lower().endswith(".csv"):
                full_path = os.path.join(dirpath, filename)
                try:
                    os.remove(full_path)
                    print(f"[✅] Supprimé : {full_path}")
                except Exception as e:
                    print(f"[⚠️] Erreur suppression {full_path} : {e}")

if __name__ == "__main__":
    nettoyer_openmeteo_files()
