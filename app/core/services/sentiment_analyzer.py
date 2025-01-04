from typing import Dict
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Prompt template for sentiment analysis
        self.prompt_template = """
        Analyze the following journal entry for emotional sentiment and mental health indicators.
        Provide a detailed analysis including:
        1. Overall sentiment (positive/negative/neutral)
        2. Emotional state score (0-10, where 0 is severely distressed and 10 is very positive)
        3. Key emotions detected
        4. Risk indicators (if any)
        5. Brief reasoning for the analysis

        Journal entry: "{text}"

        Respond in the following JSON format:
        {{
            "sentiment": "positive/negative/neutral",
            "score": 0-10,
            "emotions": ["emotion1", "emotion2", ...],
            "risk_level": "none/low/medium/high",
            "reasoning": "brief explanation",
            "suggestions": ["suggestion1", "suggestion2", ...]
        }}
        """

    def analyze(self, text: str) -> Dict:
        """Analyze the sentiment of a text using GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a mental health professional analyzing patient journal entries."},
                    {"role": "user", "content": self.prompt_template.format(text=text)}
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
            )
            
            # Parse the response
            analysis = eval(response.choices[0].message.content)
            
            # Normalize score to 0-1 range for consistency with UI
            normalized_score = analysis['score'] / 10.0
            
            return {
                "sentiment": {
                    "score": normalized_score,
                    "label": analysis['sentiment'].upper(),
                    "emotions": analysis['emotions'],
                    "risk_level": analysis['risk_level']
                },
                "details": {
                    "reasoning": analysis['reasoning'],
                    "suggestions": analysis['suggestions']
                }
            }
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            # Fallback to basic analysis
            return {
                "sentiment": {
                    "score": 0.5,
                    "label": "NEUTRAL",
                    "emotions": ["unknown"],
                    "risk_level": "unknown"
                },
                "details": {
                    "reasoning": "Error in analysis",
                    "suggestions": ["Please try again"]
                }
            } 