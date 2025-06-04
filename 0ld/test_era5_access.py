# Test rapide pour ERA5-Land
import cdsapi

def test_era5land_download():
    try:
        print("[🔍] Test de connexion Copernicus et téléchargement ERA5-Land simplifié...")

        c = cdsapi.Client()

        c.retrieve(
            'reanalysis-era5-land',
            {
                'product_type': 'reanalysis',
                'variable': [
                    '10m_u_component_of_wind',
                    '10m_v_component_of_wind'
                ],
                'year': '2020',
                'month': '01',
                'day': '01',
                'time': ['00:00', '06:00', '12:00', '18:00'],
                'area': [40.0, -105.0, 39.75, -104.75],
                'format': 'netcdf'
            },
            'era5land_test_output.nc'
        )

        print("[✅] Téléchargement ERA5-Land réussi ! Fichier : era5land_test_output.nc")

    except Exception as e:
        print(f"[❌] Erreur pendant le test ERA5-Land : {e}")

if __name__ == "__main__":
    test_era5land_download()

