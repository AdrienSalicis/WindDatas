import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_wind_direction_distribution(site_name, output_path, bin_size=15, **datasets):
    """
    Trace un graphique radar comparant la fréquence des directions du vent pour plusieurs sources.
    Chaque source est représentée comme une couche de distribution (rose superposée).
    """
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    bins = np.arange(0, 360 + bin_size, bin_size)
    colors = plt.cm.tab10.colors  # Jusqu'à 10 sources

    for i, (source_name, df) in enumerate(datasets.items()):
        if df is None or df.empty:
            continue
        if 'wind_direction' not in df.columns:
            continue

        dir_data = df['wind_direction'].dropna()
        if dir_data.empty:
            continue

        hist, _ = np.histogram(dir_data, bins=bins)
        theta = np.deg2rad((bins[:-1] + bins[1:]) / 2)  # Milieu de chaque secteur
        values = hist / hist.sum()  # Fréquence normalisée (0–1)

        ax.plot(theta, values, label=source_name, color=colors[i % len(colors)])
        ax.fill(theta, values, alpha=0.3, color=colors[i % len(colors)])

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title(f"Distribution des directions du vent – {site_name}", fontsize=13)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_rlabel_position(135)
    ax.set_yticklabels([])

    filepath = os.path.join(output_path, f"wind_direction_distribution_{site_name}.png")
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"[✅] Distribution directionnelle enregistrée : {filepath}")
    return filepath
