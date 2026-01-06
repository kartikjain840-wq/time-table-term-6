import pandas as pd
import streamlit as st

# ---- LOAD DATA ----
# If you want to use another file, change the path or add a file uploader.
FILE_PATH = "/mnt/data/Term6_Full_Class_Schedule_CORRECTED.csv"
df = pd.read_csv(FILE_PATH)

# Normalize column names (edit if yours differ)
df.columns = [c.strip().lower() for c in df.columns]

required_cols = ["date", "day", "subject", "start time", "end time", "location"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

st.set_page_config(page_title="Timetable", layout="wide")

# ---- HEADER ----
st.title("Timetable Dashboard")

# ---- SUBJECT FILTER ----
subjects = sorted(df["subject"].dropna().unique())
selected = st.multiselect("Select subjects", subjects)

filtered = df[df["subject"].isin(selected)] if selected else df.copy()
filtered = filtered.sort_values(["date", "start time"])

# ---- STYLING ----
def style_table(d):
    return (
        d.style
        .set_properties(**{
            "background-color": "#ffffff",
            "border-color": "#e5e7eb",
            "border-width": "1px",
            "border-style": "solid",
            "padding": "6px"
        })
        .set_table_styles([
            {"selector": "thead th",
             "props": [("background-color", "#f3f4f6"),
                       ("font-weight", "600"),
                       ("text-align", "left"),
                       ("border-bottom", "2px solid #d1d5db")]}
        ])
        .hide_index()
    )

st.subheader("Schedule")
st.write(style_table(filtered), unsafe_allow_html=True)

# ---- DOWNLOAD ----
csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download timetable (CSV)",
    csv_bytes,
    "timetable.csv",
    "text/csv",
)

st.caption("Select subjects to filter. Download when ready.")
