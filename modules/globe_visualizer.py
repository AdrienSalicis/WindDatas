import plotly.graph_objects as go

def visualize_sites_plotly(sites_data, output_html_path="globe_plotly.html"):
    """
    Génère une visualisation globe interactive Plotly des sites et de leurs stations associées.
    """

    # Points accumulés
    lats_sites, lons_sites, texts_sites = [], [], []
    lats_meteostat, lons_meteostat, texts_meteostat = [], [], []
    lats_noaa, lons_noaa, texts_noaa = [], [], []

    for site in sites_data:
        # Point du site
        lats_sites.append(site["latitude"])
        lons_sites.append(site["longitude"])
        texts_sites.append(
            f"<b>Site</b>: {site['name']} ({site['country']})<br>"
            f"Lat: {site['latitude']:.4f}, Lon: {site['longitude']:.4f}"
        )

        # Stations Meteostat
        for key in ["meteostat1", "meteostat2"]:
            if key in site and site[key]:
                st = site[key]
                lats_meteostat.append(st["latitude"])
                lons_meteostat.append(st["longitude"])
                texts_meteostat.append(
                    f"<b>Meteostat</b><br>ID: {st['id']}<br>Name: {st['name']}<br>"
                    f"Distance: {st['distance_km']} km<br>"
                    f"Elevation: {st['elevation']} m<br>"
                    f"Anemometer: {st['anemometer_height']} m"
                )

        # Stations NOAA
        for key in ["noaa1", "noaa2"]:
            if key in site and site[key]:
                st = site[key]
                lats_noaa.append(st["latitude"])
                lons_noaa.append(st["longitude"])
                texts_noaa.append(
                    f"<b>NOAA</b><br>ID: {st['id']}<br>Name: {st['name']}<br>"
                    f"Distance: {st['distance_km']} km<br>"
                    f"Elevation: {st['elevation']} m<br>"
                    f"Anemometer: {st['anemometer_height']} m"
                )

    # === Figure Plotly
    fig = go.Figure()

    # Site principal
    fig.add_trace(go.Scattergeo(
        lat=lats_sites,
        lon=lons_sites,
        mode='markers+text',
        text=texts_sites,
        marker=dict(size=10, color='red', symbol='star'),
        name='Sites étudiés'
    ))

    # Meteostat
    fig.add_trace(go.Scattergeo(
        lat=lats_meteostat,
        lon=lons_meteostat,
        mode='markers',
        text=texts_meteostat,
        marker=dict(size=7, color='blue', symbol='circle'),
        name='Stations Meteostat'
    ))

    # NOAA
    fig.add_trace(go.Scattergeo(
        lat=lats_noaa,
        lon=lons_noaa,
        mode='markers',
        text=texts_noaa,
        marker=dict(size=7, color='green', symbol='square'),
        name='Stations NOAA'
    ))

    # Mise en page
    fig.update_geos(
        projection_type="orthographic",
        showland=True,
        landcolor="rgb(230, 230, 230)",
        showocean=True,
        oceancolor="rgb(180, 220, 255)",
        showcountries=True,
        countrycolor="rgb(100, 100, 100)",
        showlakes=True,
        lakecolor="rgb(200, 200, 255)"
    )

    fig.update_layout(
        title=dict(
            text="Carte interactive – Sites et Stations Météo",
            x=0.5,
            font=dict(size=20)
        ),
        legend=dict(
            yanchor="bottom",
            y=0.01,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="gray",
            borderwidth=1
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    fig.write_html(output_html_path)
    print(f"[✅] Visualisation Plotly générée : {output_html_path}")
