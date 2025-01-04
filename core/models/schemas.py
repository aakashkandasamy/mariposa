from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    SEVERE = "severe"

class Schedule(BaseModel):
    availability: List[str] = Field(..., description="List of available days for therapy")

    def dict(self, *args, **kwargs):
        return {
            "availability": self.availability
        }

class PatientInput(BaseModel):
    symptoms: str = Field(..., description="Detailed description of symptoms")
    severity: SeverityLevel = Field(..., description="Severity level of symptoms")
    schedule: Schedule = Field(..., description="Patient's availability schedule")

    def dict(self, *args, **kwargs):
        return {
            "symptoms": self.symptoms,
            "severity": self.severity,
            "schedule": self.schedule.dict()
        }

class TherapyPlan(BaseModel):
    identified_conditions: List[str] = Field(..., description="List of identified conditions")
    confidence_scores: Dict[str, float] = Field(..., description="Confidence scores for each condition")
    therapy_type: str = Field(..., description="Type of therapy recommended")
    session_frequency: str = Field(..., description="Recommended frequency of sessions")
    goals: List[str] = Field(..., description="Treatment goals")
    techniques: List[str] = Field(..., description="Recommended therapeutic techniques")
    duration: str = Field(..., description="Recommended duration of therapy")

    class Config:
        schema_extra = {
            "example": {
                "identified_conditions": ["anxiety", "depression"],
                "confidence_scores": {"anxiety": 0.85, "depression": 0.65},
                "therapy_type": "Cognitive Behavioral Therapy",
                "session_frequency": "weekly",
                "goals": ["Reduce anxiety symptoms", "Improve mood"],
                "techniques": ["CBT", "Mindfulness"],
                "duration": "12-16 weeks"
            }
        } 