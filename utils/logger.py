"""
FILE: utils/logger.py
DESCRIPTION: Centralized logging configuration
"""

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logging():
    """
    Configure application logging
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Main application log
    app_log = logging.getLogger("kra_nlp")
    app_log.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "kra_nlp.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(levelname)s - %(message)s"
    ))
    
    app_log.addHandler(file_handler)
    app_log.addHandler(console_handler)
    
    return app_log

# Initialize logger
logger = setup_logging()