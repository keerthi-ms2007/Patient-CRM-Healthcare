import streamlit as st
import pandas as pd

st.set_page_config(page_title="Patient CRM", layout="wide")
st.title("🏥 Patient CRM - Healthcare")

# Sample Data - CSV tho pani ledu, direct ga vastundi
if "patients" not in st.session_state:
    st.session_state.patients = pd.DataFrame([
        {"Name": "Keerthi", "Age": 21, "Disease": "Fever", "Phone": "9876543210", "Status": "Active"},
        {"Name": "Ramesh", "Age": 35, "Disease": "Diabetes", "Phone": "9876543211", "Status": "Active"},
        {"Name": "Sita", "Age": 28, "Disease": "Fever", "Phone": "9876543212", "Status": "Recovered"},
        {"Name": "Arjun", "Age": 42, "Disease": "BP", "Phone": "9876543213", "Status": "Active"},
    ])

df = st.session_state.patients

# Top numbers
c1, c2, c3 = st.columns(3)
c1.metric("Total Patients", len(df))
c2.metric("Active", len(df[df["Status"]=="Active"]))
c3.metric("Recovered", len(df[df["Status"]=="Recovered"]))

st.divider()

# Left - Add Patient, Right - Chart
left, right = st.columns([1, 1])

with left:
    st.subheader("➕ Add New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", 1, 100, 21)
    disease = st.selectbox("Disease", ["Fever", "Diabetes", "BP", "Cold", "Other"])
    phone = st.text_input("Phone")
    status = st.selectbox("Status", ["Active", "Recovered"])
    if st.button("Add Patient"):
        if name:
            new = pd.DataFrame([{"Name": name, "Age": age, "Disease": disease, "Phone": phone, "Status": status}])
            st.session_state.patients = pd.concat([df, new], ignore_index=True)
            st.success(f"{name} Added!")
            st.rerun()
        else:
            st.error("Name ivvu!")

with right:
    st.subheader("📊 Disease Wise Count")
    st.bar_chart(df["Disease"].value_counts())

st.divider()
st.subheader("📋 All Patients")
search = st.text_input("🔍 Search Patient")
if search:
    df = df[df["Name"].str.contains(search, case=False, na=False)]
st.dataframe(df, use_container_width=True)
