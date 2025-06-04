import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from modules.nasa_power_fetcher import fetch_nasa_power_data
import pandas as pd

def get_date_range_from_user():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    start_str = simpledialog.askstring("Date de début", "Entrez la date de début (YYYY-MM-DD) :")
    end_str = simpledialog.askstring("Date de fin", "Entrez la date de fin (YYYY-MM-DD) :")

    try:
        from datetime import datetime
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

        if start_date >= end_date:
            raise ValueError("La date de début doit être antérieure à la date de fin.")

        return str(start_date), str(end_date)
    except Exception as e:
        messagebox.showerror("Erreur", f"Format de dates incorrect : {e}")
        return None, None

def download_power_with_tkinter():
    start_date, end_date = get_date_range_from_user()
    if not start_date or not end_date:
        return

    site_name = "TestDenver"
    site_folder = os.path.join("data", site_name)
    latitude = 39.7392
    longitude = -104.9903

    try:
        print("[🚀] Récupération des données journalières principales...")
        result_main = fetch_nasa_power_data(
            site_name=site_name,
            site_folder=site_folder,
            lat=latitude,
            lon=longitude,
            start_date=start_date,
            end_date=end_date
        )

        messagebox.showinfo("Succès", f"Fichier créé :\n{result_main['filepath']}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur pendant le téléchargement :\n{e}")

if __name__ == "__main__":
    download_power_with_tkinter()