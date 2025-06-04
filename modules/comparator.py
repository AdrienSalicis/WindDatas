# modules/comparator.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modules.stats_calculator import compute_wind_stats
from modules.merger import merge_datasets

def load_wind_data(filepath):
    df = pd.read_csv(filepath)
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'])
    elif 'date' in df.columns:
        df = df.rename(columns={'date': 'time'})
        df['time'] = pd.to_datetime(df['time'])
    else:
        raise Exception("Colonne 'time' ou 'date' manquante dans le fichier.")
    return df

def radar_plot_direction_means(site_name, output_folder, **datasets):
    angles = []
    values = []
    labels = []

    for name, df in datasets.items():
        if df is None or df.empty:
            continue
        for col in ['wind_direction', 'wind_dir', 'winddirection_10m']:
            if col in df.columns:
                avg = np.nanmean(df[col])
                values.append(avg)
                labels.append(name)
                break

    if not values:
        return None

    angles_rad = np.linspace(0, 2 * np.pi, len(values), endpoint=False).tolist()
    angles_rad.append(angles_rad[0])
    values.append(values[0])
    labels.append(labels[0])

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles_rad, values, marker='o')
    ax.fill(angles_rad, values, alpha=0.25)
    ax.set_xticks(angles_rad[:-1])
    ax.set_xticklabels(labels[:-1])
    ax.set_title(f"Direction moyenne du vent – {site_name}")

    radar_path = os.path.join(output_folder, f"wind_direction_radar_{site_name}.png")
    plt.savefig(radar_path)
    plt.close()
    return radar_path

def generate_comparison_report(site_name, site_folder, files_dict):
    print(f"[🔍] Analyse comparative pour {site_name}...")
    sources = {}
    for key in files_dict:
        try:
            sources[key] = load_wind_data(files_dict[key])
        except Exception as e:
            print(f"[❌] Erreur lecture {key} : {e}")

    available = list(sources.keys())
    if len(available) < 2:
        print("[⚠️] Pas assez de sources disponibles pour comparaison.")
        return None

    results = []
    already_done = set()

    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            s1 = available[i]
            s2 = available[j]
            if (s1, s2) in already_done or (s2, s1) in already_done:
                continue

            df1 = sources[s1]
            df2 = sources[s2]
            stats, _ = compute_wind_stats(df1, df2, s1, s2)
            if stats:
                results.append(stats)
                already_done.add((s1, s2))

    if not results:
        print("[⚠️] Aucune comparaison valide.")
        return None

    stats_df = pd.DataFrame(results)
    stats_path = os.path.join(site_folder, f'statistics_comparison_{site_name}.csv')
    stats_df.to_csv(stats_path, index=False)
    print(f"[✅] Rapport statistique : {stats_path}")
    return stats_path
