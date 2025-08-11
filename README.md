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

1. [Project Motivation](#project-motivation)
2. [Installation](#installation)
3. [File Descriptions](#file-descriptions)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing-authors-and-acknowledgements)
## Project Motivation
<div align="justify">

</div>

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



## File Descriptions
<div align="justify">
# Project Files — Overview

The project folder **COVID_VN** contains the core source files and assets required to run the Vietnam COVID-19 Case Explorer. Below is an overview of each main component:

1. **src/web_app.py**  
   Main Streamlit application. Defines layout (tabs, cards, 2-column chart grid), filters (province, status, nationality), charts (top provinces, age distribution, status overall/stacked), CSV download, and loads external CSS.
2. **src/config.py**  
   Central configuration: data path (`CSV_PATH`), raw→standardized column mapping (`COLS`), age bins/labels. Update this file if your CSV uses different column names.
3. **src/assets/styles.css**  
   Custom stylesheet for the app (cards, KPIs, tables, container width). Safe to tweak colors/spacing without touching Python code.
4. **requirements.txt**  
   Python dependencies: `pandas`, `numpy`, `matplotlib`, `python-dateutil`, `streamlit`.
5. **README.md**  
   Installation and run instructions, project structure, troubleshooting, and deployment notes.
6. **data/patients.csv** *(user-provided; not committed)*  
   Input dataset. Expected raw columns: `_id, ID, Patient, Age, Location, Status, Nationality`. Place the file here or upload via the app.

7. **.gitignore**  
   Excludes `.venv/`, `__pycache__/`, `out/`, and `data/*.csv` to avoid committing large or sensitive data.
</div>

## Result

## Licensing, Authors, and Acknowledgements
We would like to thank the following sources and tools that made this project possible:

<p align="justify">
  Data on Covid-19 cases in Vietnam from <a href="https://github.com/highcharts/map-collection-dist/blob/master/countries/vn/vn-all.topo.json?short_path=881c496"></a>
</p>






