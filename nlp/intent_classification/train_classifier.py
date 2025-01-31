"""
FILE: nlp/intent_classification/train_classifier.py
MODEL: XLM-RoBERTa fine-tuned on Kenyan tax corpus
TASKS: Detect intent in Swahili/English code-switched queries
"""

from transformers import XLMRobertaForSequenceClassification, XLMRobertaTokenizer
import torch

class TaxIntentClassifier:
    def __init__(self, model_path="models/nlp/intent_classifier"):
        """
        Initialize multilingual tax intent classifier
        :param model_path: Path to fine-tuned model
        """
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
        self.model = XLMRobertaForSequenceClassification.from_pretrained(model_path)
        self.labels = [
            "payment_issue", 
            "deadline_query",
            "form_help",
            "complaint",
            "policy_clarification"
        ]

    def predict_intent(self, text):
        """
        Classify taxpayer query intent
        :param text: Raw user input (English/Swahili mix)
        :return: Predicted intent and confidence
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        confidence, pred_idx = torch.max(probs, dim=1)
        
        return {
            "intent": self.labels[pred_idx.item()],
            "confidence": confidence.item()
        }

# Example usage:
# classifier = TaxIntentClassifier()
# query = "Nina shida kulipa KRA kwa M-Pesa, sielewi"
# result = classifier.predict_intent(query)  # {'intent': 'payment_issue', 'confidence': 0.92}