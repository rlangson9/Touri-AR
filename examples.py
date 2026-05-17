"""
Tourista AR AI Model - Example Usage
Demonstrates all core capabilities of the proprietary AI model
"""

from tourista_ai_model import MODEL
from tourista_ai_model.matching.engine import UserProfile, Product, UserRole, ProductCategory
from tourista_ai_model.risk_analysis.engine import UnbankedProfile

def example_translation():
    print("=" * 70)
    print("EXAMPLE 1: Multi-language Translation")
    print("=" * 70)

    test_cases = [
        ("我想购买高质量的非洲手工艺品", "zh", "en"),
        ("Looking for premium coffee suppliers", "en", "zh"),
        ("Ndinovana nehupenyu hwehurapi", "sn", "en"),
        ("Sawubona ngemikhiqizo emihle", "zu", "en"),
    ]

    for text, source, target in test_cases:
        result = MODEL.translate(text, source, target)
        print(f"\n{source.upper()} → {target.upper()}:")
        print(f"  Original: {result.original_text}")
        print(f"  Translated: {result.translated_text}")
        print(f"  Confidence: {result.confidence:.2%}")
        if result.business_terms_found:
            print(f"  Business Terms: {', '.join(result.business_terms_found)}")
        if result.local_slang_found:
            print(f"  Local Slang: {', '.join(result.local_slang_found)}")
        print(f"  Needs Review: {result.needs_review}")

def example_matching():
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Intelligent Buyer-Supplier Matching")
    print("=" * 70)

    chinese_buyer = UserProfile(
        user_id="buyer_china_001",
        role=UserRole.CHINESE_BUYER,
        country="China",
        region="Shanghai",
        languages=["zh", "en"],
        business_type="import_export",
        product_interests=[ProductCategory.AGRICULTURAL, ProductCategory.MINERALS],
        budget_range=(5000, 50000),
        verification_status="verified",
        rating=4.8,
        total_transactions=25
    )

    MODEL.register_user(chinese_buyer)

    zimbabwe_supplier = UserProfile(
        user_id="supplier_zim_001",
        role=UserRole.AFRICAN_SUPPLIER,
        country="Zimbabwe",
        region="Harare",
        languages=["en", "sn"],
        business_type="agricultural_exports",
        product_offers=[ProductCategory.AGRICULTURAL, ProductCategory.TEXTILES],
        verification_status="verified",
        rating=4.6,
        total_transactions=15,
        response_rate=0.95,
        avg_response_time=120
    )

    MODEL.register_user(zimbabwe_supplier)

    print(f"\nBuyer Profile: {chinese_buyer.user_id}")
    print(f"  Country: {chinese_buyer.country}")
    print(f"  Interests: {[p.value for p in chinese_buyer.product_interests]}")
    print(f"  Budget: ${chinese_buyer.budget_range[0]:,.0f} - ${chinese_buyer.budget_range[1]:,.0f}")

    print(f"\nSupplier Profile: {zimbabwe_supplier.user_id}")
    print(f"  Country: {zimbabwe_supplier.country}")
    print(f"  Offers: {[p.value for p in zimbabwe_supplier.product_offers]}")
    print(f"  Rating: {zimbabwe_supplier.rating}/5.0")

    matches = MODEL.find_matches("buyer_china_001", "B2B_TRADE", limit=5)
    print(f"\nFound {len(matches)} matches for buyer:")
    for match in matches[:3]:
        print(f"\n  Match Score: {match.similarity_score:.2%}")
        print(f"  Type: {match.match_type.value}")
        print(f"  Reasons: {', '.join(match.match_reasons[:2])}")
        print(f"  Actions: {', '.join(match.recommended_actions[:2])}")
        if match.risk_factors:
            print(f"  ⚠️  Risk Factors: {', '.join(match.risk_factors[:2])}")

def example_recommendations():
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Trade & Market Recommendations")
    print("=" * 70)

    recommendations = MODEL.get_recommendations(
        "buyer_china_001",
        "chinese_buyer",
        context={"current_interest": "coffee"},
        limit=5
    )

    print(f"\nGenerated {len(recommendations)} recommendations:")
    for rec in recommendations[:3]:
        print(f"\n  [{rec.recommendation_type.value.upper()}]")
        print(f"  Title: {rec.title}")
        print(f"  Priority: {rec.priority_score:.2%}")
        print(f"  Rationale:")
        for reason in rec.rationale[:2]:
            print(f"    - {reason}")
        print(f"  Actions:")
        for action in rec.action_items[:2]:
            print(f"    • {action}")
        if rec.metadata:
            print(f"  Impact: {rec.estimated_impact}")

def example_risk_assessment():
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Risk Analysis for Cash-based Payments")
    print("=" * 70)

    transaction_data = {
        "transaction_id": "TXN2024001",
        "counterparty_id": "supplier_zim_001",
        "counterparty_type": "supplier",
        "payment_method": "mobile_money",
        "amount": 5000,
        "currency": "USD",
        "buyer_country": "China",
        "seller_country": "Zimbabwe",
        "transaction_type": "B2B",
        "mobile_money_provider": "ecocash"
    }

    assessment = MODEL.assess_risk(transaction_data)

    print(f"\nTransaction: {assessment.transaction_id}")
    print(f"  Amount: ${assessment.transaction_amount:,.2f} {assessment.currency}")
    print(f"  Payment Method: {assessment.payment_method.value}")
    print(f"\n  Risk Score: {assessment.risk_score:.2%}")
    print(f"  Risk Level: {assessment.risk_level.value.upper()}")
    print(f"\n  Assessment: {assessment.overall_assessment}")

    if assessment.identified_risks:
        print(f"\n  Identified Risks ({len(assessment.identified_risks)}):")
        for risk in assessment.identified_risks[:3]:
            print(f"    ⚠️  {risk.name} ({risk.severity.value})")
            print(f"        {risk.description}")
            print(f"        Mitigation: {', '.join(risk.mitigation_strategies[:2])}")

    print(f"\n  Recommendations:")
    for rec in assessment.recommendations[:3]:
        print(f"    • {rec}")

    print(f"\n  Required Verifications:")
    for verify in assessment.required_verifications:
        print(f"    ✓ {verify}")

    print(f"\n  Status: {assessment.approval_status}")

def example_ar_recognition():
    print("\n" + "=" * 70)
    print("EXAMPLE 5: AR Scene Recognition & Product Preview")
    print("=" * 70)

    result = MODEL.recognize_ar_scene(
        b"",  # image_data
        user_location=(-17.9244, 25.8572),  # Victoria Falls location
        language="zh"
    )

    print(f"\nScene Recognition Result:")
    print(f"  Scene Type: {result.scene_type.value}")
    print(f"  Confidence: {result.confidence.value} ({result.confidence_score:.2%})")

    if result.detected_markers:
        print(f"\n  Detected Markers:")
        for marker in result.detected_markers[:2]:
            print(f"    📍 {marker.name}")
            print(f"       {marker.description}")
            if marker.cultural_significance:
                print(f"       Cultural: {marker.cultural_significance}")

    if result.augmented_content:
        print(f"\n  AR Content:")
        print(f"    Title: {result.augmented_content.get('title', 'N/A')}")
        print(f"    Description: {result.augmented_content.get('description', 'N/A')[:100]}...")

    if result.related_products:
        print(f"\n  Related Products ({len(result.related_products)}):")
        for product in result.related_products[:2]:
            print(f"    🛍️  {product['name']}")
            print(f"       Price: ${product['price_usd']:,.2f}")
            print(f"       Origin: {product['origin']}")

def example_payment_recommendation():
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Payment Solution Recommendation")
    print("=" * 70)

    recommendation = MODEL.get_payment_recommendation(
        amount=5000,
        buyer_profile={"country": "China"},
        seller_profile={"country": "Zimbabwe"}
    )

    print(f"\nTransaction Amount: ${recommendation['amount']:,.2f}")
    print(f"\n  Recommended Method: {recommendation['recommended_method'].upper()}")

    if recommendation['alternative_methods']:
        print(f"\n  Alternative Methods:")
        for method in recommendation['alternative_methods'][:3]:
            print(f"    {method['method'].upper()} - {method['recommendation']}")
            print(f"      Reason: {method['reason']}")

    if recommendation['risk_mitigation']:
        print(f"\n  Risk Mitigation:")
        for mitigation in recommendation['risk_mitigation'][:3]:
            print(f"    • {mitigation}")

    if recommendation['fees_estimate']:
        fees = recommendation['fees_estimate']
        print(f"\n  Fee Estimate:")
        print(f"    Amount: ${fees['estimated_fee']:,.2f}")
        print(f"    Percentage: {fees['fee_percentage']:.1f}%")

def example_market_insights():
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Market Insights & Seasonal Pricing")
    print("=" * 70)

    insights = MODEL.recommendation_engine.get_market_insights(ProductCategory.AGRICULTURAL)

    print(f"\nMarket Insights for: {insights['category']}")
    print(f"  Demand Trend: {insights['demand_trend'].upper()}")
    print(f"  Seasonal Availability: {', '.join(insights['seasonal_availability'])}")
    print(f"  Top Regions: {', '.join(insights['top_regions'])}")

    print(f"\n  Pricing Tips:")
    for tip in insights['pricing_tips'][:3]:
        print(f"    • {tip}")

    print(f"\n  Logistics Considerations:")
    for tip in insights['logistics_considerations'][:3]:
        print(f"    • {tip}")

    seasonal = MODEL.recommendation_engine.get_seasonal_pricing("avocado", "June")
    print(f"\n  Seasonal Pricing (Avocados, June):")
    print(f"    Peak Season: {', '.join(seasonal['peak_season_months'])}")
    print(f"    Off Season: {', '.join(seasonal['off_season_months'])}")
    print(f"    Price Variation: {seasonal['price_variation']}")
    print(f"    Recommendation: {seasonal['buying_recommendation']}")
    print(f"    Estimated Savings: {seasonal['estimated_savings']}")

def main():
    print("\n" + "=" * 70)
    print("TOURISTA AR AI MODEL - EXAMPLES")
    print("Proprietary China-Africa Cross-Border Intelligence System")
    print("=" * 70)

    try:
        example_translation()
        example_matching()
        example_recommendations()
        example_risk_assessment()
        example_ar_recognition()
        example_payment_recommendation()
        example_market_insights()

        print("\n" + "=" * 70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nFor more information:")
        print("  API Documentation: https://api.tourista-ar.ai/docs")
        print("  Technical Support: support@tourista-ar.ai")
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n❌ Error during examples: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
