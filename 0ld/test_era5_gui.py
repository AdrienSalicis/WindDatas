import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import os
import sys

# Vérifie si cdsapi est dans requirements.txt
def check_requirements():
    if not os.path.exists("requirements.txt"):
        print("[⚠️] Fichier requirements.txt introuvable.")
        return
    with open("requirements.txt", "r") as f:
        lines = f.read().lower()
        if "cdsapi" not in lines:
            print("[❌] Attention : 'cdsapi' n’est pas listé dans requirements.txt.")
        else:
            print("[✅] 'cdsapi' trouvé dans requirements.txt.")

# Lit les sites du fichier modele_sites.csv
def load_sites(csv_path="modele_sites.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError("Fichier modele_sites.csv introuvable.")
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

# Interface pour sélectionner un site et une période
def ask_user_input(sites):
    root = tk.Tk()
    root.title("Test ERA5")

    site_var = tk.StringVar(root)
    site_names = [site["name"] for site in sites]
    site_var.set(site_names[0])

    tk.Label(root, text="Choisissez un site :").pack(pady=5)
    tk.OptionMenu(root, site_var, *site_names).pack()

    tk.Label(root, text="Date de début (YYYY-MM-DD) :").pack(pady=5)
    start_entry = tk.Entry(root)
    start_entry.insert(0, "1979-01-01")
    start_entry.pack()

    tk.Label(root, text="Date de fin (YYYY-MM-DD) :").pack(pady=5)
    end_entry = tk.Entry(root)
    end_entry.insert(0, "1980-01-01")
    end_entry.pack()

    user_input = {}

    def on_confirm():
        user_input["site"] = site_var.get()
        user_input["start"] = start_entry.get()
        user_input["end"] = end_entry.get()
        root.quit()

    tk.Button(root, text="Lancer le test", command=on_confirm).pack(pady=10)
    root.mainloop()
    root.destroy()

    return user_input["site"], user_input["start"], user_input["end"]


# === Intégration de save_era5_data ===
from modules.era5_fetcher import save_era5_data

def main():
    check_requirements()
    try:
        sites = load_sites()
    except Exception as e:
        print(f"[❌] Erreur de chargement des sites : {e}")
        sys.exit(1)

    site_name, start_date, end_date = ask_user_input(sites)
    site = next((s for s in sites if s["name"] == site_name), None)

    if not site:
        print("[❌] Site non trouvé.")
        return

    lat = float(site["latitude"])
    lon = float(site["longitude"])
    folder = os.path.join("data", f"test_era5_{site_name}")
    os.makedirs(folder, exist_ok=True)

    print(f"[ℹ️] Lancement du test ERA5 pour {site_name} ({lat}, {lon})...")

    result = save_era5_data(site_name, folder, lat, lon, start_date, end_date)
    if result:
        messagebox.showinfo("Succès", f"Données ERA5 téléchargées dans :\n{result['filepath']}")
    else:
        messagebox.showerror("Erreur", "Le téléchargement ERA5 a échoué.")

if __name__ == "__main__":
    main()
