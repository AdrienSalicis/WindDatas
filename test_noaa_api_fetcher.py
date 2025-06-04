from modules.noaa_api_fetcher import save_noaa_data_for_site

if __name__ == "__main__":
    site_name = "PIOLENC"
    start_date = "1975-01-01"
    end_date = "2024-12-31"

    # Station 1 (Caritat)
    usaf1 = "075790"
    wban1 = "99999"
    save_noaa_data_for_site(site_name, usaf1, wban1, start_date, end_date, index=1)

    # Station 2 (Carpentras)
    usaf2 = "075860"
    wban2 = "99999"
    save_noaa_data_for_site(site_name, usaf2, wban2, start_date, end_date, index=2)
