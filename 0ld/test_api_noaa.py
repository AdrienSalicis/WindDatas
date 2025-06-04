
import os
import pandas as pd
from tkinter import Tk, simpledialog, messagebox, Text, Scrollbar, Toplevel, END, RIGHT, Y
from modules.noaa_api_fetcher import fetch_noaa_api_data  # adapte si besoin

# Interface pour saisir les dates
root = Tk()
root.withdraw()

start_date = simpledialog.askstring("Date de début", "Entrez la date de début (YYYY-MM-DD) :")
end_date = simpledialog.askstring("Date de fin", "Entrez la date de fin (YYYY-MM-DD) :")

# Fenêtre de log déroulante
log_window = Toplevel()
log_window.title("📋 Journal NOAA")
log_text = Text(log_window, wrap="word", height=30, width=100)
log_text.pack(side="left", fill="both", expand=True)
scrollbar = Scrollbar(log_window, command=log_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
log_text.config(yscrollcommand=scrollbar.set)

def log(msg):
    log_text.insert(END, msg + "\n")
    log_text.see(END)
    log_window.update()

# Chargement des sites
sites_df = pd.read_csv("modele_sites.csv")  # adapte le chemin si nécessaire
output_dir = "noaa_test_outputs_gui"
os.makedirs(output_dir, exist_ok=True)

success, failure = [], []

for _, row in sites_df.iterrows():
    name = row["name"]
    station_id = row.get("noaa_id", "")
    if pd.isna(station_id) or station_id.strip() == "":
        log(f"[⏭️] Station NOAA absente pour {name}, on passe.")
        continue

    log(f"\n[🚀] Téléchargement des données NOAA pour {name} – {station_id}")
    folder = os.path.join(output_dir, name)
    result = fetch_noaa_api_data(name, folder, station_id, start_date, end_date)

    if result:
        log(f"[✅] {name} – {result['rows']} jours récupérés\n→ {result['filepath']}")
        success.append(name)
    else:
        log(f"[❌] Échec pour {name}")
        failure.append(name)

# Résumé final
message = f"✅ Succès : {len(success)} sites\n❌ Échecs : {len(failure)} sites"
if failure:
    message += "\n\nSites en échec :\n" + "\n".join(failure)

messagebox.showinfo("Résultat final", message)
log("\n🎉 Traitement terminé.")
root.mainloop()
