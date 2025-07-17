import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ------------------- SYMPTOMS, DISEASES & MAPS ------------------------
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
    "Thyroid": ["fatigue", "weight_loss", "constipation", "cold"],
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

disease_health_tips = {
    "Malaria": "Use mosquito repellents, sleep under nets, and keep surroundings clean.",
    "Dengue": "Avoid mosquito bites, stay hydrated, avoid aspirin-based meds.",
    "Chickenpox": "Rest, avoid scratching, and isolate to prevent spreading.",
    "Typhoid": "Drink boiled water, eat hygienic food, complete antibiotic course.",
    "Pneumonia": "Rest, fluids, antibiotics/antivirals, avoid smoking.",
    "Cancer": "Maintain a healthy diet, avoid tobacco, get regular screenings.",
    "Tuberculosis": "Take medication regularly, avoid crowded areas, good ventilation.",
    "Diabetes": "Exercise, low-sugar diet, regular monitoring of glucose levels.",
    "Thyroid": "Regular thyroid tests, eat iodine-rich food, avoid stress.",
    "Covid-19": "Wear masks, maintain hygiene, get vaccinated, rest well.",
    "HIV/AIDS": "Practice safe sex, avoid sharing needles, take antiretrovirals.",
    "Brain Tumor": "Early diagnosis is key; follow-up with neurologist regularly.",
    "Blood Clotting Disorder": "Avoid injuries, monitor bleeding, follow doctor instructions strictly."
}

hospital_data = [
    {"name": "Apollo Hospitals", "location": "Hyderabad", "contact": "040-23607777"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-26588500"},
    {"name": "Fortis Healthcare", "location": "Bangalore", "contact": "080-66214444"},
    {"name": "Rainbow Hospitals", "location": "Hyderabad", "contact": "040-44665555"},
    {"name": "KIMS Hospitals", "location": "Hyderabad", "contact": "040-49405050"}
]

# ------------------- UI -------------------
st.set_page_config(page_title="Healthcare Predictor", layout="wide")
st.title("🩺 Intelligent Disease Prediction & Health Recommendation System")

with st.form("health_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Name")
        age = st.number_input("🎂 Age", min_value=1, max_value=120)
        email = st.text_input("📧 Email")
    with col2:
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        city = st.text_input("🏙️ City")
        st.write(f"🗓️ Date: {datetime.now().strftime('%Y-%m-%d')}")

    selected_symptoms = st.multiselect("### ✅ Select Symptoms", symptoms_list)

    submitted = st.form_submit_button("🔍 Predict Disease")

# ------------------- PREDICTION LOGIC -------------------
if submitted:
    if len(selected_symptoms) < 2:
        st.warning("⚠️ Please select at least 2 symptoms.")
    else:
        matched_disease = None
        highest_score = 0

        for disease, symptoms in disease_symptom_map.items():
            matches = len(set(selected_symptoms) & set(symptoms))
            score = (2 * matches) / (len(symptoms) + len(selected_symptoms))
            if score > highest_score and matches >= 2:
                highest_score = score
                matched_disease = disease

        if matched_disease:
            st.subheader("🧬 Diagnosis Result")
            st.success(f"**Disease Predicted:** {matched_disease}")
            st.info(f"📚 Explanation: {disease_explanations[matched_disease]}")
            st.warning(f"💡 Health Tip: {disease_health_tips[matched_disease]}")

            st.subheader("🏥 Nearby Hospital Recommendations")
            matched_hospitals = [h for h in hospital_data if city.lower() in h["location"].lower()]
            if matched_hospitals:
                for h in matched_hospitals:
                    st.markdown(f"**{h['name']}**, {h['location']} — 📞 {h['contact']}")
            else:
                st.write("🚫 No hospital found in your city. Showing general recommendations:")
                for h in hospital_data:
                    st.markdown(f"**{h['name']}**, {h['location']} — 📞 {h['contact']}")

            # ------------------- REPORT DOWNLOAD -------------------
            report = f"""
Healthcare Report
------------------
Name: {name}
Age: {age}
Gender: {gender}
Email: {email}
City: {city}
Date: {datetime.now().strftime('%Y-%m-%d')}
Symptoms: {', '.join(selected_symptoms)}

Predicted Disease: {matched_disease}
Explanation: {disease_explanations[matched_disease]}
Health Tip: {disease_health_tips[matched_disease]}
"""
            st.download_button("📥 Download Report", report, "healthcare_report.txt")

            # ------------------- EMAIL -------------------
            if email:
                try:
                    msg = MIMEText(report)
                    msg["Subject"] = "Your Health Prediction Report"
                    msg["From"] = st.secrets["email"]
                    msg["To"] = email

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(st.secrets["email"], st.secrets["password"])
                        server.send_message(msg)

                    st.success(f"📤 Report emailed to {email}")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")
        else:
            st.error("❌ Unable to confidently predict a disease. Try adding more symptoms.")

# ------------------- UI Suggestion -------------------
st.markdown("---")
st.caption("🔁 You can refresh and try again with different symptoms.")
