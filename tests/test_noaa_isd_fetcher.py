import os
from modules.noaa_isd_fetcher import fetch_isd_series

# 🔧 Paramètres du site
site_name = "PIOLENC"

# 🔧 Informations de la station NOAA (exemple station1)
station1 = {
    "station_id": "075790-99999",
    "usaf": "075790",
    "wban": "99999",
    "years_available": list(range(1975, 2025))
}

# 📁 Dossier de sortie
output_dir = os.path.join("data", site_name)
os.makedirs(output_dir, exist_ok=True)

# 🚀 Lancement du téléchargement et traitement
print(f"\n📡 Traitement de station1 ({station1['station_id']}) pour {site_name}")
df = fetch_isd_series(
    site_name=site_name,
    usaf=station1["usaf"],
    wban=station1["wban"],
    years=station1["years_available"],
    output_dir=output_dir,
    verbose=True
)

# 💾 Sauvegarde des données
if not df.empty:
    output_path = os.path.join(output_dir, f"noaa_station1_{site_name}.csv")
    df.to_csv(output_path, index=False)
    print(f"[✅] Données sauvegardées : {output_path}")
else:
    print("[⚠️] Aucune donnée récupérée pour la station.")
