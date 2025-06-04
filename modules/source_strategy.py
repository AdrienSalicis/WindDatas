def determine_sources(site_info):
    country = site_info.get("country", "").upper()

    sources = {
        "observed": [],
        "modeled": ["openmeteo", "nasa_power", "era5"] # sans "visualcrossing". Fetcher  présent dans modules/ (limitations plan gratuit de l'API)
    }

    if country in ["US", "USA"]:
        sources["observed"] = ["noaa"]
    elif country in ["FR", "FRANCE", "DE", "GERMANY", "ES", "SPAIN", "IT", "ITALY", "UK", "UNITED KINGDOM", "NL", "BE", "LU"]:
        sources["observed"] = ["meteostat"]
    else:
        sources["observed"] = ["meteostat"]

    return sources

