import numpy as np
import pandas as pd

def compute_wind_stats(df1, df2, label1, label2, threshold=15):
    stats = {}

    # Vérification présence colonnes
    col1 = 'windspeed_gust' if 'windspeed_gust' in df1.columns else 'windspeed_mean'
    col2 = 'windspeed_gust' if 'windspeed_gust' in df2.columns else 'windspeed_mean'

    if col1 not in df1.columns or col2 not in df2.columns:
        print(f"[⚠️] Colonnes manquantes : {col1} ou {col2} ({label1} vs {label2})")
        return {}, pd.DataFrame()

    df1_renamed = df1[['time', col1]].rename(columns={col1: label1})
    df2_renamed = df2[['time', col2]].rename(columns={col2: label2})
    merged = pd.merge(df1_renamed, df2_renamed, on="time")

    if merged.empty:
        print(f"[⚠️] Aucune correspondance temporelle entre {label1} et {label2}")
        return {}, pd.DataFrame()

    stats.update({
        'comparison': f"{label1} vs {label2}",
        f"mean_{label1}": round(merged[label1].mean(), 3),
        f"mean_{label2}": round(merged[label2].mean(), 3),
        'mean_diff': round(merged[label2].mean() - merged[label1].mean(), 3),
        'mae': round((merged[label1] - merged[label2]).abs().mean(), 3),
        'correlation': round(merged[label1].corr(merged[label2]), 3),
        f"std_{label1}": round(merged[label1].std(), 3),
        f"std_{label2}": round(merged[label2].std(), 3),
        f"max_{label1}": round(merged[label1].max(), 3),
        f"max_{label2}": round(merged[label2].max(), 3),
        f"min_{label1}": round(merged[label1].min(), 3),
        f"min_{label2}": round(merged[label2].min(), 3),
        'count': merged.shape[0],
        f"extreme_days_{label1}": int((merged[label1] > threshold).sum()),
        f"extreme_days_{label2}": int((merged[label2] > threshold).sum())
    })

    for df, label in zip([df1, df2], [label1, label2]):
        for col in ['wind_direction', 'wind_dir', 'winddirection_10m']:
            if col in df.columns:
                dir_mean = np.nanmean(df[col])
                stats[f"mean_dir_{label}"] = round(dir_mean, 2)
                break

    if f"mean_dir_{label1}" in stats and f"mean_dir_{label2}" in stats:
        d1 = stats[f"mean_dir_{label1}"]
        d2 = stats[f"mean_dir_{label2}"]
        stats['dir_diff_abs'] = round(abs(d1 - d2), 2)

    return stats, merged
