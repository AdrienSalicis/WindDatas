# tests/test_noaa_fetcher_paris.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.noaa_isd_fetcher import fetch_isd_series

# === Paramètres de test ===
site_name = "PARIS_Montsouris"
usaf = "071560"
wban = "99999"
years = list(range(2010, 2013))  # ajustable

# === Dossier de sortie
output_dir = os.path.join("data", f"TEST_{site_name}")
os.makedirs(output_dir, exist_ok=True)

# === Lancement du test
print(f"\n📡 Test NOAA ISD – Station {site_name} ({usaf}-{wban})\n")
df_daily = fetch_isd_series(
    usaf=usaf,
    wban=wban,
    years=years,
    output_dir=output_dir,
    site_name=site_name,
    verbose=True
)

# === Résultat
if df_daily is not None and not df_daily.empty:
    print(f"\n✅ Données NOAA ISD récupérées ({len(df_daily)} jours)\n")
    print(df_daily.head())
else:
    print(f"\n[❌] Aucune donnée récupérée pour {site_name}")
