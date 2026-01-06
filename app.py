import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Timetable", layout="wide")
st.title("Timetable Dashboard")

DATA = """
date,day,subject,start time,end time,location
2026-01-05,Monday,Math,09:00,10:00,Room 101
2026-01-05,Monday,Physics,10:00,11:00,Room 202
2026-01-06,Tuesday,Chemistry,09:00,10:00,Lab 1
2026-01-06,Tuesday,Biology,11:00,12:00,Room 220
"""

df = pd.read_csv(StringIO(DATA))
df.columns = [c.strip().lower() for c in df.columns]

subjects = sorted(df["subject"].dropna().unique())
selected = st.multiselect("Select subjects", subjects)

filtered = df[df["subject"].isin(selected)] if selected else df.copy()
filtered = filtered.sort_values(["date", "start time"])

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
             "props": [
                 ("background-color", "#f3f4f6"),
                 ("font-weight", "600"),
                 ("text-align", "left"),
                 ("border-bottom", "2px solid #d1d5db")
             ]}
        ])
        .hide_index()
    )

st.subheader("Schedule")
st.write(style_table(filtered), unsafe_allow_html=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download timetable (CSV)",
    csv_bytes,
    "timetable.csv",
    "text/csv",
)

st.caption("Pick subjects. View timetable. Download.")
