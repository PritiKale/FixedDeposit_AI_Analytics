FD Booking Analytics — Run Instructions

1) Setup (Mac / Linux / Windows)
   - Ensure Python 3.8+ installed.
   - Install packages:
     python3 -m pip install -r requirements.txt

   If you prefer not to use AI or transformers, remove them:
     python3 -m pip install pandas openpyxl

2) Generate dummy data (optional)
   python3 generate_dummy_excel.py

3) Run the processor (creates/updates fd_data.db and ai_summary.txt):
   python3 fd_ai_sql.py

4) Open Power BI Desktop:
   - Get Data -> SQLite database -> select fd_data.db
   - Load tables and build visuals as described in build_pbix_sql_instructions.md

5) To refresh:
   - Re-run python script whenever you have a new Excel upload.
   - Then click Refresh in Power BI Desktop.

Troubleshooting:
- If transformers/torch installation fails because of system constraints, install without AI and USE_AI will be disabled automatically:
  pip uninstall transformers torch
  pip install pandas openpyxl
