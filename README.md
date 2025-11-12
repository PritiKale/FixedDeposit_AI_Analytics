💰 FD_Booking_System_SQL_PowerBI
📘 Project Overview

The FD Booking System is a Python-based automation project that integrates with SQL Server for data storage and Power BI for visualization.
It allows users to book Fixed Deposits (FDs) with validation, interest calculation, and AI-powered insights.
The dashboard created in Power BI (FD_Booking_Dashboard.pbix) provides an interactive view of all booking activities.

⚙️ Key Features

✅ User Validation – Checks KYC status, age, and account validity before booking.

💾 SQL Server Integration – Stores all booking and validation data in relational tables.

🧠 AI Automation Ready – Python scripts can be extended to include ML models for interest forecasting.

📊 Power BI Dashboard – Visualizes key metrics such as total FD amount, booking progress, status distribution, and interest rate trends.

📅 Booking Logs – Each booking (successful or failed) is recorded with timestamps.

🧮 FD Interest & Maturity Calculation – Auto-calculates interest rates based on amount and tenor.


🧩 Database Design (SQL Server)

Database Name: FD_Booking_DB
Tables:

validated_users

Name, Age, KYC_Completed, Account_Number, FD_Amount, Tenor_Years, Status, Error_Details

fd_bookings

Booking_ID, Name, Account_Number, FD_Amount, Tenor_Years, Interest_Rate, Maturity_Amount, Booked_At, Progress, Error_Details

🧠 Python Components
File	Purpose
fd_ai_single_user.py	Validates and books FD for a single user interactively.
fd_ai_sqlserver.py	Handles multiple user bookings directly from SQL database.
generate_dummy_excel.py	Creates dummy users for testing FD logic.
app.py	Optional file to integrate logic or run automated flows.
🚀 How to Run the Project
🧾 Step 1: Install Requirements

Open your terminal or command prompt inside the project folder and run:

pip install -r requirements.txt

🧩 Step 2: Ensure SQL Server is Running

Make sure your local SQL Server service is active.
In PowerShell or Command Prompt:

Get-Service *sql*


You should see services like MSSQLSERVER or SQLEXPRESS running.

🧱 Step 3: Run the Python Script

To book an FD for a single user:

python fd_ai_single_user.py


Follow the prompts:

Enter name, age, KYC status, and account number

Enter FD amount and tenor (in years)

The script validates and stores data into FD_Booking_DB automatically.

For multi-user or AI-based processing:

python fd_ai_sqlserver.py

📊 Step 4: Open the Power BI Dashboard

Launch Power BI Desktop

Open your file:
FD_Booking_Dashboard.pbix

Connect to the SQL Server database:

Home → Get Data → SQL Server Database
Server: localhost
Database: FD_Booking_DB


Load both tables:

fd_bookings

validated_users

Refresh data to view new bookings and status updates.

🔗 Power BI Dashboard Highlights

File: FD_Booking_Dashboard.pbix

Connected Source: SQL Server → FD_Booking_DB

Visuals Included:

📈 FD Bookings over Time (Line Chart)

💵 FD Amount by Tenor (Bar Chart)

🟢 Booking Status (Donut Chart)

📊 Interest Rate by Tenor

🔍 Validation Errors Summary

🧾 Requirements
pandas>=1.3
openpyxl>=3.0
transformers>=4.30
torch>=1.12
pyodbc

🧩 Future Enhancements

🔹 Add AI prediction model for FD interest rate forecasting

🔹 Automate email alerts for failed bookings

🔹 Add Power BI buttons for “View FD Details” or “Add New Booking”

🔹 Integrate API-based booking with real-time data
