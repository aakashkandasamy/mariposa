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
        print(f"Received techniques: {techniques}")  # Debug print
        if start_date is None:
            start_date = datetime.now()

        # Convert day names to datetime objects for the next occurrence
        available_days = []
        for day in availability:
            day_num = list(calendar.day_name).index(day)
            days_ahead = day_num - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            available_days.append(start_date + timedelta(days=days_ahead))

        # Determine number of sessions per week
        sessions_per_week = {
            "bi-weekly": 0.5,
            "weekly": 1,
            "twice-weekly": 2,
            "intensive outpatient": 3,
            "intensive support": 3,
            "immediate intervention": 5
        }
        
        weekly_sessions = sessions_per_week.get(session_frequency, 1)

        # Generate schedule
        schedule = []
        techniques_cycle = techniques.copy()
        
        # Generate 4 weeks of schedule
        for week in range(4):
            week_schedule = []
            session_days = available_days[:int(weekly_sessions)]
            
            for session_day in session_days:
                session_date = session_day + timedelta(weeks=week)
                technique = techniques_cycle.pop(0) if techniques_cycle else "General therapy session"
                
                # Get detailed technique information
                technique_info = self.technique_db.get_technique_info(technique)
                
                session = {
                    "date": session_date.strftime("%Y-%m-%d"),
                    "day": session_date.strftime("%A"),
                    "activity": technique,
                    "type": therapy_type,
                    "duration": "50 minutes",
                    "technique_details": technique_info
                }
                week_schedule.append(session)
                
                # Rotate techniques list
                if not techniques_cycle:
                    techniques_cycle = techniques.copy()
            
            schedule.extend(week_schedule)

        return schedule 