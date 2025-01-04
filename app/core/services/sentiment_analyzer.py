from typing import Dict
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        
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

        Return your analysis in valid JSON format with these exact keys:
        {{
            "sentiment": "positive/negative/neutral",
            "score": <number between 0-10>,
            "emotions": ["emotion1", "emotion2"],
            "risk_level": "none/low/medium/high",
            "reasoning": "brief explanation",
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """

    def analyze(self, text: str) -> Dict:
        """Analyze the sentiment of a text using GPT"""
        try:
            # Check for API key first
            if not self.client.api_key:
                raise ValueError("OpenAI API key not configured")

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a mental health professional analyzing patient journal entries. Always respond with valid JSON."
                    },
                    {
                        "role": "user", 
                        "content": self.prompt_template.format(text=text)
                    }
                ],
                temperature=0.3,
            )
            
            try:
                response_text = response.choices[0].message.content.strip()
                analysis = json.loads(response_text)
                
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
                
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {str(e)}")
                print(f"Raw response: {response_text}")
                raise
                
        except Exception as e:
            error_msg = str(e)
            if "billing_not_active" in error_msg:
                return {
                    "sentiment": {
                        "score": 0.5,
                        "label": "NEUTRAL",
                        "emotions": ["not available"],
                        "risk_level": "unknown"
                    },
                    "details": {
                        "reasoning": "OpenAI API billing not active. Please set up billing at https://platform.openai.com/account/billing",
                        "suggestions": [
                            "Set up OpenAI API billing",
                            "Ensure API key is correctly configured",
                            "Contact administrator for assistance"
                        ]
                    }
                }
            else:
                print(f"Error in sentiment analysis: {error_msg}")
                return {
                    "sentiment": {
                        "score": 0.5,
                        "label": "NEUTRAL",
                        "emotions": ["unknown"],
                        "risk_level": "unknown"
                    },
                    "details": {
                        "reasoning": f"Error in analysis: {error_msg}",
                        "suggestions": ["Please try again"]
                    }
                } 

    def test_connection(self) -> bool:
        """Test the OpenAI API connection"""
        try:
            # Try a simple test analysis
            test_response = self.analyze("This is a test message to verify the API connection.")
            if test_response.get('sentiment', {}).get('label') != "NEUTRAL":
                return True
            return False
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False 