"""
Student Dropout Risk Prediction — Streamlit Frontend
=====================================================
Run: streamlit run streamlit_app.py
Make sure your Flask API is running on http://127.0.0.1:5000
"""

import streamlit as st
import requests
import json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dropout Risk Predictor",
    page_icon="🎓",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0d0f14;
        color: #e8e8e8;
    }

    .stApp {
        background: linear-gradient(135deg, #0d0f14 0%, #111520 50%, #0d1117 100%);
    }

    /* Header */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7EB8F7, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #6b7280;
        font-size: 1rem;
        font-weight: 300;
        letter-spacing: 0.3px;
    }

    /* Card */
    .card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
    }
    .card-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #7EB8F7;
        margin-bottom: 1rem;
    }

    /* Result boxes */
    .result-high {
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(220,38,38,0.05));
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .result-medium {
        background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.05));
        border: 1px solid rgba(251,191,36,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .result-low {
        background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(16,185,129,0.05));
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
    }
    .result-label {
        font-family: 'Syne', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.3rem 0;
    }
    .result-prob {
        font-size: 0.95rem;
        color: #9ca3af;
        margin-top: 0.4rem;
    }

    /* Probability bar */
    .prob-bar-bg {
        background: rgba(255,255,255,0.06);
        border-radius: 999px;
        height: 8px;
        margin: 1rem 0 0.3rem;
        overflow: hidden;
    }
    .prob-bar-fill-high   { background: linear-gradient(90deg, #f87171, #ef4444); border-radius: 999px; height: 8px; }
    .prob-bar-fill-medium { background: linear-gradient(90deg, #fbbf24, #f59e0b); border-radius: 999px; height: 8px; }
    .prob-bar-fill-low    { background: linear-gradient(90deg, #34d399, #10b981); border-radius: 999px; height: 8px; }

    /* Divider */
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 1.5rem 0;
    }

    /* Streamlit widget overrides */
    .stSlider > div > div > div { background: #7EB8F7 !important; }
    .stNumberInput input, .stSelectbox select {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7EB8F7, #A78BFA) !important;
        color: #0d0f14 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        width: 100% !important;
        letter-spacing: 0.5px;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    label, .stSlider label { color: #d1d5db !important; font-size: 0.9rem !important; }
    .stNumberInput label   { color: #d1d5db !important; }

    /* Footer */
    .footer {
        text-align: center;
        color: #374151;
        font-size: 0.78rem;
        padding: 2rem 0 1rem;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎓 Dropout Risk Predictor</h1>
    <p>Enter student academic details to assess dropout risk using AI</p>
</div>
""", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">📋 Academic Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    study_time = st.slider(
        "Study Time (hrs/week)",
        min_value=0, max_value=10, value=4, step=1,
        help="1=<2hrs, 2=2-5hrs, 3=5-10hrs, 4=>10hrs"
    )
    number_of_failures = st.number_input(
        "Number of Past Failures",
        min_value=0, max_value=20, value=0, step=1
    )
    number_of_absences = st.number_input(
        "Number of Absences",
        min_value=0, max_value=100, value=5, step=1
    )

with col2:
    grade_1 = st.slider("Grade - Period 1 (0–20)", min_value=0, max_value=20, value=12)
    grade_2 = st.slider("Grade - Period 2 (0–20)", min_value=0, max_value=20, value=12)
    final_grade = st.slider("Final Grade (0–20)",   min_value=0, max_value=20, value=12)

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict button ────────────────────────────────────────────────────────────
predict_clicked = st.button("⚡ Predict Dropout Risk")

if predict_clicked:
    payload = {
        "Study_Time":         study_time,
        "Number_of_Failures": number_of_failures,
        "Number_of_Absences": number_of_absences,
        "Grade_1":            grade_1,
        "Grade_2":            grade_2,
        "Final_Grade":        final_grade,
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            result      = response.json()
            risk        = result["risk_level"]
            probability = result["probability"]
            pct         = int(probability * 100)

            # Risk styling
            if risk == "High":
                css_class  = "result-high"
                bar_class  = "prob-bar-fill-high"
                emoji      = "🔴"
                advice     = "Immediate intervention recommended. Connect student with academic counselor."
            elif risk == "Medium":
                css_class  = "result-medium"
                bar_class  = "prob-bar-fill-medium"
                emoji      = "🟡"
                advice     = "Monitor closely. Consider additional academic support or mentoring."
            else:
                css_class  = "result-low"
                bar_class  = "prob-bar-fill-low"
                emoji      = "🟢"
                advice     = "Student is on track. Keep encouraging consistent study habits."

            st.markdown(f"""
            <div class="{css_class}">
                <div style="font-size:0.8rem;letter-spacing:2px;text-transform:uppercase;color:#9ca3af;">
                    DROPOUT RISK LEVEL
                </div>
                <div class="result-label">{emoji} {risk} Risk</div>
                <div class="result-prob">Dropout probability: <strong>{pct}%</strong></div>
                <div class="prob-bar-bg">
                    <div class="{bar_class}" style="width:{pct}%"></div>
                </div>
                <hr class="divider">
                <div style="font-size:0.9rem;color:#d1d5db;">💡 {advice}</div>
            </div>
            """, unsafe_allow_html=True)

            # Raw JSON expander
            with st.expander("View raw API response"):
                st.json(result)

        else:
            st.error(f"API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Flask API. Make sure it's running with: `python app.py`")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Student Dropout Risk Prediction System &nbsp;·&nbsp; Powered by Logistic Regression + Flask + Streamlit
</div>
""", unsafe_allow_html=True)