# test_noaa_isd_fetcher_PARIS.py

from modules.noaa_isd_fetcher import fetch_isd_series

# 🔧 Informations de la station Paris Montsouris
station_name = "PARIS_Montsouris"
usaf = "071560"
wban = "99999"
years = list(range(2000, 2024))  # à ajuster selon la période souhaitée
output_dir = f"data/{station_name}"

print(f"\n📡 Traitement de la station {usaf}-{wban} pour {station_name}\n")

# 📥 Téléchargement et traitement des données horaires NOAA ISD
df = fetch_isd_series(usaf, wban, years, output_dir, site_name=station_name, verbose=True)

# ✅ Résultat
if df is not None and not df.empty:
    print(f"\n✅ Données NOAA ISD récupérées avec succès pour {station_name}")
    print(df.head())
else:
    print(f"\n[⚠️] Aucune donnée disponible pour la station {station_name}")
