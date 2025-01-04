from typing import Dict
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('vader_lexicon')
            nltk.data.find('punkt')
            nltk.data.find('stopwords')
        except LookupError:
            nltk.download('vader_lexicon')
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.sia = SentimentIntensityAnalyzer()
        self.emotion_keywords = {
            'joy': ['happy', 'excited', 'delighted', 'joyful', 'pleased', 'grateful'],
            'sadness': ['sad', 'depressed', 'unhappy', 'miserable', 'down', 'blue'],
            'anger': ['angry', 'frustrated', 'irritated', 'annoyed', 'furious'],
            'anxiety': ['anxious', 'worried', 'nervous', 'stressed', 'tense'],
            'fear': ['scared', 'afraid', 'terrified', 'fearful', 'panicked'],
            'hope': ['hopeful', 'optimistic', 'looking forward', 'confident'],
            'calm': ['peaceful', 'relaxed', 'serene', 'tranquil', 'calm']
        }
        
        self.risk_keywords = {
            'high': ['suicide', 'kill myself', 'end my life', 'want to die', 'better off dead'],
            'medium': ['hopeless', 'worthless', 'can\'t go on', 'give up', 'no point'],
            'low': ['exhausted', 'overwhelmed', 'struggling', 'difficult', 'hard time']
        }

    def detect_emotions(self, text: str) -> list:
        """Detect emotions present in the text"""
        text = text.lower()
        detected_emotions = []
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions if detected_emotions else ['neutral']

    def assess_risk_level(self, text: str) -> str:
        """Assess risk level based on keywords"""
        text = text.lower()
        
        for level, keywords in self.risk_keywords.items():
            if any(keyword in text for keyword in keywords):
                return level
        return 'none'

    def get_suggestions(self, sentiment_score: float, emotions: list, risk_level: str) -> list:
        """Generate suggestions based on analysis"""
        suggestions = []
        
        if sentiment_score < 0.4:
            suggestions.extend([
                "Consider reaching out to a trusted friend or family member",
                "Try some deep breathing exercises",
                "Take a short walk or get some light exercise"
            ])
        
        if 'anxiety' in emotions or 'fear' in emotions:
            suggestions.extend([
                "Practice grounding techniques (5-4-3-2-1 method)",
                "Try progressive muscle relaxation",
                "Write down your worries and challenge negative thoughts"
            ])
            
        if risk_level != 'none':
            suggestions.extend([
                "Please speak with a mental health professional",
                "Contact a crisis helpline for immediate support",
                "Don't hesitate to reach out for help"
            ])
            
        return suggestions if suggestions else ["Continue your current positive practices"]

    def analyze(self, text: str) -> Dict:
        """Analyze the sentiment of a text"""
        try:
            # Get VADER sentiment scores
            scores = self.sia.polarity_scores(text)
            
            # Normalize compound score to 0-1 range
            normalized_score = (scores['compound'] + 1) / 2
            
            # Determine sentiment label
            if normalized_score > 0.6:
                sentiment_label = "POSITIVE"
            elif normalized_score < 0.4:
                sentiment_label = "NEGATIVE"
            else:
                sentiment_label = "NEUTRAL"
            
            # Detect emotions and risk level
            emotions = self.detect_emotions(text)
            risk_level = self.assess_risk_level(text)
            
            # Generate suggestions
            suggestions = self.get_suggestions(normalized_score, emotions, risk_level)
            
            # Generate reasoning
            reasoning = f"Analysis shows {sentiment_label.lower()} sentiment"
            if emotions != ['neutral']:
                reasoning += f" with detected emotions: {', '.join(emotions)}"
            if risk_level != 'none':
                reasoning += f". Risk level: {risk_level}"
            
            return {
                "sentiment": {
                    "score": normalized_score,
                    "label": sentiment_label,
                    "emotions": emotions,
                    "risk_level": risk_level
                },
                "details": {
                    "reasoning": reasoning,
                    "suggestions": suggestions
                }
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return {
                "sentiment": {
                    "score": 0.5,
                    "label": "NEUTRAL",
                    "emotions": ["unknown"],
                    "risk_level": "unknown"
                },
                "details": {
                    "reasoning": f"Error in analysis: {str(e)}",
                    "suggestions": ["Please try again"]
                }
            } 