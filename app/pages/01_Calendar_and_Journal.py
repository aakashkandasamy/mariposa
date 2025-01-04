import streamlit as st
import calendar
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import nltk
from typing import List, Dict
from app.core.services.sentiment_analyzer import SentimentAnalyzer

def analyze_journal_entry(text: str) -> dict:
    """Analyze journal entry using our custom SentimentAnalyzer"""
    if not text:
        return None
    
    # Use our custom sentiment analyzer
    analyzer = SentimentAnalyzer()
    analysis = analyzer.analyze(text)
    
    return {
        "sentiment": analysis["sentiment"],
        "details": analysis["details"],
        "date": datetime.now().strftime("%Y-%m-%d")
    }

def show_progress_charts(journal_entries):
    """Display progress charts based on journal entries"""
    if not journal_entries:
        st.info("Start journaling to see your progress!")
        return
    
    # Convert journal entries to DataFrame
    df = pd.DataFrame(journal_entries)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create sentiment trend chart
    fig_sentiment = go.Figure()
    fig_sentiment.add_trace(go.Scatter(
        x=df['date'],
        y=[entry['score'] for entry in df['sentiment']],
        mode='lines+markers',
        name='Emotional State Score'
    ))
    fig_sentiment.update_layout(
        title='Emotional Well-being Trend',
        yaxis_title='Emotional State Score (0-1)',
        yaxis=dict(range=[0, 1])
    )
    st.plotly_chart(fig_sentiment)
    
    # Create emotions frequency chart
    all_emotions = []
    emotion_counts = {}
    
    # Collect all emotions and their frequencies
    for entry in journal_entries:
        emotions = entry['sentiment']['emotions']
        for emotion in emotions:
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
            emotion_counts[emotion] += 1
            if emotion not in all_emotions:
                all_emotions.append(emotion)
    
    # Create bar chart for emotions
    fig_emotions = go.Figure(data=[
        go.Bar(
            name='Frequency',
            x=list(emotion_counts.keys()),
            y=list(emotion_counts.values())
        )
    ])
    fig_emotions.update_layout(
        title='Emotional Pattern Analysis',
        xaxis_title='Emotions',
        yaxis_title='Frequency'
    )
    st.plotly_chart(fig_emotions)
    
    # Create risk level trend if applicable
    risk_levels = {'none': 0, 'low': 0.33, 'medium': 0.66, 'high': 1}
    risk_data = [risk_levels[entry['sentiment']['risk_level']] 
                 for entry in journal_entries if entry['sentiment']['risk_level'] != 'unknown']
    
    if any(level > 0 for level in risk_data):
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=df['date'],
            y=risk_data,
            mode='lines+markers',
            name='Risk Level'
        ))
        fig_risk.update_layout(
            title='Risk Level Trend',
            yaxis_title='Risk Level',
            yaxis=dict(
                range=[0, 1],
                ticktext=['None', 'Low', 'Medium', 'High'],
                tickvals=[0, 0.33, 0.66, 1]
            )
        )
        st.plotly_chart(fig_risk)

def show_technique_details(technique: dict, session: dict):
    """Display technique details in a structured format"""
    if not technique:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### About this Technique")
        st.write(technique.get('description', ''))
        
        st.markdown("### Steps")
        for step in technique.get('steps', []):
            st.markdown(f"\n• {step}")
    
    with col2:
        st.markdown("### Today's Exercise")
        exercises = technique.get('exercises', [])
        if exercises:
            exercise = exercises[0]
            st.markdown(f"**{exercise['name']}** ({exercise['duration']})")
            for instruction in exercise['instructions']:
                st.markdown(f"\n• {instruction}")
        
        st.markdown("### Additional Resources")
        for resource in technique.get('resources', []):
            st.markdown(f"\n• [{resource['title']}]({resource['url']}) ({resource['type']})")

def show_daily_activities(sessions: List[Dict], date: datetime):
    """Display activities and journal entries for a day"""
    # Show journal entries first
    if 'journal_entries' in st.session_state:
        entries = [
            entry for entry in st.session_state.journal_entries 
            if entry['date'] == date.strftime("%Y-%m-%d")
        ]
        if entries:
            st.markdown("#### 📝 Journal Entries")
            for entry in entries:
                st.markdown(f"**Time:** {entry['time']}")
                st.markdown(f"**Mood Score:** {entry['sentiment']['score']:.2f}")
                st.markdown(f"**Mood:** {entry['sentiment']['label']}")
                st.markdown("**Entry:**")
                st.write(entry['text'])
                st.markdown("---")

    # Show activities
    st.markdown("#### 📅 Activities")
    for session in sessions:
        st.markdown(f"**🕐 {session['time']} - {session['activity']} ({session['duration']})**")
        st.markdown(f"Type: {session['type']}")
        
        technique_details = session.get('technique_details', {})
        if technique_details:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### About this Technique")
                st.write(technique_details.get('description', ''))
                
                st.markdown("### Steps")
                for step in technique_details.get('steps', []):
                    st.markdown(f"• {step}")
            
            with col2:
                st.markdown("### Today's Exercise")
                exercises = technique_details.get('exercises', [])
                if exercises:
                    exercise = exercises[0]
                    st.markdown(f"**{exercise['name']}** ({exercise['duration']})")
                    for instruction in exercise['instructions']:
                        st.markdown(f"• {instruction}")
                
                st.markdown("### Additional Resources")
                for resource in technique_details.get('resources', []):
                    st.markdown(f"• [{resource['title']}]({resource['url']}) ({resource['type']})")
        st.markdown("---")

def create_calendar_view(schedule: List[Dict]):
    """Create an interactive calendar view"""
    if not schedule:
        st.info("No schedule available yet. Generate a therapy plan first!")
        return

    # Get the current month and year
    today = datetime.now()
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        month = st.selectbox("Month", range(1, 13), index=today.month - 1)
    with col2:
        year = st.selectbox("Year", range(today.year, today.year + 2), index=0)
    
    # Create calendar
    cal = calendar.monthcalendar(year, month)
    
    # Create schedule lookup that groups sessions by date
    schedule_lookup = {}
    for session in schedule:
        date = datetime.strptime(session['date'], "%Y-%m-%d").date()
        if date not in schedule_lookup:
            schedule_lookup[date] = []
        schedule_lookup[date].append(session)
    
    # Add journal entries to calendar
    if 'journal_entries' in st.session_state:
        for entry in st.session_state.journal_entries:
            date = datetime.strptime(entry['date'], "%Y-%m-%d").date()
            if date not in schedule_lookup:
                schedule_lookup[date] = []
    
    # Display calendar
    st.markdown("### Therapy Calendar")
    
    # Display weekday headers
    cols = st.columns(7)
    for idx, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        cols[idx].markdown(f"**{day}**")
    
    # Display calendar weeks
    selected_date = None
    for week in cal:
        cols = st.columns(7)
        for idx, day in enumerate(week):
            if day == 0:
                cols[idx].markdown("")
                continue
            
            date = datetime(year, month, day).date()
            
            with cols[idx]:
                has_journal = date in schedule_lookup
                has_activities = any(isinstance(s, dict) and 'activity' in s 
                                  for s in schedule_lookup.get(date, []))
                
                if has_journal or has_activities:
                    if st.button(
                        f"**{day}** {'📝' if has_journal else ''} {'📅' if has_activities else ''}",
                        key=f"day_{date}"
                    ):
                        selected_date = date
                else:
                    st.markdown(str(day))
    
    # Show selected day's activities
    if selected_date and selected_date in schedule_lookup:
        st.markdown("---")
        st.markdown(f"### Activities for {selected_date.strftime('%A, %B %d, %Y')}")
        show_daily_activities(schedule_lookup[selected_date], selected_date)

def show_schedule_view(schedule: List[Dict]):
    """Display schedule in a day-by-day view"""
    if not schedule:
        st.info("No schedule available yet. Generate a therapy plan first!")
        return

    # Group sessions by week and day
    weeks = {}
    for session in schedule:
        date = datetime.strptime(session['date'], "%Y-%m-%d")
        week_num = (date - datetime.now()).days // 7 + 1
        if week_num not in weeks:
            weeks[week_num] = {}
        
        day = date.strftime("%Y-%m-%d")
        if day not in weeks[week_num]:
            weeks[week_num][day] = []
        weeks[week_num][day].append(session)

    # Display each week
    for week_num in sorted(weeks.keys()):
        with st.expander(f"Week {week_num}", expanded=True):
            # Display each day
            for day, sessions in sorted(weeks[week_num].items()):
                date_obj = datetime.strptime(day, "%Y-%m-%d")
                st.markdown(f"### {date_obj.strftime('%A, %B %d, %Y')}")
                
                # Create a table for daily schedule
                schedule_data = []
                for session in sorted(sessions, key=lambda x: x['time']):
                    schedule_data.append([
                        session['time'],
                        session['activity'],
                        session['type'],
                        session['duration']
                    ])
                
                if schedule_data:
                    df = pd.DataFrame(
                        schedule_data,
                        columns=['Time', 'Activity', 'Type', 'Duration']
                    )
                    st.table(df)
                
                # Show detailed activities
                show_daily_activities(sorted(sessions, key=lambda x: x['time']), date_obj)

def show_journal_entry_form():
    """Show the journal entry form"""
    st.markdown("### New Journal Entry")
    
    # Date and time selection
    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("Date", datetime.now())
    with col2:
        entry_time = st.time_input("Time", datetime.now().time())
    
    # Journal text
    journal_text = st.text_area(
        "How are you feeling?",
        height=150,
        help="Write about your thoughts, feelings, and experiences."
    )
    
    if st.button("Save Entry"):
        if journal_text:
            # Initialize sentiment analyzer
            analyzer = SentimentAnalyzer()
            analysis = analyzer.analyze(journal_text)
            
            # Create entry
            entry = {
                "date": entry_date.strftime("%Y-%m-%d"),
                "time": entry_time.strftime("%H:%M"),
                "text": journal_text,
                **analysis
            }
            
            # Initialize journal entries if not exists
            if 'journal_entries' not in st.session_state:
                st.session_state.journal_entries = []
            
            # Add entry
            st.session_state.journal_entries.append(entry)
            st.success("Journal entry saved!")
            
            # Show mood feedback
            if analysis['sentiment']['label'] == 'NEGATIVE' and analysis['sentiment']['score'] < 0.3:
                st.warning("""
                I notice you're feeling down. Here are some suggestions:
                - Try one of the recommended exercises from your therapy plan
                - Practice a mindfulness exercise
                - Reach out to your support network
                - Consider scheduling an extra therapy session
                """)

def show_journal_history(journal_entries):
    """Display journal history with detailed analysis"""
    st.markdown("### Journal History")
    
    # Group entries by date
    entries_by_date = {}
    for entry in reversed(journal_entries):
        date = entry['date']
        if date not in entries_by_date:
            entries_by_date[date] = []
        entries_by_date[date].append(entry)
    
    # Display entries grouped by date
    for date, entries in entries_by_date.items():
        st.markdown(f"#### {date}")
        for entry in entries:
            st.markdown(f"**Time:** {entry['time']}")
            st.write(entry['text'])
            
            # Show sentiment analysis
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(entry['sentiment']['score'])
                st.write(f"Emotions detected: {', '.join(entry['sentiment']['emotions'])}")
            with col2:
                st.write(f"Mood: {entry['sentiment']['label']}")
                if entry['sentiment']['risk_level'] != 'none':
                    st.warning(f"Risk Level: {entry['sentiment']['risk_level']}")
            
            # Show analysis details
            with st.expander("Analysis Details"):
                st.write("**Analysis:**", entry['details']['reasoning'])
                st.write("**Suggestions:**")
                for suggestion in entry['details']['suggestions']:
                    st.write(f"• {suggestion}")
            
            st.markdown("---")

def test_api_connection():
    st.markdown("### Testing API Connection")
    analyzer = SentimentAnalyzer()
    
    with st.spinner("Testing OpenAI API connection..."):
        if analyzer.test_connection():
            st.success("✅ OpenAI API connection successful!")
        else:
            st.error("❌ OpenAI API connection failed. Please check your API key and billing status.")

def main():
    st.title("🗓️ Therapy Calendar & Journal")
    
    # Get session state for journal entries
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    
    # Create tabs
    calendar_tab, journal_tab, progress_tab = st.tabs(["Calendar", "Journal", "Progress"])
    
    with calendar_tab:
        st.markdown("### Your Therapy Schedule")
        
        # Add view selection
        view_type = st.radio(
            "Select View",
            ["Daily Schedule", "Calendar View"],
            horizontal=True
        )
        
        if 'therapy_schedule' in st.session_state:
            if view_type == "Daily Schedule":
                show_schedule_view(st.session_state.therapy_schedule)
            else:
                create_calendar_view(st.session_state.therapy_schedule)
        else:
            st.info("Please generate a therapy plan to see your schedule.")
    
    with journal_tab:
        st.markdown("### Daily Journal")
        
        # Date and time selection
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", datetime.now())
        with col2:
            entry_time = st.time_input("Time", datetime.now().time())
        
        # Journal entry
        journal_text = st.text_area(
            "How are you feeling today?",
            height=200,
            help="Write about your thoughts, feelings, and experiences."
        )
        
        if st.button("Save Journal Entry"):
            if journal_text:
                analysis = analyze_journal_entry(journal_text)
                entry = {
                    "text": journal_text,
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "time": entry_time.strftime("%H:%M"),
                    "sentiment": analysis["sentiment"],
                    "details": analysis["details"]
                }
                st.session_state.journal_entries.append(entry)
                st.success("Journal entry saved!")
                
                # Provide feedback based on analysis
                if analysis['sentiment']['label'] == 'NEGATIVE' and analysis['sentiment']['score'] < 0.3:
                    st.warning("""
                    I notice you're feeling down. Here are some suggestions:
                    - Try one of the recommended exercises from your therapy plan
                    - Practice a mindfulness exercise
                    - Reach out to your support network
                    - Consider scheduling an extra therapy session
                    """)
    
    with progress_tab:
        st.markdown("### Your Progress")
        show_progress_charts(st.session_state.journal_entries)
        
        # Show detailed journal history
        if st.session_state.journal_entries:
            show_journal_history(st.session_state.journal_entries)

    # Add this at the start of the main() function:
    if st.sidebar.button("Test API Connection"):
        test_api_connection()

if __name__ == "__main__":
    main() 