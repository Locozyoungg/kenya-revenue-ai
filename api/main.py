"""
FILE: api/main.py
DESCRIPTION: FastAPI service for taxpayer assistance
"""

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
from nlp.full_pipeline import TaxNLP
import logging

app = FastAPI(
    title="KRA Tax Assistance API",
    description="AI-powered taxpayer support system",
    version="1.0.0"
)

# Security setup
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# Initialize NLP
nlp_processor = TaxNLP()

# Request models
class TaxQuery(BaseModel):
    query: str
    language: Optional[str] = "sw"
    user_id: Optional[str] = None

# Logging configuration
logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_api_key(api_key: str = Security(api_key_header)):
    """
    Validate API key against KRA's auth service
    """
    if not api_key or not is_valid_key(api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return api_key

@app.post("/assist", dependencies=[Security(validate_api_key)])
async def tax_assistance(query: TaxQuery):
    """
    Main endpoint for taxpayer queries
    {
        "query": "Nahitaji msaada na malipo ya VAT",
        "language": "sw",
        "user_id": "12345"
    }
    """
    try:
        # Process query through NLP pipeline
        result = nlp_processor.process_query(
            query.query,
            query.language
        )
        
        # Log interaction
        logging.info(f"Processed query: {query.query} | Result: {result}")
        
        return {
            "success": True,
            "data": result,
            "metadata": {
                "user_id": query.user_id,
                "language": query.language
            }
        }
        
    except Exception as e:
        logging.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

def is_valid_key(api_key: str) -> bool:
    """
    Validate API key against KRA's auth service
    """
    # Implement actual key validation logic
    return api_key == "VALID_API_KEY"

# Run with: uvicorn api.main:app --reload