# Netflix Insights

A redesigned Streamlit analytics dashboard using the original project dataset and core metrics, with a premium dark interface, responsive KPI cards, interactive Plotly charts, filters, tabs, and CSV export.

## Run on Windows

1. Extract this ZIP.
2. Open the extracted `netflixpython-main` folder in VS Code or PowerShell.
3. (Recommended) Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```
5. Start the app:
   ```powershell
   py -m streamlit run Untitled1.py
   ```
6. Open the local URL shown in the terminal (usually http://localhost:8501).

The app loads the included `netflix.csv` by default. You can also upload a CSV with the required columns: `Watch_Date`, `Region`, `Monthly_Revenue`, `Subscription_Plan`, `Rating`, and `Category`. Optional columns such as `Title`, `Language`, `Device`, `Type`, and `Watch_Time_Minutes` enable additional charts and filters.
