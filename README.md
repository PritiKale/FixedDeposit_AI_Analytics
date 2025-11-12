FD Booking & Data Analytics Demo
================================

What's included
- Flask web app to upload an Excel file with user details and simulate FD bookings.
- Dummy Excel file with 10 users: dummy_users.xlsx
- CSV for Power BI import: powerbi_users.csv
- Simple validation logic and booking simulation saved to fd_bookings.csv

Validation rules used (demo):
- Age must be >= 18
- KYC must be completed (True/Yes/1)
- Account number must be exactly 12 digits
- Minimum FD amount is 1000
- Maximum FD amount is 2,000,000
- Uniqueness: the demo prevents booking more than one FD for the same account number by checking fd_bookings.csv

How to run
1. Create a virtualenv and install requirements:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt

2. Run the Flask app:
   python app.py

3. Open http://127.0.0.1:5000 and upload dummy_users.xlsx (or your own Excel)

Power BI
--------
- Use powerbi_users.csv (provided) to import into Power BI Desktop.
- Create visuals: count of successful FDs (based on post-processing fd_bookings.csv), distribution of FD amounts, maturity amount vs tenor, etc.
- For automated analytics, export fd_bookings.csv from the app folder and import/update into Power BI.

ML / Recommendation (optional)
------------------------------
A simple demo ML approach would be to train a small model that recommends tenor or FD amount based on user age and amount — in this project we provide a rule-based rate calculator in app.py.
If you want, I can add a small sklearn example that predicts recommended tenor based on historical dummy data.

Files
- app.py
- templates/ (index.html, upload.html, result.html)
- static/styles.css
- dummy_users.xlsx
- powerbi_users.csv
- requirements.txt
- README.md