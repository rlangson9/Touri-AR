"""
Intelligent Matching System for Tourista AR
Matches Chinese buyers with African suppliers and tourism service providers
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math

class MatchType(Enum):
    B2B_TRADE = "business_to_business_trade"
    B2C_RETAIL = "business_to_consumer_retail"
    TOURISM_SERVICE = "tourism_service"
    LOGISTICS_PROVIDER = "logistics_provider"
    PAYMENT_SERVICE = "payment_service"

class UserRole(Enum):
    CHINESE_BUYER = "chinese_buyer"
    AFRICAN_SUPPLIER = "african_supplier"
    AFRICAN_TOURISM_PROVIDER = "african_tourism_provider"
    LOGISTICS_PROVIDER = "logistics_provider"
    PAYMENT_SERVICE_PROVIDER = "payment_service_provider"

class ProductCategory(Enum):
    AGRICULTURAL = "agricultural_products"
    MINERALS = "minerals_gemstones"
    TEXTILES = "textiles_crafts"
    ELECTRONICS = "electronics"
    TOURISM_EXPERIENCES = "tourism_experiences"
    TRANSPORTATION = "transportation"
    ACCOMMODATION = "accommodation"
    GUIDED_TOURS = "guided_tours"

@dataclass
class UserProfile:
    user_id: str
    role: UserRole
    country: str
    region: str
    languages: List[str] = field(default_factory=list)
    business_type: Optional[str] = None
    product_interests: List[ProductCategory] = field(default_factory=list)
    product_offers: List[ProductCategory] = field(default_factory=list)
    preferred_payment_methods: List[str] = field(default_factory=list)
    budget_range: Optional[Tuple[float, float]] = None
    transaction_volume: Optional[int] = None
    verification_status: str = "unverified"
    rating: float = 0.0
    total_transactions: int = 0
    response_rate: float = 0.0
    avg_response_time: Optional[int] = None

@dataclass
class Product:
    product_id: str
    supplier_id: str
    category: ProductCategory
    name: str
    description: str
    price: float
    currency: str
    min_order_quantity: int
    available_quantity: int
    quality_certifications: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    logistics_options: List[str] = field(default_factory=list)
    delivery_time_days: int = 30
    location: str = ""

@dataclass
class MatchResult:
    match_id: str
    buyer_profile: UserProfile
    supplier_profile: Optional[UserProfile]
    match_type: MatchType
    product: Optional[Product]
    similarity_score: float
    match_reasons: List[str]
    recommended_actions: List[str]
    risk_factors: List[str]
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class MatchingCriteria:
    category_match_weight: float = 0.3
    price_range_weight: float = 0.2
    location_weight: float = 0.15
    rating_weight: float = 0.15
    response_time_weight: float = 0.1
    verification_weight: float = 0.1
    min_similarity_threshold: float = 0.7

class IntelligentMatchingSystem:
    def __init__(self):
        self.user_profiles: Dict[str, UserProfile] = {}
        self.products: Dict[str, Product] = {}
        self.match_history: List[MatchResult] = []
        self.criteria = MatchingCriteria()
        self.china_africa_trade_knowledge = self._initialize_trade_knowledge()

    def _initialize_trade_knowledge(self) -> Dict[str, any]:
        return {
            "high_demand_chinese_products": [
                "avocado", "cocoa", "coffee", "tea", "shea_butter",
                "gemstones", "copper", "cobalt", "cotton", "sisal",
                "wildlife_products", "tourism_experiences"
            ],
            "popular_import_categories": [
                "electronics", "machinery", "textiles", "vehicles",
                "construction_materials", "consumer_goods"
            ],
            "seasonal_products": {
                "avocado": ["march", "april", "may", "june", "july", "august"],
                "coffee": ["october", "november", "december", "january"],
                "cocoa": ["march", "april", "may", "june", "july", "august"],
                "tourism": ["june", "july", "august", "december", "january"]
            },
            "trusted_supplier_regions": {
                "zimbabwe": ["harare", "bulawayo", "mutare"],
                "south_africa": ["johannesburg", "cape_town", "durban"],
                "kenya": ["nairobi", "mombasa"],
                "ethiopia": ["addis_ababa"]
            },
            "logistics_hubs": {
                "zimbabwe": ["harare_international_airport", "beitbridge_border"],
                "south_africa": ["johannesburg_international", "durban_port", "cape_town_port"],
                "china": ["shenzhen", "guangzhou", "shanghai", "yiwu"]
            }
        }

    def register_user(self, profile: UserProfile) -> bool:
        self.user_profiles[profile.user_id] = profile
        return True

    def register_product(self, product: Product) -> bool:
        self.products[product.product_id] = product
        return True

    def find_matches(self, user_id: str, match_type: MatchType,
                    limit: int = 10) -> List[MatchResult]:
        if user_id not in self.user_profiles:
            return []

        user = self.user_profiles[user_id]
        matches = []

        for other_id, other_user in self.user_profiles.items():
            if other_id == user_id:
                continue

            if self._is_compatible_match(user, other_user, match_type):
                match_result = self._calculate_match_score(user, other_user, match_type)

                if match_result.similarity_score >= self.criteria.min_similarity_threshold:
                    matches.append(match_result)

        if user.role == UserRole.CHINESE_BUYER and match_type in [MatchType.B2B_TRADE, MatchType.B2C_RETAIL]:
            product_matches = self._match_products_for_buyer(user, limit)
            matches.extend(product_matches)

        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        return matches[:limit]

    def _is_compatible_match(self, user: UserProfile, other: UserProfile,
                           match_type: MatchType) -> bool:
        if user.role == UserRole.CHINESE_BUYER:
            if other.role == UserRole.AFRICAN_SUPPLIER and match_type in [MatchType.B2B_TRADE, MatchType.B2C_RETAIL]:
                return True
            if other.role == UserRole.AFRICAN_TOURISM_PROVIDER and match_type == MatchType.TOURISM_SERVICE:
                return True
            if other.role == UserRole.LOGISTICS_PROVIDER and match_type == MatchType.LOGISTICS_PROVIDER:
                return True

        elif user.role == UserRole.AFRICAN_SUPPLIER:
            if other.role == UserRole.CHINESE_BUYER and match_type in [MatchType.B2B_TRADE, MatchType.B2C_RETAIL]:
                return True

        return False

    def _calculate_match_score(self, user: UserProfile, other: UserProfile,
                              match_type: MatchType) -> MatchResult:
        scores = {}

        if user.role == UserRole.CHINESE_BUYER and other.role == UserRole.AFRICAN_SUPPLIER:
            scores['category'] = self._calculate_category_match(user, other)
            scores['price'] = self._calculate_price_match(user, other)
            scores['location'] = self._calculate_location_match(user, other)
            scores['rating'] = self._calculate_rating_score(other)
            scores['response'] = self._calculate_response_score(other)
            scores['verification'] = self._calculate_verification_score(other)

        total_score = (
            scores['category'] * self.criteria.category_match_weight +
            scores['price'] * self.criteria.price_range_weight +
            scores['location'] * self.criteria.location_weight +
            scores['rating'] * self.criteria.rating_weight +
            scores['response'] * self.criteria.response_time_weight +
            scores['verification'] * self.criteria.verification_weight
        )

        match_reasons = self._generate_match_reasons(user, other, scores)
        recommended_actions = self._generate_recommendations(user, other, match_type)
        risk_factors = self._identify_risk_factors(user, other)

        return MatchResult(
            match_id=f"match_{user.user_id}_{other.user_id}_{int(datetime.now().timestamp())}",
            buyer_profile=user,
            supplier_profile=other,
            match_type=match_type,
            product=None,
            similarity_score=total_score,
            match_reasons=match_reasons,
            recommended_actions=recommended_actions,
            risk_factors=risk_factors,
            confidence=min(total_score + 0.1, 0.95)
        )

    def _calculate_category_match(self, buyer: UserProfile, supplier: UserProfile) -> float:
        if not buyer.product_interests or not supplier.product_offers:
            return 0.5

        matching_categories = set(buyer.product_interests) & set(supplier.product_offers)
        return len(matching_categories) / max(len(buyer.product_interests), len(supplier.product_offers))

    def _calculate_price_match(self, buyer: UserProfile, supplier: Product) -> float:
        if not buyer.budget_range:
            return 0.7

        min_price, max_price = buyer.budget_range
        if min_price <= supplier.price <= max_price:
            return 1.0
        elif supplier.price < min_price:
            return 0.8
        else:
            proximity = max_price / supplier.price if supplier.price > 0 else 0
            return max(0.3, proximity - 0.2)

    def _calculate_location_match(self, buyer: UserProfile, supplier: UserProfile) -> float:
        if buyer.country == "China" and supplier.country in ["Zimbabwe", "South Africa"]:
            return 0.8

        if buyer.region and supplier.region:
            regions = self.china_africa_trade_knowledge.get("trusted_supplier_regions", {})
            for country, trusted_regions in regions.items():
                if supplier.country == country and supplier.region in trusted_regions:
                    return 0.9

        return 0.6

    def _calculate_rating_score(self, supplier: UserProfile) -> float:
        if supplier.total_transactions == 0:
            return 0.5
        return min(supplier.rating / 5.0, 1.0)

    def _calculate_response_score(self, supplier: UserProfile) -> float:
        if supplier.response_rate == 0:
            return 0.5

        response_score = supplier.response_rate * 0.5

        if supplier.avg_response_time:
            if supplier.avg_response_time <= 60:
                response_score += 0.5
            elif supplier.avg_response_time <= 360:
                response_score += 0.3
            else:
                response_score += 0.1

        return min(response_score, 1.0)

    def _calculate_verification_score(self, supplier: UserProfile) -> float:
        verification_scores = {
            "verified": 1.0,
            "pending": 0.5,
            "unverified": 0.2
        }
        return verification_scores.get(supplier.verification_status, 0.3)

    def _match_products_for_buyer(self, buyer: UserProfile, limit: int) -> List[MatchResult]:
        matching_products = []

        for product_id, product in self.products.items():
            supplier = self.user_profiles.get(product.supplier_id)
            if not supplier:
                continue

            if buyer.role != UserRole.CHINESE_BUYER:
                continue

            product_categories = [product.category]
            if set(product_categories) & set(buyer.product_interests):
                product_score = self._calculate_product_match_score(buyer, product, supplier)
                match_result = self._create_product_match_result(buyer, supplier, product, product_score)
                matching_products.append(match_result)

        matching_products.sort(key=lambda x: x.similarity_score, reverse=True)
        return matching_products[:limit]

    def _calculate_product_match_score(self, buyer: UserProfile, product: Product,
                                     supplier: UserProfile) -> float:
        base_score = 0.5

        if product.category in buyer.product_interests:
            base_score += 0.3

        if buyer.budget_range:
            min_price, max_price = buyer.budget_range
            if min_price <= product.price <= max_price:
                base_score += 0.15

        if supplier.verification_status == "verified":
            base_score += 0.1

        base_score += (supplier.rating / 5.0) * 0.1

        return min(base_score, 0.95)

    def _create_product_match_result(self, buyer: UserProfile, supplier: UserProfile,
                                    product: Product, score: float) -> MatchResult:
        return MatchResult(
            match_id=f"product_{buyer.user_id}_{product.product_id}_{int(datetime.now().timestamp())}",
            buyer_profile=buyer,
            supplier_profile=supplier,
            match_type=MatchType.B2B_TRADE,
            product=product,
            similarity_score=score,
            match_reasons=[
                f"Product matches interest: {product.category.value}",
                f"Price within budget range" if buyer.budget_range else "Price competitive",
                f"Supplier rating: {supplier.rating}/5"
            ],
            recommended_actions=[
                "Send inquiry to supplier",
                "Request product samples",
                "View supplier profile and ratings"
            ],
            risk_factors=self._identify_product_risk_factors(product, supplier),
            confidence=score
        )

    def _generate_match_reasons(self, user: UserProfile, other: UserProfile,
                               scores: Dict[str, float]) -> List[str]:
        reasons = []

        if scores['category'] > 0.7:
            reasons.append("Strong category alignment between buyer interests and supplier offerings")

        if scores['price'] > 0.8:
            reasons.append("Price range matches buyer budget")

        if scores['location'] > 0.7:
            reasons.append("Strategic location for China-Africa trade")

        if scores['rating'] > 0.8:
            reasons.append("High supplier rating from previous transactions")

        if scores['verification'] > 0.8:
            reasons.append("Supplier is verified and trusted")

        if scores['response'] > 0.8:
            reasons.append("Supplier has excellent response time")

        return reasons

    def _generate_recommendations(self, user: UserProfile, other: UserProfile,
                                 match_type: MatchType) -> List[str]:
        recommendations = []

        if user.role == UserRole.CHINESE_BUYER:
            recommendations.append("Send initial inquiry to African supplier")
            recommendations.append("Request product catalog and pricing")

            if other.verification_status == "verified":
                recommendations.append("Consider requesting sample order")
            else:
                recommendations.append("Verify supplier credentials before proceeding")

            if other.total_transactions > 0:
                recommendations.append("Review supplier transaction history")
            else:
                recommendations.append("Start with small trial order to build trust")

        elif user.role == UserRole.AFRICAN_SUPPLIER:
            recommendations.append("Prepare quotation for Chinese buyer")
            recommendations.append("Highlight quality certifications")
            recommendations.append("Explain logistics and delivery options")

        return recommendations

    def _identify_risk_factors(self, user: UserProfile, other: UserProfile) -> List[str]:
        risks = []

        if other.verification_status != "verified":
            risks.append("Supplier verification pending - proceed with caution")

        if other.total_transactions < 5:
            risks.append("Limited transaction history - higher uncertainty")

        if other.rating < 4.0:
            risks.append("Below average supplier rating")

        if other.avg_response_time and other.avg_response_time > 720:
            risks.append("Slow response time may affect communication")

        if user.country == "China" and other.country in ["Zimbabwe"]:
            risks.append("Currency fluctuation risk between CNY and ZWL")
            risks.append("Logistics complexity to remote African regions")

        return risks

    def _identify_product_risk_factors(self, product: Product, supplier: UserProfile) -> List[str]:
        risks = []

        if not product.quality_certifications:
            risks.append("Product lacks quality certifications")

        if product.delivery_time_days > 60:
            risks.append("Long delivery time may affect cash flow")

        if product.min_order_quantity > 1000 and supplier.total_transactions < 10:
            risks.append("High MOQ from unverified supplier - consider trial order")

        return risks

    def get_market_insights(self, category: ProductCategory) -> Dict[str, any]:
        insights = {
            "category": category.value,
            "demand_trend": "growing" if category.value in self.china_africa_trade_knowledge["high_demand_chinese_products"] else "stable",
            "seasonal_availability": self.china_africa_trade_knowledge.get("seasonal_products", {}).get(category.value, []),
            "top_regions": self._get_top_regions_for_category(category),
            "pricing_tips": self._generate_pricing_tips(category),
            "logistics_considerations": self._generate_logistics_tips(category)
        }
        return insights

    def _get_top_regions_for_category(self, category: ProductCategory) -> List[str]:
        category_region_map = {
            ProductCategory.AGRICULTURAL: ["zimbabwe", "south_africa", "kenya"],
            ProductCategory.MINERALS: ["zimbabwe", "south_africa", "dr_congo"],
            ProductCategory.TOURISM_EXPERIENCES: ["south_africa", "zimbabwe", "kenya"],
            ProductCategory.TEXTILES: ["south_africa", "nigeria", "kenya"]
        }
        return category_region_map.get(category, ["south_africa"])

    def _generate_pricing_tips(self, category: ProductCategory) -> List[str]:
        tips = {
            ProductCategory.AGRICULTURAL: [
                "Seasonal pricing varies by 20-40%",
                "Quality grades significantly impact price",
                "Bulk orders can reduce per-unit cost by 15-25%"
            ],
            ProductCategory.MINERALS: [
                "Gemstone pricing highly variable based on quality",
                "Volume discounts available for large orders",
                "Certification costs add 5-10% to total price"
            ],
            ProductCategory.TOURISM_EXPERIENCES: [
                "Peak season pricing 30-50% higher",
                "Package deals offer 15-20% savings",
                "Early booking often secures better rates"
            ]
        }
        return tips.get(category, ["Market pricing varies by quality and quantity"])

    def _generate_logistics_tips(self, category: ProductCategory) -> List[str]:
        tips = {
            ProductCategory.AGRICULTURAL: [
                "Temperature-controlled shipping required",
                "Fumigation certificates often required",
                "Transit time: 3-6 weeks by sea"
            ],
            ProductCategory.MINERALS: [
                "Specialized secure packaging needed",
                "Insurance highly recommended",
                "Customs clearance may take 1-2 weeks"
            ],
            ProductCategory.TOURISM_EXPERIENCES: [
                "Local transportation coordination needed",
                "Booking confirmation 48-72 hours in advance",
                "Local SIM card recommended for tourists"
            ]
        }
        return tips.get(category, ["Contact logistics provider for specific requirements"])
