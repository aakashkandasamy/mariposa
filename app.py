import streamlit as st
from app.core.models.schemas import PatientInput, SeverityLevel
from app.core.services.plan_service import TherapyPlanGenerator
from app.core.utils.exceptions import NoMatchingConditionsError
from typing import List, Dict
from datetime import datetime

st.set_page_config(
    page_title="Mariposa - Plan Generator",
    page_icon="🦋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_supported_conditions():
    """Display currently supported conditions"""
    with st.expander("📚 Currently Supported Conditions"):
        st.markdown("""
        Mariposa can currently identify and provide recommendations for:
        
        - **Anxiety Disorders**
          - Generalized Anxiety Disorder (GAD)
          - Social Anxiety Disorder
          - Panic Disorder
        
        - **Mood Disorders**
          - Major Depressive Disorder
        
        - **Crisis Situations**
          - Suicidal Ideation
          - Mental Health Crisis
        
        *Note: This list is continuously updated based on DSM-5 criteria and current research.*
        """)

def check_for_crisis(symptoms: str) -> bool:
    """Check for crisis keywords in symptoms"""
    crisis_keywords = [
        "suicide", "kill myself", "die", "end my life", "self harm",
        "hurt myself", "don't want to live", "want to die"
    ]
    return any(keyword in symptoms.lower() for keyword in crisis_keywords)

def show_crisis_resources():
    """Display crisis resources and helplines"""
    st.error("🚨 IMMEDIATE SUPPORT AVAILABLE 🚨")
    st.markdown("""
        ### Crisis Helplines - Available 24/7:
        
        - **National Suicide Prevention Lifeline (US)**: 
          - Call 988 or 1-800-273-8255
          - [Click to Chat](https://suicidepreventionlifeline.org/chat/)
        
        - **Crisis Text Line**: 
          - Text HOME to 741741
        
        ### Please Reach Out:
        - Call emergency services (911 in US)
        - Go to the nearest emergency room
        - Contact a mental health professional immediately
        - Reach out to a trusted friend or family member
        
        You are not alone. Help is available and people care about you.
    """)

def main():
    st.title("🦋 Mariposa")
    st.subheader("AI-Powered Therapy Plan Generator")
    
    # Show supported conditions at the top
    show_supported_conditions()
    
    # Create two columns for the main layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Severity Selection
        severity = st.radio(
            "How severely do these symptoms affect your daily life?",
            options=[SeverityLevel.LOW, SeverityLevel.MODERATE, SeverityLevel.SEVERE],
            format_func=lambda x: {
                "low": "😊 Mildly affecting daily life",
                "moderate": "😐 Moderately affecting daily life",
                "severe": "😟 Severely affecting daily life"
            }[x.value]
        )
        
        # Schedule Information
        st.subheader("Availability")
        availability = st.multiselect(
            "Which days are you available?",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
    
    with col2:
        with st.form("therapy_plan_form"):
            symptoms = st.text_area(
                "Describe your symptoms",
                height=200,
                help="Please describe your symptoms, feelings, and experiences in detail.",
                placeholder="Example: I've been feeling anxious and overwhelmed..."
            )

            submitted = st.form_submit_button("Generate Therapy Plan")

            if submitted:
                if check_for_crisis(symptoms):
                    show_crisis_resources()
                
                if not all([symptoms, severity, availability]):
                    st.error("Please fill in all fields")
                    return

                try:
                    patient_input = PatientInput(
                        symptoms=symptoms,
                        severity=severity,
                        schedule={"availability": availability}
                    )

                    planner = TherapyPlanGenerator()
                    therapy_plan = planner.generate_therapy_plan(patient_input)

                    # Display the plan
                    st.success("Your therapy plan is ready!")
                    
                    st.markdown("### Identified Conditions")
                    for condition, confidence in therapy_plan.confidence_scores.items():
                        st.write(f"**{condition.replace('_', ' ').title()}**")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.progress(confidence)
                        with col2:
                            st.write(f"{confidence*100:.1f}%")
                        
                        # Show matching criteria
                        if condition in st.session_state.condition_details:
                            details = st.session_state.condition_details[condition]
                            with st.expander("See matching criteria"):
                                st.markdown("#### Why this condition was identified:")
                                for criterion in details["matching_criteria"]:
                                    st.markdown(f"• {criterion}")
                                
                                st.markdown("\n#### All DSM-5 Criteria for this condition:")
                                for criterion in details["all_criteria"]:
                                    st.markdown(f"• {criterion}")

                    st.markdown("### Treatment Plan")
                    st.write("**Type of Therapy:**", therapy_plan.therapy_type)
                    st.write("**Session Frequency:**", therapy_plan.session_frequency)
                    st.write("**Duration:**", therapy_plan.duration)

                    st.markdown("### Treatment Goals")
                    for goal in therapy_plan.goals:
                        st.markdown(f"• {goal}")

                    st.markdown("### Recommended Techniques")
                    for technique in therapy_plan.techniques:
                        st.markdown(f"• {technique}")

                except Exception as e:
                    st.error(f"Error generating therapy plan: {str(e)}")

if __name__ == "__main__":
    main() 