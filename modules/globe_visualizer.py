
import plotly.graph_objects as go

def visualize_sites_on_globe(sites_data, output_html_path):
    lats_sites, lons_sites, texts_sites = [], [], []
    lats_ms1, lons_ms1, texts_ms1 = [], [], []
    lats_ms2, lons_ms2, texts_ms2 = [], [], []
    lats_om, lons_om, texts_om = [], [], []

    for site in sites_data:
        lats_sites.append(site["latitude"])
        lons_sites.append(site["longitude"])
        texts_sites.append(f"Site: {site['name']} ({site['country']})")

        ms1 = site["meteostat1"]
        lats_ms1.append(ms1["latitude"])
        lons_ms1.append(ms1["longitude"])
        texts_ms1.append(f"Meteostat 1: {ms1['name']} ({ms1['id']})\nDistance: {ms1['distance_km']:.2f} km")

        ms2 = site["meteostat2"]
        lats_ms2.append(ms2["latitude"])
        lons_ms2.append(ms2["longitude"])
        texts_ms2.append(f"Meteostat 2: {ms2['name']} ({ms2['id']})\nDistance: {ms2['distance_km']:.2f} km")

        lats_om.append(site["latitude"])
        lons_om.append(site["longitude"])
        texts_om.append("OpenMeteo – données API")

    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lat=lats_sites, lon=lons_sites, text=texts_sites, mode='markers',
        marker=dict(size=5, color='red'), name='Sites étudiés'))

    fig.add_trace(go.Scattergeo(
        lat=lats_ms1, lon=lons_ms1, text=texts_ms1, mode='markers',
        marker=dict(size=4, color='blue'), name='Meteostat 1'))

    fig.add_trace(go.Scattergeo(
        lat=lats_ms2, lon=lons_ms2, text=texts_ms2, mode='markers',
        marker=dict(size=4, color='green'), name='Meteostat 2'))

    fig.add_trace(go.Scattergeo(
        lat=lats_om, lon=lons_om, text=texts_om, mode='markers',
        marker=dict(size=3, color='purple'), name='OpenMeteo'))

    fig.update_layout(
        title='🌐 Visualisation interactive des sites et stations météo',
        geo=dict(projection_type='orthographic', showland=True, landcolor="rgb(250, 250, 250)",
                 showocean=True, oceancolor="rgb(200, 230, 255)", showcountries=True,
                 lataxis_showgrid=True, lonaxis_showgrid=True),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig.write_html(output_html_path)
    return output_html_path
