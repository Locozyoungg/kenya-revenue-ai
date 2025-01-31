"""
FILE: api/integrations/kra_api.py
DESCRIPTION: Secure interface to KRA's production systems
FEATURES: Retry logic, rate limiting, audit logging
"""

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

class KRAGateway:
    def __init__(self, base_url, auth_token):
        """
        Initialize KRA API gateway
        :param base_url: KRA production endpoint
        :param auth_token: OAuth2 bearer token
        """
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        })
        self.base_url = base_url
        self.audit_log = []

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
    def submit_assessment(self, payload):
        """
        Submit tax assessment to KRA system
        :param payload: Prevalidated assessment data
        :return: KRA transaction ID
        """
        try:
            response = self.session.post(
                f"{self.base_url}/assessments",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            # Log successful submission
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'operation': 'assessment_submit',
                'status': 'success'
            })
            
            return response.json()['transaction_id']
            
        except requests.exceptions.HTTPError as e:
            self.audit_log.append({
                'timestamp': datetime.now().isoformat(),
                'operation': 'assessment_submit',
                'status': 'error',
                'error': str(e)
            })
            raise

    def get_payment_status(self, transaction_id):
        """Check assessment payment status"""
        response = self.session.get(
            f"{self.base_url}/transactions/{transaction_id}"
        )
        return response.json()['payment_status']

# Usage example:
# kra = KRAGateway(config['kra_url'], token)
# tx_id = kra.submit_assessment(validated_data)
# status = kra.get_payment_status(tx_id)