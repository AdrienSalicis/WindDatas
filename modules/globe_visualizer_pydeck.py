import pydeck as pdk
import pandas as pd

def visualize_sites_pydeck(sites_data, output_html_path="globe_pydeck.html"):
    """
    Crée une visualisation globe immersive avec PyDeck en utilisant le style satellite et relief.
    """
    rows = []
    for site in sites_data:
        # Site principal
        rows.append({
            "lon": site["longitude"],
            "lat": site["latitude"],
            "type": "Site",
            "label": f"{site['name']} ({site['country']})",
            "color": [255, 0, 0],
            "size": 50000
        })

        # Stations Meteostat
        for key in ["meteostat1", "meteostat2"]:
            if key in site and site[key]:
                st = site[key]
                label = (
                    f"Meteostat\nID: {st.get('id','N/A')}\nName: {st.get('name','N/A')}\n"
                    f"Dist: {st.get('distance_km','N/A')} km\nElev: {st.get('elevation','N/A')} m\nAnemo: {st.get('anemometer_height','N/A')} m"
                )
                rows.append({
                    "lon": st["longitude"],
                    "lat": st["latitude"],
                    "type": "Meteostat",
                    "label": label,
                    "color": [0, 100, 255],
                    "size": 30000
                })

        # Stations NOAA
        for key in ["noaa1", "noaa2"]:
            if key in site and site[key]:
                st = site[key]
                label = (
                    f"NOAA\nID: {st.get('id','N/A')}\nName: {st.get('name','N/A')}\n"
                    f"Dist: {st.get('distance_km','N/A')} km\nElev: {st.get('elevation','N/A')} m\nAnemo: {st.get('anemometer_height','N/A')} m"
                )
                rows.append({
                    "lon": st["longitude"],
                    "lat": st["latitude"],
                    "type": "NOAA",
                    "label": label,
                    "color": [0, 200, 0],
                    "size": 30000
                })

    df = pd.DataFrame(rows)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='color',
        get_radius='size',
        pickable=True,
        auto_highlight=True,
        get_line_color=[0, 0, 0],
        get_line_width=50,
        opacity=0.9,
        filled=True
    )

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=1.5,
        pitch=45,
        bearing=0
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{label}"},
        map_style='mapbox://styles/mapbox/satellite-streets-v12'
    )

    r.to_html(output_html_path)
    print(f"[✅] Visualisation PyDeck générée : {output_html_path}")
