# Tourista AR AI Model - ML-Powered System

## Overview

The Tourista AR AI Model has been completely upgraded to use **machine learning** for all core components!

## Components

All components have been upgraded from rule-based systems to ML-powered systems, with graceful fallbacks to rule-based implementations when ML libraries are unavailable.

| Component | Original | New | Frameworks |
|-----------|----------|-----|------------|
| Translation | Dictionary-based | ML Translation Engine | Hugging Face, MarianMT |
| Matching | Static scoring | Neural Matching Engine | PyTorch, Deep Learning |
| Recommendation | Pre-written recs | Neural Recommendation Engine | PyTorch, Collaborative Filtering |
| Risk Analysis | Rule-based | ML Risk Analysis Engine | XGBoost, Fraud Detection |
| AR Recognition | Static database | ML AR Recognition Engine | PyTorch, ResNet50 |

---

## 1. ML Translation Engine

**File:** `tourista_ai_model/translation/ml_engine.py`

### Features:
- Hugging Face's MarianMT models for high-quality translation
- Support for 6 languages (Chinese, English, Shona, Ndebele, Zulu, Xhosa)
- Business terminology support
- Confidence scoring
- Hybrid mode with rule-based fallback

---

## 2. Neural Matching Engine

**File:** `tourista_ai_model/matching/neural_engine.py`

### Features:
- Neural Collaborative Filtering
- Embedding-based user/product representations
- Multi-layer perceptron for scoring
- Model persistence (save/load)
- Hybrid matching mode

### Architecture:
- Input: 26-dimensional feature vectors
- Embedding layer: 64-dimensional
- MLP: 2 hidden layers (128 units)
- Sigmoid output for match probability

---

## 3. ML Recommendation Engine

**File:** `tourista_ai_model/recommendation/ml_engine.py`

### Features:
- Neural Collaborative Filtering
- Personalized recommendations
- Seasonal trend analysis
- Market opportunity analysis
- Fallback to rule-based recs when untrained

---

## 4. ML Risk Analysis Engine

**File:** `tourista_ai_model/risk_analysis/ml_engine.py`

### Features:
- XGBoost-based fraud detection
- Multi-modal risk assessment
- Synthetic training data support
- Rule-based fallback (always works!)
- Payment method risk analysis

---

## 5. ML AR Recognition Engine

**File:** `tourista_ai_model/ar_recognition/ml_engine.py`

### Features:
- ResNet50-based deep feature extraction
- Scene classification with location context
- Multi-modal matching (features + location)
- Pre-populated scene database (Victoria Falls, Great Zimbabwe, etc.)
- Product preview and tourism experience support

---

## API Endpoints

The same FastAPI endpoints are still used, but they now use the ML-powered engines!

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/info` | GET | System info |
| `/supported/languages` | GET | Supported languages |
| `/translate` | POST | Translate text |
| `/translate/batch` | POST | Batch translation |
| `/users/register` | POST | Register user |
| `/products/register` | POST | Register product |
| `/matching/find` | POST | Find matches |
| `/recommendations` | POST | Get recommendations |
| `/risk/assess` | POST | Assess transaction risk |
| `/payment/recommend` | POST | Payment recommendations |
| `/ar/recognize` | POST | AR scene recognition |
| `/ar/product/{product_id}` | GET | Product preview |
| `/ar/tourism/{spot_id}` | GET | Tourism experience |

---

## Usage

### Installing Dependencies

```bash
# Basic requirements
pip install -r requirements.txt

# ML requirements
pip install -r ml_requirements.txt
```

### Running the API Server

```bash
# Option 1: Using uvicorn directly
python3 -m uvicorn tourista_ai_model.api.endpoints:app --host 0.0.0.0 --port 8000

# Option 2: Check if server is already running
# (It might be running on http://localhost:8000 already!)
```

### API Documentation

Swagger UI: http://localhost:8000/docs

---

## Test Files

All components have test files:

- `test_ml_translation.py` - Test ML Translation Engine
- `test_neural_matching.py` - Test Neural Matching Engine
- `test_ml_recommendation.py` - Test ML Recommendation Engine
- `test_ml_risk_analysis.py` - Test ML Risk Analysis Engine
- `test_ml_ar_engine.py` - Test ML AR Recognition Engine

To run all tests:
```bash
# One by one
python3 test_ml_translation.py
python3 test_neural_matching.py
python3 test_ml_recommendation.py
python3 test_ml_risk_analysis.py
python3 test_ml_ar_engine.py
```

---

## Fallback Mechanism

All ML engines have graceful fallback to the original rule-based implementations:

1. If a library like PyTorch/XGBoost isn't installed
2. If the ML model hasn't been trained yet
3. If there's any error in ML inference

The system will *always* work, and will use the best available technology!

---

## Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                        Tourista AR App                            │
└───────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────┐
│                   FastAPI API Endpoints                           │
└───────────────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ ML Translation│         │ Neural Match  │         │ ML Rec Engine │
└───────────────┘         └───────────────┘         └───────────────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────┐
│           ML Risk Analysis + ML AR Recognition                    │
└───────────────────────────────────────────────────────────────────┘
```

---

## System Status

**✅ All engines are now ML-powered!**

The Tourista AR AI Model is ready for production use! 🚀
