from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import pandas as pd
from pathlib import Path
import csv
import datetime
import os
import sqlite3

BASE = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE / "uploads"
BOOKING_FILE = BASE / "fd_bookings.csv"
UPLOAD_FOLDER.mkdir(exist_ok=True)
app = Flask(__name__)

MIN_FD = 1000
MAX_FD = 2000000

def validate_row(row):
    errors = []
    try:
        age = int(row.get("age",0))
    except:
        errors.append("Invalid age")
        age = 0
    if age < 18:
        errors.append("Age must be at least 18")
    if str(row.get("kyc_completed","")).strip().lower() not in ("true","1","yes"):
        errors.append("KYC not completed")
    acc = str(row.get("account_number","")).strip()
    if not (acc.isdigit() and len(acc)==12):
        errors.append("Account number must be exactly 12 digits")
    try:
        amount = float(row.get("amount_to_fd",0))
    except:
        errors.append("Invalid amount")
        amount = 0
    if amount < MIN_FD:
        errors.append(f"Minimum FD amount is {MIN_FD}")
    if amount > MAX_FD:
        errors.append(f"Maximum FD amount is {MAX_FD}")
   
    if BOOKING_FILE.exists():
        dfb = pd.read_csv(BOOKING_FILE)
        if acc in dfb.account_number.astype(str).tolist():
            errors.append("An FD already exists for this account (demo uniqueness rule)")
    return errors

def book_fd(row):
    amount = float(row["amount_to_fd"])
    tenor = int(row.get("preferred_tenor_years",1))
  
    if amount >= 500000:
        base_rate = 6.5
    elif amount >= 100000:
        base_rate = 6.0
    else:
        base_rate = 5.5
   
    rate = base_rate + (0.1 * (tenor-1))
    maturity_amount = amount * ((1 + rate/100) ** tenor)
    booking = {
        "booking_id": f"FD{int(pd.Timestamp.now().timestamp())}",
        "user_id": row.get("user_id"),
        "name": row.get("name"),
        "account_number": row.get("account_number"),
        "amount": amount,
        "tenor_years": tenor,
        "annual_rate_percent": round(rate,2),
        "maturity_amount": round(maturity_amount,2),
        "booked_at": pd.Timestamp.now()
    }
   
    write_header = not BOOKING_FILE.exists()
    with open(BOOKING_FILE, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(booking.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(booking)
    return booking

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            return render_template('upload.html', error="No file uploaded")
        path = UPLOAD_FOLDER / f.filename
        f.save(path)
        try:
            df = pd.read_excel(path)
        except Exception as e:
            return render_template('upload.html', error="Error reading Excel file: "+str(e))
        results = []
        for row in df.to_dict(orient="records"):
            errs = validate_row(row)
            if errs:
                results.append({"row": row, "status":"failed", "errors": errs})
            else:
                booking = book_fd(row)
                results.append({"row": row, "status":"success", "booking": booking})
        
        successes = [r for r in results if r["status"]=="success"]
        if successes:
            return render_template('result.html', results=results)
        else:
            return render_template('result.html', results=results)
    return render_template('upload.html')

@app.route('/templates/<path:filename>')
def send_template(filename):
    return send_from_directory(BASE / "templates", filename)

if __name__ == '__main__':
    app.run(debug=True)


