# Demo and Viva Notes

## 60-second project explanation
"My project is Care Transition Efficiency and Placement Outcome Analytics. I used Python, Pandas, Matplotlib, and Streamlit to analyze aggregate reporting data about CBP custody, transfers to HHS care, and discharges. The dashboard cleans blank rows, displays key counts and trends, calculates simple transfer and discharge ratios, and flags dates below user-selected thresholds. These ratios are descriptive indicators, not direct processing times or individual outcomes."

## Questions and simple answers

**1. What is the purpose of the project?**  
To make reported care-transition counts easier to explore and compare over time.

**2. What is Pandas used for?**  
To load, clean, sort, filter, and summarize the CSV data.

**3. What is Streamlit?**  
A Python library for building a small interactive web application.

**4. Why are blank rows removed?**  
They contain no usable date or measurements and should not appear in analysis.

**5. What is the transfer ratio?**  
The number of transfers reported on a date divided by the reported number in CBP custody for that date, multiplied by 100.

**6. Does the transfer ratio measure actual speed?**  
No. It compares same-day aggregate values. To measure actual speed, we would need timestamps showing when each transition began and ended.

**7. What is a threshold alert?**  
A visual flag when a selected ratio is below a value chosen by the dashboard user.

**8. Why is the date filter useful?**  
It lets a user focus on a specific period instead of viewing the entire dataset.

**9. Is this machine learning?**  
No. It is a descriptive data analytics and visualization project.

**10. What is one limitation?**  
The dataset has missing rows and non-consecutive dates. Its aggregate counts cannot reveal an individual child's waiting time or prove why a change occurred.
