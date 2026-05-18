# Tourista AR ML-Powered System

## Overview

The Tourista AR AI Model has been upgraded from rule-based expert systems to **true machine learning-powered intelligent systems**.

## ML Engines Implemented

### 1. Neural Matching Engine (PyTorch)
**File:** `tourista_ai_model/matching/neural_engine.py`

**Architecture:**
- Embedding layer: 64-dimensional user/item embeddings
- Neural network: 2 hidden layers (128 units each)
- Activation: ReLU with dropout (0.1)
- Optimizer: Adam
- Loss function: Binary cross-entropy

**Features:**
- Collaborative filtering using neural networks
- User and item embeddings
- Fallback to rule-based when no training data
- Model persistence (save/load)
- Hybrid matching engine available

**Test:** `test_neural_matching.py`

---

### 2. ML Recommendation Engine (PyTorch)
**File:** `tourista_ai_model/recommendation/ml_engine.py`

**Architecture:**
- Neural Collaborative Filtering (NCF)
- User/item embeddings (64 dimensions)
- MLP layers (2-3 hidden layers, 64-128 units)
- Sigmoid output for rating prediction

**Features:**
- Personalized recommendations based on user behavior
- Collaborative filtering
- Content-based recommendations
- Seasonal trend analysis
- Market opportunity analysis
- Fallback mode

**Test:** `test_ml_recommendation.py`

---

### 3. ML Translation Engine (Hugging Face)
**File:** `tourista_ai_model/translation/ml_engine.py`

**Architecture:**
- MarianMT models from Hugging Face
- Fallback to NLLB-200 models
- Language pairs: zh-en, en-zh, en-sn, en-zu, etc.

**Features:**
- Multi-language support (6 languages)
- Business terminology database
- Translation confidence scoring
- Hybrid mode (rule-based + ML)

**Test:** `test_ml_translation.py`

---

## API Endpoints

### Base URL: `http://localhost:8000`

### System Endpoints
- `GET /` - API info
- `GET /health` - Health check
- `GET /info` - System information

### Translation Endpoints
- `POST /translate` - Single translation
- `POST /translate/batch` - Batch translation
- `GET /supported/languages` - List supported languages

### Matching Endpoints
- `POST /users/register` - Register user
- `POST /products/register` - Register product
- `POST /matching/find` - Find matches

### Recommendation Endpoints
- `POST /recommendations` - Get personalized recommendations
- `GET /trade/insights/{category}` - Market insights
- `GET /seasonal/pricing/{category}` - Seasonal pricing
- `GET /market/opportunity/{category}/{country}` - Market analysis

### Risk Analysis
- `POST /risk/assess` - Assess transaction risk
- `POST /payment/recommend` - Payment recommendations

### AR Endpoints
- `POST /ar/recognize` - Recognize scene
- `GET /ar/product/{product_id}` - Product preview
- `GET /ar/tourism/{spot_id}` - Tourism experience

---

## Training & Usage

### Neural Matching Engine

```python
from tourista_ai_model.matching import NeuralMatchingEngine

# Initialize
engine = NeuralMatchingEngine(embedding_dim=64, hidden_dim=128)

# Train with user interactions
users = [...]  # User profile data
interactions = [...]  # (buyer_id, supplier_id, rating) tuples
engine.train(users, interactions, epochs=100)

# Find matches
matches = engine.find_matches(buyer_profile, suppliers, top_k=10)

# Save/load model
engine.save_model('matching_model.pt')
engine.load_model('matching_model.pt')
```

### ML Recommendation Engine

```python
from tourista_ai_model.recommendation import MLRecommendationEngine

# Initialize
engine = MLRecommendationEngine()

# Train
users = [...]
items = [...]  # Products, suppliers, etc.
interactions = [...]  # (user_id, item_id, rating)
engine.train(users, items, interactions, epochs=100)

# Get recommendations
recs = engine.generate_recommendations(user_id, user_type)

# Market analysis
pricing = engine.get_seasonal_pricing("coffee")
opportunity = engine.analyze_market_opportunity("coffee", "zimbabwe")
```

### ML Translation Engine

```python
from tourista_ai_model.translation import MLTranslationEngine

# Initialize
engine = MLTranslationEngine()

# Translate
result = engine.translate("Hello", "en", "zh")
print(result.translated_text)
print(f"Confidence: {result.confidence}")
```

---

## Running the API

```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the server
python3 -m uvicorn tourista_ai_model.api.endpoints:app --host 0.0.0.0 --port 8000

# Access docs
open http://localhost:8000/docs
```

---

## Project Files Summary

### Core ML Files
- `tourista_ai_model/matching/neural_engine.py` - Neural matching engine
- `tourista_ai_model/recommendation/ml_engine.py` - ML recommendation engine  
- `tourista_ai_model/translation/ml_engine.py` - ML translation engine

### Test Files
- `test_neural_matching.py` - Matching engine tests
- `test_ml_recommendation.py` - Recommendation engine tests
- `test_ml_translation.py` - Translation engine tests

### Configuration Files
- `requirements.txt` - Core dependencies
- `ml_requirements.txt` - ML-specific dependencies
- `neural_matching_requirements.txt` - Matching engine requirements

---

## Architecture Comparison

| Feature | Before (Rule-Based) | After (ML-Powered) |
|---------|----------------------|---------------------|
| Translation | Dictionary lookups | MarianMT/NLLB models |
| Matching | Static scoring rules | Neural collaborative filtering |
| Recommendations | Pre-written | Learned user behavior patterns |
| Learning | No | Yes, trains on interactions |
| Personalization | Limited | High |
| Scalability | Limited | High, can learn patterns |

---

## System Components

```
Tourista AR ML System
├── API Layer (FastAPI)
├── ML Engines
│   ├── Neural Matching Engine (PyTorch)
│   ├── ML Recommendation Engine (PyTorch)
│   └── ML Translation Engine (Hugging Face)
└── Fallback Engines (Rule-Based)
```

---

## Next Steps

1. **Data Collection** - Gather real user interaction data for training
2. **Model Fine-tuning** - Optimize hyperparameters based on real data
3. **A/B Testing** - Compare ML vs rule-based recommendations
4. **Monitoring** - Track model performance and drift
5. **Deployment** - Deploy to cloud with proper scaling

---

## Credits

- Tourista AR - Shanghai, China
- PyTorch for neural networks
- Hugging Face for transformers
- FastAPI for API layer
