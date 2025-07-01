import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
from scipy.stats import weibull_min, gumbel_r

def generate_analysis_for_site(site_ref):
    print(f"\n📌 [ANALYSE] Traitement du site : {site_ref}")
    data_folder = os.path.join("data", site_ref)
    figures_folder = os.path.join(data_folder, "figures")
    tables_folder = os.path.join(data_folder, "tables")

    os.makedirs(figures_folder, exist_ok=True)
    os.makedirs(tables_folder, exist_ok=True)

    # 1️⃣ Chargement de tous les CSV sauf raw_
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv") and not f.startswith("raw_")]
    all_data = {}
    for filename in csv_files:
        path = os.path.join(data_folder, filename)
        try:
            df = pd.read_csv(path)
            if not df.empty:
                key = filename.replace(f"_{site_ref}.csv", "")
                all_data[key] = df
                print(f"[✅] Chargé : {filename}")
            else:
                print(f"[⚠️] Fichier vide ignoré : {filename}")
        except Exception as e:
            print(f"[❌] Erreur lecture {filename} : {e}")

    if not all_data:
        print("[⚠️] Aucun CSV valide trouvé, analyse interrompue.")
        return

    # 2️⃣ Statistiques descriptives avancées
    stats_rows = []
    for source, df in all_data.items():
        for col in df.columns:
            if 'wind' in col and df[col].dtype in [np.float64, np.float32, np.int64]:
                s = df[col].dropna()
                if not s.empty:
                    stats_rows.append({
                        "Site": site_ref,
                        "Source": source,
                        "Variable": col,
                        "Count": s.count(),
                        "Mean": round(s.mean(), 3),
                        "Median": round(s.median(), 3),
                        "Std": round(s.std(), 3),
                        "Min": round(s.min(), 3),
                        "Max": round(s.max(), 3),
                        "P90": round(s.quantile(0.90), 3),
                        "P95": round(s.quantile(0.95), 3),
                        "P99": round(s.quantile(0.99), 3)
                    })

    if stats_rows:
        stats_df = pd.DataFrame(stats_rows)
        stats_path = os.path.join(tables_folder, f"stats_descriptives_{site_ref}.csv")
        stats_df.to_csv(stats_path, index=False)
        print(f"[💾] Statistiques sauvegardées : {stats_path}")
    else:
        print("[⚠️] Aucune statistique calculable.")

    # 3️⃣ Plots pour chaque source
    for source, df in all_data.items():
        wind_cols = [c for c in df.columns if 'wind' in c]
        if not wind_cols:
            continue

        # Histogrammes avec KDE
        for col in wind_cols:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[col].dropna(), bins=30, kde=True, color="steelblue")
            plt.title(f"Histogramme et KDE - {source} - {col}")
            plt.xlabel("Valeur (m/s)")
            plt.ylabel("Fréquence")
            plt.grid()
            path = os.path.join(figures_folder, f"hist_{col}_{source}.png")
            plt.savefig(path, bbox_inches='tight')
            plt.close()

        # Boxplot des colonnes de vent
        plt.figure(figsize=(8, 5))
        df[wind_cols].boxplot()
        plt.title(f"Boxplot - {source}")
        plt.ylabel("Valeur (m/s)")
        plt.xticks(rotation=45)
        plt.grid()
        path = os.path.join(figures_folder, f"boxplot_{source}.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()

        # Séries temporelles
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors='coerce')
            for col in wind_cols:
                plt.figure(figsize=(12, 5))
                plt.plot(df["date"], df[col], color="darkorange")
                plt.title(f"Série temporelle - {source} - {col}")
                plt.xlabel("Date")
                plt.ylabel(col)
                plt.grid()
                path = os.path.join(figures_folder, f"timeseries_{col}_{source}.png")
                plt.savefig(path, bbox_inches='tight')
                plt.close()

        # Rose des vents si direction disponible
        if "wind_direction" in df.columns and "windspeed_mean" in df.columns:
            try:
                ax = WindroseAxes.from_ax()
                ax.bar(df["wind_direction"], df["windspeed_mean"], normed=True, opening=0.8, edgecolor='white')
                ax.set_title(f"Rose des vents – {source}")
                ax.set_legend()
                path = os.path.join(figures_folder, f"rose_{source}.png")
                plt.savefig(path, bbox_inches='tight')
                plt.close()
            except Exception as e:
                print(f"[⚠️] Erreur génération rose des vents pour {source} : {e}")

        # Ajustements de lois si variable windspeeds disponibles
        for col in wind_cols:
            s = df[col].dropna()
            if len(s) > 50:
                try:
                    plt.figure(figsize=(8, 5))
                    sns.histplot(s, bins=30, kde=False, color='lightgrey', stat='density', edgecolor='black')
                    # Weibull
                    c, loc, scale = weibull_min.fit(s, floc=0)
                    x = np.linspace(s.min(), s.max(), 100)
                    plt.plot(x, weibull_min.pdf(x, c, loc, scale), 'b-', label=f"Weibull c={c:.2f}, scale={scale:.2f}")
                    # Gumbel
                    loc_g, scale_g = gumbel_r.fit(s)
                    plt.plot(x, gumbel_r.pdf(x, loc_g, scale_g), 'orange', label=f"Gumbel loc={loc_g:.2f}, scale={scale_g:.2f}")
                    plt.title(f"Ajustement de lois – {source} ({col})")
                    plt.xlabel("Vitesse (m/s)")
                    plt.ylabel("Densité de probabilité")
                    plt.legend()
                    plt.grid()
                    path = os.path.join(figures_folder, f"fit_{col}_{source}.png")
                    plt.savefig(path, bbox_inches='tight')
                    plt.close()
                except Exception as e:
                    print(f"[⚠️] Erreur ajustement lois pour {source} - {col} : {e}")

    print(f"\n✅ Analyse complète pour {site_ref}. Résultats sauvegardés dans figures/ et tables/")
