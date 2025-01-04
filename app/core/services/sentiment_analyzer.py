from typing import Dict
import re

class SentimentAnalyzer:
    def __init__(self):
        # Define positive and negative word lists
        self.positive_words = {
            'happy', 'good', 'great', 'better', 'improving', 'hopeful', 'calm',
            'peaceful', 'relaxed', 'confident', 'energetic', 'motivated', 'positive',
            'accomplished', 'proud', 'grateful', 'thankful', 'relieved', 'joy',
            'excited', 'optimistic', 'strong', 'supported', 'capable', 'progress'
        }
        
        self.negative_words = {
            'sad', 'bad', 'worse', 'anxious', 'worried', 'stressed', 'depressed',
            'tired', 'exhausted', 'overwhelmed', 'afraid', 'scared', 'hopeless',
            'lonely', 'frustrated', 'angry', 'upset', 'confused', 'worthless',
            'guilty', 'ashamed', 'stuck', 'terrible', 'miserable', 'panic'
        }

        # Intensity modifiers
        self.intensifiers = {
            'very': 1.5,
            'really': 1.5,
            'extremely': 2.0,
            'completely': 2.0,
            'totally': 2.0,
            'absolutely': 2.0,
            'deeply': 1.5,
            'quite': 1.2,
            'somewhat': 0.8,
            'little': 0.5,
            'bit': 0.5
        }

    def analyze(self, text: str) -> Dict:
        """Analyze the sentiment of a text"""
        words = text.lower().split()
        
        # Initialize scores
        positive_score = 0
        negative_score = 0
        modifier = 1.0
        
        for i, word in enumerate(words):
            # Clean the word
            word = re.sub(r'[^\w\s]', '', word)
            
            # Check for intensifiers
            if i > 0:
                prev_word = re.sub(r'[^\w\s]', '', words[i-1])
                modifier = self.intensifiers.get(prev_word, 1.0)
            
            # Update scores
            if word in self.positive_words:
                positive_score += 1 * modifier
            elif word in self.negative_words:
                negative_score += 1 * modifier
            
            # Reset modifier
            modifier = 1.0
        
        # Calculate final sentiment score (-1 to 1)
        total_words = len(words)
        if total_words == 0:
            sentiment_score = 0
        else:
            sentiment_score = (positive_score - negative_score) / (positive_score + negative_score + 1)
        
        # Normalize to 0-1 range
        normalized_score = (sentiment_score + 1) / 2
        
        # Determine sentiment label
        if normalized_score > 0.6:
            label = "POSITIVE"
        elif normalized_score < 0.4:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        return {
            "sentiment": {
                "score": normalized_score,
                "label": label
            },
            "details": {
                "positive_words": positive_score,
                "negative_words": negative_score,
                "total_words": total_words
            }
        } 