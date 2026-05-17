"""
Tourista AR AI Model - FastAPI Integration
Lightweight API for Mobile App Integration
Optimized for Low-Latency Cloud Deployment
"""

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Tuple
from datetime import datetime
import asyncio
import json

app = FastAPI(
    title="Tourista AR AI Model API",
    description="Proprietary AI Model for China-Africa Cross-Border Intelligence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tourista_ai_model import MODEL

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str
    context: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    source_language: str
    target_language: str
    context: Optional[str] = None

class UserProfileRequest(BaseModel):
    user_id: str
    role: str
    country: str
    region: str
    languages: List[str] = []
    business_type: Optional[str] = None
    product_interests: List[str] = []
    product_offers: List[str] = []
    preferred_payment_methods: List[str] = []
    budget_range_min: Optional[float] = None
    budget_range_max: Optional[float] = None
    transaction_volume: Optional[int] = None
    verification_status: str = "unverified"
    rating: float = 0.0
    total_transactions: int = 0
    response_rate: float = 0.0
    avg_response_time: Optional[int] = None

class ProductRequest(BaseModel):
    product_id: str
    supplier_id: str
    category: str
    name: str
    description: str
    price: float
    currency: str = "USD"
    min_order_quantity: int = 1
    available_quantity: int = 100
    quality_certifications: List[str] = []
    images: List[str] = []
    logistics_options: List[str] = []
    delivery_time_days: int = 30
    location: str = ""

class MatchingRequest(BaseModel):
    user_id: str
    match_type: str = "B2B_TRADE"
    limit: int = 10

class RecommendationRequest(BaseModel):
    user_id: str
    user_type: str
    context: Optional[Dict] = None
    limit: int = 10

class TransactionRiskRequest(BaseModel):
    transaction_id: Optional[str] = None
    counterparty_id: str
    counterparty_type: str
    payment_method: str
    amount: float
    currency: str = "USD"
    buyer_country: str = "China"
    seller_country: str = "Zimbabwe"
    transaction_type: str = "B2B"
    mobile_money_provider: Optional[str] = None
    velocity_count: int = 0

class ARSceneRequest(BaseModel):
    user_latitude: Optional[float] = None
    user_longitude: Optional[float] = None
    language: str = "en"

class ProductPreviewRequest(BaseModel):
    product_id: str
    language: str = "en"

class TourismExperienceRequest(BaseModel):
    spot_id: str
    language: str = "en"

@app.get("/")
async def root():
    return {
        "service": "Tourista AR AI Model API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
async def health_check():
    return MODEL.health_check()

@app.get("/info")
async def system_info():
    return MODEL.get_system_info()

@app.post("/translate", response_model=Dict)
async def translate_text(request: TranslationRequest):
    try:
        result = MODEL.translate(
            request.text,
            request.source_language,
            request.target_language,
            request.context
        )
        return {
            "success": True,
            "original_text": result.original_text,
            "translated_text": result.translated_text,
            "source_language": result.source_language,
            "target_language": result.target_language,
            "confidence": result.confidence,
            "business_terms_found": result.business_terms_found,
            "local_slang_found": result.local_slang_found,
            "needs_review": result.needs_review
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate/batch", response_model=Dict)
async def batch_translate(request: BatchTranslationRequest):
    try:
        results = MODEL.batch_translate(
            request.texts,
            request.source_language,
            request.target_language,
            request.context
        )
        return {
            "success": True,
            "count": len(results),
            "results": [{
                "original_text": r.original_text,
                "translated_text": r.translated_text,
                "confidence": r.confidence
            } for r in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users/register")
async def register_user(request: UserProfileRequest):
    try:
        profile = UserProfileRequest(
            user_id=request.user_id,
            role=request.role,
            country=request.country,
            region=request.region,
            languages=request.languages,
            business_type=request.business_type,
            product_interests=request.product_interests,
            product_offers=request.product_offers,
            preferred_payment_methods=request.preferred_payment_methods,
            budget_range=(request.budget_range_min, request.budget_range_max) if request.budget_range_min else None,
            transaction_volume=request.transaction_volume,
            verification_status=request.verification_status,
            rating=request.rating,
            total_transactions=request.total_transactions,
            response_rate=request.response_rate,
            avg_response_time=request.avg_response_time
        )
        success = MODEL.register_user(profile)
        return {"success": success, "user_id": request.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products/register")
async def register_product(request: ProductRequest):
    try:
        product = Product(
            product_id=request.product_id,
            supplier_id=request.supplier_id,
            category=ProductCategory[request.category.upper()] if request.category.upper() in ProductCategory.__members__ else ProductCategory.AGRICULTURAL,
            name=request.name,
            description=request.description,
            price=request.price,
            currency=request.currency,
            min_order_quantity=request.min_order_quantity,
            available_quantity=request.available_quantity,
            quality_certifications=request.quality_certifications,
            images=request.images,
            logistics_options=request.logistics_options,
            delivery_time_days=request.delivery_time_days,
            location=request.location
        )
        success = MODEL.register_product(product)
        return {"success": success, "product_id": request.product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/matching/find")
async def find_matches(request: MatchingRequest):
    try:
        matches = MODEL.find_matches(
            request.user_id,
            request.match_type,
            request.limit
        )
        return {
            "success": True,
            "count": len(matches),
            "matches": [{
                "match_id": m.match_id,
                "similarity_score": m.similarity_score,
                "match_type": m.match_type.value,
                "match_reasons": m.match_reasons,
                "recommended_actions": m.recommended_actions,
                "risk_factors": m.risk_factors,
                "confidence": m.confidence
            } for m in matches]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = MODEL.get_recommendations(
            request.user_id,
            request.user_type,
            request.context,
            request.limit
        )
        return {
            "success": True,
            "count": len(recommendations),
            "recommendations": [{
                "recommendation_id": r.recommendation_id,
                "type": r.recommendation_type.value,
                "title": r.title,
                "description": r.description,
                "rationale": r.rationale,
                "priority_score": r.priority_score,
                "action_items": r.action_items,
                "estimated_impact": r.estimated_impact
            } for r in recommendations]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/risk/assess")
async def assess_risk(request: TransactionRiskRequest):
    try:
        transaction_data = {
            "transaction_id": request.transaction_id,
            "counterparty_id": request.counterparty_id,
            "counterparty_type": request.counterparty_type,
            "payment_method": request.payment_method,
            "amount": request.amount,
            "currency": request.currency,
            "buyer_country": request.buyer_country,
            "seller_country": request.seller_country,
            "type": request.transaction_type,
            "mobile_money_provider": request.mobile_money_provider,
            "velocity_count": request.velocity_count
        }
        assessment = MODEL.assess_risk(transaction_data)
        return {
            "success": True,
            "assessment_id": assessment.assessment_id,
            "risk_score": assessment.risk_score,
            "risk_level": assessment.risk_level.value,
            "overall_assessment": assessment.overall_assessment,
            "identified_risks": [{
                "name": r.name,
                "category": r.category.value,
                "severity": r.severity.value,
                "mitigation_strategies": r.mitigation_strategies
            } for r in assessment.identified_risks],
            "recommendations": assessment.recommendations,
            "required_verifications": assessment.required_verifications,
            "approval_status": assessment.approval_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/payment/recommend")
async def get_payment_recommendation(
    amount: float = Query(...),
    buyer_country: str = Query(...),
    seller_country: str = Query(...)
):
    try:
        recommendation = MODEL.get_payment_recommendation(
            amount,
            {"country": buyer_country},
            {"country": seller_country}
        )
        return {"success": True, **recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ar/recognize")
async def recognize_ar_scene(request: ARSceneRequest):
    try:
        user_location = None
        if request.user_latitude and request.user_longitude:
            user_location = (request.user_latitude, request.user_longitude)

        result = MODEL.recognize_ar_scene(
            b"",  # image_data - would be actual image bytes in production
            user_location,
            request.language
        )
        return {
            "success": True,
            "result_id": result.result_id,
            "scene_type": result.scene_type.value,
            "confidence": result.confidence.value,
            "confidence_score": result.confidence_score,
            "augmented_content": result.augmented_content,
            "related_products": result.related_products,
            "related_tours": result.related_tours,
            "language_options": result.language_options
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ar/product/{product_id}")
async def get_product_preview(
    product_id: str,
    language: str = Query(default="en")
):
    try:
        preview = MODEL.get_product_preview(product_id, language)
        if not preview:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"success": True, **preview}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ar/tourism/{spot_id}")
async def get_tourism_experience(
    spot_id: str,
    language: str = Query(default="en")
):
    try:
        experience = MODEL.get_tourism_experience(spot_id, language)
        if not experience:
            raise HTTPException(status_code=404, detail="Tourism spot not found")
        return {"success": True, **experience}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported/languages")
async def get_supported_languages():
    return {
        "languages": [
            {"code": code, "name": name}
            for code, name in MODEL.config.supported_languages.items()
        ]
    }

@app.get("/supported/regions")
async def get_supported_regions():
    return {
        "regions": MODEL.config.supported_regions,
        "payment_methods": TRADE_CONFIG.payment_methods,
        "logistics_partners": TRADE_CONFIG.logistics_partners
    }

@app.get("/trade/insights/{category}")
async def get_trade_insights(category: str):
    try:
        insights = MODEL.recommendation_engine.get_market_insights(
            ProductCategory[category.upper()]
        )
        return {"success": True, **insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/seasonal/pricing/{product_category}")
async def get_seasonal_pricing(product_category: str, month: Optional[str] = None):
    try:
        pricing = MODEL.recommendation_engine.get_seasonal_pricing(
            product_category, month
        )
        return {"success": True, **pricing}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/opportunity/{product_category}/{country}")
async def analyze_market_opportunity(product_category: str, country: str):
    try:
        opportunity = MODEL.recommendation_engine.analyze_market_opportunity(
            product_category, country
        )
        return {"success": True, **opportunity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
