import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional

from .config import CSV_PATH, OUT_DIR, FIG_DIR, TAB_DIR, COLS, AGE_BINS, AGE_LABELS

# ----------------- tiện ích -----------------
def ensure_dirs():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)

def save_table(df: pd.DataFrame, name: str) -> Path:
    out = TAB_DIR / f"{name}.csv"
    df.to_csv(out, index=False)
    return out

def save_plot(ax, name: str) -> Path:
    fig = ax.get_figure()
    out = FIG_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out

# ----------------- 1) nạp & làm sạch -----------------
def load_raw() -> pd.DataFrame:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Không thấy file CSV tại: {CSV_PATH}")
    # file của bạn có header ở dòng đầu, phân cách bằng dấu phẩy
    return pd.read_csv(CSV_PATH)

def standardize(df: pd.DataFrame) -> pd.DataFrame:
    # đổi tên cột về chuẩn
    rename_map = {}
    for std, raw in COLS.items():
        if raw and raw in df.columns:
            rename_map[raw] = std
    df = df.rename(columns=rename_map)

    # chỉ giữ những cột mình quan tâm nếu có
    keep = [c for c in ["province", "age", "status", "nationality", "patient_code"] if c in df.columns]
    df = df[keep].copy()

    # chuẩn hóa tỉnh/thành
    if "province" in df.columns:
        df["province"] = df["province"].astype(str).str.strip()
        # nhiều giá trị như "Binh Duong" => chuẩn hóa kiểu Title Case
        df["province"] = df["province"].str.title()

    # tuổi & nhóm tuổi
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS, right=True)
    else:
        df["age_group"] = pd.Series(["unknown"] * len(df), dtype="object")

    # tình trạng
    if "status" in df.columns:
        df["status"] = df["status"].astype(str).str.strip().str.lower()

    # quốc tịch
    if "nationality" in df.columns:
        df["nationality"] = df["nationality"].astype(str).str.strip().str.title()

    return df

# ----------------- 2) bảng thống kê -----------------
def t_top_provinces(df: pd.DataFrame, top_n=10) -> pd.DataFrame:
    if "province" not in df.columns: 
        return pd.DataFrame(columns=["province","cases"])
    return (df["province"].value_counts().head(top_n)
            .rename_axis("province").reset_index(name="cases"))

def t_cases_by_age(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("age_group").size()
            .reset_index(name="cases"))

def t_status_overall(df: pd.DataFrame) -> pd.DataFrame:
    if "status" not in df.columns:
        return pd.DataFrame(columns=["status","cases"])
    return df["status"].value_counts().rename_axis("status").reset_index(name="cases")

def t_status_by_age(df: pd.DataFrame) -> pd.DataFrame:
    if not {"age_group","status"}.issubset(df.columns):
        return pd.DataFrame(columns=["age_group","status","cases"])
    return (df.groupby(["age_group","status"]).size()
            .reset_index(name="cases"))

def t_nationality(df: pd.DataFrame, top_n=10) -> pd.DataFrame:
    if "nationality" not in df.columns:
        return pd.DataFrame(columns=["nationality","cases"])
    return (df["nationality"].value_counts().head(top_n)
            .rename_axis("nationality").reset_index(name="cases"))

# ----------------- 3) biểu đồ -----------------
def p_top_provinces(top_df: pd.DataFrame):
    ax = top_df.plot(x="province", y="cases", kind="barh", figsize=(8,6))
    ax.set_title("Top tỉnh/thành có số ca nhiều nhất")
    ax.set_xlabel("Số ca"); ax.set_ylabel("Tỉnh/Thành")
    return save_plot(ax, "top_provinces")

def p_cases_by_age(age_df: pd.DataFrame):
    ax = age_df.plot(x="age_group", y="cases", kind="bar", figsize=(10,5))
    ax.set_title("Phân bố số ca theo nhóm tuổi")
    ax.set_xlabel("Nhóm tuổi"); ax.set_ylabel("Số ca")
    return save_plot(ax, "cases_by_age_group")

def p_status_overall(st_df: pd.DataFrame):
    ax = st_df.plot(x="status", y="cases", kind="bar", figsize=(8,5))
    ax.set_title("Tình trạng ca bệnh (tổng)")
    ax.set_xlabel("Tình trạng"); ax.set_ylabel("Số ca")
    return save_plot(ax, "status_overall")

def p_status_by_age(sbag_df: pd.DataFrame):
    if sbag_df.empty: return None
    pv = sbag_df.pivot(index="age_group", columns="status", values="cases").fillna(0)
    ax = pv.plot(kind="bar", stacked=True, figsize=(10,6))
    ax.set_title("Tình trạng theo nhóm tuổi")
    ax.set_xlabel("Nhóm tuổi"); ax.set_ylabel("Số ca")
    return save_plot(ax, "status_by_age_group")

def p_nationality(nat_df: pd.DataFrame):
    ax = nat_df.plot(x="nationality", y="cases", kind="barh", figsize=(8,6))
    ax.set_title("Top quốc tịch")
    ax.set_xlabel("Số ca"); ax.set_ylabel("Quốc tịch")
    return save_plot(ax, "top_nationality")

# ----------------- 4) pipeline -----------------
def run():
    ensure_dirs()

    raw = load_raw()
    df = standardize(raw)

    # bảng
    toppr = t_top_provinces(df);      save_table(toppr, "top_provinces")
    age   = t_cases_by_age(df);       save_table(age, "cases_by_age_group")
    st    = t_status_overall(df);     save_table(st, "status_overall")
    sbag  = t_status_by_age(df);      save_table(sbag, "status_by_age_group")
    nat   = t_nationality(df);        save_table(nat, "top_nationality")

    # biểu đồ
    figs = [
        p_top_provinces(toppr),
        p_cases_by_age(age),
        p_status_overall(st),
        p_status_by_age(sbag),
        p_nationality(nat),
    ]

    print("Hoàn tất!")
    print(f"- Bảng: {TAB_DIR}")
    print(f"- Hình: {FIG_DIR}")
    for f in figs:
        if f: print("  →", f)

if __name__ == "__main__":
    run()
