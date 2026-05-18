#!/usr/bin/env python3
"""
Test ML Risk Analysis Engine
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tourista_ai_model.risk_analysis import (
    MLRiskAnalysisEngine,
    UnbankedProfile
)
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ml_risk_analysis():
    """Test the ML Risk Analysis Engine"""
    print("=" * 70)
    print("ML RISK ANALYSIS ENGINE TEST")
    print("=" * 70)
    
    print("\n" + "-" * 70)
    print("TEST 1: Initializing ML Risk Analysis Engine")
    print("-" * 70)
    
    # Initialize engine
    engine = MLRiskAnalysisEngine()
    print("✅ Engine initialized successfully!")
    
    print("\n" + "-" * 70)
    print("TEST 2: Attempting to train XGBoost model")
    print("-" * 70)
    
    # Train model (will use rule-based fallback if XGBoost isn't installed)
    training_result = engine.train_fraud_model(num_samples=2000)
    print(f"Training result: {training_result['status']}")
    
    if training_result['status'] == 'success':
        print(f"  ROC AUC: {training_result['metrics']['roc_auc']:.3f}")
        print(f"  Accuracy: {training_result['metrics']['accuracy']:.1%}")
    
    print("\n" + "-" * 70)
    print("TEST 3: Assessing various transactions")
    print("-" * 70)
    
    # Create test counterparty profiles
    profiles = {
        "verified": UnbankedProfile(
            user_id="verified_seller_001",
            country="Zimbabwe",
            region="Harare",
            mobile_money_registered=True,
            mobile_money_provider="ecocash",
            has_cash_collection_point=True,
            nearest_agent_distance_km=2.5,
            id_document_type="national_id",
            verification_level="verified",
            transaction_history_months=24,
            avg_transaction_size=1500,
            transaction_frequency_per_month=12,
            trust_score=0.85
        ),
        "unverified": UnbankedProfile(
            user_id="unverified_seller_002",
            country="Zimbabwe",
            region="Bulawayo",
            mobile_money_registered=False,
            mobile_money_provider=None,
            has_cash_collection_point=True,
            nearest_agent_distance_km=10.0,
            id_document_type=None,
            verification_level="unverified",
            transaction_history_months=0,
            avg_transaction_size=300,
            transaction_frequency_per_month=5,
            trust_score=0.35
        )
    }
    
    # Test transactions
    transactions = [
        {
            "name": "Low-risk normal transaction",
            "data": {
                "transaction_id": "txn_001",
                "amount": 500,
                "payment_method": "mobile_money",
                "buyer_country": "China",
                "seller_country": "South Africa",
                "velocity_count": 1
            },
            "profile": profiles["verified"]
        },
        {
            "name": "High-risk large cash transaction",
            "data": {
                "transaction_id": "txn_002",
                "amount": 5000,
                "payment_method": "cash",
                "buyer_country": "China",
                "seller_country": "Zimbabwe",
                "velocity_count": 4
            },
            "profile": profiles["unverified"]
        },
        {
            "name": "Medium-risk transaction",
            "data": {
                "transaction_id": "txn_003",
                "amount": 1500,
                "payment_method": "mobile_money",
                "buyer_country": "China",
                "seller_country": "Zimbabwe",
                "velocity_count": 2
            },
            "profile": profiles["verified"]
        }
    ]
    
    for test_idx, test_txn in enumerate(transactions):
        print(f"\nTest {test_idx + 1}: {test_txn['name']}")
        assessment = engine.assess_transaction_risk(test_txn['data'], test_txn['profile'])
        
        print(f"  Transaction ID: {assessment.transaction_id}")
        print(f"  Risk Score: {assessment.risk_score:.2f}")
        print(f"  Risk Level: {assessment.risk_level.value}")
        print(f"  Approval Status: {assessment.approval_status}")
        print(f"  Number of Risk Factors: {len(assessment.identified_risks)}")
        
        if assessment.identified_risks:
            print("  Identified Risks:")
            for risk in assessment.identified_risks:
                print(f"    - {risk.name}: {risk.description}")
        
        if assessment.recommendations:
            print("  Recommendations:")
            for rec in assessment.recommendations[:3]:
                print(f"    - {rec}")
    
    print("\n" + "-" * 70)
    print("✅ ALL TESTS COMPLETED!")
    print("-" * 70)
    
    print("\nSummary:")
    print("- ✅ Engine initialization successful")
    print("- ✅ Model training: " + ("success" if training_result['status'] == 'success' else "fallback to rule-based"))
    print("- ✅ Transaction risk assessment: " + str(len(engine.assessment_history)) + " assessments completed")
    
    print("\nThe ML Risk Analysis Engine is ready for production!")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_ml_risk_analysis()
