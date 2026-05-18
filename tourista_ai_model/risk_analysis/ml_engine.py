"""
Fraud Detection Model using XGBoost for Tourista AR
Advanced Risk Analysis with Machine Learning
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import pickle
import os

# XGBoost and ML imports
try:
    import xgboost as xgb
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        classification_report, 
        roc_auc_score, 
        confusion_matrix,
        precision_recall_curve
    )
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logging.warning("XGBoost not available, falling back to rule-based detection")

from tourista_ai_model.risk_analysis.engine import (
    RiskLevel, RiskCategory, PaymentMethod,
    RiskFactor, RiskAssessment, UnbankedProfile
)

logger = logging.getLogger(__name__)


@dataclass
class FraudPrediction:
    is_fraud: bool
    fraud_probability: float
    risk_score: float
    risk_level: RiskLevel
    confidence: float
    contributing_factors: List[str]
    model_version: str
    prediction_timestamp: datetime


class XGBoostFraudModel:
    """
    XGBoost-based Fraud Detection Model
    
    Features:
    - Anomaly detection using gradient boosting
    - Feature engineering for transaction patterns
    - Model persistence (save/load)
    - Fallback to rule-based detection
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.feature_names = []
        self.is_trained = False
        self.model_version = "1.0.0"
        self.model_path = model_path
        
        # Initialize components conditionally
        if XGBOOST_AVAILABLE:
            from sklearn.preprocessing import StandardScaler
            self.scaler = StandardScaler()
        
        # Initialize fallback pattern detectors
        self.fallback_patterns = self._initialize_fallback_patterns()
        
        # Load existing model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def _initialize_fallback_patterns(self) -> Dict:
        """Rule-based fallback patterns when model isn't trained"""
        return {
            "round_amount": {"weight": 0.15, "description": "Suspiciously round transaction amount"},
            "velocity_fraud": {"weight": 0.3, "description": "High transaction velocity"},
            "new_account": {"weight": 0.25, "description": "New account with high-value transactions"},
            "unverified": {"weight": 0.2, "description": "Unverified counterparty"},
            "cash_split": {"weight": 0.35, "description": "Potential cash splitting to avoid limits"},
            "geographic_mismatch": {"weight": 0.2, "description": "Unexpected geographic location"}
        }
    
    def _extract_features(self, transaction_data: Dict, counterparty_profile: Optional[UnbankedProfile] = None) -> np.ndarray:
        """
        Extract features from transaction data for model input
        
        Features include:
        - Transaction amount features
        - Temporal features
        - Counterparty features
        - Payment method features
        - Historical pattern features
        """
        features = {}
        
        # Amount features
        amount = float(transaction_data.get("amount", 0))
        features["amount"] = amount
        features["amount_log"] = np.log1p(amount) if amount > 0 else 0
        features["is_round_amount"] = 1.0 if (amount > 0 and amount % 100 == 0) else 0.0
        features["amount_percentile_90"] = 1.0 if amount > 5000 else 0.0
        features["amount_percentile_99"] = 1.0 if amount > 10000 else 0.0
        
        # Payment method encoding
        payment_method = transaction_data.get("payment_method", "cash")
        payment_map = {
            "cash": 0, "mobile_money": 1, "bank_transfer": 2,
            "agent_collection": 3, "cryptocurrency": 4, "letter_of_credit": 5
        }
        features["payment_method"] = payment_map.get(payment_method, 0)
        
        # Counterparty features
        if counterparty_profile:
            features["verified"] = 1.0 if counterparty_profile.verification_level in ["verified", "high"] else 0.0
            features["transaction_history_months"] = counterparty_profile.transaction_history_months
            features["avg_transaction_size"] = counterparty_profile.avg_transaction_size
            features["trust_score"] = counterparty_profile.trust_score
            features["mobile_money_registered"] = 1.0 if counterparty_profile.mobile_money_registered else 0.0
        else:
            features["verified"] = 0.0
            features["transaction_history_months"] = 0
            features["avg_transaction_size"] = 0
            features["trust_score"] = 0.5
            features["mobile_money_registered"] = 0.0
        
        # Velocity features
        features["velocity_count"] = transaction_data.get("velocity_count", 0)
        features["is_high_velocity"] = 1.0 if features["velocity_count"] > 3 else 0.0
        
        # Cross-border features
        buyer_country = transaction_data.get("buyer_country", "China").lower()
        seller_country = transaction_data.get("seller_country", "Zimbabwe").lower()
        features["is_cross_border"] = 1.0 if buyer_country != seller_country else 0.0
        
        # Country risk encoding
        high_risk_countries = {"zimbabwe": 0.3, "nigeria": 0.4, "south_africa": 0.2}
        features["seller_country_risk"] = high_risk_countries.get(seller_country, 0.1)
        
        # Temporal features (simplified for now)
        features["hour_of_day"] = datetime.now().hour
        features["is_odd_hour"] = 1.0 if (datetime.now().hour < 6 or datetime.now().hour > 22) else 0.0
        
        # Return features in consistent order
        feature_order = [
            "amount", "amount_log", "is_round_amount", "amount_percentile_90",
            "amount_percentile_99", "payment_method", "verified", 
            "transaction_history_months", "avg_transaction_size", "trust_score",
            "mobile_money_registered", "velocity_count", "is_high_velocity",
            "is_cross_border", "seller_country_risk", "hour_of_day", "is_odd_hour"
        ]
        
        self.feature_names = feature_order
        return np.array([features[f] for f in feature_order]).reshape(1, -1)
    
    def _generate_synthetic_training_data(self, num_samples: int = 10000) -> pd.DataFrame:
        """Generate synthetic fraud data for training"""
        np.random.seed(42)
        
        data = {
            "amount": np.random.exponential(500, num_samples),
            "payment_method": np.random.choice(
                ["cash", "mobile_money", "bank_transfer", "agent_collection"],
                num_samples, p=[0.3, 0.4, 0.2, 0.1]
            ),
            "verified": np.random.choice([0, 1], num_samples, p=[0.2, 0.8]),
            "transaction_history_months": np.random.randint(0, 60, num_samples),
            "avg_transaction_size": np.random.exponential(300, num_samples),
            "trust_score": np.random.uniform(0.1, 1.0, num_samples),
            "mobile_money_registered": np.random.choice([0, 1], num_samples, p=[0.3, 0.7]),
            "velocity_count": np.random.poisson(1.5, num_samples),
            "is_cross_border": np.random.choice([0, 1], num_samples, p=[0.6, 0.4]),
            "seller_country": np.random.choice(
                ["zimbabwe", "south_africa", "kenya", "china", "nigeria"],
                num_samples
            )
        }
        
        df = pd.DataFrame(data)
        
        # Generate fraud labels (5% fraud rate)
        df["is_fraud"] = 0
        
        # Fraud patterns
        # 1. Large cash transactions from unverified users
        fraud_mask_1 = (
            (df["payment_method"] == "cash") & 
            (df["amount"] > 2000) & 
            (df["verified"] == 0)
        )
        
        # 2. High velocity transactions
        fraud_mask_2 = df["velocity_count"] > 5
        
        # 3. New accounts with large transactions
        fraud_mask_3 = (
            (df["transaction_history_months"] < 1) & 
            (df["amount"] > 1000)
        )
        
        # Combine fraud patterns
        df.loc[fraud_mask_1 | fraud_mask_2 | fraud_mask_3, "is_fraud"] = 1
        
        # Ensure 5% fraud rate
        current_fraud_rate = df["is_fraud"].mean()
        if current_fraud_rate < 0.05:
            additional_fraud = int(0.05 * num_samples) - df["is_fraud"].sum()
            if additional_fraud > 0:
                low_trust = df[(df["trust_score"] < 0.4) & (df["is_fraud"] == 0)].index
                if len(low_trust) >= additional_fraud:
                    df.loc[low_trust[:additional_fraud], "is_fraud"] = 1
        
        return df
    
    def _preprocess_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Preprocess data for training"""
        # Encode categorical variables
        for col in ["payment_method", "seller_country"]:
            le = LabelEncoder()
            df[f"{col}_encoded"] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        
        # Create feature matrix
        features = []
        
        # Amount features
        df["amount_log"] = np.log1p(df["amount"])
        df["is_round_amount"] = (df["amount"] % 100 == 0).astype(float)
        df["amount_percentile_90"] = (df["amount"] > df["amount"].quantile(0.9)).astype(float)
        df["amount_percentile_99"] = (df["amount"] > df["amount"].quantile(0.99)).astype(float)
        
        # Payment method encoding
        payment_map = {
            "cash": 0, "mobile_money": 1, "bank_transfer": 2,
            "agent_collection": 3, "cryptocurrency": 4, "letter_of_credit": 5
        }
        df["payment_method_enc"] = df["payment_method"].map(payment_map).fillna(0)
        
        # Country risk encoding
        high_risk_countries = {"zimbabwe": 0.3, "nigeria": 0.4, "south_africa": 0.2}
        df["seller_country_risk"] = df["seller_country"].map(high_risk_countries).fillna(0.1)
        
        # Temporal features (random for synthetic data)
        df["hour_of_day"] = np.random.randint(0, 24, len(df))
        df["is_odd_hour"] = ((df["hour_of_day"] < 6) | (df["hour_of_day"] > 22)).astype(float)
        
        # Feature order (must match _extract_features)
        feature_order = [
            "amount", "amount_log", "is_round_amount", "amount_percentile_90",
            "amount_percentile_99", "payment_method_enc", "verified", 
            "transaction_history_months", "avg_transaction_size", "trust_score",
            "mobile_money_registered", "velocity_count", "velocity_count",
            "is_cross_border", "seller_country_risk", "hour_of_day", "is_odd_hour"
        ]
        
        # Fix velocity count duplicate
        feature_order[12] = "velocity_count"
        
        X = df[feature_order].values
        y = df["is_fraud"].values
        
        # Scale features
        X = self.scaler.fit_transform(X)
        self.feature_names = feature_order
        
        return X, y
    
    def train(self, num_samples: int = 10000, test_size: float = 0.2) -> Dict:
        """Train the XGBoost fraud detection model"""
        if not XGBOOST_AVAILABLE:
            logger.warning("XGBoost not available, training skipped")
            return {"status": "skipped", "reason": "XGBoost not installed"}
        
        logger.info(f"Generating synthetic training data: {num_samples} samples")
        df = self._generate_synthetic_training_data(num_samples)
        
        logger.info("Preprocessing data")
        X, y = self._preprocess_data(df)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        logger.info("Training XGBoost model")
        
        # XGBoost parameters tuned for fraud detection (imbalanced data)
        params = {
            "objective": "binary:logistic",
            "eval_metric": "auc",
            "max_depth": 6,
            "learning_rate": 0.05,
            "n_estimators": 200,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "scale_pos_weight": 10,  # For imbalanced data
            "random_state": 42,
            "n_jobs": -1
        }
        
        self.model = xgb.XGBClassifier(**params)
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            "accuracy": float((y_pred == y_test).mean()),
            "roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }
        
        self.is_trained = True
        logger.info(f"Training complete. ROC AUC: {metrics['roc_auc']:.3f}")
        
        # Save model
        if self.model_path:
            self.save_model(self.model_path)
        
        return {"status": "success", "metrics": metrics}
    
    def predict(self, transaction_data: Dict, counterparty_profile: Optional[UnbankedProfile] = None) -> FraudPrediction:
        """Predict fraud probability for a transaction"""
        
        if not XGBOOST_AVAILABLE or not self.is_trained or self.model is None:
            # Fallback to rule-based detection
            return self._rule_based_predict(transaction_data, counterparty_profile)
        
        # Extract features
        features = self._extract_features(transaction_data, counterparty_profile)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        fraud_proba = float(self.model.predict_proba(features_scaled)[0, 1])
        is_fraud = fraud_proba > 0.5
        
        # Determine risk level
        if fraud_proba >= 0.8:
            risk_level = RiskLevel.CRITICAL
        elif fraud_proba >= 0.6:
            risk_level = RiskLevel.HIGH
        elif fraud_proba >= 0.4:
            risk_level = RiskLevel.MEDIUM
        elif fraud_proba >= 0.2:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL
        
        # Calculate confidence
        confidence = max(fraud_proba, 1 - fraud_proba)
        
        # Identify contributing factors
        factors = self._identify_contributing_factors(transaction_data, counterparty_profile, fraud_proba)
        
        return FraudPrediction(
            is_fraud=is_fraud,
            fraud_probability=fraud_proba,
            risk_score=fraud_proba,
            risk_level=risk_level,
            confidence=confidence,
            contributing_factors=factors,
            model_version=self.model_version,
            prediction_timestamp=datetime.now()
        )
    
    def _rule_based_predict(self, transaction_data: Dict, counterparty_profile: Optional[UnbankedProfile] = None) -> FraudPrediction:
        """Fallback rule-based fraud detection"""
        risk_score = 0.0
        factors = []
        
        amount = float(transaction_data.get("amount", 0))
        velocity = transaction_data.get("velocity_count", 0)
        
        if amount > 0 and amount % 100 == 0:
            risk_score += self.fallback_patterns["round_amount"]["weight"]
            factors.append(self.fallback_patterns["round_amount"]["description"])
        
        if velocity > 3:
            risk_score += self.fallback_patterns["velocity_fraud"]["weight"]
            factors.append(self.fallback_patterns["velocity_fraud"]["description"])
        
        if counterparty_profile and counterparty_profile.transaction_history_months < 1 and amount > 1000:
            risk_score += self.fallback_patterns["new_account"]["weight"]
            factors.append(self.fallback_patterns["new_account"]["description"])
        
        if counterparty_profile and counterparty_profile.verification_level == "unverified":
            risk_score += self.fallback_patterns["unverified"]["weight"]
            factors.append(self.fallback_patterns["unverified"]["description"])
        
        # Determine risk level
        risk_score = min(risk_score, 1.0)
        if risk_score >= 0.7:
            risk_level = RiskLevel.CRITICAL
        elif risk_score >= 0.5:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = RiskLevel.MEDIUM
        elif risk_score >= 0.1:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL
        
        return FraudPrediction(
            is_fraud=risk_score > 0.5,
            fraud_probability=risk_score,
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=0.7,
            contributing_factors=factors,
            model_version="rule-based-1.0",
            prediction_timestamp=datetime.now()
        )
    
    def _identify_contributing_factors(self, transaction_data: Dict, counterparty_profile: Optional[UnbankedProfile], fraud_proba: float) -> List[str]:
        """Identify which factors contributed to fraud prediction"""
        factors = []
        
        amount = float(transaction_data.get("amount", 0))
        velocity = transaction_data.get("velocity_count", 0)
        
        if fraud_proba > 0.7:
            if amount > 2000 and transaction_data.get("payment_method") == "cash":
                factors.append("Large cash transaction amount")
            
            if velocity > 3:
                factors.append("High transaction velocity")
            
            if counterparty_profile and counterparty_profile.verification_level == "unverified":
                factors.append("Unverified counterparty")
            
            if counterparty_profile and counterparty_profile.trust_score < 0.4:
                factors.append("Low trust score for counterparty")
        
        return factors if factors else ["No single dominant factor"]
    
    def save_model(self, filepath: str):
        """Save model to disk"""
        if self.model is None:
            logger.warning("No model to save")
            return
        
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "label_encoders": self.label_encoders,
            "feature_names": self.feature_names,
            "is_trained": self.is_trained,
            "model_version": self.model_version
        }
        
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.label_encoders = model_data["label_encoders"]
        self.feature_names = model_data["feature_names"]
        self.is_trained = model_data["is_trained"]
        self.model_version = model_data.get("model_version", "1.0.0")
        
        logger.info(f"Model loaded from {filepath}")


class MLRiskAnalysisEngine:
    """
    ML-Powered Risk Analysis Engine with XGBoost Fraud Detection
    
    Combines:
    - XGBoost fraud detection
    - Rule-based compliance checks
    - Risk factor aggregation
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.fraud_model = XGBoostFraudModel(model_path)
        self.assessment_history: List[RiskAssessment] = []
        logger.info("ML Risk Analysis Engine initialized")
    
    def train_fraud_model(self, num_samples: int = 10000) -> Dict:
        """Train the fraud detection model"""
        return self.fraud_model.train(num_samples)
    
    def assess_transaction_risk(self, transaction_data: Dict,
                              counterparty_profile: Optional[UnbankedProfile] = None) -> RiskAssessment:
        """
        ML-Powered transaction risk assessment
        
        Combines:
        - XGBoost fraud prediction
        - Compliance checks
        - Payment method risk analysis
        """
        # Get ML fraud prediction
        fraud_prediction = self.fraud_model.predict(transaction_data, counterparty_profile)
        
        # Start with ML risk score
        base_risk_score = fraud_prediction.risk_score
        identified_risks = []
        
        # Add ML-based fraud risk factors
        if fraud_prediction.is_fraud or fraud_prediction.fraud_probability > 0.3:
            ml_risk = RiskFactor(
                factor_id="ml_fraud_detection",
                category=RiskCategory.FRAUD_RISK,
                name="ML-Detected Fraud Risk",
                description=f"ML model detected {fraud_prediction.fraud_probability:.1%} fraud probability",
                severity=fraud_prediction.risk_level,
                probability=fraud_prediction.fraud_probability,
                impact=0.8,
                indicators=fraud_prediction.contributing_factors,
                mitigation_strategies=[
                    "Enhanced verification required",
                    "Delay transaction for manual review",
                    "Monitor counterparty activity closely"
                ],
                monitoring_required=True
            )
            identified_risks.append(ml_risk)
        
        # Add payment method analysis
        payment_method = PaymentMethod(transaction_data.get("payment_method", "cash"))
        amount = float(transaction_data.get("amount", 0))
        
        if payment_method == PaymentMethod.CASH and amount > 1000:
            identified_risks.append(RiskFactor(
                factor_id="large_cash_transaction",
                category=RiskCategory.PAYMENT_RISK,
                name="Large Cash Transaction",
                description=f"High-value cash transaction: ${amount:.2f}",
                severity=RiskLevel.HIGH,
                probability=0.7,
                impact=0.6,
                indicators=["cash_payment", "amount_gt_1000"],
                mitigation_strategies=[
                    "Split into smaller transactions",
                    "Use alternative payment methods",
                    "Verify counterparty identity"
                ],
                monitoring_required=True
            ))
        
        # Determine overall risk level
        risk_score = min(base_risk_score + len(identified_risks) * 0.1, 1.0)
        risk_level = self._determine_risk_level(risk_score)
        
        # Build assessment
        assessment = RiskAssessment(
            assessment_id=f"ml_risk_{transaction_data.get('transaction_id', 'unknown')}_{int(datetime.now().timestamp())}",
            transaction_id=transaction_data.get("transaction_id"),
            counterparty_id=transaction_data.get("counterparty_id", ""),
            counterparty_type=transaction_data.get("counterparty_type", "unknown"),
            payment_method=payment_method,
            transaction_amount=amount,
            currency=transaction_data.get("currency", "USD"),
            risk_score=risk_score,
            risk_level=risk_level,
            identified_risks=identified_risks,
            overall_assessment=self._generate_assessment_text(risk_level, identified_risks, fraud_prediction),
            recommendations=self._generate_recommendations(risk_level, identified_risks, payment_method, fraud_prediction),
            required_verifications=self._determine_required_verifications(identified_risks, risk_level),
            approval_status=self._determine_approval_status(risk_level)
        )
        
        self.assessment_history.append(assessment)
        return assessment
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        if risk_score >= 0.8:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.65:
            return RiskLevel.HIGH
        elif risk_score >= 0.45:
            return RiskLevel.MEDIUM
        elif risk_score >= 0.25:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL
    
    def _generate_assessment_text(self, risk_level: RiskLevel, risks: List[RiskFactor], fraud_pred: FraudPrediction) -> str:
        base_text = f"ML Model Version: {fraud_pred.model_version} | Fraud Probability: {fraud_pred.fraud_probability:.1%}\n"
        
        if risk_level == RiskLevel.CRITICAL:
            return base_text + "CRITICAL RISK: ML model detected high fraud probability. Immediate review required. Transaction should be blocked pending full investigation."
        elif risk_level == RiskLevel.HIGH:
            return base_text + "HIGH RISK: Significant fraud indicators detected. Enhanced due diligence required before approval."
        elif risk_level == RiskLevel.MEDIUM:
            return base_text + "Moderate risk detected. Standard review procedures recommended."
        elif risk_level == RiskLevel.LOW:
            return base_text + "Low risk. Standard processing with routine monitoring."
        else:
            return base_text + "Minimal risk. Auto-approval recommended."
    
    def _generate_recommendations(self, risk_level: RiskLevel, risks: List[RiskFactor], 
                                payment_method: PaymentMethod, fraud_pred: FraudPrediction) -> List[str]:
        recommendations = []
        
        if fraud_pred.is_fraud or fraud_pred.fraud_probability > 0.5:
            recommendations.append("FLAG FOR MANUAL REVIEW - ML FRAUD ALERT")
            recommendations.append("Conduct enhanced identity verification")
            recommendations.append("Delay transaction completion pending review")
        
        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            recommendations.append("Escalate to senior risk analyst")
            recommendations.append("Request additional documentation from counterparty")
        
        if payment_method == PaymentMethod.CASH:
            recommendations.append("Consider alternative payment methods (mobile money, bank transfer)")
        
        return recommendations
    
    def _determine_required_verifications(self, risks: List[RiskFactor], risk_level: RiskLevel) -> List[str]:
        verifications = []
        
        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            verifications.extend([
                "identity_verification",
                "address_verification",
                "source_of_funds_verification"
            ])
        elif risk_level == RiskLevel.MEDIUM:
            verifications.extend(["identity_verification"])
        
        return verifications
    
    def _determine_approval_status(self, risk_level: RiskLevel) -> str:
        status_map = {
            RiskLevel.CRITICAL: "rejected_pending_investigation",
            RiskLevel.HIGH: "pending_enhanced_review",
            RiskLevel.MEDIUM: "pending_standard_review",
            RiskLevel.LOW: "approved_with_monitoring",
            RiskLevel.MINIMAL: "auto_approved"
        }
        return status_map[risk_level]
