import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# --------------------------
# Session State to Save Previous Symptoms
# --------------------------
if "prev_symptoms" not in st.session_state:
    st.session_state.prev_symptoms = []

# --------------------------
# Data Setup
# --------------------------
symptoms_list = [
    "fever", "headache", "fatigue", "nausea", "vomiting", "cough", "cold", "muscle_pain",
    "joint_pain", "rash", "abdominal_pain", "loss_of_appetite", "diarrhea", "constipation",
    "chills", "sore_throat", "weight_loss", "night_sweats", "breathlessness", "chest_pain",
    "vision_problem", "excessive_thirst", "frequent_urination", "bleeding_gums",
    "unexplained_bleeding", "itching", "yellow_skin", "swollen_lymph_nodes",
    "seizures", "speech_difficulty", "paralysis", "confusion", "memory_loss"
]

disease_symptom_map = {
    "Malaria": ["fever", "chills", "sweating", "headache", "nausea", "vomiting", "muscle_pain"],
    "Dengue": ["fever", "headache", "joint_pain", "muscle_pain", "rash", "nausea", "vomiting"],
    "Chickenpox": ["fever", "rash", "fatigue", "itching", "headache", "loss_of_appetite"],
    "Typhoid": ["fever", "abdominal_pain", "headache", "diarrhea", "loss_of_appetite"],
    "Pneumonia": ["fever", "cough", "chest_pain", "breathlessness", "fatigue"],
    "Cancer": ["weight_loss", "fatigue", "unexplained_bleeding", "vision_problem", "swollen_lymph_nodes"],
    "Tuberculosis": ["cough", "fever", "night_sweats", "weight_loss", "chest_pain"],
    "Diabetes": ["frequent_urination", "excessive_thirst", "fatigue", "weight_loss", "vision_problem"],
    "Thyroid": ["fatigue", "weight_loss", "constipation", "cold", "swelling_neck"],
    "Covid-19": ["fever", "cough", "fatigue", "sore_throat", "breathlessness", "loss_of_appetite"],
    "HIV/AIDS": ["fatigue", "weight_loss", "swollen_lymph_nodes", "fever", "night_sweats"],
    "Brain Tumor": ["headache", "vision_problem", "seizures", "speech_difficulty", "memory_loss"],
    "Blood Clotting Disorder": ["unexplained_bleeding", "fatigue", "bleeding_gums", "joint_pain"]
}

disease_explanations = {
    "Malaria": "Mosquito-borne disease caused by Plasmodium parasites.",
    "Dengue": "Viral infection from Aedes mosquitoes causing high fever, pain.",
    "Chickenpox": "Highly contagious viral disease with rash and blisters.",
    "Typhoid": "Bacterial infection due to contaminated food or water.",
    "Pneumonia": "Lung inflammation caused by bacterial or viral infections.",
    "Cancer": "Uncontrolled abnormal cell growth, may affect any organ.",
    "Tuberculosis": "Chronic bacterial lung infection, spreads via droplets.",
    "Diabetes": "High blood sugar levels due to insulin problems.",
    "Thyroid": "Hormonal imbalance affecting metabolism and mood.",
    "Covid-19": "Respiratory disease caused by coronavirus SARS-CoV-2.",
    "HIV/AIDS": "Virus attacking immune system, transmitted through blood/fluids.",
    "Brain Tumor": "Abnormal growth in brain cells affecting cognition and motor functions.",
    "Blood Clotting Disorder": "Genetic or acquired conditions affecting normal blood clotting."
}

health_tips = {
    "Malaria": "Use mosquito nets and repellents. Stay hydrated.",
    "Dengue": "Avoid stagnant water. Take rest and drink fluids.",
    "Chickenpox": "Avoid scratching. Use calamine lotion and stay isolated.",
    "Typhoid": "Drink boiled water. Eat light, nutritious food.",
    "Pneumonia": "Take antibiotics if bacterial. Rest and stay warm.",
    "Cancer": "Regular screening. Healthy lifestyle. Follow treatment strictly.",
    "Tuberculosis": "Adhere to full TB treatment course. Cover coughs.",
    "Diabetes": "Avoid sugary foods. Regular exercise and monitor glucose.",
    "Thyroid": "Regular checkups. Maintain a balanced iodine-rich diet.",
    "Covid-19": "Wear masks. Sanitize hands. Isolate when sick.",
    "HIV/AIDS": "Take antiretroviral drugs regularly. Practice safe methods.",
    "Brain Tumor": "Follow medical imaging & surgery plans. Rest needed.",
    "Blood Clotting Disorder": "Avoid injuries. Use prescribed anticoagulants properly."
}

hospital_data = [
    {"name": "Apollo Hospitals", "location": "Hyderabad", "contact": "040-23607777"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-26588500"},
    {"name": "Fortis Healthcare", "location": "Bangalore", "contact": "080-66214444"},
]

# --------------------------
# UI Setup
# --------------------------
st.set_page_config(page_title="Healthcare Predictor", layout="wide")
st.title("🧠 Disease Prediction & Report Generator")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", 1, 120)
    email = st.text_input("📧 Email")

with col2:
    gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
    location = st.selectbox("🏙️ Location", ["Hyderabad", "Delhi", "Bangalore", "Other"])
    date = datetime.now().strftime("%Y-%m-%d")
    st.markdown(f"🗓️ **Date:** `{date}`")

st.markdown("### 🩺 Select Your Symptoms")
selected_symptoms = st.multiselect("Choose from the list:", symptoms_list)

# --------------------------
# Predict Disease
# --------------------------
if st.button("🔍 Predict Disease"):
    if len(selected_symptoms) < 2:
        st.warning("⚠️ Please select at least 2 symptoms.")
    else:
        st.session_state.prev_symptoms = selected_symptoms  # Save history

        matched_disease = None
        highest_score = 0

        for disease, symptoms in disease_symptom_map.items():
            match_count = len(set(symptoms) & set(selected_symptoms))
            score = match_count / len(symptoms)
            if score > highest_score and match_count >= 2:
                highest_score = score
                matched_disease = disease

        if matched_disease:
            explanation = disease_explanations.get(matched_disease, "Information unavailable.")
            tips = health_tips.get(matched_disease, "General rest and hydration advised.")

            st.success(f"🎯 **Predicted Disease:** {matched_disease}")
            st.info(f"📚 **Cause:** {explanation}")
            st.warning(f"💡 **Health Tip:** {tips}")

            st.markdown("### 🏥 Recommended Hospitals")
            filtered_hospitals = [h for h in hospital_data if h['location'] == location]
            if not filtered_hospitals:
                filtered_hospitals = hospital_data  # fallback

            for i, hospital in enumerate(filtered_hospitals, 1):
                st.markdown(f"{i}. **{hospital['name']}**, {hospital['location']} — 📞 {hospital['contact']}")

            report = f"""
Healthcare Prediction Report
----------------------------
Name: {name}
Age: {age}
Gender: {gender}
Email: {email}
Location: {location}
Date: {date}

Symptoms: {', '.join(selected_symptoms)}
Predicted Disease: {matched_disease}
Cause: {explanation}
Health Tip: {tips}

Top Hospitals:
"""
            for i, h in enumerate(filtered_hospitals, 1):
                report += f"{i}. {h['name']} - {h['location']} ({h['contact']})\n"

            st.download_button("⬇️ Download Report", report, file_name="healthcare_report.txt")

            # Send Email
            if email:
                try:
                    msg = MIMEText(report)
                    msg['Subject'] = 'Healthcare Prediction Report'
                    msg['From'] = "your_email@gmail.com"
                    msg['To'] = email

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login("your_email@gmail.com", "your_password")  # Use app password
                        server.send_message(msg)

                    st.success(f"📧 Report sent to {email}")
                except Exception as e:
                    st.error(f"❌ Email send failed: {e}")
        else:
            st.error("❌ Could not confidently predict the disease. Try selecting more symptoms.")

# --------------------------
# Previous Symptoms Section
# --------------------------
if st.session_state.prev_symptoms:
    st.markdown("### 📌 Previously Selected Symptoms")
    st.code(", ".join(st.session_state.prev_symptoms))
