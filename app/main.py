import streamlit as st
from app.core.models.schemas import PatientInput, SeverityLevel
from app.core.services.plan_service import TherapyPlanGenerator
from app.core.utils.exceptions import NoMatchingConditionsError
from typing import List, Dict
from datetime import datetime
from app.core.services.calendar_planner import TherapyCalendarPlanner

st.set_page_config(
    page_title="Mariposa - Therapy Plan Optimizer",
    page_icon="🦋",
    layout="wide"
)

def check_for_crisis(symptoms: str) -> bool:
    crisis_keywords = [
        "suicide", "kill myself", "die", "end my life", "self harm",
        "hurt myself", "don't want to live", "want to die"
    ]
    return any(keyword in symptoms.lower() for keyword in crisis_keywords)

def show_crisis_resources():
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

def show_supported_conditions():
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

def show_dsm5_criteria(condition: str, dsm5_data: dict):
    with st.expander("📖 DSM-5 Criteria"):
        if condition in dsm5_data:
            disorder_info = dsm5_data[condition]
            st.markdown(f"### {disorder_info['name']}")
            
            st.markdown("#### Diagnostic Criteria:")
            for criterion in disorder_info['diagnostic_criteria']:
                st.markdown(f"- {criterion}")
            
            st.markdown("\n*Source: Diagnostic and Statistical Manual of Mental Disorders (DSM-5)*")
        else:
            st.warning("DSM-5 criteria not available for this condition.")

def show_research_articles(articles: List[Dict]):
    with st.expander("🔍 Related Research"):
        if articles:
            st.markdown("### Recent Research Articles")
            for article in articles:
                st.markdown(f"""
                #### {article['title']}
                **Authors:** {article['author']}  
                **Year:** {article['year']}
                
                **Abstract:**  
                {article['abstract']}
                
                ---
                """)
        else:
            st.info("No research articles available for this condition.")

def show_therapy_calendar(schedule: List[Dict]):
    st.markdown("### 📅 Your 4-Week Therapy Schedule")
    
    current_week = None
    for session in schedule:
        session_date = datetime.strptime(session['date'], "%Y-%m-%d")
        week_num = (session_date - datetime.now()).days // 7 + 1
        
        if week_num != current_week:
            current_week = week_num
            st.markdown(f"\n#### Week {week_num}")
        
        # Create a container for each session
        with st.container():
            # Session Header
            st.markdown(f"""
            ### 📆 {session['date']} ({session['day']})
            
            **Activity:** {session['activity']}
            
            **Type:** {session['type']}
            
            **Duration:** {session['duration']}
            """)
            
            technique_details = session.get('technique_details', {})
            if technique_details:
                # About Section
                st.markdown("### About this Technique")
                st.write(technique_details.get('description', ''))
                
                # Steps Section
                st.markdown("### Steps")
                for step in technique_details.get('steps', []):
                    st.markdown(f"• {step}")
                
                # Exercise Section
                st.markdown("### Today's Exercise")
                exercises = technique_details.get('exercises', [])
                if exercises:
                    exercise = exercises[0]
                    st.markdown(f"**{exercise['name']}** ({exercise['duration']})")
                    for instruction in exercise['instructions']:
                        st.markdown(f"• {instruction}")
                
                # Resources Section
                st.markdown("### Additional Resources")
                for resource in technique_details.get('resources', []):
                    st.markdown(f"• [{resource['title']}]({resource['url']}) ({resource['type']})")
            
            st.markdown("---")  # Divider between sessions

def main():
    st.title("🦋 Mariposa")
    st.subheader("AI-Powered Therapy Plan Optimizer")
    
    # Show supported conditions at the top
    show_supported_conditions()
    
    # Create two columns for the main layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Severity Selection outside the form for better UX
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
            # Symptoms Input
            symptoms = st.text_area(
                "Describe your symptoms",
                height=200,
                help="Please describe your symptoms, feelings, and experiences in detail. The more information you provide, the better we can help.",
                placeholder="Example: I've been feeling anxious and overwhelmed for the past 3 months. My heart races when I'm in social situations..."
            )

            submitted = st.form_submit_button("Generate Therapy Plan")

            if submitted:
                # Check for crisis keywords first
                if check_for_crisis(symptoms):
                    show_crisis_resources()
                
                if not all([symptoms, severity, availability]):
                    st.error("Please fill in all fields")
                    return

                # Create patient input
                patient_input = PatientInput(
                    symptoms=symptoms,
                    severity=severity,
                    schedule={"availability": availability}
                )

                try:
                    # Generate plan
                    planner = TherapyPlanGenerator()
                    therapy_plan = planner.generate_therapy_plan(patient_input)
                    
                    # Display identified conditions
                    st.success("Analysis Complete!")
                    
                    # Display results in a clean layout
                    st.markdown("### Symptom Analysis")
                    for condition, confidence in therapy_plan.confidence_scores.items():
                        st.write(f"**{condition.replace('_', ' ').title()}**")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.progress(confidence)
                        with col2:
                            st.write(f"{confidence*100:.1f}%")
                        
                        # Show DSM-5 criteria for each identified condition
                        show_dsm5_criteria(condition, planner.research_service.dsm5_data)
                        
                        # Show research articles for each condition
                        articles = planner.research_service.get_scholarly_articles(condition)
                        show_research_articles(articles)
                    
                    st.markdown("### Your Personalized Therapy Plan")
                    
                    # Treatment info in expandable sections
                    with st.expander("📋 Treatment Overview", expanded=True):
                        st.write("**Therapy Type:**", therapy_plan.therapy_type)
                        st.write("**Session Frequency:**", therapy_plan.session_frequency)
                        st.write("**Duration:**", therapy_plan.duration)
                    
                    with st.expander("🎯 Goals", expanded=True):
                        for goal in therapy_plan.goals:
                            st.write(f"• {goal}")
                    
                    with st.expander("⚡ Recommended Techniques", expanded=True):
                        for technique in therapy_plan.techniques:
                            st.write(f"• {technique}")

                    st.info("⚠️ Note: This is an AI-generated suggestion. Please consult with a mental health professional for a proper diagnosis and treatment plan.")

                    # In the main function, after generating the therapy plan:
                    calendar_planner = TherapyCalendarPlanner()
                    schedule = calendar_planner.generate_weekly_schedule(
                        availability=patient_input.schedule.availability,
                        therapy_type=therapy_plan.therapy_type,
                        session_frequency=therapy_plan.session_frequency,
                        techniques=therapy_plan.techniques
                    )
                    show_therapy_calendar(schedule)

                    # In the main function, after generating the schedule:
                    st.session_state.therapy_schedule = schedule

                except NoMatchingConditionsError as e:
                    st.error("We need more information to help you better")
                    
                    st.markdown("### Suggestions to improve your description:")
                    for suggestion in e.suggestions:
                        st.markdown(f"• {suggestion}")
                    
                    with st.expander("See example description"):
                        st.info(
                            "I've been feeling anxious and overwhelmed for the past 3 months. "
                            "My heart races when I'm in social situations, and I often avoid "
                            "meeting new people. These feelings are worst in the morning and "
                            "affect my work performance. I have trouble sleeping and often feel "
                            "tired. I've tried deep breathing which helps sometimes, but the "
                            "anxiety always returns."
                        )
                    
                except Exception as e:
                    st.error(f"Error generating therapy plan: {str(e)}")

if __name__ == "__main__":
    main() 