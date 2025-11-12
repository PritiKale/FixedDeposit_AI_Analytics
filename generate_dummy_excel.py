import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
data = [
    {"Name":"Ravi Kumar","Age":32,"KYC_Completed":True,"Account_Number":"123456789012","FD_Amount":50000,"Tenor_Years":3},
    {"Name":"Sneha Patel","Age":25,"KYC_Completed":True,"Account_Number":"123456789013","FD_Amount":250000,"Tenor_Years":2},
    {"Name":"Arjun Mehta","Age":19,"KYC_Completed":True,"Account_Number":"123456789014","FD_Amount":700000,"Tenor_Years":5},
    {"Name":"Priya Sharma","Age":17,"KYC_Completed":True,"Account_Number":"123456789015","FD_Amount":50000,"Tenor_Years":1},
    {"Name":"Kiran Joshi","Age":35,"KYC_Completed":False,"Account_Number":"123456789016","FD_Amount":100000,"Tenor_Years":3},
    {"Name":"Anil Verma","Age":45,"KYC_Completed":True,"Account_Number":"123456789017","FD_Amount":1500000,"Tenor_Years":4},
    {"Name":"Neha Desai","Age":27,"KYC_Completed":True,"Account_Number":"123456789018","FD_Amount":2000,"Tenor_Years":1},
    {"Name":"Rahul Singh","Age":40,"KYC_Completed":True,"Account_Number":"123456789019","FD_Amount":300000,"Tenor_Years":3},
    {"Name":"Pooja Nair","Age":22,"KYC_Completed":True,"Account_Number":"123456789020","FD_Amount":80000,"Tenor_Years":2},
    {"Name":"Deepak Shah","Age":29,"KYC_Completed":True,"Account_Number":"123456789021","FD_Amount":400000,"Tenor_Years":3},
]
df = pd.DataFrame(data)
df.to_excel(BASE / "dummy_users.xlsx", index=False)
print("dummy_users.xlsx created.")
