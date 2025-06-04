import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import radians
import warnings

warnings.filterwarnings("ignore")

# Nom du site à analyser
site_name = "Piolenc"
base_path = os.path.join("data", site_name.replace(" ", "_"))
comp_path = os.path.join(base_path, "comparaison")
os.makedirs(comp_path, exist_ok=True)

# Chargement des fichiers CSV
meteostat_file = os.path.join(base_path, f"meteostat_{site_name}.csv")
openmeteo_file = os.path.join(base_path, f"openmeteo_{site_name}.csv")

if not os.path.exists(meteostat_file):
    print(f"[❌] Fichier Meteostat introuvable pour {site_name}")
    exit()

if not os.path.exists(openmeteo_file):
    print(f"[⚠️] Fichier OpenMeteo manquant pour {site_name}. Analyse partielle.")
    full_comparison = False
else:
    full_comparison = True

# Chargement des données
df_meteo = pd.read_csv(meteostat_file, parse_dates=["date"])
df_meteo.rename(columns={
    "wind_speed": "speed_meteostat",
    "wind_gust": "gust_meteostat",
    "wind_direction": "dir_meteostat"
}, inplace=True)

if full_comparison:
    df_open = pd.read_csv(openmeteo_file, parse_dates=["date"])
    df_open.rename(columns={
        "wind_speed_mean": "speed_openmeteo",
        "wind_speed_max": "gust_openmeteo",
        "wind_direction_dominant": "dir_openmeteo"
    }, inplace=True)

    # Fusion sur les dates communes
    df = pd.merge(df_meteo, df_open, on="date", how="inner")
else:
    df = df_meteo.copy()

# Sauvegarde des statistiques
def compute_stats(col1, col2):
    diff = np.abs(df[col1] - df[col2])
    return {
        "mean_1": df[col1].mean(),
        "mean_2": df[col2].mean(),
        "std_1": df[col1].std(),
        "std_2": df[col2].std(),
        "min_1": df[col1].min(),
        "min_2": df[col2].min(),
        "max_1": df[col1].max(),
        "max_2": df[col2].max(),
        "mean_absolute_diff": diff.mean()
    }

stats = {}

if full_comparison:
    stats["wind_speed"] = compute_stats("speed_meteostat", "speed_openmeteo")
    stats["wind_gust"] = compute_stats("gust_meteostat", "gust_openmeteo")
    stats["wind_dir"] = compute_stats("dir_meteostat", "dir_openmeteo")

    pd.DataFrame(stats).T.to_csv(os.path.join(comp_path, "stats_comparaison.csv"))
    print(f"[✅] Statistiques sauvegardées dans stats_comparaison.csv")
else:
    print(f"[ℹ️] Statistiques seulement sur Meteostat (pas de comparaison)")

# 📈 Graphe comparatif des vitesses moyennes
if full_comparison:
    plt.figure(figsize=(14, 5))
    plt.plot(df["date"], df["speed_meteostat"], label="Meteostat", color="blue")
    plt.plot(df["date"], df["speed_openmeteo"], label="OpenMeteo", color="orange", alpha=0.7)
    plt.title(f"{site_name} - Vitesse moyenne du vent")
    plt.xlabel("Date")
    plt.ylabel("Vitesse (m/s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(comp_path, "vitesse_moyenne_comparaison.png"))
    plt.close()
    print(f"[📊] Graphe de vitesses moyennes enregistré.")

# 🧭 Radar chart pour les directions moyennes (si dispo)
def plot_wind_direction_radar():
    mean_dir_open = df["dir_openmeteo"].mean()
    mean_dir_meteo = df["dir_meteostat"].mean()

    labels = np.array(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    values_meteo = [0]*8
    values_open = [0]*8

    # Bins (0-45 = N, 45-90 = NE, etc.)
    for d in df["dir_meteostat"].dropna():
        idx = int((d % 360) // 45)
        values_meteo[idx] += 1

    for d in df["dir_openmeteo"].dropna():
        idx = int((d % 360) // 45)
        values_open[idx] += 1

    values_meteo += values_meteo[:1]
    values_open += values_open[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.plot(angles, values_meteo, color='blue', label='Meteostat')
    ax.fill(angles, values_meteo, color='blue', alpha=0.25)

    ax.plot(angles, values_open, color='orange', label='OpenMeteo')
    ax.fill(angles, values_open, color='orange', alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title(f"{site_name} - Direction moyenne du vent (radar)")
    ax.legend(loc='upper right')
    plt.savefig(os.path.join(comp_path, "radar_direction_vent.png"))
    plt.close()
    print(f"[🧭] Radar chart des directions sauvegardé.")

if full_comparison:
    plot_wind_direction_radar()

print(f"\n🎉 Comparaison terminée pour {site_name}.")
