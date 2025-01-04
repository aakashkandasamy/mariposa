import json
from typing import List, Dict
from core.models.schemas import PatientInput, TherapyPlan
from core.services.research_service import ResearchService

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
            raise ValueError("Unable to identify any matching conditions")
        
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

        return TherapyPlan(
            identified_conditions=identified_conditions,
            confidence_scores=confidence_scores,
            therapy_type=therapy_type,
            session_frequency=session_frequency,
            goals=goals,
            techniques=techniques,
            duration=duration
        ) 