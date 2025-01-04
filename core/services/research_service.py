import scholarly
import json
import os
from typing import List, Dict, Tuple
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResearchService:
    def __init__(self):
        self.dsm5_data = self._load_dsm5_data()
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def _load_dsm5_data(self) -> Dict:
        """Load DSM-5 criteria and treatments from JSON file"""
        dsm5_path = Path("data/dsm5/disorders.json")
        if dsm5_path.exists():
            with open(dsm5_path, 'r') as f:
                return json.load(f)
        return {}

    def get_scholarly_articles(self, disorder: str, max_results: int = 5) -> List[Dict]:
        """Fetch relevant research papers from Google Scholar"""
        cache_file = self.cache_dir / f"{disorder.lower()}_research.json"
        
        # Check cache first
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Search query construction
        query = f"treatment therapy {disorder} clinical effectiveness"
        search_query = scholarly.search_pubs(query)
        
        articles = []
        try:
            for i in range(max_results):
                pub = next(search_query)
                articles.append({
                    'title': pub.bib.get('title', ''),
                    'author': pub.bib.get('author', ''),
                    'year': pub.bib.get('year', ''),
                    'abstract': pub.bib.get('abstract', ''),
                    'url': pub.bib.get('url', '')
                })
        except StopIteration:
            pass

        # Cache the results
        with open(cache_file, 'w') as f:
            json.dump(articles, f)

        return articles

    def get_dsm5_criteria(self, disorder: str) -> Dict:
        """Get DSM-5 criteria and recommended treatments for a disorder"""
        return self.dsm5_data.get(disorder, {})

    def analyze_treatment_effectiveness(self, articles: List[Dict]) -> Dict:
        """Analyze research papers to extract treatment effectiveness data"""
        treatments = {}
        
        for article in articles:
            # Basic NLP could be added here to extract treatment mentions
            # and their reported effectiveness
            abstract = article.get('abstract', '').lower()
            
            # Example analysis (this should be enhanced with proper NLP)
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

    def analyze_symptoms(self, symptoms: str) -> List[Tuple[str, float]]:
        """Analyze symptoms and match with possible conditions"""
        # Prepare DSM-5 criteria for comparison
        conditions = []
        criteria_texts = []
        
        for condition, data in self.dsm5_data.items():
            conditions.append(condition)
            criteria_text = " ".join(data["diagnostic_criteria"])
            criteria_texts.append(criteria_text)

        # Add symptoms to the comparison
        all_texts = criteria_texts + [symptoms]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity scores
        similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
        
        # Pair conditions with their similarity scores
        condition_scores = list(zip(conditions, similarities))
        
        # Sort by similarity score and filter those above threshold
        threshold = 0.1
        relevant_conditions = [(cond, score) for cond, score in condition_scores if score > threshold]
        relevant_conditions.sort(key=lambda x: x[1], reverse=True)
        
        return relevant_conditions 