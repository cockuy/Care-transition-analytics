# Care Transition Efficiency & Placement Outcome Analytics
## Project Report Draft

**Student:** [Your name]  
**Program / Internship:** [Program name]  
**Date:** [Submission date]

## 1. Abstract
This project uses Python to explore aggregate reporting data about the movement of unaccompanied children through CBP custody and HHS care. A Streamlit dashboard presents basic counts, trends, descriptive transfer and discharge ratios, and threshold-based visual alerts. The goal is to make the supplied data easier to explore and to highlight patterns that may merit further investigation.

## 2. Problem Statement
Aggregate counts can show how many children are reported in custody or care, but it can be difficult to compare daily transfers and discharges across a reporting period. This project provides a simple dashboard for examining those counts and their trends.

## 3. Objectives
- Load and clean the supplied CSV file.
- Summarize the main reported counts.
- Display changes in counts over time.
- Calculate simple same-day transfer and discharge ratios.
- Highlight dates that fall below user-selected ratio thresholds.
- Allow users to filter dates and download the filtered data.

## 4. Dataset
The supplied CSV contains six fields: reporting date, children apprehended and placed in CBP custody, children in CBP custody, children transferred out of CBP custody, children in HHS care, and children discharged from HHS care.

The initial file contains 1,170 rows. A preliminary inspection found 450 rows with all fields blank and 720 rows with valid dates and measurements. The app removes fully blank rows and rows without a valid date. The reporting dates are not consecutive, so the dataset should not be treated as a complete daily series without further verification.

## 5. Tools Used
- Python: general-purpose programming language.
- Pandas: reading, cleaning, filtering, and summarizing tabular data.
- Matplotlib: plotting trends and comparisons.
- Streamlit: building the interactive dashboard.

## 6. Methodology
1. Read the CSV file.
2. Convert the date field to a date format and count fields to numeric values.
3. Remove fully blank rows and rows without valid dates.
4. Sort records by date.
5. Calculate the transfer ratio as transfers divided by CBP custody, multiplied by 100.
6. Calculate the discharge ratio as discharges divided by HHS care, multiplied by 100.
7. Display selected count trends and the difference between apprehensions and discharges.
8. Allow the user to set date ranges and visual alert thresholds.

## 7. KPI Definitions and Limitations
**Transfer ratio:** Transfers recorded on a date divided by the reported CBP custody count on that date, multiplied by 100.

**Discharge ratio:** Discharges recorded on a date divided by the reported HHS care count on that date, multiplied by 100.

**Daily intake-versus-discharge balance:** Apprehensions recorded on a date minus discharges recorded on that date.

These indicators are descriptive comparisons. The numerator and denominator may refer to different groups of children, and a same-day ratio is not a direct measure of processing speed, an individual child's waiting time, or the probability of successful reunification. A true backlog measure would require a clearly defined stock-and-flow model, and a true transition-time analysis would require suitable linked timestamps.

## 8. Dashboard Features
- Date range filter.
- KPI summary cards.
- Care pipeline overview.
- Selectable time-series chart.
- Transfer and discharge ratio chart.
- User-adjustable threshold alerts.
- Intake-versus-discharge balance chart.
- Filtered data table and CSV download.
- Data quality notes.

## 9. Results
Run the dashboard and record a few findings supported by the actual charts. For example:
- Which reporting dates have the highest and lowest reported transfer counts?
- How do reported discharges change over the selected period?
- Which dates fall below the chosen alert thresholds?
- What data gaps or limitations affect interpretation?

Do not add numerical findings until you have checked the displayed data.

## 10. Recommendations
- Confirm the source and definitions of every field.
- Investigate low-ratio dates with domain experts rather than assuming they prove delays.
- Obtain linked stage-entry and stage-exit timestamps if the goal is to measure individual transition duration.
- Use consistent reporting intervals and document missing dates.
- Treat aggregate data as a planning aid, not as a basis for decisions about an individual child.

## 11. Conclusion
The project demonstrates a basic data analytics workflow: data cleaning, descriptive statistics, ratio calculation, visualization, date filtering, and dashboard development. It provides an accessible way to explore aggregate care-transition reports while making the limitations of the available data explicit.
