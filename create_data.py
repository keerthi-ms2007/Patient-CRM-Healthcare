import pandas as pd
import numpy as np
import os
from faker import Faker

fake = Faker()
np.random.seed(42)
os.makedirs("data", exist_ok=True)

# 1. Doctors - 50
doctors = []
specialties = ["Cardiology","General Medicine","Pediatrics","Orthopedics","Dermatology","Neurology"]
for i in range(1, 51):
    doctors.append({
        "doctor_id": f"D{i:03d}",
        "doctor_name": f"Dr. {fake.name()}",
        "specialty": np.random.choice(specialties),
        "experience_years": np.random.randint(2, 25),
        "rating": round(np.random.uniform(3.5, 5.0), 1)
    })
pd.DataFrame(doctors).to_csv("data/doctors.csv", index=False)

# 2. Patients - 1000 (FAKE DATA ONLY)
patients = []
conditions = ["Diabetes","Hypertension","Asthma","Fever","Migraine","Arthritis","Healthy"]
for i in range(1, 1001):
    age = np.random.randint(1, 85)
    patients.append({
        "patient_id": f"P{i:04d}",
        "name": fake.name(),
        "age": age,
        "gender": np.random.choice(["Male","Female","Other"]),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "condition": np.random.choice(conditions),
        "has_diabetes": 1 if np.random.random() < 0.25 else 0,
        "has_hypertension": 1 if np.random.random() < 0.30 else 0,
        "bmi": round(np.random.uniform(16, 38), 1),
        "last_visit": str(fake.date_between(start_date="-1y", end_date="today"))
    })
pd.DataFrame(patients).to_csv("data/patients.csv", index=False)

# 3. Appointments - 2000
appts = []
statuses = ["Completed","No-Show","Cancelled","Scheduled"]
for i in range(1, 2001):
    # No-show chance higher if long wait + young + SMS not sent
    wait_days = np.random.randint(0, 30)
    sms_sent = np.random.choice([0, 1])
    prob = 0.1 + (wait_days/100) + (0.1 if sms_sent==0 else 0)
    no_show = 1 if np.random.random() < prob else 0
    appts.append({
        "appointment_id": f"A{i:04d}",
        "patient_id": f"P{np.random.randint(1,1001):04d}",
        "doctor_id": f"D{np.random.randint(1,51):03d}",
        "date": str(fake.date_between(start_date="-6m", end_date="+1m")),
        "wait_days": wait_days,
        "sms_reminder_sent": sms_sent,
        "prev_no_shows": np.random.randint(0, 4),
        "no_show": no_show,
        "status": "No-Show" if no_show==1 else np.random.choice(["Completed","Scheduled"])
    })
pd.DataFrame(appts).to_csv("data/appointments.csv", index=False)

# 4. Prescriptions, Billing, Lab - simple
pres = []
for i in range(1, 801):
    pres.append({
        "prescription_id": f"RX{i:04d}",
        "patient_id": f"P{np.random.randint(1,1001):04d}",
        "drug": np.random.choice(["Metformin","Amlodipine","Paracetamol","Amoxicillin","Atorvastatin"]),
        "dosage": np.random.choice(["500mg","10mg","650mg","250mg"]),
        "allergy_flag": np.random.choice([0,1], p=[0.95,0.05])
    })
pd.DataFrame(pres).to_csv("data/prescriptions.csv", index=False)

billing = []
for i in range(1, 1001):
    amt = np.random.randint(500, 15000)
    billing.append({
        "bill_id": f"B{i:04d}",
        "patient_id": f"P{np.random.randint(1,1001):04d}",
        "amount": amt,
        "insurance_claim": np.random.choice(["Approved","Pending","Rejected"]),
        "paid": np.random.choice([0,1], p=[0.2,0.8])
    })
pd.DataFrame(billing).to_csv("data/billing.csv", index=False)

print("Done! Created 1000 patients, 2000 appointments, 50 doctors")
print("All data is FAKE / Synthetic - No real patient data used")
