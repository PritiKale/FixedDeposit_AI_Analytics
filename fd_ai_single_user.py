import datetime
import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=FD_Booking_DB;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='validated_users' AND xtype='U')
BEGIN
    CREATE TABLE validated_users (
        Name NVARCHAR(100),
        Age INT,
        KYC_Completed NVARCHAR(10),
        Account_Number NVARCHAR(20),
        FD_Amount FLOAT,
        Tenor_Years INT,
        Status NVARCHAR(20)
    )
END
""")


cursor.execute("""
IF NOT EXISTS (
    SELECT * FROM sys.columns 
    WHERE Name = 'Error_Details'
    AND Object_ID = Object_ID('validated_users')
)
BEGIN
    ALTER TABLE validated_users
    ADD Error_Details NVARCHAR(MAX);
END
""")


cursor.execute("""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='fd_bookings' AND xtype='U')
BEGIN
    CREATE TABLE fd_bookings (
        Booking_ID NVARCHAR(50),
        Name NVARCHAR(100),
        Account_Number NVARCHAR(20),
        FD_Amount FLOAT,
        Tenor_Years INT,
        Interest_Rate FLOAT,
        Maturity_Amount FLOAT,
        Booked_At DATETIME,
        Progress NVARCHAR(50)
    )
END
""")


cursor.execute("""
IF NOT EXISTS (
    SELECT * FROM sys.columns 
    WHERE Name = 'Error_Details'
    AND Object_ID = Object_ID('fd_bookings')
)
BEGIN
    ALTER TABLE fd_bookings
    ADD Error_Details NVARCHAR(MAX);
END
""")

def validate_user(name, age, kyc, account, amount, tenor):
    errors = []

    try:
        age_int = int(age)
        amount_float = float(amount)
        tenor_int = int(tenor)
    except:
        return ["Age / Amount / Tenor not numbers"]

    if age_int < 18:
        errors.append("Underage user")
    if kyc.lower() not in ["yes", "true", "1"]:
        errors.append("KYC incomplete")
    if not account.isdigit() or len(account) != 12:
        errors.append("Invalid account number")
    if amount_float < 1000:
        errors.append("Amount too low")
    if amount_float > 2000000:
        errors.append("Amount exceeds limit")

    return errors


def book_fd(amount, tenor):
    amount = float(amount)
    tenor = int(tenor)

    if amount >= 500000:
        base_rate = 6.5
    elif amount >= 100000:
        base_rate = 6.0
    else:
        base_rate = 5.5

    rate = base_rate + (0.1 * (tenor - 1))
    maturity = amount * ((1 + rate / 100) ** tenor)

    return round(rate, 2), round(maturity, 2)



print("\n=== Enter FD Booking Details ===")
name = input("Name: ")
age = input("Age: ")
kyc = input("KYC Completed (Yes/No): ")
account = input("Account Number (12 digits): ")

amount = input("FD Amount: ")
re_enter_amount = input("Re-enter FD Amount for confirmation: ")

tenor = input("Tenor (Years): ")


errors = validate_user(name, age, kyc, account, amount, tenor)


if amount != re_enter_amount:
    errors.append("FD Amount mismatch on re-entry")

booking_id = f"FD{int(datetime.datetime.now().timestamp())}"

if errors:
    status = "Failed"
    progress = "Incomplete"
    rate, maturity = 0, 0
    error_details = "; ".join(errors)
else:
    status = "Success"
    progress = "Completed"
    rate, maturity = book_fd(amount, tenor)
    error_details = ""


cursor.execute("""
INSERT INTO fd_bookings
(Booking_ID, Name, Account_Number, FD_Amount, Tenor_Years,
 Interest_Rate, Maturity_Amount, Booked_At, Progress, Error_Details)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
booking_id, name, account, amount, tenor,
rate, maturity, datetime.datetime.now(), progress, error_details)


cursor.execute("""
INSERT INTO validated_users
(Name, Age, KYC_Completed, Account_Number, FD_Amount,
 Tenor_Years, Status, Error_Details)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
name, age, kyc, account, amount, tenor, status, error_details)


print("\n===== RESULT =====")
print("Booking ID:", booking_id)
print("Status:", status)
print("Progress:", progress)
print("Interest Rate:", rate)
print("Maturity Amount:", maturity)
print("Errors:", error_details if error_details else "None")

conn.close()
