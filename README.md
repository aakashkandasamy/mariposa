# Mariposa

An AI-powered therapy plan optimization system that generates personalized therapy plans based on user inputs and clinical best practices. Mariposa (Spanish for "butterfly") symbolizes transformation and growth through therapeutic journey.

## Research Integration Features

Mariposa now integrates evidence-based research and clinical guidelines through:

### 1. Google Scholar Integration
- Real-time fetching of recent research papers on treatment effectiveness
- Caching system to store research results and respect API limits
- Analysis of treatment mentions and effectiveness from academic literature

### 2. DSM-5 Integration
- Comprehensive disorder criteria from DSM-5
- Evidence-based treatment recommendations
- Standardized treatment goals and techniques
- Severity-based session frequency guidelines

### 3. Treatment Plan Generation
The system combines multiple data sources to create personalized plans:
- Research-backed therapy recommendations
- DSM-5 clinical guidelines
- Severity-based adjustments
- Schedule optimization

### 4. Evidence-Based Features
- Treatment effectiveness scoring based on research mentions
- Integration of clinical best practices
- Dynamic goal generation based on disorder specifics
- Research-backed technique recommendations

## Project Structure

mariposa/
├── api/
│ ├── init.py
│ ├── main.py # FastAPI application entry point
│ ├── routes/
│ │ ├── init.py
│ │ └── therapy_routes.py # API endpoints
│ └── middleware/
│ ├── init.py
│ └── error_handler.py
├── core/
│ ├── init.py
│ ├── config.py # Configuration settings
│ ├── models/
│ │ ├── init.py
│ │ ├── schemas.py # Pydantic models
│ │ └── database.py # Database models
│ └── services/
│ ├── init.py
│ ├── nlp_service.py # NLP processing
│ └── plan_service.py # Plan generation logic
├── data/
│ ├── mock/
│ │ ├── disorders.json # Mock disorder data
│ │ └── treatments.json # Mock treatment data
│ └── ml_models/ # Directory for trained models
├── tests/
│ ├── init.py
│ ├── conftest.py
│ ├── test_api/
│ └── test_services/
├── utils/
│ ├── init.py
│ ├── constants.py
│ └── helpers.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md

