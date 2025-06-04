from era5_fetcher import save_era5_data

def main():
    site_name = "test_site"
    output_folder = "test_output/test_site"
    lat, lon = 44.25, 4.75
    start_date = "1975-01-01"
    end_date = "1975-01-05"

    result = save_era5_data(site_name, output_folder, lat, lon, start_date, end_date)
    if result:
        print(f"\n✅ Fichier CSV généré : {result['filepath']}")
        import pandas as pd
        df = pd.read_csv(result["filepath"])
        print(df.head())

if __name__ == "__main__":
    main()
