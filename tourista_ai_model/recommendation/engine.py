"""
Recommendation Engine for Tourista AR
China-Africa Cross-Border Trade & Travel Recommendations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import math

class RecommendationType(Enum):
    PRODUCT_RECOMMENDATION = "product_recommendation"
    SUPPLIER_RECOMMENDATION = "supplier_recommendation"
    TOURISM_RECOMMENDATION = "tourism_recommendation"
    LOGISTICS_RECOMMENDATION = "logistics_recommendation"
    PAYMENT_RECOMMENDATION = "payment_recommendation"
    MARKET_INSIGHT = "market_insight"
    PRICE_ALERT = "price_alert"
    TRADE_OPPORTUNITY = "trade_opportunity"

class MarketTrend(Enum):
    EMERGING = "emerging"
    GROWING = "growing"
    STABLE = "stable"
    DECLINING = "declining"
    SEASONAL = "seasonal"

@dataclass
class TradeMetrics:
    average_price: float
    price_trend: MarketTrend
    demand_score: float
    competition_level: str
    market_size: float
    growth_rate: float
    seasonality_pattern: List[str]

@dataclass
class Recommendation:
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    description: str
    rationale: List[str]
    priority_score: float
    target_user_segments: List[str]
    action_items: List[str]
    estimated_impact: str
    expiration_date: Optional[datetime]
    metadata: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class RecommendationEngine:
    def __init__(self):
        self.user_preferences: Dict[str, Dict] = {}
        self.recommendation_history: List[Recommendation] = []
        self.market_data: Dict[str, TradeMetrics] = {}
        self.seasonal_patterns = self._initialize_seasonal_patterns()
        self.trade_opportunities = self._initialize_trade_opportunities()
        self.tourism_seasons = self._initialize_tourism_seasons()

    def _initialize_seasonal_patterns(self) -> Dict[str, Dict]:
        return {
            "avocado": {
                "peak_season": ["April", "May", "June", "July", "August"],
                "off_season": ["January", "February", "March"],
                "price_variation": 0.35,
                "demand_peak": "June"
            },
            "coffee": {
                "peak_season": ["October", "November", "December", "January"],
                "off_season": ["April", "May", "June"],
                "price_variation": 0.40,
                "demand_peak": "November"
            },
            "cocoa": {
                "peak_season": ["March", "April", "May", "June", "July", "August"],
                "off_season": ["September", "October", "November"],
                "price_variation": 0.30,
                "demand_peak": "April"
            },
            "shea_butter": {
                "peak_season": ["January", "February", "March", "April", "May"],
                "off_season": ["July", "August", "September"],
                "price_variation": 0.25,
                "demand_peak": "February"
            },
            "gemstones": {
                "peak_season": ["January", "February", "October", "November", "December"],
                "off_season": ["June", "July", "August"],
                "price_variation": 0.45,
                "demand_peak": "January"
            },
            "textiles": {
                "peak_season": ["September", "October", "November", "December"],
                "off_season": ["January", "February"],
                "price_variation": 0.20,
                "demand_peak": "October"
            }
        }

    def _initialize_trade_opportunities(self) -> List[Dict]:
        return [
            {
                "category": "agricultural_products",
                "opportunity": "Chinese demand for African superfoods increasing",
                "trend": "growing",
                "market": "China",
                "volume_growth": 0.25,
                "price_trend": "increasing"
            },
            {
                "category": "minerals_gemstones",
                "opportunity": "Tanzanite and Alexandrite gaining popularity in Chinese market",
                "trend": "emerging",
                "market": "China",
                "volume_growth": 0.40,
                "price_trend": "increasing"
            },
            {
                "category": "tourism_experiences",
                "opportunity": "Chinese tourists showing interest in African safari experiences",
                "trend": "growing",
                "market": "Africa",
                "volume_growth": 0.35,
                "price_trend": "stable"
            },
            {
                "category": "textiles_crafts",
                "opportunity": "African prints gaining traction in Chinese fashion market",
                "trend": "emerging",
                "market": "China",
                "volume_growth": 0.30,
                "price_trend": "stable"
            },
            {
                "category": "coffee",
                "opportunity": "Specialty coffee from Ethiopia and Zimbabwe in high demand",
                "trend": "growing",
                "market": "China",
                "volume_growth": 0.50,
                "price_trend": "increasing"
            }
        ]

    def _initialize_tourism_seasons(self) -> Dict[str, Dict]:
        return {
            "zimbabwe": {
                "high_season": ["June", "July", "August", "October", "November"],
                "low_season": ["January", "February", "March"],
                "wildlife_viewing": ["June", "July", "August", "September"],
                "water_activities": ["September", "October", "November"],
                "weather_notes": "Best time for wildlife is dry season (May-October)"
            },
            "south_africa": {
                "high_season": ["December", "January", "February", "July"],
                "low_season": ["May", "June", "August", "September"],
                "wildlife_viewing": ["June", "July", "August", "September"],
                "beach_season": ["December", "January", "February"],
                "weather_notes": "Cape Town best visited Oct-Mar, Kruger year-round"
            }
        }

    def generate_recommendations(self, user_id: str, user_type: str,
                               current_context: Optional[Dict] = None,
                               limit: int = 10) -> List[Recommendation]:
        recommendations = []

        if user_type == "chinese_buyer":
            recommendations.extend(self._recommend_products_for_buyer(current_context))
            recommendations.extend(self._recommend_suppliers_for_buyer(current_context))
            recommendations.extend(self._recommend_market_insights())
            recommendations.extend(self._recommend_trade_opportunities())
            recommendations.extend(self._recommend_payment_solutions())
        elif user_type == "african_supplier":
            recommendations.extend(self._recommend_buyers_for_supplier(current_context))
            recommendations.extend(self._recommend_logistics_solutions())
            recommendations.extend(self._recommend_market_trends())
            recommendations.extend(self._recommend_pricing_optimization())
        elif user_type == "tourist":
            recommendations.extend(self._recommend_tourism_destinations(current_context))
            recommendations.extend(self._recommend_tourism_services())
            recommendations.extend(self._recommend_travel_logistics())

        recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        return recommendations[:limit]

    def _recommend_products_for_buyer(self, context: Optional[Dict]) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_prod_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.PRODUCT_RECOMMENDATION,
            title="Trending: Ethiopian Coffee in China",
            description="Ethiopian specialty coffee has seen 50% growth in Chinese import demand. "
                       "Consider establishing supplier relationships now to secure premium supply.",
            rationale=[
                "Growing Chinese middle-class demand for premium coffee",
                "Ethiopian coffee offers competitive pricing vs. Brazilian/Colombian",
                "Government trade agreements favor African agricultural imports"
            ],
            priority_score=0.92,
            target_user_segments=["chinese_buyers", "coffee_importers"],
            action_items=[
                "Search for certified Ethiopian coffee suppliers",
                "Request samples from top-rated suppliers",
                "Compare FOB prices from different regions"
            ],
            estimated_impact="Potential 50% increase in profit margins vs. South American sources",
            expiration_date=datetime.now() + timedelta(days=90),
            metadata={"category": "coffee", "region": "ethiopia"}
        ))

        recommendations.append(Recommendation(
            recommendation_id=f"rec_prod_2_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.PRODUCT_RECOMMENDATION,
            title="Emerging Market: Zimbabwean Avocados",
            description="Zimbabwean avocado exports to China are expected to begin in 2025. "
                       "Early partnerships can secure advantageous pricing and priority supply.",
            rationale=[
                "New market access agreement signed in 2024",
                "Zimbabwean Hass avocados competitive in quality",
                "Off-season production complements South African supply"
            ],
            priority_score=0.85,
            target_user_segments=["chinese_buyers", "fresh_produce_importers"],
            action_items=[
                "Research Zimbabwean avocado quality standards",
                "Connect with early-exporting farms",
                "Plan trial shipments for quality testing"
            ],
            estimated_impact="First-mover advantage in emerging market segment",
            expiration_date=datetime.now() + timedelta(days=180),
            metadata={"category": "avocado", "region": "zimbabwe", "status": "pre_market"}
        ))

        recommendations.append(Recommendation(
            recommendation_id=f"rec_prod_3_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.PRODUCT_RECOMMENDATION,
            title="High Demand: South African Shea Butter",
            description="South African shea butter showing strong growth in Chinese cosmetics market. "
                       "Multiple applications in skincare and haircare industries.",
            rationale=[
                "Natural cosmetics trend in China",
                "South African quality certifications recognized",
                "Competitive pricing from established suppliers"
            ],
            priority_score=0.88,
            target_user_segments=["chinese_buyers", "cosmetic_ingredients_importers"],
            action_items=[
                "Verify supplier certifications (organic, fair trade)",
                "Request lab testing reports for purity",
                "Compare prices from different South African suppliers"
            ],
            estimated_impact="Growing market with 30% YoY growth in demand",
            expiration_date=datetime.now() + timedelta(days=120),
            metadata={"category": "shea_butter", "region": "south_africa"}
        ))

        return recommendations

    def _recommend_suppliers_for_buyer(self, context: Optional[Dict]) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_sup_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.SUPPLIER_RECOMMENDATION,
            title="Verified Supplier: Zimbabwe Mining Co.",
            description="Highly rated supplier with 200+ successful transactions and verified credentials. "
                       "Specializes in amethyst and tourmaline exports.",
            rationale=[
                "Verified status with complete documentation",
                "Excellent response rate (95% within 2 hours)",
                "Provides quality certifications and grading reports"
            ],
            priority_score=0.91,
            target_user_segments=["chinese_buyers", "gemstone_importers"],
            action_items=[
                "View full supplier profile",
                "Request product catalog",
                "Inquire about minimum order requirements"
            ],
            estimated_impact="Reduced sourcing risk with verified supplier",
            expiration_date=datetime.now() + timedelta(days=30),
            metadata={"supplier_id": "zimbabwe_mining_co", "verification": "verified"}
        ))

        return recommendations

    def _recommend_market_insights(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_ins_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.MARKET_INSIGHT,
            title="Price Alert: Cocoa Market Volatility",
            description="Cocoa prices expected to remain high due to West African supply constraints. "
                       "Consider locking in prices with forward contracts.",
            rationale=[
                "Ivory Coast and Ghana production issues",
                "Global cocoa deficit continues",
                "Alternative sources from Cameroon and Nigeria becoming attractive"
            ],
            priority_score=0.87,
            target_user_segments=["chinese_buyers", "cocoa_importers", "chocolate_manufacturers"],
            action_items=[
                "Review current inventory levels",
                "Consider long-term supply agreements",
                "Explore alternative African cocoa sources"
            ],
            estimated_impact="Potential 20-30% cost savings vs. spot market",
            expiration_date=datetime.now() + timedelta(days=60),
            metadata={"category": "cocoa", "alert_type": "price_volatility"}
        ))

        return recommendations

    def _recommend_trade_opportunities(self) -> List[Recommendation]:
        recommendations = []

        for opp in self.trade_opportunities:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_trade_{opp['category']}_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.TRADE_OPPORTUNITY,
                title=f"Trade Opportunity: {opp['opportunity']}",
                description=f"{opp['category'].replace('_', ' ').title()} from Africa showing "
                           f"{opp['trend']} trend with {int(opp['volume_growth']*100)}% volume growth.",
                rationale=[
                    f"Market trend: {opp['trend']}",
                    f"Volume growth: {int(opp['volume_growth']*100)}% YoY",
                    f"Price trend: {opp['price_trend']}"
                ],
                priority_score=0.80 + (opp['volume_growth'] * 0.2),
                target_user_segments=["chinese_buyers"],
                action_items=[
                    f"Search for {opp['category'].replace('_', ' ')} suppliers",
                    "Request market analysis report",
                    "Connect with verified African exporters"
                ],
                estimated_impact=f"Growth market with {opp['price_trend']} prices",
                expiration_date=datetime.now() + timedelta(days=90),
                metadata=opp
            ))

        return recommendations

    def _recommend_payment_solutions(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_pay_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.PAYMENT_RECOMMENDATION,
            title="Payment Solution: Mobile Money Integration",
            description="For transactions with unbanked African suppliers, recommend using mobile money "
                       "options like Ecocash (Zimbabwe) or M-Pesa (Kenya).",
            rationale=[
                "High mobile money penetration in target markets",
                "Lower transaction fees for small-scale trades",
                "Improved trust and faster settlement"
            ],
            priority_score=0.83,
            target_user_segments=["chinese_buyers", "small_scale_traders"],
            action_items=[
                "Set up mobile money payment account",
                "Verify supplier mobile money details",
                "Understand daily transaction limits"
            ],
            estimated_impact="30-50% reduction in payment friction for small orders",
            expiration_date=None,
            metadata={"payment_type": "mobile_money", "regions": ["zimbabwe", "kenya"]}
        ))

        return recommendations

    def _recommend_buyers_for_supplier(self, context: Optional[Dict]) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_buy_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.SUPPLIER_RECOMMENDATION,
            title="Target Market: Chinese Cosmetic Manufacturers",
            description="Chinese cosmetics industry seeking natural ingredients from Africa. "
                       "Shea butter, marula oil, and baobab extract in high demand.",
            rationale=[
                "Growing clean beauty trend in China",
                "Willingness to pay premium for certified organic",
                "Long-term supply agreements preferred"
            ],
            priority_score=0.89,
            target_user_segments=["african_suppliers", "natural_ingredients_producers"],
            action_items=[
                "Prepare product samples with certifications",
                "Create English and Chinese marketing materials",
                "List on Tourista AR supplier marketplace"
            ],
            estimated_impact="Access to premium Chinese market with better margins",
            expiration_date=None,
            metadata={"target_market": "china", "industry": "cosmetics"}
        ))

        return recommendations

    def _recommend_logistics_solutions(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_log_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.LOGISTICS_RECOMMENDATION,
            title="Logistics Partner: DHL Africa to China",
            description="DHL offers reliable shipping from major African cities to China with "
                       "competitive rates for small packages and samples.",
            rationale=[
                "Established network in major African cities",
                "Reliable customs clearance support",
                "Track-and-trace available"
            ],
            priority_score=0.85,
            target_user_segments=["african_suppliers", "small_exporters"],
            action_items=[
                "Request DHL shipping rates for your location",
                "Set up DHL business account",
                "Understand customs documentation requirements"
            ],
            estimated_impact="Professional logistics support for international expansion",
            expiration_date=None,
            metadata={"logistics_provider": "DHL", "service": "international_shipping"}
        ))

        return recommendations

    def _recommend_market_trends(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_trend_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.MARKET_INSIGHT,
            title="Market Trend: Chinese Retail Preferences",
            description="Chinese buyers increasingly prefer smaller order quantities with more frequent "
                       "shipments rather than large bulk orders.",
            rationale=[
                "Reduced inventory risk for buyers",
                "Flexibility to test multiple suppliers",
                "Lower capital requirements for Chinese SME buyers"
            ],
            priority_score=0.82,
            target_user_segments=["african_suppliers"],
            action_items=[
                "Consider offering MOQ flexibility",
                "Prepare for more frequent, smaller shipments",
                "Build relationships for repeat orders"
            ],
            estimated_impact="Access to larger customer base with flexible terms",
            expiration_date=None,
            metadata={"trend": "smaller_orders", "region": "china"}
        ))

        return recommendations

    def _recommend_pricing_optimization(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_price_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.PRICE_ALERT,
            title="Pricing Strategy: Seasonal Adjustment",
            description="Consider offering 10-15% discounts during off-peak seasons to maintain "
                       "steady orders and optimize production planning.",
            rationale=[
                "Stable revenue during low-demand periods",
                "Better production scheduling",
                "Competitive advantage over peers"
            ],
            priority_score=0.78,
            target_user_segments=["african_suppliers", "agricultural_exporters"],
            action_items=[
                "Review seasonal demand patterns",
                "Prepare discounted pricing tiers",
                "Communicate seasonal offers to buyers"
            ],
            estimated_impact="20% increase in off-season order volume",
            expiration_date=datetime.now() + timedelta(days=60),
            metadata={"optimization": "seasonal_pricing"}
        ))

        return recommendations

    def _recommend_tourism_destinations(self, context: Optional[Dict]) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_tour_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Experience: Victoria Falls Adventure",
            description="Combine your trade visit with an unforgettable Victoria Falls experience. "
                       "Guided tours, helicopter rides, and bungee jumping available.",
            rationale=[
                "World Wonder designation",
                "Multiple activity options",
                "Easy access from major African trade hubs"
            ],
            priority_score=0.90,
            target_user_segments=["business_travelers", "chinese_tourists"],
            action_items=[
                "Book guided tour in advance",
                "Check visa requirements for Zimbabwe",
                "Plan 2-3 day visit for complete experience"
            ],
            estimated_impact="Enhanced business trip with memorable experience",
            expiration_date=None,
            metadata={"location": "victoria_falls", "country": "zimbabwe", "type": "adventure"}
        ))

        recommendations.append(Recommendation(
            recommendation_id=f"rec_tour_2_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Experience: South African Safari",
            description="Visit world-class game reserves near Johannesburg for authentic safari experience. "
                       "Big Five viewing and luxury accommodation options.",
            rationale=[
                "World-renowned wildlife experience",
                "Easy connectivity from Chinese cities",
                "Multiple budget and luxury options"
            ],
            priority_score=0.93,
            target_user_segments=["chinese_tourists", "luxury_travelers"],
            action_items=[
                "Choose between Kruger, Sabi Sands, or Pilanesberg",
                "Book through verified tour operators",
                "Consider combining with Cape Town visit"
            ],
            estimated_impact="Bucket-list experience at competitive rates",
            expiration_date=None,
            metadata={"location": "south_africa_safari", "country": "south_africa", "type": "wildlife"}
        ))

        return recommendations

    def _recommend_tourism_services(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_serv_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Service: Multilingual Tour Guide",
            description="Book certified tour guides who speak Mandarin for seamless experience "
                       "at African tourist destinations.",
            rationale=[
                "Language barrier elimination",
                "Cultural interpretation",
                "Better local insights"
            ],
            priority_score=0.88,
            target_user_segments=["chinese_tourists", "non_english_speakers"],
            action_items=[
                "Request Mandarin-speaking guide when booking",
                "Verify guide certification",
                "Prepare translation of key questions"
            ],
            estimated_impact="Enhanced experience with cultural context",
            expiration_date=None,
            metadata={"service": "multilingual_guide", "languages": ["mandarin", "english"]}
        ))

        return recommendations

    def _recommend_travel_logistics(self) -> List[Recommendation]:
        recommendations = []

        recommendations.append(Recommendation(
            recommendation_id=f"rec_trav_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Travel Tip: Visa Requirements for Zimbabwe",
            description="Chinese citizens need a visa for Zimbabwe. Consider using the Kigali "
                       "International Airport for smoother entry process.",
            rationale=[
                "Visa on arrival available at major airports",
                "Kigali route often has better connectivity",
                "Transit visa options for multi-country visits"
            ],
            priority_score=0.75,
            target_user_segments=["chinese_tourists", "business_travelers"],
            action_items=[
                "Check latest visa requirements",
                "Prepare required documents",
                "Consider travel insurance"
            ],
            estimated_impact="Smoother entry and travel planning",
            expiration_date=datetime.now() + timedelta(days=90),
            metadata={"country": "zimbabwe", "type": "visa_information"}
        ))

        return recommendations

    def get_seasonal_pricing(self, product_category: str, target_month: Optional[str] = None) -> Dict:
        seasonal_data = self.seasonal_patterns.get(product_category, {})

        if not seasonal_data:
            return {
                "category": product_category,
                "seasonal_pattern": "No seasonal data available",
                "recommendation": "Contact suppliers for current pricing"
            }

        peak_months = seasonal_data.get("peak_season", [])
        off_months = seasonal_data.get("off_season", [])
        price_variation = seasonal_data.get("price_variation", 0.25)

        recommendation = {
            "category": product_category,
            "peak_season_months": peak_months,
            "off_season_months": off_months,
            "price_variation": f"{int(price_variation * 100)}%",
            "buying_recommendation": "Buy during off-season for better pricing" if price_variation > 0.2 else "Price relatively stable year-round",
            "estimated_savings": f"Up to {int(price_variation * 100)}% during off-peak"
        }

        return recommendation

    def analyze_market_opportunity(self, product_category: str, target_country: str) -> Dict:
        opportunity_score = 0.7
        factors = []

        for opp in self.trade_opportunities:
            if opp['category'] == product_category:
                opportunity_score += opp['volume_growth'] * 0.3
                factors.append({
                    "trend": opp['trend'],
                    "volume_growth": f"{int(opp['volume_growth']*100)}%",
                    "price_trend": opp['price_trend']
                })

        country_relevance = {
            "zimbabwe": ["agricultural_products", "minerals_gemstones"],
            "south_africa": ["tourism_experiences", "minerals_gemstones", "textiles_crafts"],
            "kenya": ["agricultural_products", "textiles_crafts"]
        }

        relevant_categories = country_relevance.get(target_country.lower(), [])
        if product_category in relevant_categories:
            opportunity_score += 0.1
            factors.append({"country_relevance": "High demand in target market"})

        return {
            "product_category": product_category,
            "target_country": target_country,
            "opportunity_score": min(opportunity_score, 1.0),
            "factors": factors,
            "recommendation": "High opportunity - pursue actively" if opportunity_score > 0.85 else "Moderate opportunity - evaluate carefully"
        }
