"""
FILE: nlp/tax_knowledge/knowledge_connector.py
INTEGRATION: KRA Document Management System + FAQ Database
"""

from rank_bm25 import BM25Okapi
import sqlite3

class TaxKnowledgeBase:
    def __init__(self, db_path="nlp/tax_knowledge/tax_db.sqlite"):
        """
        Semantic search over tax regulations
        :param db_path: Path to SQLite knowledge base
        """
        self.conn = sqlite3.connect(db_path)
        self._build_search_index()

    def _build_search_index(self):
        """Create BM25 search index from documents"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM tax_documents")
        self.documents = [row[0] for row in cursor.fetchall()]
        self.bm25 = BM25Okapi([doc.split() for doc in self.documents])

    def search(self, query, language="sw"):
        """
        Find relevant tax articles
        :param query: Natural language question
        :param language: Preferred response language
        :return: Formatted answer from official docs
        """
        tokenized_query = query.split()
        doc_scores = self.bm25.get_scores(tokenized_query)
        best_match_idx = doc_scores.argmax()
        
        return self._format_response(
            self.documents[best_match_idx], 
            language
        )

    def _format_response(self, text, language):
        """Localize and simplify official text"""
        # Implement translation and summarization
        return text[:500] + "..."  # Temporary implementation

# Example usage:
# kb = TaxKnowledgeBase()
# answer = kb.search("Muda wa kuwasilisha fomu ya VAT")