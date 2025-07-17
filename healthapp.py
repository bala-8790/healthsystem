import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ------------------ Data ------------------
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
    "Dengue": "Viral infection from Aedes mosquitoes causing high fever and pain.",
    "Chickenpox": "Highly contagious viral disease with rash and blisters.",
    "Typhoid": "Bacterial infection due to contaminated food or water.",
    "Pneumonia": "Lung inflammation caused by bacterial or viral infections.",
    "Cancer": "Uncontrolled abnormal cell growth that may affect any organ.",
    "Tuberculosis": "Chronic bacterial lung infection, spreads via droplets.",
    "Diabetes": "High blood sugar levels due to insulin problems.",
    "Thyroid": "Hormonal imbalance affecting metabolism and mood.",
    "Covid-19": "Respiratory disease caused by coronavirus SARS-CoV-2.",
    "HIV/AIDS": "Virus attacking immune system, transmitted through blood/fluids.",
    "Brain Tumor": "Abnormal growth in brain cells affecting cognition and motor functions.",
    "Blood Clotting Disorder": "Conditions affecting normal blood clotting."
}

health_tips = {
    "Malaria": "Use mosquito nets, avoid stagnant water, and take antimalarial meds if prescribed.",
    "Dengue": "Stay hydrated, avoid mosquito bites, and seek medical care for severe symptoms.",
    "Chickenpox": "Rest, avoid scratching, apply calamine lotion, and stay isolated.",
    "Typhoid": "Drink clean water, take antibiotics as prescribed, and maintain hygiene.",
    "Pneumonia": "Rest, drink fluids, use prescribed antibiotics, avoid smoking.",
    "Cancer": "Regular screening, healthy diet, avoid tobacco, early detection helps.",
    "Tuberculosis": "Complete antibiotic course, cover mouth, and regular check-ups.",
    "Diabetes": "Eat balanced meals, exercise regularly, monitor blood sugar levels.",
    "Thyroid": "Follow medication schedule, eat iodine-rich food, regular checkups.",
    "Covid-19": "Wear masks, stay isolated, monitor oxygen levels, stay hydrated.",
    "HIV/AIDS": "Use protection, avoid sharing needles, and maintain a healthy immune system.",
    "Brain Tumor": "Monitor neurological signs, follow treatment plan, and reduce stress.",
    "Blood Clotting Disorder": "Avoid injury, regular monitoring, and follow prescribed treatment."
}

hospital_data = [
    {"name": "Apollo Hospitals", "location": "Hyderabad", "contact": "040-23607777"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-26588500"},
    {"name": "Fortis Healthcare", "location": "Bangalore", "contact": "080-66214444"},
]

# ------------------ UI ------------------
st.set_page_config(page_title="🩺 AI Healthcare Predictor", layout="wide")
st.title("🧠 AI-Powered Disease Predictor")
st.markdown("_By analyzing your symptoms, we provide disease prediction, health tips, hospital info, and reports._")

# ------------------ Form ------------------
with st.form("health_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Name")
        age = st.number_input("🎂 Age", min_value=1, max_value=120, step=1)
        email = st.text_input("📧 Email Address")
    with col2:
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        city = st.text_input("🏙️ Your City (Optional)")
        date = datetime.now().strftime("%Y-%m-%d")
        st.markdown(f"🗓️ **Date:** {date}")

    selected_symptoms = st.multiselect("### 🩺 Select Symptoms", symptoms_list)
    submitted = st.form_submit_button("🔍 Predict Disease")

# ------------------ Prediction ------------------
if submitted:
    if len(selected_symptoms) < 2:
        st.warning("⚠️ Please select at least 2 symptoms.")
    else:
        matched_disease = None
        highest_score = 0

        for disease, symptoms in disease_symptom_map.items():
            match_count = len(set(symptoms) & set(selected_symptoms))
            score = (2 * match_count) / (len(symptoms) + len(selected_symptoms))
            if score > highest_score and match_count >= 2:
                highest_score = score
                matched_disease = disease

        if matched_disease:
            st.success(f"🎯 **Predicted Disease:** {matched_disease}")
            st.info(f"📚 **Cause:** {disease_explanations[matched_disease]}")
            st.warning(f"💡 **Health Tips:** {health_tips[matched_disease]}")

            st.markdown("### 🏥 Recommended Hospitals")
            filtered_hospitals = [h for h in hospital_data if city.lower() in h["location"].lower()] if city else hospital_data
            for h in filtered_hospitals:
                st.markdown(f"**{h['name']}**, {h['location']} — 📞 {h['contact']}")

            # Report
            report_text = f"""
Healthcare Prediction Report
----------------------------
Name: {name}
Age: {age}
Gender: {gender}
Email: {email}
Date: {date}
City: {city}

Symptoms: {', '.join(selected_symptoms)}
Predicted Disease: {matched_disease}
Explanation: {disease_explanations[matched_disease]}
Health Tips: {health_tips[matched_disease]}
"""
            st.download_button("⬇️ Download Report", report_text, file_name="healthcare_report.txt")

            # Send Email
            if email:
                try:
                    msg = MIMEText(report_text, "plain")
                    msg['Subject'] = 'Your Healthcare Disease Prediction Report'
                    msg['From'] = st.secrets["email"]
                    msg['To'] = email

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(st.secrets["email"], st.secrets["password"])
                        server.send_message(msg)

                    st.success(f"📧 Report sent to **{email}**")
                except Exception as e:
                    st.error(f"❌ Email failed: {e}")
        else:
            st.error("❌ Couldn't confidently predict disease. Try different symptoms.")

# ------------------ Charts ------------------
st.markdown("### 📊 Symptom-Disease Frequency Visualization")
df_chart = pd.DataFrame([
    {"Disease": d, "Symptom": s}
    for d, symptoms in disease_symptom_map.items()
    for s in symptoms
])
symptom_counts = df_chart['Symptom'].value_counts().reset_index()
symptom_counts.columns = ["Symptom", "Frequency"]

fig, ax = plt.subplots(figsize=(12, 4))
sns.barplot(x="Symptom", y="Frequency", data=symptom_counts.head(15), ax=ax, palette="coolwarm")
plt.xticks(rotation=45)
st.pyplot(fig)
