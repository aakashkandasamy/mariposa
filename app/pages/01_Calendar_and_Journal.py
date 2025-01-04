import streamlit as st
import calendar
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from textblob import TextBlob
import nltk
from typing import List, Dict

# Download required NLTK data
@st.cache_resource
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

# Download data at app startup
download_nltk_data()

def analyze_journal_entry(text: str) -> dict:
    """Analyze journal entry using TextBlob"""
    if not text:
        return None
    
    # Sentiment analysis using TextBlob
    analysis = TextBlob(text)
    # TextBlob polarity ranges from -1 to 1, convert to 0 to 1 scale
    sentiment_score = (analysis.sentiment.polarity + 1) / 2
    
    # Determine sentiment label
    if sentiment_score > 0.6:
        sentiment_label = "POSITIVE"
    elif sentiment_score < 0.4:
        sentiment_label = "NEGATIVE"
    else:
        sentiment_label = "NEUTRAL"
    
    # Basic text analysis
    word_count = len(text.split())
    
    # Key phrase extraction (simplified)
    negative_phrases = ["worried", "anxious", "sad", "depressed", "tired", "stress", "overwhelmed"]
    positive_phrases = ["better", "happy", "improving", "hopeful", "grateful", "good", "calm"]
    
    negative_count = sum(text.lower().count(word) for word in negative_phrases)
    positive_count = sum(text.lower().count(word) for word in positive_phrases)
    
    # Extract key topics
    topics = [word.lower() for word, tag in analysis.tags if tag.startswith('NN')]
    
    return {
        "sentiment": {
            "score": sentiment_score,
            "label": sentiment_label
        },
        "word_count": word_count,
        "negative_phrases": negative_count,
        "positive_phrases": positive_count,
        "topics": topics[:5],  # Top 5 topics
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
        y=[entry['sentiment']['score'] for entry in df['sentiment']],
        mode='lines+markers',
        name='Sentiment Score'
    ))
    fig_sentiment.update_layout(
        title='Emotional Well-being Trend',
        yaxis_title='Mood Score',
        yaxis=dict(range=[0, 1])
    )
    st.plotly_chart(fig_sentiment)
    
    # Create phrase comparison chart
    fig_phrases = go.Figure(data=[
        go.Bar(name='Positive Expressions', x=df['date'], y=df['positive_phrases']),
        go.Bar(name='Negative Expressions', x=df['date'], y=df['negative_phrases'])
    ])
    fig_phrases.update_layout(
        title='Expression Pattern Analysis',
        barmode='group',
        yaxis_title='Frequency'
    )
    st.plotly_chart(fig_phrases)

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
    
    # Create schedule lookup
    schedule_lookup = {
        datetime.strptime(session['date'], "%Y-%m-%d").date(): session 
        for session in schedule
    }
    
    # Display calendar
    st.markdown("### Therapy Calendar")
    
    # Display weekday headers
    cols = st.columns(7)
    for idx, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
        cols[idx].markdown(f"**{day}**")
    
    # Display calendar weeks
    for week in cal:
        cols = st.columns(7)
        for idx, day in enumerate(week):
            if day == 0:
                cols[idx].markdown("")
                continue
            
            date = datetime(year, month, day).date()
            
            if date in schedule_lookup:
                session = schedule_lookup[date]
                with cols[idx]:
                    with st.expander(f"**{day}** 📅"):
                        st.markdown(f"**Activity:** {session['activity']}")
                        st.markdown(f"**Time:** {session['duration']}")
                        
                        if st.button("View Details", key=f"view_{date}"):
                            st.session_state.selected_session = session
            else:
                cols[idx].markdown(str(day))
    
    # Show selected session details
    if 'selected_session' in st.session_state:
        st.markdown("---")
        st.markdown("### Session Details")
        show_technique_details(
            st.session_state.selected_session.get('technique_details', {}),
            st.session_state.selected_session
        )

def main():
    st.title("🗓️ Therapy Calendar & Journal")
    
    # Get session state for journal entries
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    
    # Create tabs
    calendar_tab, journal_tab, progress_tab = st.tabs(["Calendar", "Journal", "Progress"])
    
    with calendar_tab:
        st.markdown("### Your Therapy Schedule")
        if 'therapy_schedule' in st.session_state:
            create_calendar_view(st.session_state.therapy_schedule)
            
            st.markdown("### All Sessions")
            for session in st.session_state.therapy_schedule:
                with st.expander(f"📅 {session['date']} - {session['activity']}"):
                    show_technique_details(session.get('technique_details', {}), session)
    
    with journal_tab:
        st.markdown("### Daily Journal")
        
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
                    **analysis
                }
                st.session_state.journal_entries.append(entry)
                st.success("Journal entry saved!")
                
                # Provide feedback based on analysis
                sentiment = analysis['sentiment']
                if sentiment['label'] == 'NEGATIVE' and sentiment['score'] < 0.3:
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
            st.markdown("### Journal History")
            for entry in reversed(st.session_state.journal_entries):
                with st.expander(f"Entry from {entry['date']}"):
                    st.write(entry['text'])
                    st.markdown("**Sentiment Analysis:**")
                    st.progress(entry['sentiment']['score'])
                    st.write(f"Mood: {entry['sentiment']['label']}")

if __name__ == "__main__":
    main() 