import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# -------------- Symptoms and Diseases ----------------
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

disease_tips = {
    "Malaria": "Avoid mosquito bites, use nets, and take antimalarial drugs as prescribed.",
    "Dengue": "Stay hydrated, avoid NSAIDs, and protect against mosquito bites.",
    "Chickenpox": "Rest, apply calamine lotion, avoid scratching blisters.",
    "Typhoid": "Eat clean food, take antibiotics properly, and rest well.",
    "Pneumonia": "Take full antibiotics course, stay hydrated, avoid smoking.",
    "Cancer": "Follow oncologist's advice, take adequate rest, and maintain nutrition.",
    "Tuberculosis": "Take all TB medications regularly, maintain respiratory hygiene.",
    "Diabetes": "Control diet, exercise regularly, and monitor blood sugar levels.",
    "Thyroid": "Take hormone replacement medicines and maintain a balanced diet.",
    "Covid-19": "Isolate, monitor oxygen levels, and stay hydrated.",
    "HIV/AIDS": "Take ART medication, maintain immunity and avoid infections.",
    "Brain Tumor": "Follow neurological advice and take adequate rest.",
    "Blood Clotting Disorder": "Avoid injury, take clotting factor injections as needed."
}

hospital_data = [
    {"name": "Apollo Hospitals", "location": "Hyderabad", "contact": "040-23607777"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-26588500"},
    {"name": "Fortis Healthcare", "location": "Bangalore", "contact": "080-66214444"},
    {"name": "Care Hospitals", "location": "Hyderabad", "contact": "040-30417777"},
    {"name": "KIMS", "location": "Secunderabad", "contact": "040-44885000"}
]

# -------------- Streamlit UI ----------------
st.set_page_config(page_title="Healthcare Predictor", layout="wide")
st.title("🧠 Healthcare Disease Predictor with Email & Report")

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
        st.markdown(f"🗓️ Date: {date}")

    selected_symptoms = st.multiselect("### 🩺 Select Symptoms", symptoms_list)
    submitted = st.form_submit_button("🔍 Predict Disease")

# -------------- Prediction Logic ----------------
if submitted:
    if not selected_symptoms:
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
            explanation = disease_explanations.get(matched_disease, "No info available.")
            tips = disease_tips.get(matched_disease, "No tips available.")
            st.success(f"🎯 Predicted Disease: **{matched_disease}**")
            st.info(f"📚 Cause: {explanation}")
            st.warning(f"💡 Health Tip: {tips}")

            st.markdown("### 🏥 Recommended Hospitals")
            hospitals_to_show = [h for h in hospital_data if city.lower() in h["location"].lower()] if city else hospital_data
            if hospitals_to_show:
                for h in hospitals_to_show:
                    st.markdown(f"**{h['name']}**, {h['location']} — 📞 {h['contact']}")
            else:
                st.info("No hospitals found for your city. Showing top general hospitals.")
                for h in hospital_data:
                    st.markdown(f"**{h['name']}**, {h['location']} — 📞 {h['contact']}")

            # Prepare Report
            report_html = f"""
                <h2>Healthcare Prediction Report</h2>
                <p><strong>Name:</strong> {name}<br>
                <strong>Age:</strong> {age}<br>
                <strong>Gender:</strong> {gender}<br>
                <strong>Email:</strong> {email}<br>
                <strong>Date:</strong> {date}<br>
                <strong>Symptoms:</strong> {', '.join(selected_symptoms)}<br>
                <strong>Predicted Disease:</strong> {matched_disease}<br>
                <strong>Explanation:</strong> {explanation}<br>
                <strong>Health Tip:</strong> {tips}</p>
            """

            report_text = f"""
Healthcare Prediction Report
----------------------------
Name: {name}
Age: {age}
Gender: {gender}
Email: {email}
Date: {date}

Symptoms: {', '.join(selected_symptoms)}
Predicted Disease: {matched_disease}
Explanation: {explanation}
Health Tip: {tips}
"""
            st.download_button("⬇️ Download Report", report_text, file_name="healthcare_report.txt")

            # Send Email
            if email:
                try:
                    msg = MIMEText(report_html, "html")
                    msg['Subject'] = 'Your Healthcare Disease Prediction Report'
                    msg['From'] = st.secrets["email"]
                    msg['To'] = email

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(st.secrets["email"], st.secrets["password"])
                        server.send_message(msg)

                    st.success(f"📧 Report successfully sent to {email}")
                except Exception as e:
                    st.error(f"❌ Email sending failed: {e}")
        else:
            st.error("❌ Could not confidently predict the disease. Try selecting more symptoms.")
