"""
FILE: nlp/full_pipeline.py
DESCRIPTION: End-to-end NLP processing for taxpayer queries
"""

from transformers import pipeline
from typing import Dict, Any
import re

class TaxNLP:
    def __init__(self):
        """
        Initialize all NLP components
        """
        # Load multilingual models
        self.translator = pipeline("translation", model="Helsinki-NLP/opus-mt-sw-en")
        self.classifier = self._load_intent_classifier()
        self.ner = self._load_entity_recognizer()
        self.sentiment = pipeline("sentiment-analysis")
        
        # Tax-specific configurations
        self.TAX_TERMS = {
            "sw": {"VAT": "VAT", "PAYE": "PAYE", "P9A": "P9A"},
            "en": {"VAT": "VAT", "PAYE": "PAYE", "P9A": "P9A"}
        }
        
    def _load_intent_classifier(self):
        """Load fine-tuned intent classification model"""
        return pipeline(
            "text-classification", 
            model="models/nlp/intent_classifier"
        )

    def _load_entity_recognizer(self):
        """Load custom NER model"""
        return pipeline(
            "ner", 
            model="models/nlp/entity_recognizer",
            grouped_entities=True
        )

    def process_query(self, query: str, language: str = "sw") -> Dict[str, Any]:
        """
        Full NLP processing pipeline
        :param query: User input text
        :param language: Preferred response language
        :return: Structured analysis results
        """
        try:
            # Step 1: Language detection and normalization
            normalized_text = self._normalize_text(query, language)
            
            # Step 2: Intent classification
            intent = self.classifier(normalized_text)[0]
            
            # Step 3: Entity extraction
            entities = self.ner(normalized_text)
            tax_entities = self._filter_tax_entities(entities)
            
            # Step 4: Sentiment analysis
            sentiment = self.sentiment(normalized_text)[0]
            
            return {
                "intent": intent['label'],
                "confidence": intent['score'],
                "entities": tax_entities,
                "sentiment": sentiment['label'],
                "language": language
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "fallback_response": self._get_fallback_response(language)
            }

    def _normalize_text(self, text: str, language: str) -> str:
        """
        Standardize text for processing
        :param text: Raw input
        :param language: Target language
        :return: Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Replace tax terms with standard forms
        for term, standard in self.TAX_TERMS[language].items():
            text = text.replace(term.lower(), standard)
            
        # Remove special characters
        text = re.sub(r"[^\w\s]", "", text)
        
        return text

    def _filter_tax_entities(self, entities: list) -> dict:
        """
        Extract tax-specific entities
        :param entities: Raw NER results
        :return: Structured tax entities
        """
        tax_entities = {
            "TAX_TYPE": [],
            "KRA_PIN": [],
            "AMOUNT": [],
            "DATE": []
        }
        
        for entity in entities:
            label = entity['entity_group']
            if label in tax_entities:
                tax_entities[label].append(entity['word'])
                
        return tax_entities

    def _get_fallback_response(self, language: str) -> str:
        """
        Default response for failed processing
        :param language: Preferred language
        :return: Fallback message
        """
        return {
            "sw": "Samahani, kuna tatizo la kiufundi. Tafadhali jaribu tena baadaye.",
            "en": "Sorry, we're experiencing technical difficulties. Please try again later."
        }[language]

# Example usage:
# nlp = TaxNLP()
# result = nlp.process_query("Nahitaji msaada na malipo ya VAT", language="sw")