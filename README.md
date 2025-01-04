🦋 Mariposa - AI-Powered Therapy Plan Optimizer
Mariposa is an intelligent therapy planning and journaling application that helps users track their mental health journey and receive personalized therapy recommendations.

🌟 Core Services
Plan Service (plan_service.py)
Generates personalized therapy plans based on user input
Analyzes symptoms and severity levels
Recommends therapy types and techniques
Integrates with research service for evidence-based recommendations
Research Service (research_service.py)
Provides access to DSM-5 criteria
Manages disorder classifications
Delivers relevant research articles
Supports evidence-based decision making
Calendar Planner (calendar_planner.py)
Creates structured weekly therapy schedules
Balances session frequency based on severity
Integrates techniques into daily activities
Manages therapy session timing and duration
Sentiment Analysis (sentiment_analyzer.py)
Uses NLTK's VADER for sophisticated sentiment analysis:
Emotion detection through keyword matching
Risk level assessment
Sentiment scoring and normalization
Contextual suggestions based on mood

📱 User Interface Components
Main Application (main.py)
Initial symptom assessment
Therapy plan generation
Crisis detection system
Treatment recommendations display
Calendar & Journal (01_Calendar_and_Journal.py)
Features:
Interactive calendar views (daily/monthly)
Journal entry system with sentiment analysis
Progress tracking and visualization
Activity scheduling and management

🛠️ Technical Stack
Core Dependencies:
streamlit: Web interface framework
pandas: Data handling and analysis
numpy: Numerical operations
scikit-learn: ML utilities
plotly: Interactive charts
nltk: Natural language processing with VADER sentiment analysis
Key Visualizations:
Emotional Trend Charts
Emotion Frequency Analysis
3. Risk Level Monitoring
Daily Mood Tracking

🔍 Sentiment Analysis System
VADER Implementation:
Compound sentiment scoring (-1 to 1)
Normalized to 0-1 range for UI
Emotion detection through keyword matching
Risk level assessment
Risk Assessment Levels:
High: Immediate intervention needed
Medium: Increased monitoring required
Low: General support recommended
None: Standard monitoring

📊 Data Models
Patient Input Structure:
Symptoms description
Severity level assessment
Schedule availability
Treatment preferences
Therapy Plan Components:
Treatment recommendations
Session scheduling
Technique assignments
Progress tracking

🚀 Getting Started
Clone the repository:
git clone https://github.com/aakashkandasamy/mariposa.git
cd mariposa
Install dependencies:
pip install -r requirements.txt
Run the application:
streamlit run app/main.py

📁 Project Structure
mariposa/
├── app/
│ ├── main.py # Main application
│ ├── pages/
│ │ └── 01_Calendar_and_Journal.py # Calendar & journal
│ └── core/
│ ├── models/
│ │ ├── schemas.py # Data models
│ │ └── severity_level.py # Severity enums
│ ├── services/
│ │ ├── plan_service.py # Therapy planning
│ │ ├── research_service.py # Research integration
│ │ ├── calendar_planner.py # Schedule management
│ │ └── sentiment_analyzer.py # Sentiment analysis
│ └── utils/
│ └── exceptions.py # Custom exceptions
├── requirements.txt # Dependencies
└── setup.py # Package config

🔒 Privacy & Security
Local session state storage
No external API dependencies
No personal data collection
Secure data handling

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.