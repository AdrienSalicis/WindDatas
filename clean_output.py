import os
import shutil
import stat

def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.unlink, os.remove, os.rmdir) and excvalue.errno == 5:
        print(f"[⚠️] Accès refusé. Tentative de forcer la suppression : {path}")
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def clean_all_sites_outputs():
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"[⚠️] Dossier {data_dir} introuvable.")
        return

    sites = [name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))]

    if not sites:
        print("[ℹ️] Aucun site trouvé dans data/.")
        return

    for site_ref in sites:
        base_dir = os.path.join(data_dir, site_ref)
        print(f"\n📌 Nettoyage du site : {site_ref}")

        # 🔹 Suppression des dossiers figures, report, tables
        for sub in ["figures", "report", "tables"]:
            path = os.path.join(base_dir, sub)
            if os.path.exists(path):
                try:
                    print(f"[🧹] Suppression du dossier : {path}")
                    shutil.rmtree(path, onerror=handle_remove_readonly)
                except Exception as e:
                    print(f"[⚠️] Erreur lors de la suppression de {path} : {e}")
            else:
                print(f"[ℹ️] Dossier déjà vide ou inexistant : {path}")

        # 🔹 Suppression des fichiers raw_noaa_station*.csv
        for fname in os.listdir(base_dir):
            if fname.startswith("raw_noaa_station") and fname.endswith(".csv"):
                fpath = os.path.join(base_dir, fname)
                try:
                    os.remove(fpath)
                    print(f"[🗑️] Fichier supprimé : {fpath}")
                except Exception as e:
                    print(f"[⚠️] Erreur lors de la suppression de {fpath} : {e}")

if __name__ == "__main__":
    confirm = input("⚠️ Voulez-vous vraiment nettoyer TOUS les sites ? (o/N) : ").strip().lower()
    if confirm == 'o':
        clean_all_sites_outputs()
    else:
        print("✅ Opération annulée.")
