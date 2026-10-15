# Care Transition Efficiency & Placement Outcome Analytics

## What this project does
This beginner-friendly Streamlit dashboard analyzes a public aggregate dataset about:
- children apprehended and placed in CBP custody
- children in CBP custody
- transfers out of CBP custody
- children in HHS care
- discharges from HHS care

It includes data cleaning, date filtering, KPI summaries, line charts, simple ratios, threshold-based visual alerts, a daily intake-versus-discharge chart, and CSV download.

## Files
- `app.py` — dashboard code
- `HHS_Unaccompanied_Alien_Children_Program.csv` — supplied dataset
- `requirements.txt` — Python packages
- `PROJECT_REPORT.md` — editable report draft
- `PRESENTATION_NOTES.md` — short demo and viva notes

## How to run it
1. Install Python 3.10 or later.
2. Open a terminal in this folder.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start the dashboard:
   `streamlit run app.py`
5. A browser tab should open with the dashboard.

If you use Google Colab, this exact launch workflow is intended for a local Python environment. Streamlit can also be deployed online, but deployment is an optional extra.

## Important interpretation notes
- The CSV contains fully blank rows; the app removes rows with no data and rows without a valid date.
- The transfer and discharge ratios are simple same-day descriptive ratios. They are not true processing speeds, cohort success rates, or individual wait times.
- `Apprehended - Discharged` is a comparison of two daily flows, not a complete backlog calculation.
- This is an aggregate educational analysis, not a tool for decisions about individual children.
- Verify the original dataset's source, date coverage, definitions, and any internship-specific rubric before final submission.
