from typing import List, Dict
from app.core.models.schemas import PatientInput, TherapyPlan
from app.core.services.research_service import ResearchService
from app.core.utils.exceptions import NoMatchingConditionsError
from app.core.services.technique_database import TechniqueDatabase

class TherapyPlanGenerator:
    def __init__(self):
        self.research_service = ResearchService()
        self.technique_db = TechniqueDatabase()

    def generate_therapy_plan(self, patient_input: PatientInput) -> TherapyPlan:
        # Analyze symptoms to identify possible conditions
        condition_matches = self.research_service.analyze_symptoms(patient_input.symptoms)
        
        if not condition_matches:
            suggestions = []
            symptoms_length = len(patient_input.symptoms.split())
            
            if symptoms_length < 10:
                suggestions.append("Please provide a more detailed description of your symptoms")
            if "feel" not in patient_input.symptoms.lower():
                suggestions.append("Describe how these symptoms make you feel")
            if "when" not in patient_input.symptoms.lower():
                suggestions.append("Include when these symptoms typically occur")
            if "impact" not in patient_input.symptoms.lower() and "affect" not in patient_input.symptoms.lower():
                suggestions.append("Explain how these symptoms impact your daily life")
            
            raise NoMatchingConditionsError(patient_input.symptoms, suggestions)
        
        # Convert condition matches to the format needed for TherapyPlan
        identified_conditions = [cond for cond, _ in condition_matches]
        confidence_scores = {cond: score for cond, score in condition_matches}
        
        # Get primary condition (highest confidence)
        primary_condition = identified_conditions[0]
        
        # Get DSM-5 info for primary condition
        dsm5_info = self.research_service.get_dsm5_criteria(primary_condition)
        
        # Get session frequency based on severity
        session_frequencies = {
            "low": "bi-weekly",
            "moderate": "weekly",
            "severe": "twice-weekly"
        }
        session_frequency = session_frequencies[patient_input.severity.value]

        # Get therapy type and other details from DSM-5 data
        therapy_type = dsm5_info.get("name", "Cognitive Behavioral Therapy")
        goals = dsm5_info.get("treatment_goals", ["Reduce symptoms", "Improve daily functioning"])
        techniques = dsm5_info.get("recommended_techniques", ["Regular therapy sessions"])
        duration = dsm5_info.get("recommended_duration", "12-16 weeks")

        # Validate techniques
        validated_techniques = []
        for technique in techniques:
            technique_info = self.technique_db.get_technique_info(technique)
            if technique_info:
                validated_techniques.append(technique)
        
        return TherapyPlan(
            identified_conditions=identified_conditions,
            confidence_scores=confidence_scores,
            therapy_type=therapy_type,
            session_frequency=session_frequency,
            goals=goals,
            techniques=validated_techniques,
            duration=duration
        ) 