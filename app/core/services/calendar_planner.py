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
        if not availability or not techniques:
            return []  # Return empty schedule if no availability or techniques

        if start_date is None:
            start_date = datetime.now()

        # Debug print
        print(f"Generating schedule with: {availability}, {therapy_type}, {session_frequency}, {techniques}")

        # Convert day names to datetime objects for the next occurrence
        available_days = []
        for day in availability:
            day_num = list(calendar.day_name).index(day)
            days_ahead = day_num - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_date = start_date + timedelta(days=days_ahead)
            available_days.append(next_date)

        # Sort available days
        available_days.sort()

        # Debug print
        print(f"Available dates: {[d.strftime('%Y-%m-%d') for d in available_days]}")

        # Determine number of sessions per week based on frequency
        sessions_per_week = {
            "bi-weekly": 0.5,
            "weekly": 1,
            "twice-weekly": 2,
            "intensive outpatient": 3,
            "intensive support": 3,
            "immediate intervention": 5
        }.get(session_frequency.lower(), 1)  # Added .lower() for case insensitivity

        # Calculate number of sessions needed
        if sessions_per_week < 1:  # bi-weekly
            sessions_needed = 2  # 2 sessions per month
        else:
            sessions_needed = int(sessions_per_week * 4)  # 4 weeks of therapy

        # Generate schedule
        schedule = []
        techniques_cycle = techniques.copy()
        
        # Generate 4 weeks of schedule
        current_date = start_date
        session_count = 0
        week = 0

        while session_count < sessions_needed and week < 4:
            # For bi-weekly, only schedule every other week
            if sessions_per_week < 1 and week % 2 == 1:
                week += 1
                current_date += timedelta(weeks=1)
                continue

            # Get available days for this week
            week_days = [day + timedelta(weeks=week) for day in available_days]
            
            # Calculate sessions for this week
            week_sessions = min(int(sessions_per_week), sessions_needed - session_count)
            week_sessions = min(week_sessions, len(week_days))
            
            for _ in range(week_sessions):
                if not week_days:  # No more available days this week
                    break
                    
                session_date = week_days.pop(0)
                
                # Get next technique
                if not techniques_cycle:
                    techniques_cycle = techniques.copy()
                technique = techniques_cycle.pop(0)
                
                # Get technique details
                technique_info = self.technique_db.get_technique_info(technique)
                
                session = {
                    "date": session_date.strftime("%Y-%m-%d"),
                    "day": session_date.strftime("%A"),
                    "activity": technique,
                    "type": therapy_type,
                    "duration": "50 minutes",
                    "technique_details": technique_info
                }
                schedule.append(session)
                session_count += 1
            
            week += 1

        # Debug print
        print(f"Generated {len(schedule)} sessions")
        return schedule 