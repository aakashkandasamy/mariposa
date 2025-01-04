from datetime import datetime, timedelta
from typing import List, Dict
import calendar
from app.core.services.technique_database import TechniqueDatabase

class TherapyCalendarPlanner:
    def __init__(self):
        self.technique_db = TechniqueDatabase()

    def generate_weekly_schedule(self, 
                               availability: List[str],
                               therapy_type: str,
                               session_frequency: str,
                               techniques: List[str],
                               start_date: datetime = None) -> List[Dict]:
        if start_date is None:
            start_date = datetime.now()

        # Create a structured weekly schedule
        schedule = []
        
        # Map frequency to number of sessions per week
        sessions_per_week = {
            "bi-weekly": 1,  # Every other week
            "weekly": 1,
            "twice-weekly": 2,
            "intensive outpatient": 3,
            "intensive support": 5,
            "immediate intervention": 5
        }
        
        weekly_sessions = sessions_per_week.get(session_frequency, 1)
        
        # Generate 4-week schedule
        for week in range(4):
            current_week_start = start_date + timedelta(weeks=week)
            
            # Morning routine (daily)
            for day in range(7):
                current_date = current_week_start + timedelta(days=day)
                
                # Morning routine
                schedule.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": current_date.strftime("%A"),
                    "time": "08:00",
                    "activity": "Morning Mindfulness",
                    "type": "Daily Practice",
                    "duration": "15 minutes",
                    "technique_details": self.technique_db.get_technique_info("Mindfulness Meditation")
                })
                
                # Evening routine
                schedule.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": current_date.strftime("%A"),
                    "time": "20:00",
                    "activity": "Progressive Muscle Relaxation",
                    "type": "Daily Practice",
                    "duration": "15 minutes",
                    "technique_details": self.technique_db.get_technique_info("Progressive Muscle Relaxation")
                })

            # Main therapy sessions
            available_days = sorted([list(calendar.day_name).index(day) for day in availability])
            session_days = available_days[:weekly_sessions]
            
            for day_index in session_days:
                session_date = current_week_start + timedelta(days=day_index)
                technique = techniques[week % len(techniques)]  # Rotate through techniques
                
                schedule.append({
                    "date": session_date.strftime("%Y-%m-%d"),
                    "day": session_date.strftime("%A"),
                    "time": "14:00",
                    "activity": technique,
                    "type": therapy_type,
                    "duration": "50 minutes",
                    "technique_details": self.technique_db.get_technique_info(technique)
                })
                
                # Add homework/practice session
                practice_date = session_date + timedelta(days=2)
                schedule.append({
                    "date": practice_date.strftime("%Y-%m-%d"),
                    "day": practice_date.strftime("%A"),
                    "time": "17:00",
                    "activity": f"Practice: {technique}",
                    "type": "Self-Practice",
                    "duration": "30 minutes",
                    "technique_details": self.technique_db.get_technique_info(technique)
                })

            # Weekly review session
            week_end = current_week_start + timedelta(days=6)
            schedule.append({
                "date": week_end.strftime("%Y-%m-%d"),
                "day": week_end.strftime("%A"),
                "time": "19:00",
                "activity": "Weekly Progress Review",
                "type": "Self-Assessment",
                "duration": "20 minutes",
                "technique_details": self.technique_db.get_technique_info("General therapy session")
            })

        return sorted(schedule, key=lambda x: (x['date'], x['time'])) 