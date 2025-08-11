import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path
import pandas as pd
pd.set_option("styler.render.max_elements", 1_000_000)  # hoặc số lớn hơn df_f.size

# ---- config (import works both: `python -m src.app` and `python src/app.py`) ----
try:
    from .config import CSV_PATH, COLS, AGE_BINS, AGE_LABELS
except Exception:
    from config import CSV_PATH, COLS, AGE_BINS, AGE_LABELS

ASSETS_CSS = Path(__file__).resolve().parent / "assets" / "styles.css"

# ---------------- helpers ----------------
def load_css(path: Path):
    if path.exists():
        st.markdown(f"<style>{path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

@st.cache_data
def load_raw(path_or_file):
    return pd.read_csv(path_or_file)

def standardize(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {raw: std for std, raw in COLS.items() if raw in df.columns}
    df = df.rename(columns=rename_map)

    keep = [c for c in ["province", "age", "status", "nationality", "patient_code"] if c in df.columns]
    df = df[keep].copy()

    if "province" in df:
        df["province"] = df["province"].astype(str).str.strip().str.title()
    if "age" in df:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS, right=True)
    else:
        df["age_group"] = pd.Series(["unknown"] * len(df), dtype="object")
    if "status" in df:
        df["status"] = df["status"].astype(str).str.strip().str.lower()
    if "nationality" in df:
        df["nationality"] = df["nationality"].astype(str).str.strip().str.title()
    return df

def pivot_counts(df: pd.DataFrame, index, col=None):
    if col is None:
        return (df.groupby(index).size()
                .reset_index(name="cases")
                .sort_values("cases", ascending=False))
    t = df.groupby([index, col]).size().reset_index(name="cases")
    return t.pivot(index=index, columns=col, values="cases").fillna(0).astype(int)

def card(title: str):
    st.markdown(f"<div class='cv-card'><h3>{title}</h3>", unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

def style_table(df: pd.DataFrame):
    return (df.style
            .hide(axis="index")
            .format(thousands=",")
            .set_table_styles([
                {"selector": "thead th", "props": "font-weight:700;"},
                {"selector": "tbody td", "props": "padding:8px 10px;"},
            ]))

def add_grid(ax):
    ax.grid(alpha=.3, linestyle="--", linewidth=.6, axis="y")

# ---------------- UI ----------------
st.set_page_config(page_title="COVID VN — Dashboard", layout="wide")
load_css(ASSETS_CSS)

st.title("COVID VN — Dashboard")

# Sidebar — data source & filters
source = st.sidebar.radio("Data source", ["Project file", "Upload CSV"], index=0)
if source == "Project file":
    csv_src = CSV_PATH
else:
    uploaded = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if not uploaded:
        st.stop()
    csv_src = uploaded

raw = load_raw(csv_src)
df = standardize(raw)

st.sidebar.markdown("---")
prov_opts = ["(All)"] + sorted(df["province"].dropna().unique().tolist()) if "province" in df else ["(All)"]
status_opts = ["(All)"] + sorted(df["status"].dropna().unique().tolist()) if "status" in df else ["(All)"]
nat_opts = ["(All)"] + sorted(df["nationality"].dropna().unique().tolist()) if "nationality" in df else ["(All)"]

f_prov = st.sidebar.selectbox("Province/City", prov_opts, index=0)
f_status = st.sidebar.selectbox("Case status", status_opts, index=0)
f_nat = st.sidebar.selectbox("Nationality", nat_opts, index=0)

mask = pd.Series(True, index=df.index)
if "province" in df and f_prov != "(All)":
    mask &= (df["province"] == f_prov)
if "status" in df and f_status != "(All)":
    mask &= (df["status"] == f_status)
if "nationality" in df and f_nat != "(All)":
    mask &= (df["nationality"] == f_nat)
df_f = df[mask].copy()

# Tabs
tab_overview, tab_charts, tab_table = st.tabs(["📊 Overview", "📈 Charts", "🧾 Data"])

# ---------- Overview ----------
with tab_overview:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='cv-kpi'><div class='label'>Total records</div>"
            f"<div class='value'>{len(df_f):,}</div></div>", unsafe_allow_html=True
        )
    with c2:
        common_status = (df_f["status"].value_counts().idxmax()
                         if "status" in df_f and not df_f.empty else "—")
        st.markdown(
            f"<div class='cv-kpi'><div class='label'>Most common status</div>"
            f"<div class='value'>{common_status}</div></div>", unsafe_allow_html=True
        )
    with c3:
        median_age = int(df_f["age"].median()) if "age" in df_f and df_f["age"].notna().any() else 0
        st.markdown(
            f"<div class='cv-kpi'><div class='label'>Median age</div>"
            f"<div class='value'>{median_age}</div></div>", unsafe_allow_html=True
        )

    card("Quick breakdowns")
    colA, colB, colC = st.columns(3)
    with colA:
        if "province" in df_f:
            top_prov = pivot_counts(df_f, "province").head(10)
            st.write("Top provinces/cities by cases")
            st.dataframe(style_table(top_prov), use_container_width=True)
    with colB:
        if "age_group" in df_f:
            age_tbl = pivot_counts(df_f, "age_group")
            st.write("Cases by age group")
            st.dataframe(style_table(age_tbl), use_container_width=True)
    with colC:
        if "status" in df_f:
            st_tbl = pivot_counts(df_f, "status")
            st.write("Cases by status")
            st.dataframe(style_table(st_tbl), use_container_width=True)
    card_end()

# ---------- Charts ----------
with tab_charts:
    # === Row 1: two charts side-by-side ===
    c1, c2 = st.columns(2, gap="large")

    with c1:
        card("Top provinces/cities")
        top_prov = pivot_counts(df_f, "province").head(15)
        fig1, ax1 = plt.subplots(figsize=(6,4))           # nhỏ lại để nằm vừa cột
        ax1.barh(top_prov["province"], top_prov["cases"])
        ax1.set_xlabel("Cases"); ax1.set_ylabel("Province/City")
        ax1.invert_yaxis(); add_grid(ax1)
        st.pyplot(fig1, use_container_width=True)
        card_end()

    with c2:
        card("Age-group distribution")
        age_tbl = pivot_counts(df_f, "age_group")
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.bar(age_tbl["age_group"].astype(str), age_tbl["cases"])
        ax2.set_xlabel("Age group"); ax2.set_ylabel("Cases")
        add_grid(ax2)
        st.pyplot(fig2, use_container_width=True)
        card_end()

    # === Row 2: các chart còn lại (nếu muốn cũng cho hai cột) ===
    if "status" in df_f:
        c3, c4 = st.columns(2, gap="large")

        with c3:
            card("Overall status")
            st_tbl = pivot_counts(df_f, "status")
            fig3, ax3 = plt.subplots(figsize=(6,4))
            ax3.bar(st_tbl["status"], st_tbl["cases"])
            ax3.set_xlabel("Status"); ax3.set_ylabel("Cases")
            add_grid(ax3)
            st.pyplot(fig3, use_container_width=True)
            card_end()

        with c4:
            card("Status by age group")
            pv = pivot_counts(df_f, "age_group", "status")
            pv_num = pv.apply(pd.to_numeric, errors="coerce").fillna(0)
            st.dataframe(pv_num.reset_index(), use_container_width=True)
            fig4, ax4 = plt.subplots(figsize=(6,4))
            pv_num.plot(kind="bar", stacked=True, ax=ax4)
            ax4.set_xlabel("Age group"); ax4.set_ylabel("Cases")
            add_grid(ax4)
            st.pyplot(fig4, use_container_width=True)
            card_end()


# ---------- Data table ----------
with tab_table:
    card("Filtered dataset")
    st.dataframe(style_table(df_f), use_container_width=True)
    csv_bytes = df_f.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", data=csv_bytes, file_name="filtered_patients.csv", mime="text/csv")
    card_end()

# EOF
