import streamlit as st
import json
import smtplib
from email.message import EmailMessage

# Sample hospital data
hospital_data = [
    {"name": "Apollo Hospital", "location": "Hyderabad", "contact": "040-12345678"},
    {"name": "Yashoda Hospital", "location": "Secunderabad", "contact": "040-87654321"},
    {"name": "KIMS Hospital", "location": "Hyderabad", "contact": "040-11223344"},
    {"name": "AIIMS", "location": "Delhi", "contact": "011-22334455"},
    {"name": "NIMS", "location": "Hyderabad", "contact": "040-44556677"},
]

# Sample disease information
disease_info = {
    "Malaria": "Caused by Plasmodium parasites transmitted by mosquito bites.",
    "Diabetes": "A chronic condition that affects how your body processes blood sugar.",
    "Cold": "A viral infectious disease of the upper respiratory tract.",
    "Flu": "A contagious respiratory illness caused by influenza viruses.",
    "Typhoid": "A bacterial infection due to Salmonella typhi spread through contaminated food and water."
}

# Health tips data
health_tips = {
    "Malaria": ["Use mosquito nets.", "Avoid stagnant water.", "Use mosquito repellents."],
    "Diabetes": ["Monitor blood sugar levels.", "Exercise regularly.", "Eat low sugar foods."],
    "Cold": ["Drink warm fluids.", "Rest well.", "Use steam inhalation."],
    "Flu": ["Get vaccinated.", "Stay hydrated.", "Avoid crowded places."],
    "Typhoid": ["Drink clean water.", "Maintain hygiene.", "Eat cooked food."]
}

def send_email(receiver_email, subject, content):
    sender_email = st.secrets["email"]
    password = st.secrets["password"]
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

st.set_page_config(page_title="Disease Prediction App", layout="centered")
st.title("🤖 AI Disease Prediction & Care Assistant")

# Tabs for better layout
tab1, tab2 = st.tabs(["📝 Health Form", "🔍 Prediction Result"])

with tab1:
    with st.form("disease_form"):
        name = st.text_input("👤 Your Name")
        age = st.number_input("🎂 Age", min_value=1, max_value=120)
        gender = st.radio("🚻 Gender", ["Male", "Female", "Other"], horizontal=True)
        symptoms = st.text_area("😷 Enter your symptoms (comma-separated)")
        city = st.text_input("🏙️ City")
        email = st.text_input("📧 Email to receive report")
        submitted = st.form_submit_button("🔍 Predict Disease")

if submitted:
    symptom_list = [s.strip().lower() for s in symptoms.split(",")]
    matched_disease = None

    for disease in disease_info:
        if disease.lower() in symptoms.lower():
            matched_disease = disease
            break

    if matched_disease:
        explanation = disease_info[matched_disease]
        with tab2:
            st.markdown(f"""
                <div style='padding:10px; background-color:#e0f7fa; border-radius:10px;'>
                    <h3 style='color:#00796b;'>🎯 <u>Predicted Disease:</u> {matched_disease}</h3>
                    <p><b>📘 Cause:</b> {explanation}</p>
                </div>
            """, unsafe_allow_html=True)

            if matched_disease in health_tips:
                st.markdown(f"""
                <div style='border:2px solid #4caf50; padding:10px; border-radius:10px; background-color:#e8f5e9;'>
                    <h4>💡 <u>Health Tips for {matched_disease}</u></h4>
                    <ul>
                        {''.join([f"<li>{tip}</li>" for tip in health_tips[matched_disease]])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            st.subheader("🏥 Recommended Hospitals")
            input_city = city.lower().strip()
            matched_hospitals = [h for h in hospital_data if input_city and input_city in h["location"].lower()]
            hospitals_to_show = matched_hospitals if matched_hospitals else hospital_data

            for hospital in hospitals_to_show:
                st.markdown(f"""
                    - 🏥 **{hospital['name']}**  
                      📍 Location: *{hospital['location']}*  
                      ☎️ Contact: `{hospital['contact']}`
                """)

            # Report
            report = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Symptoms": symptom_list,
                "Predicted Disease": matched_disease,
                "Explanation": explanation,
                "City": city
            }
            report_json = json.dumps(report, indent=4)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button("⬇️ Download Report", report_json, file_name="report.json")
            with col2:
                if email:
                    send_email(email, "Your Disease Prediction Report", report_json)
                    st.success("📩 Report sent to your email!")
    else:
        with tab2:
            st.error("❌ No disease match found. Please recheck your symptoms.")
