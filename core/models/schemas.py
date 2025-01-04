from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    SEVERE = "severe"

class Schedule(BaseModel):
    availability: List[str]

class PatientInput(BaseModel):
    symptoms: str
    severity: SeverityLevel
    schedule: Schedule

class TherapyPlan(BaseModel):
    identified_conditions: List[str]
    confidence_scores: dict
    therapy_type: str
    session_frequency: str
    goals: List[str]
    techniques: List[str]
    duration: str 