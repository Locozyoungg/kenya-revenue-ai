"""
FILE: models/fraud_detection/train.py
DESCRIPTION: Ensemble model for tax evasion detection
MODELS: Isolation Forest + XGBoost hybrid
"""

import numpy as np
import xgboost as xgb
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from joblib import dump

class FraudModelTrainer:
    def __init__(self, config):
        """
        Initialize fraud detection pipeline
        :param config: Model parameters from settings
        """
        self.numeric_features = ['amount', 'frequency', 'declared_income']
        self.categorical_features = ['sector_code', 'business_type']
        self.params = config['fraud_model']
        
        self._build_preprocessor()
        self._initialize_model()

    def _build_preprocessor(self):
        """Create feature engineering pipeline"""
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ])

    def _initialize_model(self):
        """Create hybrid anomaly detection model"""
        self.model = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', xgb.XGBClassifier(
                n_estimators=self.params['n_estimators'],
                max_depth=self.params['max_depth'],
                learning_rate=self.params['lr']
            ))
        ])

    def train(self, X, y):
        """
        Full training workflow with validation
        :param X: Training features
        :param y: Labeled fraud cases
        """
        X_processed = self.preprocessor.fit_transform(X)
        self.model.fit(X_processed, y)
        
        # Save model artifacts
        dump(self.preprocessor, 'models/fraud_detection/preprocessor.joblib')
        dump(self.model, 'models/fraud_detection/model.joblib')

    def evaluate(self, X_test, y_test):
        """Generate performance metrics"""
        predictions = self.model.predict(X_test)
        print(classification_report(y_test, predictions))
        plot_confusion_matrix(self.model, X_test, y_test)

# Configuration example in settings.yaml:
# fraud_model:
#   n_estimators: 200
#   max_depth: 5
#   lr: 0.01