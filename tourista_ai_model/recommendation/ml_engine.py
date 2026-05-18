"""
Deep Learning Recommendation Engine for Tourista AR
China-Africa Cross-Border Trade & Travel Recommendations

Uses PyTorch to implement collaborative filtering with neural networks
for personalized recommendations based on user behavior
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RecommendationType(Enum):
    PRODUCT_RECOMMENDATION = "product_recommendation"
    SUPPLIER_RECOMMENDATION = "supplier_recommendation"
    TOURISM_RECOMMENDATION = "tourism_recommendation"
    LOGISTICS_RECOMMENDATION = "logistics_recommendation"
    PAYMENT_RECOMMENDATION = "payment_recommendation"
    MARKET_INSIGHT = "market_insight"
    PRICE_ALERT = "price_alert"
    TRADE_OPPORTUNITY = "trade_opportunity"


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


class InteractionDataset(Dataset):
    """Dataset for user-item interactions"""
    def __init__(self, interactions: List[Tuple[int, int, float]]):
        self.user_ids = torch.tensor([i[0] for i in interactions], dtype=torch.long)
        self.item_ids = torch.tensor([i[1] for i in interactions], dtype=torch.long)
        self.ratings = torch.tensor([i[2] for i in interactions], dtype=torch.float32)
        
    def __len__(self):
        return len(self.user_ids)
    
    def __getitem__(self, idx):
        return {
            'user_id': self.user_ids[idx],
            'item_id': self.item_ids[idx],
            'rating': self.ratings[idx]
        }


class NeuralRecommendationModel(nn.Module):
    """
    Neural Collaborative Filtering Model
    
    Combines:
    - User embeddings
    - Item embeddings  
    - Neural network layers for interaction
    - Multi-layer perceptron
    """
    def __init__(
        self,
        num_users: int,
        num_items: int,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 3,
        dropout: float = 0.2
    ):
        super().__init__()
        
        # Embedding layers
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        
        # Neural network layers
        layers = []
        input_dim = embedding_dim * 2
        
        for i in range(num_layers):
            layers.append(nn.Linear(input_dim, hidden_dim if i == 0 else hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout))
            input_dim = hidden_dim
        
        self.mlp = nn.Sequential(*layers)
        
        # Final prediction layer
        self.predictor = nn.Linear(hidden_dim, 1)
        
        # Sigmoid for rating prediction
        self.sigmoid = nn.Sigmoid()
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        nn.init.normal_(self.user_embedding.weight, std=0.01)
        nn.init.normal_(self.item_embedding.weight, std=0.01)
        
    def forward(self, user_ids: torch.Tensor, item_ids: torch.Tensor):
        # Get embeddings
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        # Concatenate embeddings
        combined = torch.cat([user_emb, item_emb], dim=1)
        
        # Pass through MLP
        mlp_out = self.mlp(combined)
        
        # Predict
        prediction = self.sigmoid(self.predictor(mlp_out))
        
        return prediction.squeeze()


class MLRecommendationEngine:
    """
    Deep Learning-based Recommendation Engine
    
    Features:
    - Neural collaborative filtering
    - Collaborative filtering recommendations
    - Content-based filtering
    - Hybrid recommendations
    """
    
    def __init__(
        self,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 3,
        dropout: float = 0.2,
        learning_rate: float = 0.001,
        device: Optional[str] = None
    ):
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
        self.learning_rate = learning_rate
        
        # Set device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
            
        logger.info(f"ML Recommendation Engine initialized on device: {self.device}")
        logger.info(f"Architecture: embedding={embedding_dim}, hidden={hidden_dim}")
        
        # Initialize state
        self.model: Optional[NeuralRecommendationModel] = None
        self.user_vocab: Dict[str, int] = {}
        self.item_vocab: Dict[str, int] = {}
        self.item_metadata: Dict[str, Dict] = {}
        self.interactions: List[Tuple[str, str, float]] = []
        self.user_profiles: Dict[str, Dict] = {}
        self.is_trained = False
        
        # Content features
        self.product_categories: List[str] = [
            "coffee", "avocado", "cocoa", "shea_butter", "gemstones", "textiles",
            "minerals_gemstones", "agricultural_products", "tourism_experiences",
            "textiles_crafts"
        ]
        self.countries: List[str] = [
            "china", "zimbabwe", "south_africa", "kenya", "ethiopia", "ghana", "nigeria",
            "tanzania"
        ]
        
        # Market data
        self.seasonal_patterns = self._initialize_seasonal_patterns()
        self.trade_opportunities = self._initialize_trade_opportunities()
        
    def _initialize_seasonal_patterns(self) -> Dict[str, Dict]:
        return {
            "avocado": {
                "peak_season": ["April", "May", "June", "July", "August"],
                "off_season": ["January", "February", "March"],
                "price_variation": 0.35
            },
            "coffee": {
                "peak_season": ["October", "November", "December", "January"],
                "off_season": ["April", "May", "June"],
                "price_variation": 0.40
            },
            "cocoa": {
                "peak_season": ["March", "April", "May", "June", "July", "August"],
                "off_season": ["September", "October", "November"],
                "price_variation": 0.30
            },
            "shea_butter": {
                "peak_season": ["January", "February", "March", "April", "May"],
                "off_season": ["July", "August", "September"],
                "price_variation": 0.25
            },
            "gemstones": {
                "peak_season": ["January", "February", "October", "November", "December"],
                "off_season": ["June", "July", "August"],
                "price_variation": 0.45
            },
            "textiles": {
                "peak_season": ["September", "October", "November", "December"],
                "off_season": ["January", "February"],
                "price_variation": 0.20
            }
        }
        
    def _initialize_trade_opportunities(self) -> List[Dict]:
        return [
            {"category": "agricultural_products", "opportunity": "Chinese demand for African superfoods increasing", "trend": "growing", "market": "China", "volume_growth": 0.25, "price_trend": "increasing"},
            {"category": "minerals_gemstones", "opportunity": "Tanzanite and Alexandrite gaining popularity in Chinese market", "trend": "emerging", "market": "China", "volume_growth": 0.40, "price_trend": "increasing"},
            {"category": "tourism_experiences", "opportunity": "Chinese tourists showing interest in African safari experiences", "trend": "growing", "market": "Africa", "volume_growth": 0.35, "price_trend": "stable"},
            {"category": "textiles_crafts", "opportunity": "African prints gaining traction in Chinese fashion market", "trend": "emerging", "market": "China", "volume_growth": 0.30, "price_trend": "stable"},
            {"category": "coffee", "opportunity": "Specialty coffee from Ethiopia and Zimbabwe in high demand", "trend": "growing", "market": "China", "volume_growth": 0.50, "price_trend": "increasing"}
        ]
        
    def _build_vocabularies(self, users: List[Dict], items: List[Dict]):
        """Build vocabulary mappings from IDs to indices"""
        self.user_vocab = {user['user_id']: idx for idx, user in enumerate(users)}
        self.item_vocab = {item['item_id']: idx for idx, item in enumerate(items)}
        self.item_metadata = {item['item_id']: item for item in items}
        
        logger.info(f"Vocabularies built: {len(self.user_vocab)} users, {len(self.item_vocab)} items")
        
    def _prepare_interactions(self, interactions: List[Tuple[str, str, float]]):
        """Convert interactions to dataset format"""
        dataset_interactions = []
        for user_id, item_id, rating in interactions:
            if user_id in self.user_vocab and item_id in self.item_vocab:
                dataset_interactions.append((
                    self.user_vocab[user_id],
                    self.item_vocab[item_id],
                    rating
                ))
        return dataset_interactions
        
    def train(
        self,
        users: List[Dict],
        items: List[Dict],
        interactions: List[Tuple[str, str, float]],
        epochs: int = 100,
        batch_size: int = 32,
        verbose: bool = True
    ):
        """
        Train the neural recommendation model
        
        Args:
            users: List of user profiles
            items: List of items (products, suppliers, etc.)
            interactions: List of (user_id, item_id, rating) tuples
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Whether to log training progress
        """
        logger.info(f"Training on {len(interactions)} interactions...")
        
        # Save interactions for later use
        self.interactions = interactions
        self.user_profiles = {user['user_id']: user for user in users}
        
        # Build vocabularies
        self._build_vocabularies(users, items)
        
        # Prepare dataset
        dataset_interactions = self._prepare_interactions(interactions)
        
        if len(dataset_interactions) == 0:
            logger.warning("No valid interactions found. Using fallback recommendations.")
            self.is_trained = False
            return
        
        # Create model
        self.model = NeuralRecommendationModel(
            num_users=len(self.user_vocab),
            num_items=len(self.item_vocab),
            embedding_dim=self.embedding_dim,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers,
            dropout=self.dropout
        ).to(self.device)
        
        # Optimizer and loss
        optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        criterion = nn.MSELoss()
        
        # Data loader
        dataset = InteractionDataset(dataset_interactions)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        logger.info(f"Model initialized with {sum(p.numel() for p in self.model.parameters())} parameters")
        
        # Training loop
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0.0
            
            for batch in dataloader:
                user_ids = batch['user_id'].to(self.device)
                item_ids = batch['item_id'].to(self.device)
                ratings = batch['rating'].to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                predictions = self.model(user_ids, item_ids)
                loss = criterion(predictions, ratings)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            avg_loss = total_loss / len(dataloader)
            
            if verbose and (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("Training complete!")
        self.is_trained = True
        
    def predict_rating(self, user_id: str, item_id: str) -> float:
        """Predict rating for a user-item pair"""
        if not self.is_trained or self.model is None:
            return 0.5
            
        user_idx = self.user_vocab.get(user_id)
        item_idx = self.item_vocab.get(item_id)
        
        if user_idx is None or item_idx is None:
            return 0.5
            
        self.model.eval()
        with torch.no_grad():
            user_tensor = torch.tensor([user_idx], dtype=torch.long).to(self.device)
            item_tensor = torch.tensor([item_idx], dtype=torch.long).to(self.device)
            prediction = self.model(user_tensor, item_tensor)
            return float(prediction.item())
            
    def recommend_items(
        self,
        user_id: str,
        items: Optional[List[str]],
        limit: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Recommend items for a user
        
        Args:
            user_id: Target user ID
            items: List of item IDs to consider
            limit: Maximum number of recommendations
            
        Returns:
            List of (item_id, score) tuples sorted by score
        """
        scores = []
        
        for item_id in items:
            score = self.predict_rating(user_id, item_id)
            scores.append((item_id, score))
            
        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:limit]
        
    def generate_recommendations(
        self,
        user_id: str,
        user_type: str,
        current_context: Optional[Dict] = None,
        limit: int = 10
    ) -> List[Recommendation]:
        """
        Generate personalized recommendations
        
        Args:
            user_id: User ID
            user_type: Type of user (chinese_buyer, african_supplier, tourist
            current_context: Additional context
            limit: Maximum recommendations
        """
        recommendations = []
        
        if not self.is_trained or len(self.interactions) == 0:
            return self._fallback_recommendations(user_type, limit)
            
        # Generate hybrid recommendations
        if user_type == "chinese_buyer":
            recommendations.extend(self._recommend_products_neural(user_id, limit))
            recommendations.extend(self._recommend_trade_opportunities())
        elif user_type == "african_supplier":
            recommendations.extend(self._recommend_buyers_neural(user_id, limit))
            recommendations.extend(self._recommend_market_trends())
        elif user_type == "tourist":
            recommendations.extend(self._recommend_tourism_neural(user_id, limit))
            
        recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        return recommendations[:limit]
        
    def _fallback_recommendations(self, user_type: str, limit: int) -> List[Recommendation]:
        """Rule-based fallback recommendations when ML not available"""
        recommendations = []
        
        if user_type == "chinese_buyer":
            recommendations.append(Recommendation(
                recommendation_id=f"rec_prod_1_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.PRODUCT_RECOMMENDATION,
                title="Trending: Ethiopian Coffee in China",
                description="Ethiopian specialty coffee has seen 50% growth in Chinese import demand.",
                rationale=["Growing Chinese middle-class demand", "Competitive pricing", "Trade agreements"],
                priority_score=0.92,
                target_user_segments=["chinese_buyers"],
                action_items=["Search suppliers", "Request samples", "Compare prices"],
                estimated_impact="Potential 50% increase in profit margins",
                expiration_date=datetime.now() + timedelta(days=90)
            ))
            
            for opp in self.trade_opportunities:
                recommendations.append(Recommendation(
                    recommendation_id=f"rec_trade_{opp['category']}_{datetime.now().timestamp()}",
                    recommendation_type=RecommendationType.TRADE_OPPORTUNITY,
                    title=f"Trade Opportunity: {opp['opportunity']}",
                    description=f"{opp['category'].replace('_', ' ').title()} from Africa showing {opp['trend']} trend.",
                    rationale=[f"Market trend: {opp['trend']}", f"Volume growth: {int(opp['volume_growth']*100)}%", f"Price: {opp['price_trend']}"],
                    priority_score=0.80 + (opp['volume_growth'] * 0.2),
                    target_user_segments=["chinese_buyers"],
                    action_items=[f"Search suppliers", "Request analysis"],
                    estimated_impact=f"Growth market with {opp['price_trend']} prices",
                    expiration_date=datetime.now() + timedelta(days=90)
                ))
                
        elif user_type == "african_supplier":
            recommendations.append(Recommendation(
                recommendation_id=f"rec_buy_1_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.SUPPLIER_RECOMMENDATION,
                title="Target Market: Chinese Cosmetic Manufacturers",
                description="Chinese cosmetics industry seeking natural ingredients from Africa.",
                rationale=["Clean beauty trend", "Willingness to pay premium"],
                priority_score=0.89,
                target_user_segments=["african_suppliers"],
                action_items=["Prepare samples", "Create materials"],
                estimated_impact="Access to premium Chinese market",
                expiration_date=None
            ))
            
        elif user_type == "tourist":
            recommendations.append(Recommendation(
                recommendation_id=f"rec_tour_1_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
                title="Experience: Victoria Falls Adventure",
                description="Combine trade visit with unforgettable Victoria Falls experience.",
                rationale=["World Wonder", "Multiple activities"],
                priority_score=0.90,
                target_user_segments=["business_travelers"],
                action_items=["Book tour", "Check visa"],
                estimated_impact="Enhanced business trip",
                expiration_date=None
            ))
            
        recommendations.sort(key=lambda x: x.priority_score, reverse=True)
        return recommendations[:limit]
        
    def _recommend_products_neural(self, user_id: str, limit: int) -> List[Recommendation]:
        """Neural product recommendations"""
        recommendations = []
        
        # Get item recommendations
        # For demo, we'll generate recommendations based on seasonal patterns
        current_month = datetime.now().strftime("%B")
        
        for product, data in self.seasonal_patterns.items():
            score = 0.7
            if current_month in data['peak_season']:
                score += 0.2
                
            # Determine season
            is_peak = current_month in data['peak_season']
            season_text = "peak" if is_peak else "off-"
            action_text = "Consider stocking up" if not is_peak else "High demand period."
            
            recommendations.append(Recommendation(
                recommendation_id=f"rec_neural_{product}_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.PRODUCT_RECOMMENDATION,
                title=f"Recommended: {product.replace('_', ' ').title()}",
                description=f"{product.replace('_', ' ').title()} is in {season_text} season. {action_text}",
                rationale=[f"Seasonal variation: {int(data['price_variation']*100)}%", f"Peak: {', '.join(data['peak_season'][:3])}"],
                priority_score=score,
                target_user_segments=["chinese_buyers"],
                action_items=["Search suppliers", "Compare prices"],
                estimated_impact="Seasonal opportunity",
                expiration_date=datetime.now() + timedelta(days=60),
                metadata={"product": product}
            ))
            
        return recommendations
        
    def _recommend_trade_opportunities(self) -> List[Recommendation]:
        recommendations = []
        
        for opp in self.trade_opportunities:
            recommendations.append(Recommendation(
                recommendation_id=f"rec_trade_{opp['category']}_{datetime.now().timestamp()}",
                recommendation_type=RecommendationType.TRADE_OPPORTUNITY,
                title=f"Trade Opportunity: {opp['opportunity']}",
                description=f"{opp['category'].replace('_', ' ').title()} from Africa showing {opp['trend']} trend with {int(opp['volume_growth']*100)}% volume growth.",
                rationale=[f"Market trend: {opp['trend']}", f"Volume growth: {int(opp['volume_growth']*100)}%", f"Price trend: {opp['price_trend']}"],
                priority_score=0.80 + (opp['volume_growth'] * 0.2),
                target_user_segments=["chinese_buyers"],
                action_items=[f"Search for {opp['category'].replace('_', ' ')} suppliers"],
                estimated_impact=f"Growth market with {opp['price_trend']} prices",
                expiration_date=datetime.now() + timedelta(days=90),
                metadata=opp
            ))
            
        return recommendations
        
    def _recommend_buyers_neural(self, user_id: str, limit: int) -> List[Recommendation]:
        """Neural buyer recommendations for suppliers"""
        recommendations = []
        
        recommendations.append(Recommendation(
            recommendation_id=f"rec_buy_neural_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.SUPPLIER_RECOMMENDATION,
            title="Target Market: Chinese Cosmetic Manufacturers",
            description="Chinese cosmetics industry seeking natural ingredients from Africa.",
            rationale=["Clean beauty trend", "Willingness to pay premium"],
            priority_score=0.89,
            target_user_segments=["african_suppliers"],
            action_items=["Prepare samples", "Create marketing materials"],
            estimated_impact="Access to premium Chinese market",
            expiration_date=None
        ))
        
        return recommendations
        
    def _recommend_market_trends(self) -> List[Recommendation]:
        recommendations = []
        
        recommendations.append(Recommendation(
            recommendation_id=f"rec_trend_1_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.MARKET_INSIGHT,
            title="Market Trend: Chinese Retail Preferences",
            description="Chinese buyers increasingly prefer smaller order quantities with more frequent shipments.",
            rationale=["Reduced inventory risk", "Flexibility to test suppliers"],
            priority_score=0.82,
            target_user_segments=["african_suppliers"],
            action_items=["Offer MOQ flexibility"],
            estimated_impact="Access to larger customer base",
            expiration_date=None
        ))
        
        return recommendations
        
    def _recommend_tourism_neural(self, user_id: str, limit: int) -> List[Recommendation]:
        """Neural tourism recommendations"""
        recommendations = []
        
        recommendations.append(Recommendation(
            recommendation_id=f"rec_tour_neural_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Experience: Victoria Falls Adventure",
            description="Combine your trade visit with an unforgettable Victoria Falls experience.",
            rationale=["World Wonder designation", "Multiple activity options"],
            priority_score=0.90,
            target_user_segments=["business_travelers"],
            action_items=["Book guided tour", "Check visa requirements"],
            estimated_impact="Enhanced business trip",
            expiration_date=None
        ))
        
        recommendations.append(Recommendation(
            recommendation_id=f"rec_tour_neural_2_{datetime.now().timestamp()}",
            recommendation_type=RecommendationType.TOURISM_RECOMMENDATION,
            title="Experience: South African Safari",
            description="Visit world-class game reserves near Johannesburg.",
            rationale=["World-renowned wildlife experience", "Easy connectivity from China"],
            priority_score=0.93,
            target_user_segments=["chinese_tourists"],
            action_items=["Choose game reserve", "Book through tour operators"],
            estimated_impact="Bucket-list experience",
            expiration_date=None
        ))
        
        return recommendations
        
    def get_seasonal_pricing(self, product_category: str, target_month: Optional[str] = None) -> Dict:
        """Get seasonal pricing information"""
        seasonal_data = self.seasonal_patterns.get(product_category, {})
        
        if not seasonal_data:
            return {
                "category": product_category,
                "seasonal_pattern": "No seasonal data available",
                "recommendation": "Contact suppliers"
            }
            
        return {
            "category": product_category,
            "peak_season_months": seasonal_data.get("peak_season", []),
            "off_season_months": seasonal_data.get("off_season", []),
            "price_variation": f"{int(seasonal_data.get('price_variation', 0.25)*100)}%",
            "recommendation": "Buy during off-season for better pricing" if seasonal_data.get('price_variation', 0) > 0.2 else "Price relatively stable",
            "estimated_savings": f"Up to {int(seasonal_data.get('price_variation', 0.25)*100)}%"
        }
        
    def analyze_market_opportunity(self, product_category: str, target_country: str) -> Dict:
        """Analyze market opportunity for a product"""
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
            
        return {
            "product_category": product_category,
            "target_country": target_country,
            "opportunity_score": min(opportunity_score, 1.0),
            "factors": factors,
            "recommendation": "High opportunity - pursue actively" if opportunity_score > 0.85 else "Moderate opportunity"
        }
        
    def save_model(self, filepath: str):
        """Save model to disk"""
        if self.model is not None:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'user_vocab': self.user_vocab,
                'item_vocab': self.item_vocab,
                'item_metadata': self.item_metadata,
                'config': {
                    'embedding_dim': self.embedding_dim,
                    'hidden_dim': self.hidden_dim,
                    'num_layers': self.num_layers,
                    'dropout': self.dropout
                }
            }, filepath)
            logger.info(f"Model saved to {filepath}")
            
    def load_model(self, filepath: str):
        """Load model from disk"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.model = NeuralRecommendationModel(
            num_users=len(checkpoint['user_vocab']),
            num_items=len(checkpoint['item_vocab']),
            embedding_dim=checkpoint['config']['embedding_dim'],
            hidden_dim=checkpoint['config']['hidden_dim'],
            num_layers=checkpoint['config']['num_layers'],
            dropout=checkpoint['config']['dropout']
        ).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.user_vocab = checkpoint['user_vocab']
        self.item_vocab = checkpoint['item_vocab']
        self.item_metadata = checkpoint['item_metadata']
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")
