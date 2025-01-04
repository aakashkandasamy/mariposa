import json
from typing import List, Dict
from app.core.models.schemas import PatientInput, TherapyPlan
from app.core.services.research_service import ResearchService
from app.core.utils.exceptions import NoMatchingConditionsError
from app.core.services.technique_database import TechniqueDatabase
import streamlit as st

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
        
        # Store condition matches in session state for display
        st.session_state.condition_details = {}
        for condition, score, matching_criteria in condition_matches:
            details = self.research_service.get_condition_details(condition, matching_criteria)
            st.session_state.condition_details[condition] = details
        
        # Convert condition matches to the format needed for TherapyPlan
        identified_conditions = [cond for cond, score, _ in condition_matches if score > 0.1]  # Lower threshold
        if not identified_conditions:
            identified_conditions = [condition_matches[0][0]]  # Take best match if none above threshold
        
        confidence_scores = {cond: score for cond, score, _ in condition_matches}
        
        # Get primary condition (highest confidence)
        primary_condition = identified_conditions[0]
        dsm5_info = self.research_service.get_dsm5_criteria(primary_condition)
        
        # Determine session frequency based on severity and availability
        available_days = len(patient_input.schedule.availability)
        severity_level = patient_input.severity.value
        
        if severity_level == "severe":
            sessions_per_week = min(2, available_days)  # Twice weekly if possible
            session_frequency = "twice-weekly" if available_days >= 2 else "weekly"
        elif severity_level == "moderate":
            sessions_per_week = 1  # Weekly
            session_frequency = "weekly"
        else:  # low severity
            sessions_per_week = 0.5  # Bi-weekly
            session_frequency = "bi-weekly"
        
        # Adjust if not enough available days
        if available_days < sessions_per_week:
            session_frequency = "weekly"
            sessions_per_week = 1
        
        # Get recommended techniques based on availability
        all_techniques = dsm5_info.get("recommended_techniques", [
            "Cognitive Behavioral Therapy",
            "Mindfulness exercises",
            "Behavioral activation",
            "Stress management"
        ])
        
        # Validate and organize techniques
        validated_techniques = []
        technique_db = TechniqueDatabase()
        
        for technique in all_techniques:
            technique_info = technique_db.get_technique_info(technique)
            if technique_info:
                validated_techniques.append(technique)
        
        # Ensure we have enough techniques for the schedule
        while len(validated_techniques) < (sessions_per_week * 4):  # 4 weeks
            validated_techniques.extend(validated_techniques[:])
        
        therapy_plan = TherapyPlan(
            identified_conditions=identified_conditions,
            confidence_scores=confidence_scores,
            therapy_type=dsm5_info.get("name", "Cognitive Behavioral Therapy"),
            session_frequency=session_frequency,
            goals=dsm5_info.get("treatment_goals", ["Improve symptoms", "Develop coping skills"]),
            techniques=validated_techniques,
            duration=dsm5_info.get("recommended_duration", "12-16 weeks")
        )

        return therapy_plan 