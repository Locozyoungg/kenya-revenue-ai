"""
FILE: config/settings.py
DESCRIPTION: Centralized configuration management
SECURITY: Environment variable injection for secrets
"""

import os
import yaml
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()  # Load .env file

class AppSettings(BaseSettings):
    # Database configuration
    db_host: str = os.getenv('DB_HOST')
    db_port: int = os.getenv('DB_PORT', 5432)
    
    # KRA API credentials
    kra_client_id: str = os.getenv('KRA_CLIENT_ID')
    kra_secret: str = os.getenv('KRA_SECRET')
    
    # Model parameters
    fraud_detection_threshold: float = 0.85
    
    class Config:
        env_file = '.env'

def load_config():
    """Load YAML configuration with environment overrides"""
    with open('config/settings.yaml') as f:
        yaml_config = yaml.safe_load(f)
    
    # Merge environment variables
    env_config = AppSettings().dict()
    return {**yaml_config, **env_config}

# Initialize configuration
config = load_config()