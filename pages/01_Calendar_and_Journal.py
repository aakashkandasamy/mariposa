import streamlit as st
import calendar
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize session state variables
if 'therapy_schedule' not in st.session_state:
    st.session_state.therapy_schedule = None
if 'journal_entries' not in st.session_state:
    st.session_state.journal_entries = []

st.set_page_config(
    page_title="Mariposa - Calendar & Journal",
    page_icon="🦋",
    layout="wide"
)

def add_navigation():
    if st.sidebar.button("🔙 Back to Plan Generator", use_container_width=True):
        st.switch_page("app.py")

def main():
    st.title("🗓️ Therapy Calendar & Journal")
    
    # Add navigation
    add_navigation()
    
    # Rest of your calendar and journal code...

if __name__ == "__main__":
    main() 