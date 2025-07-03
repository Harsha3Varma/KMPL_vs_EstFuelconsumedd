# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ——— Page config —————————————————————————————
st.set_page_config(
    page_title="Vehicle Fuel Efficiency Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚗 KMPL vs Estimated Fuel Consumed Explorer")
st.markdown(
    """
    Enter a **Vehicle Number** to see how its fuel consumption (Est_fuel_Consumed) 
    varies with kilometers‑per‑liter (Last_Tnx_Kmpl).
    """
)

# ——— Load & clean data ——————————————————————————
@st.cache_data
def load_data(path="task1.xlsx"):
    df = pd.read_excel(path)
    # ensure numeric
    df["Est_fuel_Consumed"] = pd.to_numeric(df["Est_fuel_Consumed"], errors="coerce")
    df["Last_Tnx_Kmpl"]    = pd.to_numeric(df["Last_Tnx_Kmpl"], errors="coerce")
    return df.dropna(subset=["Vehicle_no", "Est_fuel_Consumed", "Last_Tnx_Kmpl"])

df = load_data()

# ——— Sidebar input ————————————————————————————
vehicle = st.sidebar.text_input("Vehicle Number", "").strip().upper()

if vehicle:
    vdf = df[df["Vehicle_no"].str.upper() == vehicle]
    if vdf.empty:
        st.error(f"No records found for vehicle **{vehicle}**.")
    else:
        # optional: sort by Created_date if present
        if "Created_date" in vdf.columns:
            vdf["Created_date"] = pd.to_datetime(vdf["Created_date"], errors="coerce")
            vdf = vdf.sort_values("Created_date")

        # ——— Build interactive chart ——————————————————
        fig = px.line(
            vdf,
            x="Last_Tnx_Kmpl",
            y="Est_fuel_Consumed",
            markers=True,
            title=f"Vehicle {vehicle}: KMPL vs Estimated Fuel Consumed",
            labels={
                "Last_Tnx_Kmpl": "Last Transaction (KMPL)",
                "Est_fuel_Consumed": "Estimated Fuel Consumed"
            },
            hover_data={
                "Last_Tnx_Kmpl": ":.2f",
                "Est_fuel_Consumed": ":.2f"
            }
        )
        fig.update_layout(
            hovermode="closest",
            margin=dict(l=40, r=40, t=80, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

        # show raw data table
        st.subheader("Underlying Data")
        st.dataframe(vdf[[
            "Vehicle_no", "Last_Tnx_Kmpl", "Est_fuel_Consumed", "Created_date"
        ]].reset_index(drop=True))
else:
    st.info("🔎 Enter a vehicle number in the sidebar to get started.")
