from datetime import datetime, timedelta
from typing import List, Dict
import calendar
from app.core.services.technique_database import TechniqueDatabase
from app.core.models.severity_level import SeverityLevel

class TherapyCalendarPlanner:
    def __init__(self):
        self.technique_db = TechniqueDatabase()

    def generate_weekly_schedule(self, 
                               therapy_type: str,
                               session_frequency: str,
                               techniques: List[str],
                               severity: SeverityLevel,
                               start_date: datetime = None) -> List[Dict]:
        if start_date is None:
            start_date = datetime.now()

        # Create a structured weekly schedule
        schedule = []
        
        # Adjust activities based on severity
        daily_activities = {
            SeverityLevel.LOW: [
                ("08:00", "Morning Mindfulness", "15 minutes"),
                ("20:00", "Progressive Muscle Relaxation", "15 minutes")
            ],
            SeverityLevel.MODERATE: [
                ("08:00", "Morning Mindfulness", "20 minutes"),
                ("14:00", "Afternoon Practice", "20 minutes"),
                ("20:00", "Progressive Muscle Relaxation", "20 minutes")
            ],
            SeverityLevel.SEVERE: [
                ("08:00", "Morning Mindfulness", "30 minutes"),
                ("11:00", "Mid-morning Practice", "30 minutes"),
                ("14:00", "Afternoon Practice", "30 minutes"),
                ("17:00", "Evening Practice", "30 minutes"),
                ("20:00", "Progressive Muscle Relaxation", "30 minutes")
            ]
        }

        # Session frequency based on severity
        sessions_per_week = {
            SeverityLevel.LOW: {
                "bi-weekly": 1,
                "weekly": 1,
                "twice-weekly": 2
            },
            SeverityLevel.MODERATE: {
                "bi-weekly": 2,
                "weekly": 2,
                "twice-weekly": 3
            },
            SeverityLevel.SEVERE: {
                "bi-weekly": 3,
                "weekly": 3,
                "twice-weekly": 5
            }
        }
        
        weekly_sessions = sessions_per_week[severity].get(session_frequency, 1)
        
        # Generate 4-week schedule
        for week in range(4):
            current_week_start = start_date + timedelta(weeks=week)
            
            # Add daily activities based on severity
            for day in range(7):
                current_date = current_week_start + timedelta(days=day)
                
                # Add severity-based daily activities
                for time, activity, duration in daily_activities[severity]:
                    schedule.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "day": current_date.strftime("%A"),
                        "time": time,
                        "activity": activity,
                        "type": "Daily Practice",
                        "duration": duration,
                        "technique_details": self.technique_db.get_technique_info(activity)
                    })

            # Add therapy sessions
            available_days = list(range(7))  # All days available
            session_days = available_days[:weekly_sessions]
            
            for day_index in session_days:
                session_date = current_week_start + timedelta(days=day_index)
                technique = techniques[week % len(techniques)]
                
                # Adjust session duration based on severity
                session_duration = {
                    SeverityLevel.LOW: "45 minutes",
                    SeverityLevel.MODERATE: "60 minutes",
                    SeverityLevel.SEVERE: "90 minutes"
                }[severity]
                
                schedule.append({
                    "date": session_date.strftime("%Y-%m-%d"),
                    "day": session_date.strftime("%A"),
                    "time": "14:00",
                    "activity": technique,
                    "type": therapy_type,
                    "duration": session_duration,
                    "technique_details": self.technique_db.get_technique_info(technique)
                })

        return sorted(schedule, key=lambda x: (x['date'], x['time'])) 