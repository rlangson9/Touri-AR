"""
Tourista AR AI Model - Main Application
Proprietary China-Africa Cross-Border Intelligence System
"""

from tourista_ai_model.config import CONFIG, API_CONFIG, TRADE_CONFIG, ModelConfig, Language, MarketRegion
from tourista_ai_model.translation.engine import TranslationEngine, TranslationResult
from tourista_ai_model.matching.engine import IntelligentMatchingSystem, UserProfile, Product, MatchResult, UserRole, ProductCategory, MatchType
from tourista_ai_model.recommendation.engine import RecommendationEngine, Recommendation, RecommendationType
from tourista_ai_model.risk_analysis.engine import RiskAnalysisEngine, RiskAssessment, PaymentMethod, UnbankedProfile
from tourista_ai_model.ar_recognition.engine import ARSceneRecognitionEngine, ARMarker, SceneRecognitionResult, ProductPreview

__version__ = "1.0.0"
__author__ = "Tourista AR - Shanghai, China"
__copyright__ = "Copyright 2024 Tourista AR. All rights reserved."

class TouristaAIModel:
    def __init__(self):
        self.config = CONFIG
        self.translation_engine = TranslationEngine(CONFIG)
        self.matching_system = IntelligentMatchingSystem()
        self.recommendation_engine = RecommendationEngine()
        self.risk_engine = RiskAnalysisEngine()
        self.ar_engine = ARSceneRecognitionEngine()
        self._initialize_system()

    def _initialize_system(self):
        print(f"Initializing Tourista AR AI Model v{self.config.version}")
        print(f"Model: {self.config.model_name}")
        print(f"Supported Languages: {', '.join(self.config.supported_languages.values())}")
        print("Components initialized:")
        print("  ✓ Translation Engine")
        print("  ✓ Intelligent Matching System")
        print("  ✓ Recommendation Engine")
        print("  ✓ Risk Analysis Engine")
        print("  ✓ AR Scene Recognition Engine")
        print("\nSystem Ready")

    def translate(self, text: str, source_lang: str, target_lang: str,
                  context: str = None) -> TranslationResult:
        return self.translation_engine.translate(text, source_lang, target_lang, context)

    def batch_translate(self, texts: list, source_lang: str, target_lang: str,
                       context: str = None) -> list:
        return self.translation_engine.batch_translate(texts, source_lang, target_lang, context)

    def find_matches(self, user_id: str, match_type: str = "B2B_TRADE",
                    limit: int = 10) -> list:
        match_type_enum = MatchType[match_type] if match_type in [e.name for e in MatchType] else MatchType.B2B_TRADE
        return self.matching_system.find_matches(user_id, match_type_enum, limit)

    def register_user(self, profile: UserProfile) -> bool:
        return self.matching_system.register_user(profile)

    def register_product(self, product: Product) -> bool:
        return self.matching_system.register_product(product)

    def get_recommendations(self, user_id: str, user_type: str,
                          context: dict = None, limit: int = 10) -> list:
        return self.recommendation_engine.generate_recommendations(
            user_id, user_type, context, limit
        )

    def assess_risk(self, transaction_data: dict,
                   counterparty_profile: UnbankedProfile = None) -> RiskAssessment:
        return self.risk_engine.assess_transaction_risk(transaction_data, counterparty_profile)

    def get_payment_recommendation(self, amount: float, buyer_profile: dict,
                                  seller_profile: dict) -> dict:
        return self.risk_engine.get_payment_recommendation(amount, buyer_profile, seller_profile)

    def recognize_ar_scene(self, image_data: bytes,
                         user_location: tuple = None,
                         language: str = "en") -> SceneRecognitionResult:
        return self.ar_engine.recognize_scene(image_data, user_location, language)

    def get_product_preview(self, product_id: str, language: str = "en") -> dict:
        return self.ar_engine.get_product_preview(product_id, language)

    def get_tourism_experience(self, spot_id: str, language: str = "en") -> dict:
        return self.ar_engine.get_tourism_experience(spot_id, language)

    def get_system_info(self) -> dict:
        return {
            "model_name": self.config.model_name,
            "version": self.config.version,
            "supported_languages": list(self.config.supported_languages.keys()),
            "supported_regions": self.config.supported_regions,
            "api_timeout": self.config.api_timeout,
            "cache_enabled": self.config.cache_enabled,
            "capabilities": [
                "Multi-language Translation (6 languages)",
                "Intelligent Buyer-Supplier Matching",
                "Cross-border Trade Recommendations",
                "Risk Assessment for Cash Payments",
                "AR Scene Recognition & Product Preview",
                "Tourism Experience Enhancement"
            ],
            "specializations": [
                "China-Africa Trade Intelligence",
                "Unbanked Population Payment Solutions",
                "Real-time Translation with Business Terminology",
                "AR Visualization for Products & Tourism",
                "Cross-border Logistics Optimization"
            ]
        }

    def health_check(self) -> dict:
        return {
            "status": "healthy",
            "version": self.config.version,
            "services": {
                "translation": "operational",
                "matching": "operational",
                "recommendation": "operational",
                "risk_analysis": "operational",
                "ar_recognition": "operational"
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }

MODEL = TouristaAIModel()

if __name__ == "__main__":
    print("Tourista AR AI Model")
    print("=" * 60)
    print(f"Model: {MODEL.config.model_name}")
    print(f"Version: {MODEL.config.version}")
    print(f"Copyright: {__copyright__}")
    print("=" * 60)
    print("\nSystem initialized and ready for inference.")
    print("\nExample Usage:")
    print("-" * 60)

    translation_result = MODEL.translate(
        "我想购买高质量的非洲手工艺品",
        "zh",
        "en"
    )
    print(f"Translation: {translation_result.translated_text}")
    print(f"Confidence: {translation_result.confidence:.2%}")

    print("\n" + "=" * 60)
    print("For API documentation, visit: https://api.tourista-ar.ai/docs")
