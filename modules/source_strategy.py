# source_strategy.py
# Définit une stratégie conditionnelle d'utilisation des sources météo par localisation ou qualité

def determine_sources(country):
    """
    Détermine dynamiquement les sources à utiliser en fonction du pays.
    Renvoie une liste de sources météo à activer (observées + modélisées).
    """
    country = country.lower()
    observed = []
    modeled = []

    if country == "france":
        observed = ["meteofrance", "meteostat"]
        modeled = ["era5", "openmeteo", "nasa_power"]
    elif country == "united states" or country == "usa":
        observed = ["noaa", "meteostat"]
        modeled = ["era5", "openmeteo", "nasa_power"]
    else:
        observed = ["meteostat"]
        modeled = ["era5", "openmeteo", "nasa_power"]

    return {
        "observed": observed,
        "modeled": modeled
    }
