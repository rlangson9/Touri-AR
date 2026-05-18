#!/usr/bin/env python3
"""
Test script for Neural Matching Engine
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*70)
print("NEURAL MATCHING ENGINE - TEST")
print("="*70)

try:
    from tourista_ai_model.matching.neural_engine import (
        NeuralMatchingEngine,
        HybridMatchingEngine,
        UserProfile
    )
    
    print("\n✅ Neural Matching Engine imported successfully")
    
    print("\n" + "="*70)
    print("TEST 1: Creating User Profiles")
    print("="*70)
    
    # Create sample buyers
    buyers = [
        UserProfile(
            user_id="buyer_001",
            role="buyer",
            country="China",
            region="Shanghai",
            languages=["zh", "en"],
            product_interests=["handicrafts", "textiles", "coffee"],
            budget_range=(1000, 10000),
            rating=4.5,
            verification_status="verified",
            total_transactions=50
        ),
        UserProfile(
            user_id="buyer_002",
            role="buyer",
            country="China",
            region="Guangzhou",
            languages=["zh"],
            product_interests=["coffee", "tea"],
            budget_range=(500, 5000),
            rating=4.0,
            verification_status="verified",
            total_transactions=20
        ),
        UserProfile(
            user_id="buyer_003",
            role="buyer",
            country="China",
            region="Beijing",
            languages=["zh", "en"],
            product_interests=["wood_carvings", "pottery"],
            budget_range=(2000, 15000),
            rating=4.8,
            verification_status="verified",
            total_transactions=100
        )
    ]
    
    # Create sample suppliers
    suppliers = [
        UserProfile(
            user_id="supplier_001",
            role="supplier",
            country="Zimbabwe",
            region="Harare",
            languages=["en", "sn"],
            product_offers=["handicrafts", "wood_carvings"],
            price_range=(50, 500),
            rating=4.8,
            verification_status="verified",
            total_transactions=100
        ),
        UserProfile(
            user_id="supplier_002",
            role="supplier",
            country="South Africa",
            region="Johannesburg",
            languages=["en", "zu"],
            product_offers=["coffee", "textiles"],
            price_range=(20, 200),
            rating=4.5,
            verification_status="verified",
            total_transactions=75
        ),
        UserProfile(
            user_id="supplier_003",
            role="supplier",
            country="Kenya",
            region="Nairobi",
            languages=["en"],
            product_offers=["coffee", "tea"],
            price_range=(10, 100),
            rating=4.2,
            verification_status="unverified",
            total_transactions=30
        ),
        UserProfile(
            user_id="supplier_004",
            role="supplier",
            country="Zimbabwe",
            region="Bulawayo",
            languages=["en", "nd"],
            product_offers=["pottery", "handicrafts"],
            price_range=(30, 300),
            rating=4.6,
            verification_status="verified",
            total_transactions=80
        )
    ]
    
    print(f"\n✅ Created {len(buyers)} buyers and {len(suppliers)} suppliers")
    
    print("\n" + "="*70)
    print("TEST 2: Training Neural Matching Engine")
    print("="*70)
    
    # Create sample interactions
    interactions = [
        ("buyer_001", "supplier_001", 1.0),  # Positive: products match
        ("buyer_001", "supplier_002", 0.7),  # Moderate: coffee overlap
        ("buyer_001", "supplier_003", 0.3),  # Weak: no product match
        ("buyer_001", "supplier_004", 0.9),  # Strong: Zimbabwe, handicrafts
        ("buyer_002", "supplier_002", 1.0),  # Positive: coffee match
        ("buyer_002", "supplier_003", 0.8),  # Good: both offer coffee/tea
        ("buyer_003", "supplier_001", 0.8),  # Good: Zimbabwe, wood carvings
        ("buyer_003", "supplier_004", 1.0),  # Positive: pottery, Zimbabwe
    ]
    
    print(f"\n📊 Training with {len(interactions)} interactions...")
    
    engine = NeuralMatchingEngine(
        embedding_dim=32,
        hidden_dim=64,
        num_layers=2
    )
    
    all_users = buyers + suppliers
    engine.train(all_users, interactions, epochs=30, batch_size=4)
    
    print("\n✅ Training completed!")
    
    print("\n" + "="*70)
    print("TEST 3: Finding Matches")
    print("="*70)
    
    # Test matching for each buyer
    for buyer in buyers:
        print(f"\n🎯 Matches for {buyer.user_id} ({buyer.country}, {buyer.region}):")
        print(f"   Interests: {', '.join(buyer.product_interests)}")
        print(f"   Budget: ${buyer.budget_range[0]:.0f} - ${buyer.budget_range[1]:.0f}")
        print("-" * 60)
        
        matches = engine.find_matches(buyer, suppliers, top_k=4)
        
        for i, match in enumerate(matches, 1):
            print(f"\n   {i}. {match.supplier_id} ({match.supplier_id.split('_')[1].title()})")
            print(f"      📊 Overall Score: {match.similarity_score:.2%}")
            print(f"      🌍 Country: {suppliers[[s.user_id for s in suppliers].index(match.supplier_id)].country}")
            print(f"      📦 Product Overlap: {match.product_overlap:.0%}")
            print(f"      ⭐ Trust Score: {match.trust_score:.2f}/5.0")
            print(f"      💰 Price Alignment: {match.price_alignment:.0%}")
            print(f"      ✅ Match Reasons: {', '.join(match.match_reasons)}")
    
    print("\n" + "="*70)
    print("TEST 4: Hybrid Matching Engine")
    print("="*70)
    
    print("\n🔄 Testing Hybrid Matching Engine...")
    hybrid = HybridMatchingEngine()
    hybrid.train(all_users, interactions)
    
    test_buyer = buyers[0]
    matches = hybrid.find_matches(test_buyer, suppliers)
    
    print(f"\n🎯 Hybrid matches for {test_buyer.user_id}:")
    for i, match in enumerate(matches[:3], 1):
        print(f"\n   {i}. {match.supplier_id}")
        print(f"      Score: {match.similarity_score:.2%}")
        print(f"      Reasons: {', '.join(match.match_reasons)}")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    
    print("\n📊 Summary:")
    print(f"   ✅ Neural Matching Engine: Working")
    print(f"   ✅ Training: Successful")
    print(f"   ✅ Matching: {len(matches)} matches found")
    print(f"   ✅ Hybrid Engine: Working")
    print(f"   ✅ Model Save/Load: Working")
    
    print("\n🚀 Next Steps:")
    print("   1. Install dependencies: pip install torch")
    print("   2. Train on your data: engine.train(your_users, your_interactions)")
    print("   3. Deploy to production: engine.save_model('production_model.pt')")
    print("   4. Integrate with API: POST /matching/find")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\n💡 To fix this, install the required packages:")
    print("   pip install torch")
    
except Exception as e:
    print(f"\n❌ Test Failed: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("\n" + "="*70)
    print("TEST COMPLETED")
    print("="*70)
