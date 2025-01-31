"""
FILE: utils/error_handler.py
DESCRIPTION: Centralized error handling utilities
"""

from fastapi import HTTPException
from typing import Dict, Any
import traceback

class TaxAPIError(Exception):
    """Base exception for API errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def handle_api_error(error: Exception) -> Dict[str, Any]:
    """
    Standard error response format
    :param error: Exception instance
    :return: Formatted error response
    """
    if isinstance(error, TaxAPIError):
        return {
            "error": error.message,
            "status_code": error.status_code,
            "type": error.__class__.__name__
        }
        
    # Log unexpected errors
    traceback.print_exc()
    
    return {
        "error": "Internal server error",
        "status_code": 500,
        "type": "UnexpectedError"
    }

def create_error_response(error: Exception):
    """
    Create HTTPException from custom errors
    """
    error_info = handle_api_error(error)
    return HTTPException(
        status_code=error_info['status_code'],
        detail={
            "message": error_info['error'],
            "type": error_info['type']
        }
    )