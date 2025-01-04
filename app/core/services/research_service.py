import scholarly
import json
import os
from typing import List, Dict, Tuple
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.services.research_database import ResearchDatabase
import spacy

class ResearchService:
    def __init__(self):
        self.dsm5_data = self._load_dsm5_data()
        self.cache_dir = Path("data/cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.research_db = ResearchDatabase()
        # Load English language model
        self.nlp = spacy.load('en_core_web_sm')

    def _load_dsm5_data(self) -> Dict:
        """Load DSM-5 criteria and treatments from JSON file"""
        dsm5_path = Path("data/dsm5/disorders.json")
        if not dsm5_path.exists():
            raise FileNotFoundError(
                "DSM-5 data file not found. Ensure data/dsm5/disorders.json exists."
            )
        with open(dsm5_path, 'r') as f:
            return json.load(f)

    def get_scholarly_articles(self, disorder: str, max_results: int = 5) -> List[Dict]:
        """Get research articles from our database"""
        return self.research_db.get_articles(disorder)[:max_results]

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

    def analyze_symptoms(self, symptoms: str) -> List[Tuple[str, float, List[str]]]:
        """Analyze symptoms using NLP and match with possible conditions"""
        # Process the input text
        doc = self.nlp(symptoms.lower())
        
        # Extract key symptoms and relevant terms
        symptom_terms = []
        key_phrases = []
        
        # Extract noun phrases for better context
        for chunk in doc.noun_chunks:
            key_phrases.append(chunk.text)
        
        # Add individual words from phrases
        for phrase in key_phrases:
            symptom_terms.extend(phrase.split())
        
        for token in doc:
            # Include more parts of speech for broader matching
            if not token.is_stop:  # Include all non-stop words
                symptom_terms.append(token.text)
                # Include lemmatized form for better matching
                symptom_terms.append(token.lemma_)

        # Remove duplicates and normalize
        symptom_terms = list(set(term.lower() for term in symptom_terms))

        # Process each condition's criteria
        condition_matches = []
        for condition, data in self.dsm5_data.items():
            matching_criteria = []
            total_score = 0
            
            # Check each criterion
            for criterion in data["diagnostic_criteria"]:
                criterion_lower = criterion.lower()
                match_score = 0
                
                # Check for direct phrase matches (more lenient)
                for phrase in key_phrases:
                    if phrase in criterion_lower or criterion_lower in phrase:
                        match_score += 0.4  # Increased score for phrase matches
                        matching_criteria.append(f"Matched phrase '{phrase}' with criterion: {criterion}")
                    elif any(word in criterion_lower for word in phrase.split()):
                        match_score += 0.2  # Partial phrase matches
                        matching_criteria.append(f"Partially matched phrase '{phrase}' with criterion: {criterion}")
                
                # Check for term matches (more lenient)
                criterion_terms = set(term.lower() for term in criterion_lower.split())
                for term in symptom_terms:
                    if term in criterion_terms:
                        match_score += 0.3  # Increased score for term matches
                        matching_criteria.append(f"Matched term '{term}' with criterion: {criterion}")
                
                # Check for semantic similarity (more lenient)
                criterion_doc = self.nlp(criterion_lower)
                symptom_doc = self.nlp(symptoms.lower())
                if criterion_doc.has_vector and symptom_doc.has_vector:
                    similarity = criterion_doc.similarity(symptom_doc)
                    if similarity > 0.3:  # Lowered threshold
                        match_score += similarity * 0.6  # Increased weight for semantic similarity
                        matching_criteria.append(f"Semantic similarity ({similarity:.2f}) with: {criterion}")
                
                total_score += match_score

            # Normalize score (more lenient)
            final_score = min((total_score / len(data["diagnostic_criteria"])) * 1.5, 1.0)  # Increased scaling
            
            # Always include the condition with its score and matching criteria
            condition_matches.append((condition, final_score, matching_criteria))

        # Sort by score but don't filter any out
        condition_matches.sort(key=lambda x: x[1], reverse=True)
        
        return condition_matches

    def get_condition_details(self, condition: str, matching_criteria: List[str]) -> Dict:
        """Get detailed information about why a condition was matched"""
        condition_data = self.dsm5_data.get(condition, {})
        return {
            "name": condition_data.get("name", condition),
            "matching_criteria": matching_criteria,
            "all_criteria": condition_data.get("diagnostic_criteria", []),
            "treatment_goals": condition_data.get("treatment_goals", []),
            "recommended_techniques": condition_data.get("recommended_techniques", [])
        } 