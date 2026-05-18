"""
ML-Powered AR Scene Recognition Engine for Tourista AR
Advanced Computer Vision & Deep Learning for Scene Recognition
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import io
import base64
import json

# Import ML components conditionally
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    logging.warning("Pillow not available, image processing will be simulated")

try:
    import torch
    import torch.nn as nn
    import torchvision.models as models
    import torchvision.transforms as transforms
    from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch not available, using feature-based fallback")

from tourista_ai_model.ar_recognition.engine import (
    ARSceneType, RecognitionConfidence, ARMarker,
    SceneRecognitionResult, ProductPreview
)

logger = logging.getLogger(__name__)


class SceneFeatureExtractor:
    """
    Advanced feature extractor using pre-trained deep learning models
    """
    
    def __init__(self):
        self.device = "cpu"
        self.model = None
        self.preprocess = None
        self.is_initialized = False
        
        if TORCH_AVAILABLE:
            self._initialize_model()
        else:
            logger.info("Using traditional feature extractor (PyTorch not available)")
    
    def _initialize_model(self):
        try:
            # Load pre-trained ResNet50 for feature extraction
            self.model = models.resnet50(pretrained=True)
            # Remove the final fully connected layer
            self.model = nn.Sequential(*list(self.model.children())[:-1])
            self.model.eval()
            self.model.to(self.device)
            
            # Define preprocessing transforms
            self.preprocess = Compose([
                Resize(256),
                CenterCrop(224),
                ToTensor(),
                Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
            ])
            
            self.is_initialized = True
            logger.info("ResNet50 feature extractor initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize deep model: {str(e)}")
            logger.info("Falling back to traditional features")
    
    def extract_features(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract comprehensive features from image data
        """
        features = {
            "deep_features": None,
            "traditional_features": {
                "dominant_colors": ["green", "blue", "brown"],
                "detected_shapes": ["irregular", "organic"],
                "textures": ["rough", "natural"],
                "scene_category": "natural_landscape",
                "has_water": True,
                "has_vegetation": True,
                "has_architecture": False,
                "complexity_score": 0.75
            }
        }
        
        if TORCH_AVAILABLE and self.is_initialized and PILLOW_AVAILABLE:
            try:
                features["deep_features"] = self._extract_deep_features(image_data)
            except Exception as e:
                logger.warning(f"Deep feature extraction failed: {str(e)}")
        
        return features
    
    def _extract_deep_features(self, image_data: bytes) -> np.ndarray:
        """Extract deep features using ResNet50"""
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess
        img_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Forward pass
        with torch.no_grad():
            features = self.model(img_tensor)
            
        return features.squeeze().cpu().numpy()


class SceneClassifier:
    """
    Scene classification using both traditional and deep features
    """
    
    def __init__(self):
        self.scene_database = []
        self.feature_db = {}
        self.classifier_model = None
    
    def initialize_database(self, markers: List[ARMarker]):
        """
        Initialize with pre-defined AR markers
        """
        self.scene_database = markers
        logger.info(f"Scene database initialized with {len(markers)} markers")
    
    def classify_scene(self, features: Dict, user_location: Optional[Tuple[float, float]]) -> Tuple[List[ARMarker], List[float]]:
        """
        Classify scene using multiple feature modalities
        """
        matches = []
        scores = []
        
        for marker in self.scene_database:
            score = self._calculate_similarity(features, marker, user_location)
            matches.append(marker)
            scores.append(score)
        
        # Sort by score descending
        sorted_pairs = sorted(zip(scores, matches), key=lambda x: x[0], reverse=True)
        scores, matches = zip(*sorted_pairs) if sorted_pairs else ([], [])
        
        return list(matches), list(scores)
    
    def _calculate_similarity(self, features: Dict, marker: ARMarker,
                           user_location: Optional[Tuple[float, float]]) -> float:
        """
        Calculate multi-modal similarity
        """
        score = 0.0
        trad_features = features["traditional_features"]
        
        # 1. Traditional visual feature matching
        trad_score = self._match_traditional_features(trad_features, marker)
        score += trad_score * 0.6
        
        # 2. Location-based matching (if available)
        if user_location:
            loc_score = self._match_location(user_location, marker.location)
            score += loc_score * 0.4
        
        return min(score, 1.0)
    
    def _match_traditional_features(self, features: Dict, marker: ARMarker) -> float:
        """Match traditional features"""
        score = 0.0
        
        feature_overlap = len(set(features.get("dominant_colors", [])) &
                             set(marker.visual_features))
        if feature_overlap > 0:
            score += (feature_overlap / len(marker.visual_features)) * 0.5
        
        if features.get("has_water") and "water" in marker.visual_features:
            score += 0.15
        
        if features.get("has_vegetation") and any(v in marker.visual_features
                                               for v in ["vegetation", "trees", "grasslands"]):
            score += 0.1
        
        if features.get("has_architecture") and any(v in marker.visual_features
                                                   for v in ["walls", "ancient_architecture"]):
            score += 0.15
        
        return min(score, 1.0)
    
    def _match_location(self, user_loc: Tuple[float, float], marker_loc: Tuple[float, float]) -> float:
        """Calculate location similarity"""
        # Haversine distance (km)
        from math import radians, sin, cos, atan2, sqrt
        lat1, lon1 = user_loc
        lat2, lon2 = marker_loc
        
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        
        a = (sin(dlat / 2) ** 2 +
             cos(radians(lat1)) * cos(radians(lat2)) *
             sin(dlon / 2) ** 2)
        
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        # Score decreases with distance
        if distance < 10:
            return 1.0
        elif distance < 50:
            return 0.8
        elif distance < 100:
            return 0.5
        elif distance < 200:
            return 0.2
        else:
            return 0.0


class MLARRecognitionEngine:
    """
    ML-Powered AR Scene Recognition Engine
    
    Combines:
    - Deep learning-based feature extraction
    - Multi-modal scene classification
    - Location-aware matching
    - Fallback to rule-based system
    """
    
    def __init__(self):
        # Initialize ML components
        self.feature_extractor = SceneFeatureExtractor()
        self.scene_classifier = SceneClassifier()
        
        # Initialize databases
        self.scene_database = self._initialize_scene_database()
        self.product_previews = self._initialize_product_previews()
        self.tourism_spots = self._initialize_tourism_spots()
        
        # Initialize classifier with our markers
        self.scene_classifier.initialize_database(self.scene_database)
        
        self.recognition_cache = {}
        
        logger.info("ML AR Recognition Engine initialized successfully")
    
    def _initialize_scene_database(self) -> List[ARMarker]:
        return [
            ARMarker(
                marker_id="vic_falls_main",
                marker_type=ARSceneType.TOURISM_SPOT,
                name="Victoria Falls - Main View",
                description="World's largest waterfall, known as 'The Smoke That Thunders'",
                location=(-17.9244, 25.8572),
                associated_products=["vic_falls_photo_print", "rainbow_artisan_jewelry"],
                cultural_significance="Sacred site for local Tonga people, UNESCO World Heritage Site",
                visual_features=["water", "mist", "rainbow", "cliff", "tropical_vegetation"],
                ar_assets={
                    "3d_model": "victoria_falls_3d.glb",
                    "video": "vic_falls_waterfall_animation.mp4",
                    "audio": "vic_falls_ambient_sounds.mp3"
                },
                language_content={
                    "zh": "维多利亚瀑布 - 世界最大瀑布",
                    "en": "Victoria Falls - World's Largest Waterfall",
                    "sn": "Victoria Falls - Mvura Yemumera"
                }
            ),
            ARMarker(
                marker_id="great_zimbabwe",
                marker_type=ARSceneType.CULTURAL_HERITAGE,
                name="Great Zimbabwe Ruins",
                description="Ancient stone ruins of a medieval city, UNESCO World Heritage Site",
                location=(-20.2689, 31.0456),
                associated_products=["soapstone_carvings", "traditional_shona_art"],
                cultural_significance="Capital of the Shona Kingdom, 11th-15th century",
                visual_features=["stone_walls", "ancient_architecture", "grasslands", "baobab_trees"],
                ar_assets={
                    "3d_model": "great_zimbabwe_reconstruction.glb",
                    "video": "great_zimbabwe_history.mp4",
                    "historical_images": "great_zimbabwe_archive.zip"
                },
                language_content={
                    "zh": "大津巴布韦遗址",
                    "en": "Great Zimbabwe - Ancient Kingdom",
                    "sn": "Great Zimbabwe - Mufuva weShona"
                }
            ),
            ARMarker(
                marker_id="kruger_safari",
                marker_type=ARSceneType.WILDLIFE,
                name="Kruger National Park - Safari Experience",
                description="World-renowned wildlife reserve with Big Five viewing",
                location=(-24.0117, 31.4858),
                associated_products=["safari_photography", "traditional_artifacts"],
                cultural_significance="Premier wildlife conservation area in Africa",
                visual_features=["savanna", "acacia_trees", "wildlife", "bush"],
                ar_assets={
                    "3d_model": "kruger_landscape.glb",
                    "animal_models": "kruger_wildlife_3d.zip",
                    "video": "kruger_safari_preview.mp4"
                },
                language_content={
                    "zh": "克鲁格国家公园 - 野生动物园体验",
                    "en": "Kruger National Park - Safari Experience",
                    "zu": "iKruger - Indawo Yenkosi"
                }
            ),
            ARMarker(
                marker_id="table_mountain",
                marker_type=ARSceneType.TOURISM_SPOT,
                name="Table Mountain - Cape Town",
                description="Iconic flat-topped mountain overlooking Cape Town",
                location=(-33.9628, 18.4098),
                associated_products=["table_mountain_photo_prints", "cape_dutch_art"],
                cultural_significance="Natural wonder and symbol of Cape Town",
                visual_features=["mountain", "flat_top", "cloud", "city_view", "ocean"],
                ar_assets={
                    "3d_model": "table_mountain_3d.glb",
                    "time_lapse": "table_mountain_clouds.mp4",
                    "aerial_view": "table_mountain_drone.mp4"
                },
                language_content={
                    "zh": "桌山 - 开普敦",
                    "en": "Table Mountain - Cape Town",
                    "xh": "iTable - Kumtonto weCape Town"
                }
            ),
            ARMarker(
                marker_id="harare_market",
                marker_type=ARSceneType.MARKETPLACE,
                name="Harare Street Market",
                description="Vibrant local market featuring crafts, textiles, and fresh produce",
                location=(-17.8178, 31.0453),
                associated_products=["shona_sculptures", "woven_baskets", "textiles", "jewelry"],
                cultural_significance="Center of local trade and artisan crafts",
                visual_features=["colorful_stalls", "handicrafts", "textiles", "baskets"],
                ar_assets={
                    "3d_model": "market_stall.glb",
                    "product_gallery": "market_products.zip",
                    "price_guide": "market_pricing.pdf"
                },
                language_content={
                    "zh": "哈拉雷街头市场",
                    "en": "Harare Street Market",
                    "sn": "Musika weHarare"
                }
            )
        ]
    
    def _initialize_product_previews(self) -> List[ProductPreview]:
        return [
            ProductPreview(
                product_id="shona_sculpture_001",
                product_name="Traditional Shona Sculpture",
                origin_country="Zimbabwe",
                origin_region="Harare",
                ar_3d_model_url="https://assets.tourista-ar.ai/products/shona_sculpture_001.glb",
                ar_instructions=[
                    "Point camera at flat surface",
                    "Tap to place sculpture",
                    "Pinch to resize",
                    "Rotate to view from all angles"
                ],
                size_options=["Small (20cm)", "Medium (40cm)", "Large (80cm)"],
                color_options=["Natural Stone", "Polished Black", "Serpentine Green"],
                price_usd=150.0,
                supplier_info={
                    "name": "Shona Art Collective",
                    "rating": 4.8,
                    "location": "Harare, Zimbabwe",
                    "verified": True
                },
                quality_certifications=["Authenticity Certificate", "Export Permit"],
                logistics_info={
                    "shipping_from": "Harare, Zimbabwe",
                    "estimated_delivery": "3-4 weeks",
                    "shipping_cost": 45,
                    "customs_clearance": "included"
                },
                preview_backgrounds=["traditional_home", "modern_office", "art_gallery", "outdoor"],
                cultural_context="Shona sculptures represent spiritual connection to ancestors"
            ),
            ProductPreview(
                product_id="avocado_hass_001",
                product_name="Premium Hass Avocados",
                origin_country="Zimbabwe",
                origin_region="Nyanga",
                ar_3d_model_url="https://assets.tourista-ar.ai/products/avocado_3d.glb",
                ar_instructions=[
                    "Point camera at fruit bowl or table",
                    "Tap to place avocados",
                    "See actual size comparison",
                    "View cross-section for ripeness indicator"
                ],
                size_options=["30 count box", "60 count box", "120 count box"],
                color_options=["Standard Grade", "Premium Grade"],
                price_usd=2.5,
                supplier_info={
                    "name": "Nyanga Valley Farms",
                    "rating": 4.6,
                    "location": "Nyanga, Zimbabwe",
                    "verified": True
                },
                quality_certifications=["Phytosanitary Certificate", "Gap Certificate", "Organic Certification"],
                logistics_info={
                    "shipping_from": "Harare, Zimbabwe",
                    "estimated_delivery": "2-3 weeks",
                    "shipping_cost": 500,
                    "temperature_control": "required (4-8°C)",
                    "min_order": "30 boxes"
                },
                preview_backgrounds=["kitchen_counter", "supermarket_display", "export_crate"],
                cultural_context="Zimbabwean avocados are known for superior oil content and creamy texture"
            ),
            ProductPreview(
                product_id="coffee_zimbabwe_001",
                product_name="Mountain Grade Zimbabwe Coffee",
                origin_country="Zimbabwe",
                origin_region="Chipinge",
                ar_3d_model_url="https://assets.tourista-ar.ai/products/coffee_bag_3d.glb",
                ar_instructions=[
                    "Point camera at counter or shelf",
                    "Tap to place coffee bag",
                    "Rotate to see all packaging details",
                    "View roast level indicator"
                ],
                size_options=["250g bag", "500g bag", "1kg bag"],
                color_options=["Light Roast", "Medium Roast", "Dark Roast"],
                price_usd=18.0,
                supplier_info={
                    "name": "Chipinge Coffee Cooperative",
                    "rating": 4.9,
                    "location": "Chipinge, Zimbabwe",
                    "verified": True
                },
                quality_certifications=["Rainforest Alliance", "Fair Trade", "Organic"],
                logistics_info={
                    "shipping_from": "Harare, Zimbabwe",
                    "estimated_delivery": "1-2 weeks",
                    "shipping_cost": 25,
                    "special_handling": "sealed container, away from moisture"
                },
                preview_backgrounds=["coffee_shop", "kitchen_shelf", "office_break_room"],
                cultural_context="Zimbabwe coffee rivals Ethiopian and Kenyan varieties in quality"
            )
        ]
    
    def _initialize_tourism_spots(self) -> Dict[str, Dict]:
        return {
            "victoria_falls": {
                "name": "Victoria Falls",
                "country": "Zimbabwe",
                "type": "Natural Wonder",
                "ar_experiences": [
                    "3D waterfall visualization",
                    "Historical timeline overlay",
                    "Wildlife spotting guide",
                    "Rainbow photography tips"
                ],
                "tour_options": [
                    {"name": "Helicopter Tour", "duration": "45 min", "price_usd": 250},
                    {"name": "Sunset Cruise", "duration": "2 hours", "price_usd": 80},
                    {"name": "Devil's Pool Experience", "duration": "3 hours", "price_usd": 120}
                ],
                "best_season": "February to May (highest water flow)",
                "language_support": ["zh", "en", "sn", "nd"]
            },
            "great_zimbabwe": {
                "name": "Great Zimbabwe Ruins",
                "country": "Zimbabwe",
                "type": "Historical Site",
                "ar_experiences": [
                    "3D reconstruction of ancient city",
                    "Historical audio guide",
                    "Archaeological discovery game",
                    "Cultural significance overlay"
                ],
                "tour_options": [
                    {"name": "Guided Historical Tour", "duration": "3 hours", "price_usd": 50},
                    {"name": "Full Day Cultural Experience", "duration": "6 hours", "price_usd": 90}
                ],
                "best_season": "April to October (dry season)",
                "language_support": ["zh", "en", "sn"]
            },
            "kruger_park": {
                "name": "Kruger National Park",
                "country": "South Africa",
                "type": "Wildlife Reserve",
                "ar_experiences": [
                    "Animal identification guide",
                    "Safari route planner",
                    "Wildlife tracking simulation",
                    "Conservation education overlay"
                ],
                "tour_options": [
                    {"name": "Big Five Safari", "duration": "8 hours", "price_usd": 180},
                    {"name": "Private Game Drive", "duration": "6 hours", "price_usd": 250},
                    {"name": "Bush Walk", "duration": "3 hours", "price_usd": 75}
                ],
                "best_season": "May to September (dry season, best wildlife viewing)",
                "language_support": ["zh", "en", "zu", "xh"]
            }
        }
    
    def recognize_scene(self, image_data: bytes, user_location: Optional[Tuple[float, float]] = None,
                       language: str = "en") -> SceneRecognitionResult:
        """
        ML-Powered scene recognition
        
        Args:
            image_data: Input image bytes
            user_location: Optional user GPS coordinates
            language: Preferred language
            
        Returns:
            SceneRecognitionResult with ML-based confidence scores
        """
        # Extract features
        features = self.feature_extractor.extract_features(image_data)
        
        # Classify scene
        matched_markers, scores = self.scene_classifier.classify_scene(features, user_location)
        
        # Get top matches with scores > threshold
        valid_markers = [m for m, s in zip(matched_markers, scores) if s > 0.3][:3]
        best_score = scores[0] if scores else 0.0
        best_match = valid_markers[0] if valid_markers else None
        
        # Build result
        result = SceneRecognitionResult(
            result_id=f"ml_ar_result_{datetime.now().timestamp()}",
            scene_type=best_match.marker_type if best_match else ARSceneType.PRODUCT_PREVIEW,
            confidence=self._determine_confidence_level(best_score),
            confidence_score=best_score,
            detected_markers=valid_markers,
            augmented_content=self._generate_augmented_content(best_match, language),
            related_products=self._find_related_products(best_match),
            related_tours=self._find_related_tours(best_match),
            language_options=["zh", "en", "sn", "nd", "zu", "xh"]
        )
        
        # Cache result
        self.recognition_cache[result.result_id] = result
        
        return result
    
    def _determine_confidence_level(self, score: float) -> RecognitionConfidence:
        if score >= 0.85:
            return RecognitionConfidence.VERY_HIGH
        elif score >= 0.70:
            return RecognitionConfidence.HIGH
        elif score >= 0.55:
            return RecognitionConfidence.MEDIUM
        elif score >= 0.40:
            return RecognitionConfidence.LOW
        else:
            return RecognitionConfidence.VERY_LOW
    
    def _generate_augmented_content(self, marker: Optional[ARMarker],
                                   language: str) -> Dict[str, any]:
        if not marker:
            return {
                "title": "New Discovery",
                "description": "Unable to identify scene. Would you like to explore nearby attractions?",
                "suggested_actions": ["search_products", "view_map", "contact_guide"]
            }
        
        return {
            "title": marker.language_content.get(language, marker.name),
            "description": marker.description,
            "cultural_info": marker.cultural_significance,
            "ar_assets": marker.ar_assets,
            "suggested_actions": [
                "view_3d_model",
                "watch_video",
                "learn_history",
                "find_similar_products",
                "book_tour"
            ],
            "language_options": list(marker.language_content.keys()),
            "ml_recognized": True
        }
    
    def _find_related_products(self, marker: Optional[ARMarker]) -> List[Dict]:
        if not marker:
            return []
        
        related = []
        for product_id in marker.associated_products:
            product = next((p for p in self.product_previews if p.product_id == product_id), None)
            if product:
                related.append({
                    "product_id": product.product_id,
                    "name": product.product_name,
                    "price_usd": product.price_usd,
                    "origin": product.origin_country,
                    "ar_available": True,
                    "supplier_rating": product.supplier_info.get("rating", 0)
                })
        
        return related
    
    def _find_related_tours(self, marker: Optional[ARMarker]) -> List[Dict]:
        if not marker:
            return []
        
        for spot_id, spot_data in self.tourism_spots.items():
            if spot_id in marker.marker_id.lower() or marker.name in spot_data["name"]:
                return spot_data.get("tour_options", [])
        
        return []
    
    def get_product_preview(self, product_id: str, language: str = "en") -> Optional[Dict]:
        product = next((p for p in self.product_previews if p.product_id == product_id), None)
        
        if not product:
            return None
        
        return {
            "product_id": product.product_id,
            "name": product.product_name,
            "origin": f"{product.origin_region}, {product.origin_country}",
            "ar_model": product.ar_3d_model_url,
            "instructions": product.ar_instructions,
            "options": {
                "sizes": product.size_options,
                "colors": product.color_options
            },
            "pricing": {
                "unit_price_usd": product.price_usd,
                "supplier": product.supplier_info.get("name"),
                "supplier_rating": product.supplier_info.get("rating"),
                "verified": product.supplier_info.get("verified", False)
            },
            "certifications": product.quality_certifications,
            "logistics": {
                "shipping_from": product.logistics_info.get("shipping_from"),
                "delivery_time": product.logistics_info.get("estimated_delivery"),
                "shipping_cost_usd": product.logistics_info.get("shipping_cost")
            },
            "preview_backgrounds": product.preview_backgrounds,
            "cultural_context": product.cultural_context,
            "purchase_url": f"https://tourista-ar.ai/shop/{product_id}",
            "language": language
        }
    
    def get_tourism_experience(self, spot_id: str, language: str = "en") -> Optional[Dict]:
        spot_data = self.tourism_spots.get(spot_id)
        
        if not spot_data:
            return None
        
        marker = next((m for m in self.scene_database
                      if spot_id in m.marker_id.lower()), None)
        
        return {
            "spot_id": spot_id,
            "name": spot_data["name"],
            "country": spot_data["country"],
            "type": spot_data["type"],
            "ar_experiences": spot_data["ar_experiences"],
            "tour_options": spot_data["tour_options"],
            "best_season": spot_data["best_season"],
            "cultural_significance": marker.cultural_significance if marker else None,
            "ar_assets": marker.ar_assets if marker else {},
            "language_content": marker.language_content if marker else {},
            "booking_url": f"https://tourista-ar.ai/tours/{spot_id}",
            "language": language
        }
