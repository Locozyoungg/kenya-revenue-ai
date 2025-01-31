"""
FILE: data/ingestion.py
DESCRIPTION: Unified data collection from multiple government sources
TECH STACK: Pandas, Requests, M-Pesa SDK
"""

import json
from datetime import datetime
import pandas as pd
from pydantic import ValidationError
from .schemas.data_contracts import KRATaxSchema, MpesaTransactionSchema

class DataIngestor:
    def __init__(self, config):
        """
        Initialize data ingestion system
        :param config: Loaded configuration from settings.yaml
        """
        self.sources = config['data_sources']
        self._setup_clients()

    def _setup_clients(self):
        """Initialize API clients with rate limiting"""
        self.kra_client = KRAClient(
            self.sources['kra']['client_id'],
            self.sources['kra']['secret']
        )
        self.mpesa_client = MpesaClient(
            api_key=self.sources['mpesa']['key'],
            api_secret=self.sources['mpesa']['secret']
        )

    def _validate_record(self, record, schema):
        """
        Validate data against predefined schemas
        :param record: Raw data record
        :param schema: Pydantic model class
        :return: Validated record or None
        """
        try:
            return schema(**record).dict()
        except ValidationError as e:
            self.logger.error(f"Validation failed: {e.json()}")
            return None

    def fetch_kra_data(self, start_date: str, end_date: str):
        """
        Fetch and validate KRA taxpayer records
        :param start_date: YYYY-MM-DD
        :param end_date: YYYY-MM-DD
        :return: Clean DataFrame
        """
        raw_data = self.kra_client.get_taxpayers(start_date, end_date)
        validated = [self._validate_record(r, KRATaxSchema) for r in raw_data]
        return pd.DataFrame([v for v in validated if v is not None])

    def fetch_mpesa_data(self, business_code: str):
        """
        Retrieve mobile money transactions
        :param business_code: KRA-registered paybill
        :return: Standardized transaction DF
        """
        raw = self.mpesa_client.transactions(business_code)
        return pd.DataFrame([
            self._validate_record(t, MpesaTransactionSchema) 
            for t in raw
        ])

# Example usage:
# ingestor = DataIngestor(config)
# kra_df = ingestor.fetch_kra_data('2024-01-01', '2024-03-31')
# mpesa_df = ingestor.fetch_mpesa_data('123456')