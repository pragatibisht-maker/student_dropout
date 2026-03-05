import streamlit as st
import requests

st.set_page_config(page_title="Dropout Risk Predictor", layout="centered")
st.title("Student Dropout Risk Predictor")
st.markdown("Enter student details below to assess dropout risk.")

col1, col2 = st.columns(2)
with col1:
    study_time = st.slider("Study Time per week", 0, 10, 4)
    number_of_failures = st.number_input("Past Failures", 0, 20, 0)
    number_of_absences = st.number_input("Absences", 0, 100, 5)
with col2:
    grade_1 = st.slider("Grade Period 1 (0-20)", 0, 20, 12)
    grade_2 = st.slider("Grade Period 2 (0-20)", 0, 20, 12)
    final_grade = st.slider("Final Grade (0-20)", 0, 20, 12)

if st.button("Predict Dropout Risk"):
    payload = {
        "Study_Time": study_time,
        "Number_of_Failures": number_of_failures,
        "Number_of_Absences": number_of_absences,
        "Grade_1": grade_1,
        "Grade_2": grade_2,
        "Final_Grade": final_grade,
    }
    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            risk = result["risk_level"]
            prob = int(result["probability"] * 100)
            if risk == "High":
                st.error("Risk Level: " + risk + " | Dropout Probability: " + str(prob) + "%")
                st.warning("Immediate intervention recommended.")
            elif risk == "Medium":
                st.warning("Risk Level: " + risk + " | Dropout Probability: " + str(prob) + "%")
                st.info("Monitor closely and provide academic support.")
            else:
                st.success("Risk Level: " + risk + " | Dropout Probability: " + str(prob) + "%")
                st.info("Student is on track!")
            with st.expander("Raw API Response"):
                st.json(result)
        else:
            st.error("API Error: " + str(response.status_code))
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Flask API. Run python app.py first.")