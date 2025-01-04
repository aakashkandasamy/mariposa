import json
from typing import List, Dict
from app.core.models.schemas import PatientInput, TherapyPlan
from app.core.services.research_service import ResearchService
from app.core.utils.exceptions import NoMatchingConditionsError
from app.core.services.technique_database import TechniqueDatabase

class TherapyPlanGenerator:
    def __init__(self):
        self.research_service = ResearchService()
        self.disorders = self._load_disorders()

    def _load_disorders(self) -> Dict:
        with open('data/mock/disorders.json', 'r') as f:
            return json.load(f)

    def generate_therapy_plan(self, patient_input: PatientInput) -> TherapyPlan:
        # Analyze symptoms to identify possible conditions
        condition_matches = self.research_service.analyze_symptoms(patient_input.symptoms)
        
        # Get the most likely condition
        if not condition_matches:
            # Analyze the symptoms to provide specific suggestions
            symptoms_length = len(patient_input.symptoms.split())
            suggestions = []
            
            if symptoms_length < 10:
                suggestions.append("Please provide a more detailed description of your symptoms")
            
            if "feel" not in patient_input.symptoms.lower():
                suggestions.append("Describe how these symptoms make you feel")
                
            if "when" not in patient_input.symptoms.lower():
                suggestions.append("Include when these symptoms typically occur")
                
            if "impact" not in patient_input.symptoms.lower() and "affect" not in patient_input.symptoms.lower():
                suggestions.append("Explain how these symptoms impact your daily life")
            
            # Add general suggestions if no specific ones were generated
            if not suggestions:
                suggestions = [
                    "Include how long you've been experiencing these symptoms",
                    "Mention any triggers you've noticed",
                    "Describe any changes in sleep, appetite, or energy levels",
                    "Note any patterns in when symptoms get better or worse",
                    "Include any past treatments or coping strategies you've tried"
                ]
            
            raise NoMatchingConditionsError(patient_input.symptoms, suggestions)
        
        # Convert condition matches to the format needed for TherapyPlan
        identified_conditions = [cond for cond, _ in condition_matches]
        confidence_scores = {cond: score for cond, score in condition_matches}
        
        # Get primary condition (highest confidence)
        primary_condition = identified_conditions[0]
        
        # Get DSM-5 info for primary condition
        dsm5_info = self.research_service.get_dsm5_criteria(primary_condition)
        
        # Get research articles for the condition
        articles = self.research_service.get_scholarly_articles(primary_condition)
        treatment_analysis = self.research_service.analyze_treatment_effectiveness(articles)

        # Determine therapy type based on research
        therapy_types = list(treatment_analysis.keys())
        therapy_type = therapy_types[0] if therapy_types else "Cognitive Behavioral Therapy"

        # Get session frequency based on severity
        session_frequencies = {
            "low": "bi-weekly",
            "moderate": "weekly",
            "severe": "twice-weekly"
        }
        session_frequency = session_frequencies[patient_input.severity.value]

        # Generate goals based on DSM-5 criteria
        goals = dsm5_info.get("treatment_goals", [
            "Reduce symptom severity",
            "Develop coping mechanisms",
            "Improve daily functioning"
        ])

        # Get recommended techniques
        techniques = dsm5_info.get("recommended_techniques", [
            f"Regular {therapy_type} sessions",
            "Mindfulness exercises",
            "Behavioral activation",
            "Stress management techniques"
        ])

        # Determine duration
        duration = dsm5_info.get("recommended_duration", "12-16 weeks")

        # Ensure all recommended techniques have complete information
        validated_techniques = []
        technique_db = TechniqueDatabase()
        
        for technique in techniques:
            technique_info = technique_db.get_technique_info(technique)
            if technique_info:
                validated_techniques.append(technique)
        
        therapy_plan = TherapyPlan(
            identified_conditions=identified_conditions,
            confidence_scores=confidence_scores,
            therapy_type=therapy_type,
            session_frequency=session_frequency,
            goals=goals,
            techniques=validated_techniques,  # Use validated techniques
            duration=duration
        )

        return therapy_plan 