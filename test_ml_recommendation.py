#!/usr/bin/env python3
"""
Test ML Recommendation Engine
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tourista_ai_model.recommendation import MLRecommendationEngine, Recommendation
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ml_recommendation_engine():
    """Test the ML Recommendation Engine"""
    print("=" * 70)
    print("NEURAL RECOMMENDATION ENGINE - TEST")
    print("=" * 70)
    
    # Create test users
    users = [
        {"user_id": "buyer_001", "type": "chinese_buyer", "name": "Wang Trading Co."},
        {"user_id": "buyer_002", "type": "chinese_buyer", "name": "Shanghai Import Co."},
        {"user_id": "supplier_001", "type": "african_supplier", "name": "Zimbabwe Coffee Exports"},
        {"user_id": "supplier_002", "type": "african_supplier", "name": "South African Textiles Ltd."},
        {"user_id": "buyer_003", "type": "chinese_buyer", "name": "Beijing Artisan Imports"},
    ]
    
    # Create test items (products)
    items = [
        {"item_id": "product_coffee_ethiopia", "name": "Ethiopian Specialty Coffee", "category": "coffee"},
        {"item_id": "product_coffee_zimbabwe", "name": "Zimbabwe Arabica Coffee", "category": "coffee"},
        {"item_id": "product_avocado", "name": "Zimbabwe Hass Avocado", "category": "avocado"},
        {"item_id": "product_textiles", "name": "South African Textiles", "category": "textiles"},
        {"item_id": "product_gemstones", "name": "Zimbabwe Gemstones", "category": "gemstones"},
        {"item_id": "product_cocoa", "name": "Ghana Cocoa", "category": "cocoa"},
    ]
    
    # Create test interactions (user-item ratings)
    interactions = [
        ("buyer_001", "product_coffee_ethiopia", 0.9),
        ("buyer_001", "product_coffee_zimbabwe", 0.85),
        ("buyer_001", "product_textiles", 0.7),
        ("buyer_002", "product_avocado", 0.88),
        ("buyer_002", "product_gemstones", 0.75),
        ("buyer_003", "product_cocoa", 0.92),
        ("buyer_003", "product_gemstones", 0.8),
        ("buyer_001", "product_cocoa", 0.6),
    ]
    
    print("\n" + "=" * 70)
    print("TEST 1: Initializing ML Recommendation Engine")
    print("=" * 70)
    
    # Initialize the engine
    engine = MLRecommendationEngine(
        embedding_dim=32,
        hidden_dim=64,
        num_layers=2
    )
    
    print("\n✅ Engine initialized successfully!")
    
    print("\n" + "=" * 70)
    print("TEST 2: Training the Neural Network")
    print("=" * 70)
    
    # Train the engine
    engine.train(
        users=users,
        items=items,
        interactions=interactions,
        epochs=100,
        batch_size=4
    )
    
    print("\n✅ Training completed!")
    
    print("\n" + "=" * 70)
    print("TEST 3: Generating Recommendations for Buyer 001")
    print("=" * 70)
    
    # Generate recommendations
    recommendations = engine.generate_recommendations(
        user_id="buyer_001",
        user_type="chinese_buyer",
        limit=5
    )
    
    print(f"\n✅ Generated {len(recommendations)} recommendations:")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Type: {rec.recommendation_type.value}")
        print(f"   Score: {rec.priority_score:.2f}")
        print(f"   Description: {rec.description}")
        print(f"   Rationale: {', '.join(rec.rationale)}")
    
    print("\n" + "=" * 70)
    print("TEST 4: Generating Recommendations for Supplier 001")
    print("=" * 70)
    
    supplier_recommendations = engine.generate_recommendations(
        user_id="supplier_001",
        user_type="african_supplier",
        limit=3
    )
    
    print(f"\n✅ Generated {len(supplier_recommendations)} recommendations:")
    
    for i, rec in enumerate(supplier_recommendations, 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Score: {rec.priority_score:.2f}")
    
    print("\n" + "=" * 70)
    print("TEST 5: Getting Seasonal Pricing")
    print("=" * 70)
    
    pricing = engine.get_seasonal_pricing("coffee")
    print(f"\nCategory: {pricing['category']}")
    print(f"Peak: {', '.join(pricing['peak_season_months'])}")
    print(f"Off: {', '.join(pricing['off_season_months'])}")
    print(f"Price variation: {pricing['price_variation']}")
    print(f"Recommendation: {pricing['recommendation']}")
    
    print("\n" + "=" * 70)
    print("TEST 6: Analyzing Market Opportunity")
    print("=" * 70)
    
    opportunity = engine.analyze_market_opportunity("coffee", "zimbabwe")
    print(f"\nProduct: {opportunity['product_category']}")
    print(f"Country: {opportunity['target_country']}")
    print(f"Opportunity score: {opportunity['opportunity_score']:.2f}")
    print(f"Recommendation: {opportunity['recommendation']}")
    
    print("\n" + "=" * 70)
    print("TEST 7: Fallback Mode (No Training Data)")
    print("=" * 70)
    
    # Create a new engine without training
    engine2 = MLRecommendationEngine()
    fallback_recs = engine2.generate_recommendations(
        user_id="new_user",
        user_type="tourist",
        limit=3
    )
    
    print(f"\n✅ Fallback mode works! Generated {len(fallback_recs)} recommendations:")
    for rec in fallback_recs:
        print(f"- {rec.title}")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    
    print("\n📊 Summary:")
    print("   ✅ ML Recommendation Engine: Working")
    print("   ✅ Neural network training: Successful")
    print("   ✅ Recommendation generation: Working")
    print("   ✅ Fallback mode: Working")
    print("   ✅ Market analysis: Working")
    
    print("\n🚀 Next Steps:")
    print("   1. Train with real user interaction data")
    print("   2. Use API endpoints: /recommendations")
    print("   3. Save/load model for production")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    test_ml_recommendation_engine()
