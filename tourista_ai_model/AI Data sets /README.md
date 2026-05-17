# AI Datasets for Tourista AR Model

This directory contains the training and reference datasets for the Tourista AR Proprietary AI Model.

## Dataset Files

### 1. Translation Data (For AI Multilingual)
**File:** `Translation Data (For AI Multil.csv`

**Purpose:** Multi-language translation training data
- Chinese ↔ English translations
- Local African language translations (Shona, Ndebele, Zulu, Xhosa)
- Scene categorization (trade, travel, payment)

**Columns:**
- Column A: Chinese text
- Column B: English text
- Column C: Local African Language
- Column D: Scene type

**Current Size:** 5 translation pairs
**Target Size:** 200+ pairs recommended

---

### 2. Buyer–Supplier Matching Data
**File:** `Buyer–Supplier Matching Data (F.csv`

**Purpose:** Buyer-supplier matching algorithm training
- Buyer needs in Chinese and English
- Supplier products and services
- Geographic and categorical data

**Columns:**
- Column A: Buyer Need (Chinese)
- Column B: Buyer Need (English)
- Column C: Supplier Product/Service
- Column D: Country
- Column E: Category

**Current Size:** 3 entries
**Target Size:** 100+ entries recommended

---

### 3. Cash Payment & Unbanked User Data
**File:** `Cash Payment & Unbanked User Da.csv`

**Purpose:** Risk analysis for cash-based and mobile money payments
- User behavior patterns
- Risk level assessment
- Mitigation recommendations

**Columns:**
- Column A: User Behavior
- Column B: Risk Level
- Column C: Suggestion

**Current Size:** 2 risk profiles
**Target Size:** 100+ profiles recommended

---

### 4. Cross-Border Trade Rules
**File:** `Cross‑Border Trade Rules (For A.csv`

**Purpose:** Trade compliance and logistics knowledge base
- Customs procedures
- Documentation requirements
- Regional trade regulations

**Columns:**
- Column A: Question
- Column B: Answer
- Column C: Country

**Current Size:** 3 Q&A pairs
**Target Size:** 50+ Q&A pairs recommended

---

### 5. FAQ Data (For AI Customer Service)
**File:** `FAQ Data (For AI Customer Servi.csv`

**Purpose:** Customer service chatbot training
- Common user questions
- AI-generated answers
- Support topics

**Columns:**
- Column A: User Question
- Column B: AI Answer

**Current Size:** 3 Q&A pairs
**Target Size:** 100+ Q&A pairs recommended

---

### 6. Travel & Tourism Data
**File:** `Travel & Tourism Data (For AI R.csv` / `.xlsx`

**Purpose:** Tourism recommendations and AR experiences
- Destinations and attractions
- Pricing information
- Geographic coverage

**Columns:**
- Column A: City
- Column B: Country
- Column C: Attraction/Service
- Column D: Description
- Column E: Price Range

**Current Size:** 3 destinations
**Target Size:** 200+ destinations recommended

---

## Loading Datasets

Use the `data_loader.py` module to load datasets:

```python
from tourista_ai_model.data_loader import DataLoader

loader = DataLoader()

translation_data = loader.get_translation_data()
matching_data = loader.get_matching_data()
risk_data = loader.get_risk_data()
trade_rules = loader.get_trade_rules_data()
faq_data = loader.get_faq_data()
tourism_data = loader.get_tourism_data()
```

## Dataset Integration

The datasets are automatically loaded when initializing the model:

```python
from tourista_ai_model.data_loader import integrate_datasets_with_model
from tourista_ai_model import MODEL

integrated_data = integrate_datasets_with_model(MODEL)
```

## Data Format Requirements

### CSV Files
- UTF-8 encoding
- First row as header
- Comma delimiter
- No special characters in filenames

### Excel Files (.xlsx)
- Requires `openpyxl` library
- First row as header
- Standard Excel format

## Maintenance

To add new data:
1. Edit CSV files directly
2. Maintain column structure
3. Keep UTF-8 encoding
4. Test with data_loader.py

## Support

For dataset questions: support@tourista-ar.ai

---

**Copyright © 2024 Tourista AR. All rights reserved.**
**Proprietary Intellectual Property**
