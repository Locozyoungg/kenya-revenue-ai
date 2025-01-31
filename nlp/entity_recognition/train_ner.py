"""
FILE: nlp/entity_recognition/train_ner.py
MODEL: spaCy + CRF for Kenyan tax entities
ENTITIES: 
  - TAX_FORM (P9A, IT1)
  - KRA_PIN 
  - TAX_TYPE (VAT, PAYE)
  - CURRENCY
"""

import spacy
from spacy.lang.en import English
from spacy.lang.sw import Swahili
import re

class TaxEntityRecognizer:
    def __init__(self):
        """
        Hybrid entity recognizer with rules and ML
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.sw_nlp = Swahili()
        self._add_special_patterns()

    def _add_special_patterns(self):
        """Add regex patterns for KRA-specific entities"""
        # KRA PIN pattern: A letter + 9 digits + another letter
        kra_pin_pattern = re.compile(r"\b[A-Z]\d{9}[A-Z]\b")
        
        ruler = self.nlp.add_pipe("entity_ruler")
        ruler.add_patterns([
            {"label": "KRA_PIN", "pattern": [{"TEXT": {"REGEX": kra_pin_pattern}}]},
            {"label": "TAX_FORM", "pattern": [{"TEXT": {"REGEX": r"\b(P9A|IT1|VAT3)\b"}}]}
        ])

    def extract_entities(self, text):
        """
        Extract tax-related entities from query
        :param text: User input text
        :return: Dictionary of entities
        """
        doc = self.nlp(text) if self._is_english(text) else self.sw_nlp(text)
        
        entities = {
            "TAX_TYPE": [],
            "KRA_PIN": [],
            "TAX_FORM": [],
            "CURRENCY": []
        }

        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Additional currency detection
        currencies = re.findall(r"KES\s?\d+|\d+\s?(shillings|bob)", text)
        entities["CURRENCY"] = currencies

        return entities

    def _is_english(self, text):
        """Simple language detection heuristic"""
        return any(char.isascii() for char in text[:10])

# Example usage:
# ner = TaxEntityRecognizer()
# entities = ner.extract_entities("Nimekosa deadline ya P9A kwa PIN A123456789K")
# {'TAX_FORM': ['P9A'], 'KRA_PIN': ['A123456789K'], ...}