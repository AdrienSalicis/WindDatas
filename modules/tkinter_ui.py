import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

def get_date_range_from_user():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Demander les dates de début et de fin
    start_str = simpledialog.askstring("Date de début", "Entrez la date de début (YYYY-MM-DD) :")
    end_str = simpledialog.askstring("Date de fin", "Entrez la date de fin (YYYY-MM-DD) :")

    try:
        # Vérification des formats
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

        if start_date >= end_date:
            raise ValueError("La date de début doit être antérieure à la date de fin.")

        return str(start_date), str(end_date)

    except Exception as e:
        print(f"[❌] Erreur dans les dates : {e}")
        return None, None
