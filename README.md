<p align="center">
  <img src="src/assets/img/covid.png" alt="Banner" width="900" height="250"/>
</p>

<p align="center">
  <strong>Analysis of COVID-19 patient data in Vietnam.</strong>
</p>

<p align="center">
 Visualize COVID-19 case data in Vietnam by province, status, nationality and age group.
</p>

<p align="center">
  <a href="https://data.vietnam.opendevelopmentmekong.net/dataset/the-information-of-patients-infected-by-corona-virus-in-vietnam/resource/fbd07911-b72a-4bc4-8249-affb38a371be"><strong>Data on Covid-19 cases in Vietnam</strong></a>
</p>


## Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#project-motivation)
3. [File Descriptions](#file-descriptions)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing-authors-and-acknowledgements)

## Installation 
### 1. Project Structure
```text
covid-vn/
├─ data/
│  └─ patients.csv            # your CSV
├─ src/
│  ├─ app.py                  # Streamlit app (English UI)
│  ├─ config.py               # paths & column mapping
│  └─ assets/
│     └─ styles.css           # app styles
├─ .streamlit/
│  └─ config.toml             # (optional) Streamlit theme
└─ requirements.txt
```

### 2. Setup
Windows (PowerShell)
```bash
cd <project-folder>
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
macOS / Linux
```bash
cd <project-folder>
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### 3. Data & Config

Put your CSV at: data/patients.csv.
Expected raw columns (from source dataset):
_id, ID, Patient, Age, Location, Status, Nationality.

Map raw → standardized columns in src/config.py:

```bash
CSV_PATH = ROOT / "data" / "patients.csv"
COLS = {
    "province": "Location",
    "age": "Age",
    "status": "Status",
    "nationality": "Nationality",
    "patient_code": "Patient",
}
# Age bins/labels are defined here too.
```


### 4. Run
```bash
streamlit run src/app.py
If the default port is busy:
streamlit run src/app.py --server.port 8502
```
Hard refresh in the browser if needed (Ctrl/Cmd + F5).

## Project Motivation
<div align="justify">
The rapid digital transformation in Vietnam has positioned ICT adoption among SMEs as a national priority, recognised by key strategies such as the National Digital Transformation Program to 2025, orientation to 2030. However, many local enterprises still face challenges in effectively utilising digital technologies, resulting in uneven ICT adoption and productivity gaps across provinces and enterprise sizes.

This project aims to analyse the current landscape of ICT adoption and productivity among Vietnamese SMEs through an interactive dashboard. By visualising technology usage rates across provinces, enterprise scales (micro, small, medium, large), and comparing key performance indicators such as productivity, the project supports:

Policymakers in identifying digital transformation bottlenecks;

Businesses in benchmarking their ICT maturity level;

Researchers and consultants in evaluating the impact of ICT on SME performance.

The dashboard leverages official datasets and data visualisation tools to make complex information accessible and actionable. With a focus on regional disparities and enterprise segmentation, the project offers data-driven insights to guide targeted support policies, enhance SME competitiveness, and accelerate Vietnam’s digital economy.
</div>

## File Descriptions
<div align="justify">
The project folder SME_DASHBOARD contains all source files, data, and assets needed to run the Vietnam SME ICT Dashboard. Below is an overview of each component:

1. app.py
Main Python script for launching the Dash web application. It defines the dashboard layout, callbacks for interactivity, data filtering logic, and visualisations (map, bar chart, etc.).

2. README.md
This documentation file explains the installation process, project background, and usage instructions for users or contributors.

2. sme_data.csv
Preprocessed dataset combining SME ICT adoption indicators and productivity metrics by province, year, and enterprise size.

4. vn_provinces.geojson
GeoJSON file containing the geographical boundaries of all provinces in Vietnam. Used to generate the interactive choropleth map.

5. venv/
Auto-generated Python virtual environment (when using python -m venv). Contains installed dependencies like dash, pandas, geopandas, etc.
</div>

## Result
https://private-user-images.githubusercontent.com/77290046/473861087-33aff68f-1e1b-48a6-98a4-4b02b6fe5125.mp4?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQyODExNzMsIm5iZiI6MTc1NDI4MDg3MywicGF0aCI6Ii83NzI5MDA0Ni80NzM4NjEwODctMzNhZmY2OGYtMWUxYi00OGE2LTk4YTQtNGIwMmI2ZmU1MTI1Lm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODA0VDA0MTQzM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTJhMDNkYzg4ZWUxZjFiNzRkYTRjNzhhNmMzYjM2YWVkOTc5NzVmMzRjMjM4NWNkNzczZWZlOGFmNTNiMzhmNmImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.NAJjHIroxmaGulNMQRtlFc9-pfCf1pNM1uI6Ikz7rTg

## Licensing, Authors, and Acknowledgements
<div align="justify">
We would like to thank the following sources and tools that made this project possible:

Vietnam GSO and Ministry of Information and Communications (MIC) for providing access to open SME datasets.
<p align="justify">
  GeoJSON Vietnam provinces shapefile from <a href="https://github.com/highcharts/map-collection-dist/blob/master/countries/vn/vn-all.topo.json?short_path=881c496"></a>
</p>
Dash by Plotly – A powerful Python framework for building web-based data applications.

Pandas, Plotly Express, and Geopandas – For efficient data processing and visualisation.

The open-source community for continuous contributions and shared knowledge.

Special thanks to all reviewers and mentors who provided feedback during the dashboard development.

</div>





