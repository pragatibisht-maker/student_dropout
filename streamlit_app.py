import streamlit as st
import numpy as np
import pandas as pd
from model.loader import load_artifacts

# Load model + artifacts
artifacts = load_artifacts()
model = artifacts["model"]
scaler = artifacts["scaler"]
features = artifacts["features"]   # IMPORTANT

# UI
st.set_page_config(page_title="Dropout Risk Predictor", layout="centered")
st.title("🎓 Student Dropout Risk Predictor")

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

# Prediction
if st.button("Predict Dropout Risk"):

    # 🔥 Create full feature dictionary (all 33 features)
    input_dict = {col: 0 for col in features}

    # Fill only known values
    input_dict["Study_Time"] = study_time
    input_dict["Number_of_Failures"] = number_of_failures
    input_dict["Number_of_Absences"] = number_of_absences
    input_dict["Grade_1"] = grade_1
    input_dict["Grade_2"] = grade_2
    input_dict["Final_Grade"] = final_grade

    # Convert to DataFrame (IMPORTANT)
    input_df = pd.DataFrame([input_dict])

    # Scale input
    input_scaled = scaler.transform(input_df)

    # Predict
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    prob = int(probability * 100)

    # Output
    if prob > 70:
        st.error(f"⚠️ Risk Level: High | Dropout Probability: {prob}%")
        st.warning("Immediate intervention recommended.")
    elif prob > 40:
        st.warning(f"⚠️ Risk Level: Medium | Dropout Probability: {prob}%")
        st.info("Monitor closely and provide academic support.")
    else:
        st.success(f"✅ Risk Level: Low | Dropout Probability: {prob}%")
        st.info("Student is on track!")
