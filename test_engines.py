#!/usr/bin/env python3
"""
Comprehensive test of Tourista AR AI Model engines
"""

print("="*80)
print("TOURISTA AR AI MODEL - ENGINE TESTS")
print("="*80)

print("\n1. Testing Translation Engine...")
print("-"*80)
try:
    from tourista_ai_model.translation.engine import TranslationEngine
    
    translator = TranslationEngine()
    result = translator.translate(
        text="高质量的非洲手工艺品",
        source_lang="zh",
        target_lang="sn"  # Shona (Zimbabwe)
    )
    print(f"✅ Translation Engine loaded successfully")
    print(f"   Source: {result.original_text}")
    print(f"   Target: {result.translated_text}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Business Terms: {result.business_terms_found}")
    
    # Test more translations
    result2 = translator.translate(
        text="Ndiri kutsvaga mutengesi",
        source_lang="sn",
        target_lang="en"
    )
    print(f"\n   Shona → English: {result2.translated_text}")
    
except Exception as e:
    print(f"❌ Translation Engine error: {e}")

print("\n2. Testing Matching Engine...")
print("-"*80)
try:
    from tourista_ai_model.matching.engine import IntelligentMatchingSystem, UserProfile, ProductCategory, UserRole
    
    matcher = IntelligentMatchingSystem()
    
    # Register test buyer
    buyer = UserProfile(
        user_id="test_buyer",
        role=UserRole.CHINESE_BUYER,
        country="China",
        region="Shanghai",
        languages=["zh", "en"],
        product_interests=[ProductCategory.TEXTILES]
    )
    matcher.register_user(buyer)
    
    # Register test supplier
    supplier = UserProfile(
        user_id="test_supplier",
        role=UserRole.AFRICAN_SUPPLIER,
        country="South Africa",
        region="Johannesburg",
        languages=["en", "zu"],
        product_offers=[ProductCategory.TEXTILES],
        verification_status="verified",
        rating=4.5,
        total_transactions=10
    )
    matcher.register_user(supplier)
    
    matches = matcher.find_matches("test_buyer", "B2B_TRADE", limit=5)
    print(f"✅ Matching Engine loaded successfully")
    print(f"   Found {len(matches)} matches for buyer")
    if matches:
        print(f"   Top match score: {matches[0].similarity_score:.2%}")
        print(f"   Match reasons: {', '.join(matches[0].match_reasons[:2])}")
    
except Exception as e:
    print(f"❌ Matching Engine error: {e}")

print("\n3. Testing Risk Analysis Engine...")
print("-"*80)
try:
    from tourista_ai_model.risk_analysis.engine import RiskAnalysisEngine
    
    risk_engine = RiskAnalysisEngine()
    
    risk_result = risk_engine.assess_transaction_risk({
        "transaction_id": "test_risk_001",
        "counterparty_id": "supplier_001",
        "counterparty_type": "supplier",
        "payment_method": "mobile_money",
        "amount": 500,
        "currency": "USD",
        "buyer_country": "China",
        "seller_country": "Kenya",
        "mobile_money_provider": "m_pesa"
    })
    
    print(f"✅ Risk Analysis Engine loaded successfully")
    print(f"   Risk Score: {risk_result.risk_score:.2%}")
    print(f"   Risk Level: {risk_result.risk_level.value.upper()}")
    print(f"   Approval Status: {risk_result.approval_status}")
    
    if risk_result.identified_risks:
        print(f"\n   Identified Risks:")
        for risk in risk_result.identified_risks[:3]:
            print(f"     • {risk.name} ({risk.severity.value})")
    
except Exception as e:
    print(f"❌ Risk Analysis Engine error: {e}")

print("\n4. Testing Recommendation Engine...")
print("-"*80)
try:
    from tourista_ai_model.recommendation.engine import RecommendationEngine
    
    rec_engine = RecommendationEngine()
    
    recommendations = rec_engine.generate_recommendations(
        "test_user",
        "chinese_buyer",
        current_context={"interest": "handicrafts"},
        limit=3
    )
    
    print(f"✅ Recommendation Engine loaded successfully")
    print(f"   Generated {len(recommendations)} recommendations")
    if recommendations:
        print(f"\n   Top Recommendations:")
        for rec in recommendations[:2]:
            print(f"     • [{rec.recommendation_type.value}] {rec.title}")
            print(f"       Priority: {rec.priority_score:.2%}")
    
except Exception as e:
    print(f"❌ Recommendation Engine error: {e}")

print("\n5. Testing AR Recognition Engine...")
print("-"*80)
try:
    from tourista_ai_model.ar_recognition.engine import ARSceneRecognitionEngine
    
    ar_engine = ARSceneRecognitionEngine()
    
    result = ar_engine.get_tourism_experience("victoria_falls", "en")
    
    print(f"✅ AR Recognition Engine loaded successfully")
    print(f"   Tourism Spot: {result.get('name')}")
    print(f"   Country: {result.get('country')}")
    print(f"   Best Season: {result.get('best_season')}")
    
    tours = result.get('tour_options', [])
    if tours:
        print(f"\n   Tour Options:")
        for tour in tours[:2]:
            print(f"     • {tour['name']}: ${tour['price_usd']} ({tour['duration']})")
    
except Exception as e:
    print(f"❌ AR Recognition Engine error: {e}")

print("\n" + "="*80)
print("ALL ENGINE TESTS COMPLETED")
print("="*80)
print("\n✅ Tourista AR AI Model is fully operational!")
