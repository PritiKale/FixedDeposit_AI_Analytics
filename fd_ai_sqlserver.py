import pandas as pd
import datetime
import pyodbc
from transformers import pipeline


EXCEL_FILE = "dummy_users.xlsx"
AI_MODEL = "facebook/bart-large-cnn"

SERVER = "localhost"
DATABASE = "FD_Booking_DB"


conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

try:
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    print(f"Database '{DATABASE}' created.")
except Exception:
    print(f"Database '{DATABASE}' already exists.")

conn.close()


conn_str_db = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=localhost;DATABASE={DATABASE};Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str_db, autocommit=True)
cursor = conn.cursor()


cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='validated_users' AND xtype='U')
CREATE TABLE validated_users (
    Name NVARCHAR(100),
    Age INT,
    KYC_Completed NVARCHAR(10),
    Account_Number NVARCHAR(20),
    FD_Amount FLOAT,
    Tenor_Years INT,
    Status NVARCHAR(20),
    Error_Details NVARCHAR(255)
)
""")

cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='fd_bookings' AND xtype='U')
CREATE TABLE fd_bookings (
    Booking_ID NVARCHAR(50),
    Name NVARCHAR(100),
    Account_Number NVARCHAR(20),
    FD_Amount FLOAT,
    Tenor_Years INT,
    Interest_Rate FLOAT,
    Maturity_Amount FLOAT,
    Booked_At DATETIME
)
""")


cursor.execute("""
IF NOT EXISTS (
    SELECT * FROM sys.columns
    WHERE Name = 'Progress'
      AND Object_ID = Object_ID('dbo.fd_bookings')
)
BEGIN
    ALTER TABLE dbo.fd_bookings
    ADD Progress NVARCHAR(50);
END
""")


cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ai_summary' AND xtype='U')
CREATE TABLE ai_summary (
    Generated_On DATETIME,
    Summary NVARCHAR(MAX)
)
""")


def validate_row(row):
    errors = []

    if int(row.get("Age", 0)) < 18:
        errors.append("Underage user")
    if not str(row.get("KYC_Completed", "")).lower() in ["true", "yes", "1"]:
        errors.append("KYC incomplete")
    if not str(row.get("Account_Number", "")).isdigit() or len(str(row.get("Account_Number", ""))) != 12:
        errors.append("Invalid account number")
    if float(row.get("FD_Amount", 0)) < 1000:
        errors.append("Amount too low")
    if float(row.get("FD_Amount", 0)) > 2000000:
        errors.append("Amount exceeds limit")

    return errors

def book_fd(row):
    amount = float(row["FD_Amount"])
    tenor = int(row.get("Tenor_Years", 1))

    if amount >= 500000:
        base_rate = 6.5
    elif amount >= 100000:
        base_rate = 6.0
    else:
        base_rate = 5.5

    rate = base_rate + (0.1 * (tenor - 1))
    maturity = amount * ((1 + rate / 100) ** tenor)

    return round(rate, 2), round(maturity, 2)


df = pd.read_excel(EXCEL_FILE)
validated = []

for _, row in df.iterrows():
    row = row.to_dict()
    errors = validate_row(row)
    booking_id = f"FD{int(datetime.datetime.now().timestamp())}"

    if errors:
        status = "Failed"
        error_details = "; ".join(errors)
        progress_value = "Incomplete"
        rate = 0
        maturity = 0
    else:
        status = "Success"
        error_details = ""
        progress_value = "Completed"
        rate, maturity = book_fd(row)

    
    cursor.execute("""
        INSERT INTO fd_bookings
        (Booking_ID, Name, Account_Number, FD_Amount, Tenor_Years,
         Interest_Rate, Maturity_Amount, Booked_At, Progress)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    booking_id, row["Name"], row["Account_Number"], row["FD_Amount"],
    row["Tenor_Years"], rate, maturity, datetime.datetime.now(), progress_value)

  
    cursor.execute("""
        INSERT INTO validated_users
        (Name, Age, KYC_Completed, Account_Number, FD_Amount,
         Tenor_Years, Status, Error_Details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    row["Name"], row["Age"], str(row["KYC_Completed"]), str(row["Account_Number"]),
    row["FD_Amount"], row["Tenor_Years"], status, error_details)

    validated.append(row)


summary_text = f"Processed {len(validated)} users. "
success = len([v for v in validated if v["Status"] == "Success"])
failed = len(validated) - success
total_amount = sum([v["FD_Amount"] for v in validated if v["Status"] == "Success"])

summary_text += f"{success} successful, {failed} failed. Total booked amount ₹{total_amount:,.0f}."

print("Generating AI Summary...")
generator = pipeline("text2text-generation", model=AI_MODEL)
ai_result = generator(summary_text, max_length=50, do_sample=False)[0]["generated_text"]

cursor.execute("INSERT INTO ai_summary VALUES (?, ?)", (datetime.datetime.now(), ai_result))

conn.commit()
conn.close()

print("✅ FD Booking processing completed successfully!")
print("✅ Data saved in SQL Server.")
print("✅ AI Summary:", ai_result)
