import streamlit as st
from api.routes import therapy_routes
from core.services import plan_service

st.set_page_config(
    page_title="Mariposa - AI Therapy Planning",
    page_icon="🦋",
    layout="wide"
)

st.title("🦋 Mariposa")
st.subheader("AI-Powered Therapy Plan Optimization")

with st.form("therapy_plan_form"):
    patient_name = st.text_input("Patient Name")
    condition = st.selectbox(
        "Primary Condition",
        ["Depression", "Anxiety", "PTSD", "OCD", "Other"]
    )
    severity = st.slider("Condition Severity", 1, 10, 5)
    
    submitted = st.form_submit_button("Generate Plan")
    
    if submitted:
        # Here you would integrate with your existing services
        st.info("Generating personalized therapy plan...")
        # Add actual integration with your backend services here
        
        st.success("Therapy plan generated successfully!")
        # Display the generated plan 