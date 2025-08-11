from pathlib import Path

# thư mục gốc dự án
ROOT = Path(__file__).resolve().parents[1]

# ---- chỉnh nếu tên file khác ----
CSV_PATH = ROOT / "data" / "patients.csv"

# ánh xạ cột trong CSV -> tên chuẩn
# (không có cột giới tính và ngày, nên để None với "sex" và bỏ "date_reported")
COLS = {
    "province": "Location",     # Tỉnh/Thành
    "age": "Age",               # Tuổi
    "status": "Status",         # Tình trạng (Active/Recovered/Deceased...)
    "nationality": "Nationality",
    "patient_code": "Patient",  # Mã bệnh nhân (BNxxxx) — dùng để đếm nếu cần
}

# thư mục xuất
OUT_DIR = ROOT / "out"
FIG_DIR = OUT_DIR / "figures"
TAB_DIR = OUT_DIR / "tables"

# nhóm tuổi
AGE_BINS = [0, 9, 19, 29, 39, 49, 59, 69, 79, float("inf")]
AGE_LABELS = ["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]
