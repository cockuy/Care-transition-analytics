import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.write(
    "A beginner-friendly dashboard that explores daily CBP custody, "
    "transfers to HHS care, children in HHS care, and discharges."
)
st.info(
    "This dashboard describes reported aggregate counts. The ratios are simple "
    "indicators, not individual waiting times, causal findings, or measures of "
    "the quality of a child's placement."
)

# Load the CSV placed next to this Python file.
DATA_FILE = Path(__file__).with_name("HHS_Unaccompanied_Alien_Children_Program.csv")

COLUMN_MAP = {
    "Date": "Date",
    "Children apprehended and placed in CBP custody*": "Apprehended",
    "Children in CBP custody": "CBP_Custody",
    "Children transferred out of CBP custody": "Transferred",
    "Children in HHS Care": "HHS_Care",
    "Children discharged from HHS Care": "Discharged"
}

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data = data.rename(columns=COLUMN_MAP)

    # Convert dates and numbers. Remove commas from values such as "2,484".
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    number_columns = [
        "Apprehended", "CBP_Custody", "Transferred",
        "HHS_Care", "Discharged"
    ]
    for column in number_columns:
        data[column] = pd.to_numeric(
            data[column].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )

    # Remove rows where all six fields are empty.
    data = data.dropna(how="all").copy()

    # Remove rows without a usable date; sort chronologically.
    data = data.dropna(subset=["Date"])
    data = data.sort_values("Date").reset_index(drop=True)

    # Add simple descriptive ratios. These are not literal processing speeds.
    data["Transfer Ratio (%)"] = (
        data["Transferred"] / data["CBP_Custody"].replace(0, pd.NA) * 100
    )
    data["Discharge Ratio (%)"] = (
        data["Discharged"] / data["HHS_Care"].replace(0, pd.NA) * 100
    )
    data["Daily Balance"] = data["Apprehended"] - data["Discharged"]

    return data

if not DATA_FILE.exists():
    st.error(
        "Dataset not found. Put HHS_Unaccompanied_Alien_Children_Program.csv "
        "in the same folder as app.py."
    )
    st.stop()

df = load_data(DATA_FILE)

if df.empty:
    st.error("No valid dated records were found in the CSV.")
    st.stop()

st.sidebar.header("Dashboard filters")
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Choose reporting date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ].copy()
else:
    filtered = df.copy()

if filtered.empty:
    st.warning("There are no records in the selected date range.")
    st.stop()

st.sidebar.subheader("Visual alert thresholds")
transfer_threshold = st.sidebar.slider(
    "Low transfer ratio alert (%)", 0, 100, 25, 5
)
discharge_threshold = st.sidebar.slider(
    "Low discharge ratio alert (%)", 0, 100, 5, 1
)

# KPI summary
st.subheader("Key indicators")
c1, c2, c3, c4 = st.columns(4)

latest = filtered.iloc[-1]
c1.metric("Valid reporting days", f"{len(filtered):,}")
c2.metric(
    "Latest CBP custody count",
    "N/A" if pd.isna(latest["CBP_Custody"]) else f"{latest['CBP_Custody']:,.0f}"
)
c3.metric(
    "Latest HHS care count",
    "N/A" if pd.isna(latest["HHS_Care"]) else f"{latest['HHS_Care']:,.0f}"
)
c4.metric(
    "Total recorded discharges",
    f"{filtered['Discharged'].sum(min_count=1):,.0f}"
    if filtered["Discharged"].notna().any() else "N/A"
)

st.caption(
    f"Selected period: {start_date if isinstance(date_range, (tuple, list)) and len(date_range) == 2 else min_date} "
    f"to {end_date if isinstance(date_range, (tuple, list)) and len(date_range) == 2 else max_date}. "
    "Reporting dates are not necessarily consecutive."
)

# Pipeline flow overview
st.subheader("Care pipeline overview")
flow_columns = st.columns(3)
flow_columns[0].markdown("**CBP custody**")
flow_columns[0].write("Reported count of children in CBP custody")
flow_columns[1].markdown("**Transfer to HHS**")
flow_columns[1].write("Reported number transferred out of CBP custody")
flow_columns[2].markdown("**HHS care and discharge**")
flow_columns[2].write("Reported HHS care count and number discharged")

flow_summary = pd.DataFrame({
    "Measure": [
        "Apprehended / placed in CBP custody",
        "Children in CBP custody",
        "Transferred out of CBP custody",
        "Children in HHS care",
        "Discharged from HHS care"
    ],
    "Total in selected period": [
        filtered["Apprehended"].sum(min_count=1),
        filtered["CBP_Custody"].sum(min_count=1),
        filtered["Transferred"].sum(min_count=1),
        filtered["HHS_Care"].sum(min_count=1),
        filtered["Discharged"].sum(min_count=1)
    ]
})
st.dataframe(flow_summary, hide_index=True, use_container_width=True)

# Daily counts trend
st.subheader("Daily counts over time")
count_options = {
    "Apprehended / placed in CBP custody": "Apprehended",
    "Children in CBP custody": "CBP_Custody",
    "Transferred out of CBP custody": "Transferred",
    "Children in HHS care": "HHS_Care",
    "Discharged from HHS care": "Discharged"
}
selected_measures = st.multiselect(
    "Choose measures to display",
    options=list(count_options.keys()),
    default=[
        "Transferred out of CBP custody",
        "Discharged from HHS care"
    ]
)

if selected_measures:
    fig, ax = plt.subplots(figsize=(11, 4.5))
    for label in selected_measures:
        ax.plot(
            filtered["Date"],
            filtered[count_options[label]],
            marker=".",
            linewidth=1.5,
            label=label
        )
    ax.set_xlabel("Reporting date")
    ax.set_ylabel("Reported number of children")
    ax.set_title("Reported daily counts")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.autofmt_xdate()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.write("Select at least one measure to show the trend chart.")

# Simple ratios
st.subheader("Transfer and discharge ratios")
st.write(
    "Transfer ratio = transfers ÷ children in CBP custody × 100. "
    "Discharge ratio = discharges ÷ children in HHS care × 100. "
    "These are same-day comparison ratios, not the percentage of a specific "
    "cohort transferred or discharged, and not a direct measure of speed."
)

ratio_data = filtered[["Date", "Transfer Ratio (%)", "Discharge Ratio (%)"]].copy()
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(ratio_data["Date"], ratio_data["Transfer Ratio (%)"], label="Transfer ratio")
ax.plot(ratio_data["Date"], ratio_data["Discharge Ratio (%)"], label="Discharge ratio")
ax.set_xlabel("Reporting date")
ax.set_ylabel("Ratio (%)")
ax.set_title("Daily comparison ratios")
ax.legend()
ax.grid(True, alpha=0.25)
fig.autofmt_xdate()
st.pyplot(fig)
plt.close(fig)

# Alerts: visually flag low daily ratios, where ratio can be calculated.
st.subheader("Threshold-based visual alerts")
alert_left, alert_right = st.columns(2)

low_transfer = filtered[
    filtered["Transfer Ratio (%)"].notna() &
    (filtered["Transfer Ratio (%)"] < transfer_threshold)
]
low_discharge = filtered[
    filtered["Discharge Ratio (%)"].notna() &
    (filtered["Discharge Ratio (%)"] < discharge_threshold)
]

with alert_left:
    st.markdown("**Low transfer ratio dates**")
    st.caption(f"Threshold: below {transfer_threshold}%")
    if low_transfer.empty:
        st.success("No dates below this threshold in the selected period.")
    else:
        st.warning(f"{len(low_transfer)} reporting dates are below the threshold.")
        st.dataframe(
            low_transfer[["Date", "CBP_Custody", "Transferred", "Transfer Ratio (%)"]]
            .sort_values("Date"),
            hide_index=True,
            use_container_width=True
        )

with alert_right:
    st.markdown("**Low discharge ratio dates**")
    st.caption(f"Threshold: below {discharge_threshold}%")
    if low_discharge.empty:
        st.success("No dates below this threshold in the selected period.")
    else:
        st.warning(f"{len(low_discharge)} reporting dates are below the threshold.")
        st.dataframe(
            low_discharge[["Date", "HHS_Care", "Discharged", "Discharge Ratio (%)"]]
            .sort_values("Date"),
            hide_index=True,
            use_container_width=True
        )

# Inflow compared with outflow
st.subheader("Intake versus discharge")
st.write(
    "The daily balance below is apprehensions minus discharges. It compares "
    "two reported flows, but it is not a count of the total backlog because "
    "children can remain in different stages and the records are not a linked cohort."
)

fig, ax = plt.subplots(figsize=(11, 4))
ax.bar(filtered["Date"], filtered["Daily Balance"])
ax.axhline(0, linewidth=1)
ax.set_xlabel("Reporting date")
ax.set_ylabel("Apprehensions minus discharges")
ax.set_title("Daily intake-versus-discharge balance")
ax.grid(True, axis="y", alpha=0.25)
fig.autofmt_xdate()
st.pyplot(fig)
plt.close(fig)

# Show table and download
st.subheader("Filtered data table")
st.dataframe(filtered, hide_index=True, use_container_width=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="care_transition_filtered_data.csv",
    mime="text/csv"
)

with st.expander("Data quality notes"):
    st.write(f"- Valid dated records loaded: {len(df):,}")
    st.write(f"- First available date: {df['Date'].min().date()}")
    st.write(f"- Last available date: {df['Date'].max().date()}")
    st.write(
        "- Fully blank rows and rows without a valid date are removed before analysis."
    )
    st.write(
        "- The reporting dates have gaps, so the dataset should not be assumed to "
        "contain one record for every calendar day."
    )
    st.write(
        "- Ratios are descriptive comparisons of same-day aggregate values. "
        "They cannot establish individual processing time, reunification quality, "
        "or the cause of changes."
    )

st.caption("Educational analytics project. Interpret all aggregate measures carefully.")
