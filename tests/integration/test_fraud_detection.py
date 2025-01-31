"""
FILE: tests/integration/test_fraud_detection.py
DESCRIPTION: Integration tests for fraud detection pipeline
"""

import pytest
from models.fraud_detection.train import FraudModelTrainer

@pytest.fixture
def sample_data():
    return {
        'amount': [150000, 50000, 2500000],
        'frequency': [2, 45, 1],
        'declared_income': [50000, 120000, 500000],
        'sector_code': ['A', 'B', 'A'],
        'business_type': ['retail', 'service', 'manufacturing'],
        'is_fraud': [0, 1, 1]
    }

def test_full_pipeline(sample_data):
    """Test complete model training and inference flow"""
    trainer = FraudModelTrainer(config['fraud_model'])
    
    # Train model
    X = pd.DataFrame(sample_data).drop('is_fraud', axis=1)
    y = sample_data['is_fraud']
    trainer.train(X, y)
    
    # Test inference
    test_case = X.iloc[0:1]
    prediction = trainer.model.predict(test_case)
    
    assert prediction in [0, 1]
    assert hasattr(trainer.model, 'feature_importances_')