"""
Neural Matching Network for Tourista AR
Uses PyTorch for Neural Network-based Buyer-Supplier Matching

Features:
- Multi-layer Perceptron (MLP) for matching
- Embedding-based similarity learning
- Collaborative filtering
- Real-time inference
- Transfer learning support
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    """User profile for matching"""
    user_id: str
    role: str  # 'buyer' or 'supplier'
    country: str
    region: str
    languages: List[str]
    product_interests: Optional[List[str]] = None
    product_offers: Optional[List[str]] = None
    budget_range: Optional[Tuple[float, float]] = None
    price_range: Optional[Tuple[float, float]] = None
    rating: float = 0.0
    verification_status: str = "unverified"
    total_transactions: int = 0


@dataclass
class MatchResult:
    """Result of matching operation"""
    supplier_id: str
    supplier_name: str
    similarity_score: float
    match_reasons: List[str]
    product_overlap: float
    location_score: float
    trust_score: float
    price_alignment: float


class NeuralMatchingEngine:
    """
    Neural Network-based Matching Engine
    
    Architecture:
    - User Embedding Layer (learns representations)
    - Dual MLP Networks for buyer and supplier
    - Similarity Computation Layer
    - Matching Score Predictor
    """
    
    def __init__(
        self,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 2,
        dropout: float = 0.1,
        device: Optional[str] = None
    ):
        """
        Initialize Neural Matching Engine
        
        Args:
            embedding_dim: Dimension of user embeddings
            hidden_dim: Hidden layer dimension
            num_layers: Number of MLP layers
            dropout: Dropout rate
            device: 'cuda', 'cpu', or 'auto'
        """
        self.device = self._get_device(device)
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.dropout = dropout
        
        # User and product vocabularies
        self.user_vocab: Dict[str, int] = {}
        self.product_vocab: Dict[str, int] = {}
        self.country_vocab: Dict[str, int] = {}
        
        # Initialize model
        self.model = None
        self.user_embeddings = None
        self.product_embeddings = None
        
        logger.info(f"Neural Matching Engine initialized on device: {self.device}")
        logger.info(f"Architecture: embedding={embedding_dim}, hidden={hidden_dim}")
    
    def _get_device(self, device: Optional[str]) -> torch.device:
        """Auto-detect best device"""
        if device:
            return torch.device(device)
        if torch.cuda.is_available():
            return torch.device('cuda')
        return torch.device('cpu')
    
    def _build_vocabularies(self, users: List[UserProfile]):
        """Build vocabularies from user profiles"""
        user_id_set = set()
        product_set = set()
        country_set = set()
        
        for user in users:
            user_id_set.add(user.user_id)
            country_set.add(user.country)
            country_set.add(user.region)
            
            if user.product_interests:
                product_set.update(user.product_interests)
            if user.product_offers:
                product_set.update(user.product_offers)
        
        self.user_vocab = {uid: idx for idx, uid in enumerate(user_id_set)}
        self.product_vocab = {pid: idx for idx, pid in enumerate(product_set)}
        self.country_vocab = {cid: idx for idx, cid in enumerate(country_set)}
        
        vocab_sizes = {
            'users': len(self.user_vocab),
            'products': len(self.product_vocab),
            'countries': len(self.country_vocab)
        }
        logger.info(f"Vocabularies built: {vocab_sizes}")
    
    def _create_user_features(self, user: UserProfile) -> np.ndarray:
        """Create feature vector for user"""
        features = []
        
        # 1. Role encoding (buyer=0, supplier=1)
        role_enc = 0.0 if user.role == 'buyer' else 1.0
        features.append(role_enc)
        
        # 2. Country embedding (one-hot)
        country_idx = self.country_vocab.get(user.country, 0)
        country_onehot = np.zeros(len(self.country_vocab))
        country_onehot[country_idx] = 1.0
        features.extend(country_onehot.tolist())
        
        # 3. Language count
        features.append(len(user.languages))
        
        # 4. Budget range (normalized)
        if user.budget_range:
            features.append(user.budget_range[0] / 10000)
            features.append(user.budget_range[1] / 10000)
        else:
            features.extend([0.0, 0.0])
        
        # 5. Price range (normalized)
        if user.price_range:
            features.append(user.price_range[0] / 1000)
            features.append(user.price_range[1] / 1000)
        else:
            features.extend([0.0, 0.0])
        
        # 6. Rating (normalized)
        features.append(user.rating / 5.0)
        
        # 7. Verification (binary)
        features.append(1.0 if user.verification_status == 'verified' else 0.0)
        
        # 8. Transaction count (log-transformed)
        features.append(np.log1p(user.total_transactions) / 10.0)
        
        # 9. Product features (multi-hot)
        product_onehot = np.zeros(len(self.product_vocab))
        products = user.product_interests or user.product_offers or []
        for prod in products:
            prod_idx = self.product_vocab.get(prod)
            if prod_idx is not None:
                product_onehot[prod_idx] = 1.0
        features.extend(product_onehot.tolist())
        
        return np.array(features, dtype=np.float32)
    
    def initialize_model(self, num_users: int, num_products: int, num_countries: int):
        """Initialize the neural network model"""
        
        # Calculate feature dimension
        country_dim = num_countries
        product_dim = num_products
        base_features = 1 + country_dim + 1 + 2 + 2 + 1 + 1 + 1 + product_dim
        
        self.model = MatchingMLP(
            input_dim=base_features,
            embedding_dim=self.embedding_dim,
            hidden_dim=self.hidden_dim,
            num_layers=self.num_layers,
            dropout=self.dropout
        ).to(self.device)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        logger.info(f"Model initialized with {sum(p.numel() for p in self.model.parameters())} parameters")
    
    def train(
        self,
        users: List[UserProfile],
        interactions: List[Tuple[str, str, float]],
        epochs: int = 100,
        batch_size: int = 32
    ):
        """
        Train the matching model on user interactions
        """
        logger.info(f"Training on {len(interactions)} interactions...")
        
        # Build vocabularies
        self._build_vocabularies(users)
        
        # Initialize model
        self.initialize_model(
            num_users=len(self.user_vocab),
            num_products=len(self.product_vocab),
            num_countries=len(self.country_vocab)
        )
        
        # Create training data
        user_features = {}
        for user in users:
            if user.user_id in self.user_vocab:
                user_features[user.user_id] = self._create_user_features(user)
        
        # Training loop
        self.model.train()
        
        for epoch in range(epochs):
            total_loss = 0.0
            num_batches = 0
            
            # Shuffle interactions
            np.random.seed(42 + epoch)  # For reproducibility
            shuffled_interactions = interactions.copy()
            np.random.shuffle(shuffled_interactions)
            
            for i in range(0, len(shuffled_interactions), batch_size):
                batch = shuffled_interactions[i:i + batch_size]
                
                # Create batch tensors
                buyer_ids = []
                supplier_ids = []
                labels = []
                
                for buyer_id, supplier_id, label in batch:
                    if buyer_id in user_features and supplier_id in user_features:
                        buyer_ids.append(buyer_id)
                        supplier_ids.append(supplier_id)
                        labels.append(label)
                
                if not buyer_ids:
                    continue
                
                # Get features
                buyer_features = torch.tensor(
                    np.array([user_features[bid] for bid in buyer_ids]),
                    dtype=torch.float32
                ).to(self.device)
                
                supplier_features = torch.tensor(
                    np.array([user_features[sid] for sid in supplier_ids]),
                    dtype=torch.float32
                ).to(self.device)
                
                labels_tensor = torch.tensor(labels, dtype=torch.float32).to(self.device)
                
                # Forward pass
                self.optimizer.zero_grad()
                predictions = self.model(buyer_features, supplier_features)
                loss = F.binary_cross_entropy(predictions, labels_tensor)
                
                # Backward pass
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
                num_batches += 1
            
            avg_loss = total_loss / num_batches if num_batches > 0 else 0.0
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
        
        logger.info("Training completed!")
        self.model.eval()
    
    def find_matches(
        self,
        buyer: UserProfile,
        suppliers: List[UserProfile],
        top_k: int = 10
    ) -> List[MatchResult]:
        """
        Find best matching suppliers for a buyer
        """
        if self.model is None:
            logger.warning("Model not trained. Using fallback scoring.")
            return self._fallback_matching(buyer, suppliers, top_k)
        
        self.model.eval()
        
        # Create buyer features
        buyer_features = torch.tensor(
            self._create_user_features(buyer).reshape(1, -1),
            dtype=torch.float32
        ).to(self.device)
        
        results = []
        
        with torch.no_grad():
            for supplier in suppliers:
                # Create supplier features
                supplier_features = torch.tensor(
                    self._create_user_features(supplier).reshape(1, -1),
                    dtype=torch.float32
                ).to(self.device)
                
                # Get similarity score
                similarity = self.model(buyer_features, supplier_features).item()
                
                # Calculate detailed scores
                match_reasons = []
                
                # Product overlap
                buyer_products = set(buyer.product_interests or [])
                supplier_products = set(supplier.product_offers or [])
                product_overlap = len(buyer_products & supplier_products) / max(len(buyer_products), 1)
                
                if product_overlap > 0:
                    match_reasons.append(f"Product match ({product_overlap:.0%})")
                
                # Location score
                location_score = 1.0 if buyer.country == supplier.country else 0.5
                if buyer.country == supplier.country:
                    match_reasons.append("Same country")
                elif buyer.region == supplier.region:
                    match_reasons.append("Same region")
                
                # Trust score
                trust_score = supplier.rating / 5.0
                if supplier.verification_status == 'verified':
                    match_reasons.append("Verified supplier")
                    trust_score = min(1.0, trust_score + 0.2)
                
                # Price alignment
                price_alignment = 0.5
                if buyer.budget_range and supplier.price_range:
                    overlap_start = max(buyer.budget_range[0], supplier.price_range[0])
                    overlap_end = min(buyer.budget_range[1], supplier.price_range[1])
                    if overlap_start <= overlap_end:
                        overlap = overlap_end - overlap_start
                        range_size = min(
                            buyer.budget_range[1] - buyer.budget_range[0],
                            supplier.price_range[1] - supplier.price_range[0]
                        )
                        price_alignment = overlap / range_size if range_size > 0 else 0.5
                
                # Combine scores
                neural_score = similarity
                combined_score = (
                    0.4 * neural_score +
                    0.3 * product_overlap +
                    0.15 * location_score +
                    0.1 * trust_score +
                    0.05 * price_alignment
                )
                
                results.append(MatchResult(
                    supplier_id=supplier.user_id,
                    supplier_name=supplier.user_id,
                    similarity_score=combined_score,
                    match_reasons=match_reasons,
                    product_overlap=product_overlap,
                    location_score=location_score,
                    trust_score=trust_score,
                    price_alignment=price_alignment
                ))
        
        # Sort by similarity score and return top k
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
    
    def _fallback_matching(
        self,
        buyer: UserProfile,
        suppliers: List[UserProfile],
        top_k: int
    ) -> List[MatchResult]:
        """Fallback rule-based matching if model not trained"""
        results = []
        
        for supplier in suppliers:
            score = 0.0
            reasons = []
            
            # Product overlap
            buyer_prods = set(buyer.product_interests or [])
            supplier_prods = set(supplier.product_offers or [])
            overlap = len(buyer_prods & supplier_prods) / max(len(buyer_prods), 1)
            score += 0.4 * overlap
            if overlap > 0:
                reasons.append(f"Product match ({overlap:.0%})")
            
            # Location
            if buyer.country == supplier.country:
                score += 0.3
                reasons.append("Same country")
            
            # Trust
            score += 0.2 * (supplier.rating / 5.0)
            if supplier.verification_status == 'verified':
                reasons.append("Verified")
            
            # Price
            if buyer.budget_range and supplier.price_range:
                if (buyer.budget_range[0] <= supplier.price_range[1] and
                    buyer.budget_range[1] >= supplier.price_range[0]):
                    score += 0.1
                    reasons.append("Price in range")
            
            results.append(MatchResult(
                supplier_id=supplier.user_id,
                supplier_name=supplier.user_id,
                similarity_score=score,
                match_reasons=reasons,
                product_overlap=overlap,
                location_score=1.0 if buyer.country == supplier.country else 0.5,
                trust_score=supplier.rating / 5.0,
                price_alignment=0.5
            ))
        
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        if self.model is None:
            logger.warning("No model to save")
            return
        
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'user_vocab': self.user_vocab,
            'product_vocab': self.product_vocab,
            'country_vocab': self.country_vocab,
            'embedding_dim': self.embedding_dim,
            'hidden_dim': self.hidden_dim
        }, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        checkpoint = torch.load(path, map_location=self.device)
        
        self.user_vocab = checkpoint['user_vocab']
        self.product_vocab = checkpoint['product_vocab']
        self.country_vocab = checkpoint['country_vocab']
        self.embedding_dim = checkpoint['embedding_dim']
        self.hidden_dim = checkpoint['hidden_dim']
        
        self.initialize_model(
            num_users=len(self.user_vocab),
            num_products=len(self.product_vocab),
            num_countries=len(self.country_vocab)
        )
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.model.eval()
        
        logger.info(f"Model loaded from {path}")


class MatchingMLP(nn.Module):
    """
    Multi-Layer Perceptron for Buyer-Supplier Matching
    
    Architecture:
    - Dual embedding layers for buyer and supplier
    - Parallel MLP networks
    - Similarity computation (concatenation + MLP)
    - Binary classification output
    """
    
    def __init__(
        self,
        input_dim: int,
        embedding_dim: int = 64,
        hidden_dim: int = 128,
        num_layers: int = 2,
        dropout: float = 0.1
    ):
        super(MatchingMLP, self).__init__()
        
        # Embedding layers
        self.buyer_embedding = nn.Sequential(
            nn.Linear(input_dim, embedding_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        self.supplier_embedding = nn.Sequential(
            nn.Linear(input_dim, embedding_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )
        
        # Build MLP layers
        buyer_layers = []
        supplier_layers = []
        
        for i in range(num_layers):
            if i == 0:
                # First layer: embedding_dim -> hidden_dim
                buyer_layers.extend([
                    nn.Linear(embedding_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ])
                supplier_layers.extend([
                    nn.Linear(embedding_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ])
            else:
                # Subsequent layers: hidden_dim -> hidden_dim
                buyer_layers.extend([
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ])
                supplier_layers.extend([
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ])
        
        self.buyer_mlp = nn.Sequential(*buyer_layers)
        self.supplier_mlp = nn.Sequential(*supplier_layers)
        
        # Similarity computation
        self.similarity_mlp = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
            nn.Sigmoid()
        )
        
        self.dropout_layer = nn.Dropout(dropout)
    
    def forward(self, buyer_features: torch.Tensor, supplier_features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            buyer_features: [batch_size, input_dim]
            supplier_features: [batch_size, input_dim]
        
        Returns:
            match_probability: [batch_size]
        """
        # Embed users
        buyer_embed = self.buyer_embedding(buyer_features)
        supplier_embed = self.supplier_embedding(supplier_features)
        
        # Apply MLPs
        buyer_embed = self.buyer_mlp(buyer_embed)
        supplier_embed = self.supplier_mlp(supplier_embed)
        
        # Compute similarity
        combined = torch.cat([buyer_embed, supplier_embed], dim=1)
        match_score = self.similarity_mlp(combined)
        
        return match_score.squeeze()


class HybridMatchingEngine:
    """
    Hybrid Matching Engine combining:
    1. Neural Network Matching (ML-based)
    2. Rule-based Scoring (interpretable)
    """
    
    def __init__(self):
        self.neural_engine = NeuralMatchingEngine()
        self.is_trained = False
        
        logger.info("Hybrid Matching Engine initialized")
    
    def train(self, users: List[UserProfile], interactions: List[Tuple[str, str, float]]):
        """Train the hybrid engine"""
        logger.info("Training hybrid matching engine...")
        self.neural_engine.train(users, interactions, epochs=50)
        self.is_trained = True
        logger.info("Training complete!")
    
    def find_matches(
        self,
        buyer: UserProfile,
        suppliers: List[UserProfile],
        top_k: int = 10
    ) -> List[MatchResult]:
        """Find matches using hybrid approach"""
        
        if not self.is_trained:
            logger.info("Using rule-based matching (model not trained)")
            return self.neural_engine._fallback_matching(buyer, suppliers, top_k)
        
        # Use neural matching with enhanced scoring
        return self.neural_engine.find_matches(buyer, suppliers, top_k)
    
    def save(self, path: str):
        """Save hybrid engine"""
        if self.is_trained:
            self.neural_engine.save_model(path)
    
    def load(self, path: str):
        """Load hybrid engine"""
        try:
            self.neural_engine.load_model(path)
            self.is_trained = True
        except:
            logger.warning("Could not load model")


if __name__ == "__main__":
    print("="*70)
    print("NEURAL MATCHING ENGINE - TEST")
    print("="*70)
    
    # Create sample users
    print("\n📊 Creating sample users...")
    
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
        )
    ]
    
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
        )
    ]
    
    # Create sample interactions
    print("\n🤝 Creating sample interactions...")
    interactions = [
        ("buyer_001", "supplier_001", 1.0),  # Positive
        ("buyer_001", "supplier_002", 0.8),  # Positive
        ("buyer_001", "supplier_003", 0.5),  # Weak
        ("buyer_002", "supplier_003", 1.0),  # Positive
        ("buyer_002", "supplier_002", 0.6),  # Moderate
    ]
    
    # Initialize engine
    print("\n🚀 Initializing Neural Matching Engine...")
    engine = NeuralMatchingEngine(embedding_dim=32, hidden_dim=64, num_layers=2)
    
    # Train model
    print("\n📚 Training model...")
    all_users = buyers + suppliers
    engine.train(all_users, interactions, epochs=20)
    
    # Test matching
    print("\n🎯 Testing matching...")
    test_buyer = buyers[0]
    matches = engine.find_matches(test_buyer, suppliers, top_k=3)
    
    print(f"\n📋 Top matches for {test_buyer.user_id}:")
    for i, match in enumerate(matches, 1):
        print(f"\n   Match {i}:")
        print(f"     Supplier: {match.supplier_id}")
        print(f"     Score: {match.similarity_score:.2%}")
        print(f"     Reasons: {', '.join(match.match_reasons)}")
        print(f"     Product Overlap: {match.product_overlap:.2%}")
        print(f"     Trust Score: {match.trust_score:.2f}")
    
    # Test hybrid engine
    print("\n" + "="*70)
    print("Testing Hybrid Engine...")
    print("="*70)
    
    hybrid = HybridMatchingEngine()
    hybrid.train(all_users, interactions)
    
    matches = hybrid.find_matches(test_buyer, suppliers)
    
    print(f"\n📋 Hybrid matches for {test_buyer.user_id}:")
    for i, match in enumerate(matches[:3], 1):
        print(f"\n   {i}. {match.supplier_id} - Score: {match.similarity_score:.2%}")
        print(f"      Reasons: {', '.join(match.match_reasons)}")
    
    print("\n" + "="*70)
    print("✅ NEURAL MATCHING ENGINE TEST COMPLETE!")
    print("="*70)
