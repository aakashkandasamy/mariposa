from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    SEVERE = "severe"

class Schedule(BaseModel):
    availability: List[str]

    def dict(self, *args, **kwargs):
        return {
            "availability": self.availability
        }

class PatientInput(BaseModel):
    symptoms: str
    severity: SeverityLevel
    schedule: Schedule

    def dict(self, *args, **kwargs):
        return {
            "symptoms": self.symptoms,
            "severity": self.severity,
            "schedule": self.schedule.dict()
        }

class TherapyPlan(BaseModel):
    identified_conditions: List[str]
    confidence_scores: dict
    therapy_type: str
    session_frequency: str
    goals: List[str]
    techniques: List[str]
    duration: str 