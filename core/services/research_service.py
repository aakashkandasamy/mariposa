from pathlib import Path
import json
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResearchService:
    def __init__(self):
        self.dsm5_data = self._load_dsm5_data()
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def _load_dsm5_data(self) -> Dict:
        """Load DSM-5 criteria and treatments from JSON file"""
        dsm5_path = Path("data/dsm5/disorders.json")
        if not dsm5_path.exists():
            raise FileNotFoundError(
                "DSM-5 data file not found. Ensure data/dsm5/disorders.json exists."
            )
        with open(dsm5_path, 'r') as f:
            return json.load(f)

    def analyze_symptoms(self, symptoms: str) -> List[Tuple[str, float]]:
        """Analyze symptoms and match with possible conditions"""
        # Prepare DSM-5 criteria for comparison
        conditions = []
        criteria_texts = []
        
        for condition, data in self.dsm5_data.items():
            conditions.append(condition)
            # Include both criteria and name in the comparison text
            criteria_text = data["name"] + " " + " ".join(data["diagnostic_criteria"])
            criteria_texts.append(criteria_text)

        # Add symptoms to the comparison
        all_texts = criteria_texts + [symptoms]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity scores
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        # Pair conditions with their similarity scores
        condition_scores = list(zip(conditions, similarities))
        
        # Sort by similarity score and filter those above threshold
        threshold = 0.05  # Lowered threshold for better matching
        relevant_conditions = [(cond, score) for cond, score in condition_scores if score > threshold]
        relevant_conditions.sort(key=lambda x: x[1], reverse=True)
        
        return relevant_conditions

    def get_dsm5_criteria(self, disorder: str) -> Dict:
        return self.dsm5_data.get(disorder, {})

    def get_scholarly_articles(self, disorder: str, max_results: int = 5) -> List[Dict]:
        # Use the mock database instead of scholarly
        from app.core.services.research_database import ResearchDatabase
        research_db = ResearchDatabase()
        return research_db.get_articles(disorder)[:max_results]

    def analyze_treatment_effectiveness(self, articles: List[Dict]) -> Dict:
        """Analyze research papers to extract treatment effectiveness data"""
        treatments = {}
        
        for article in articles:
            abstract = article.get('abstract', '').lower()
            
            for therapy in ["cbt", "medication", "mindfulness", "psychotherapy"]:
                if therapy in abstract:
                    if therapy not in treatments:
                        treatments[therapy] = {
                            'mention_count': 0,
                            'articles': []
                        }
                    treatments[therapy]['mention_count'] += 1
                    treatments[therapy]['articles'].append(article['title'])

        return treatments 