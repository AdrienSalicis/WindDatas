import os
from docx import Document
from docx.shared import Inches
import pandas as pd

def generate_site_report(site_data, output_folder):
    """
    Génère un rapport DOCX pro par site, incluant :
    - Infos générales
    - Métadonnées des stations
    - Graphiques du notebook
    - Tableaux d'analyses
    """

    site_ref = f"{site_data['reference']}_{site_data['name']}"
    report_dir = os.path.join(output_folder, site_ref, "report")
    figures_dir = os.path.join(output_folder, site_ref, "figures")
    tables_dir = os.path.join(output_folder, site_ref, "tables")

    os.makedirs(report_dir, exist_ok=True)

    doc = Document()
    doc.add_heading(f"Fiche Technique – {site_data['name']}", 0)

    # --- 1️⃣ Infos générales
    doc.add_heading("1️⃣ Informations Générales", level=1)
    doc.add_paragraph(f"Nom du site : {site_data['name']}")
    doc.add_paragraph(f"Pays : {site_data['country']}")
    doc.add_paragraph(f"Latitude : {site_data['latitude']}")
    doc.add_paragraph(f"Longitude : {site_data['longitude']}")
    doc.add_paragraph(f"Période d'étude : {site_data['start']} – {site_data['end']}")

    # --- 2️⃣ Stations associées
    doc.add_heading("2️⃣ Métadonnées des stations associées", level=1)
    for key in ["meteostat1", "meteostat2", "noaa1", "noaa2"]:
        station = site_data.get(key)
        if station:
            doc.add_heading(f"{key.upper()}", level=2)
            for k, v in station.items():
                doc.add_paragraph(f"{k} : {v}")

    # --- 3️⃣ Graphiques Notebook
    doc.add_heading("3️⃣ Graphiques générés", level=1)
    figures_list = sorted([f for f in os.listdir(figures_dir) if f.endswith('.png')])
    for fig in figures_list:
        doc.add_paragraph(fig.replace("_", " ").split(".png")[0])
        doc.add_picture(os.path.join(figures_dir, fig), width=Inches(5.5))

    # --- 4️⃣ Tableaux d'analyses
    doc.add_heading("4️⃣ Tableaux d'analyses", level=1)
    tables_list = sorted([f for f in os.listdir(tables_dir) if f.endswith('.csv')])
    for table in tables_list:
        doc.add_paragraph(table.replace("_", " ").split(".csv")[0])
        df = pd.read_csv(os.path.join(tables_dir, table))
        t = doc.add_table(rows=(len(df)+1), cols=len(df.columns))
        t.style = 'Light Grid Accent 1'
        for j, col in enumerate(df.columns):
            t.cell(0, j).text = col
        for i, row in df.iterrows():
            for j, col in enumerate(df.columns):
                t.cell(i+1, j).text = str(row[col])

    # --- Sauvegarde
    output_docx = os.path.join(report_dir, f"fiche_{site_ref}.docx")
    doc.save(output_docx)
    print(f"[✅] Rapport DOCX généré : {output_docx}")

    return output_docx
