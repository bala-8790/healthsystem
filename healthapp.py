import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# ---------- Session State ----------
if "prev_symptoms" not in st.session_state:
    st.session_state.prev_symptoms = []

# ---------- Configuration ----------
st.set_page_config(page_title="🧠 Healthcare Predictor", layout="wide")
st.title("🧬 Smart Disease Predictor & Report Generator")

# ---------- Symptoms and Disease Mappings ----------
symptoms_list = sorted([
    "fever", "headache", "fatigue", "nausea", "vomiting", "cough", "cold", "muscle_pain",
    "joint_pain", "rash", "abdominal_pain", "loss_of_appetite", "diarrhea", "constipation",
    "chills", "sore_throat", "weight_loss", "night_sweats", "breathlessness", "chest_pain",
    "vision_problem", "excessive_thirst", "frequent_urination", "bleeding_gums",
    "unexplained_bleeding", "itching", "yellow_skin", "swollen_lymph_nodes",
    "seizures", "speech_difficulty", "paralysis", "confusion", "memory_loss"
])

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
    "Cancer": "Uncontrolled abnormal cell growth, may affect any organ.",
    "Tuberculosis": "Chronic bacterial lung infection, spreads via droplets.",
    "Diabetes": "High blood sugar levels due to insulin problems.",
    "Thyroid": "Hormonal imbalance affecting metabolism and mood.",
    "Covid-19": "Respiratory disease caused by coronavirus SARS-CoV-2.",
    "HIV/AIDS": "Virus attacking immune system, transmitted through fluids.",
    "Brain Tumor": "Abnormal brain cell growth affecting cognition.",
    "Blood Clotting Disorder": "Conditions affecting normal blood clotting."
}

disease_tips = {
    "Malaria": "Use mosquito nets and take antimalarials.",
    "Dengue": "Rest, hydration, and monitor platelet count.",
    "Chickenpox": "Use calamine lotion, rest, avoid scratching.",
    "Typhoid": "Take antibiotics as prescribed. Hydrate well.",
    "Pneumonia": "Antibiotics, oxygen support if needed, rest.",
    "Cancer": "Early detection, chemo/radiation, regular consult.",
    "Tuberculosis": "Complete full TB regimen, avoid exposure.",
    "Diabetes": "Manage with diet, exercise, insulin/orals.",
    "Thyroid": "Monitor hormone levels. Medications as needed.",
    "Covid-19": "Isolation, oxygen support, symptomatic care.",
    "HIV/AIDS": "Antiretrovirals, immunity support, hygiene.",
    "Brain Tumor": "Surgery, radiation, neuro consults.",
    "Blood Clotting Disorder": "Avoid injury, meds to thin blood."
}

hospital_data = [
    {"name": "Apollo Hospitals", "location": "Hyderabad", "contact": "040-23607777"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-26588500"},
    {"name": "Fortis Healthcare", "location": "Bangalore", "contact": "080-66214444"},
    {"name": "Care Hospitals", "location": "Hyderabad", "contact": "040-30417777"},
    {"name": "KIMS", "location": "Secunderabad", "contact": "040-44885000"}
]

# ---------- Step 1: User Info ----------
with st.expander("📋 Step 1: Enter Patient Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Full Name")
        age = st.number_input("🎂 Age", 1, 120)
        email = st.text_input("📧 Email")
    with col2:
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        city = st.text_input("🏙️ Your City")
        date = datetime.now().strftime("%Y-%m-%d")
        st.markdown(f"🗓️ Date: `{date}`")

# ---------- Step 2: Symptoms ----------
with st.expander("🤒 Step 2: Select Your Symptoms", expanded=True):
    selected_symptoms = st.multiselect("🔎 Search and select your symptoms", symptoms_list)
    if selected_symptoms:
        st.success(f"✅ {len(selected_symptoms)} symptom(s) selected.")
    if st.session_state.prev_symptoms:
        st.markdown("🕓 **Previous Session Symptoms:**")
        st.code(", ".join(st.session_state.prev_symptoms))

# ---------- Step 3: Submit and Predict ----------
if st.button("🚑 Predict Disease"):
    if len(selected_symptoms) < 2:
        st.warning("⚠️ Please select at least 2 symptoms.")
    else:
        st.session_state.prev_symptoms = selected_symptoms

        # Match logic
        matched_disease, highest_score = None, 0
        for disease, symptoms in disease_symptom_map.items():
            match = len(set(symptoms) & set(selected_symptoms))
            score = (2 * match) / (len(symptoms) + len(selected_symptoms))
            if score > highest_score and match >= 2:
                matched_disease = disease
                highest_score = score

        if matched_disease:
            explanation = disease_explanations.get(matched_disease, "Not available.")
            tip = disease_tips.get(matched_disease, "No tip available.")

            st.balloons()
            st.markdown("## 🧾 Prediction Summary")
            st.metric("Disease Predicted", matched_disease)
            st.success(f"📚 **Cause**: {explanation}")
            st.info(f"💡 **Health Tip**: {tip}")

            with st.expander("🏥 Recommended Hospitals"):
                filtered = [h for h in hospital_data if city.lower() in h["location"].lower()]
                for h in filtered or hospital_data:
                    st.markdown(f"- **{h['name']}**, {h['location']} — 📞 {h['contact']}")

            report = f"""
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
Health Tip: {tip}
"""
            st.download_button("⬇️ Download Text Report", report, file_name="healthcare_report.txt")

            if email:
                try:
                    html_msg = f"<h3>{matched_disease}</h3><p><b>Cause:</b> {explanation}<br><b>Tip:</b> {tip}</p>"
                    msg = MIMEText(html_msg, "html")
                    msg['Subject'] = '🧬 Your Healthcare Prediction Report'
                    msg['From'] = st.secrets["email"]
                    msg['To'] = email

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(st.secrets["email"], st.secrets["password"])
                        server.send_message(msg)

                    st.success(f"📧 Email sent to {email}")
                except Exception as e:
                    st.error(f"Email failed: {e}")
        else:
            st.error("❌ Unable to predict. Try more symptoms.")
