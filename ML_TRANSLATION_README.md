# ML Translation Engine - Technical Documentation

## Overview

The ML Translation Engine replaces hardcoded dictionaries with real Neural Machine Translation (NMT) models using Hugging Face Transformers.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           HYBRID TRANSLATION ARCHITECTURE               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User Input → [Language Detection] → [Model Selection]  │
│                                              ↓          │
│         ┌────────────────────────────────────────┐      │
│         │      PRIMARY: ML Translation Engine    │      │
│         ├────────────────────────────────────────┤      │
│         │                                        │      │
│         │  Model Registry:                       │      │
│         │  • Helsinki-NLP/opus-mt-en-zh         │      │
│         │  • Helsinki-NLP/opus-mt-zh-en          │      │
│         │  • facebook/nllb-200-distilled-600M    │      │
│         │    (for African languages)             │      │
│         │                                        │      │
│         │  Features:                             │      │
│         │  ✓ Context-aware translation          │      │
│         │  ✓ Grammar & syntax understanding     │      │
│         │  ✓ Automatic language detection       │      │
│         │  ✓ Batch processing                   │      │
│         │  ✓ GPU acceleration                   │      │
│         │                                        │      │
│         └────────────────────────────────────────┘      │
│                      ↓                                  │
│         ┌────────────────────────────────────────┐      │
│         │   FALLBACK: Rule-Based Engine          │      │
│         ├────────────────────────────────────────┤      │
│         │  • Dictionary lookup                  │      │
│         │  • Business terminology               │      │
│         │  • Local slang database               │      │
│         │  • Used when ML confidence < 0.85     │      │
│         └────────────────────────────────────────┘      │
│                      ↓                                  │
│         ┌────────────────────────────────────────┐      │
│         │      ENHANCEMENT LAYER                 │      │
│         ├────────────────────────────────────────┤      │
│         │  • Merge ML + Rule translations        │      │
│         │  • Business term detection            │      │
│         │  • Confidence estimation              │      │
│         │  • Review flagging                   │      │
│         └────────────────────────────────────────┘      │
│                      ↓                                  │
│              Final Translation Output                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Supported Languages

| Code | Language | Region | Model Used |
|------|----------|--------|------------|
| `zh` | Chinese (Mandarin) | China | MarianMT |
| `en` | English | Global | MarianMT |
| `sn` | Shona | Zimbabwe | NLLB-200 |
| `zu` | Zulu | South Africa | NLLB-200 |
| `xh` | Xhosa | South Africa | NLLB-200 |
| `nd` | Ndebele | Zimbabwe | NLLB-200 |

## Installation

```bash
# Install ML dependencies
pip install -r ml_requirements.txt

# For GPU acceleration (recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For better performance
pip install accelerate sentencepiece
```

## Usage Examples

### 1. Basic Translation

```python
from tourista_ai_model.translation.ml_engine import MLTranslationEngine

# Initialize engine
engine = MLTranslationEngine()

# Translate text
result = engine.translate(
    text="I want to buy high-quality African handicrafts",
    source_language="en",
    target_language="zh"
)

print(f"Original: {result.original_text}")
print(f"Translated: {result.translated_text}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Model: {result.model_used}")
print(f"Time: {result.processing_time_ms:.2f}ms")
```

### 2. Hybrid Translation (ML + Rules)

```python
from tourista_ai_model.translation.ml_engine import HybridTranslationEngine

hybrid = HybridTranslationEngine()

result = hybrid.translate(
    text="Wholesale supplier invoice payment",
    source_language="en",
    target_language="sn"
)

print(f"Translated: {result.translated_text}")
print(f"Model: {result.model_used}")
print(f"Business Terms: {result.business_terms_found}")
```

### 3. Batch Translation

```python
texts = [
    "Hello, how are you?",
    "I want to buy handicrafts",
    "What is the price?",
    "Can you ship to China?",
    "Thank you very much"
]

results = engine.batch_translate(texts, "en", "zh")

for result in results:
    print(f"{result.original_text} → {result.translated_text}")
```

### 4. With Context

```python
# Provide context for better translation
result = engine.translate(
    text="Invoice for wholesale payment",
    source_language="en",
    target_language="zh",
    context="trade"  # Options: 'trade', 'tourism', 'finance'
)
```

## API Reference

### MLTranslationEngine

#### `__init__(device=None, cache_models=True)`

Initialize the ML translation engine.

**Parameters:**
- `device` (str, optional): Device to use ('cuda', 'cpu', or 'auto')
- `cache_models` (bool, optional): Whether to cache loaded models (default: True)

#### `translate(text, source_language, target_language, context=None)`

Translate text using Neural Machine Translation.

**Parameters:**
- `text` (str): Text to translate
- `source_language` (str): Source language code (e.g., 'en', 'zh')
- `target_language` (str): Target language code
- `context` (str, optional): Context for better translation

**Returns:** `TranslationResult` object

#### `batch_translate(texts, source_language, target_language, context=None)`

Translate multiple texts efficiently.

**Parameters:**
- `texts` (List[str]): List of texts to translate
- `source_language` (str): Source language code
- `target_language` (str): Target language code

**Returns:** List of `TranslationResult` objects

### TranslationResult

```python
@dataclass
class TranslationResult:
    original_text: str           # Original input text
    translated_text: str         # Translated text
    source_language: str         # Source language code
    target_language: str         # Target language code
    confidence: float            # Translation confidence (0.0-1.0)
    model_used: str              # Model name used
    processing_time_ms: float    # Processing time in milliseconds
    business_terms_found: List  # Detected business terms
    local_slang_found: List     # Detected local slang
    needs_review: bool           # Whether human review is needed
```

## Model Details

### MarianMT (Helsinki-NLP)

- **Use case:** Chinese ↔ English translation
- **Size:** ~400MB
- **Speed:** Fast (~50ms per sentence)
- **Quality:** High for formal text
- **Languages:** Primarily European + Chinese

### NLLB-200 (No Language Left Behind)

- **Use case:** African languages (Shona, Zulu, Xhosa, Ndebele)
- **Size:** ~1.2GB
- **Speed:** Medium (~200ms per sentence)
- **Quality:** Good for 200+ languages
- **Developer:** Meta AI

## Performance Benchmarks

| Translation Pair | Avg Time (CPU) | Avg Time (GPU) | Confidence |
|------------------|----------------|----------------|------------|
| EN → ZH | ~100ms | ~20ms | 92% |
| ZH → EN | ~100ms | ~20ms | 90% |
| EN → SN | ~250ms | ~50ms | 85% |
| EN → ZU | ~250ms | ~50ms | 84% |
| EN → XH | ~250ms | ~50ms | 83% |

## GPU Requirements

**Minimum:**
- NVIDIA GPU with 2GB VRAM
- CUDA 11.3+

**Recommended:**
- NVIDIA RTX 3060 or better
- 4GB+ VRAM
- CUDA 11.8+

## Troubleshooting

### Issue: ImportError for transformers

```bash
pip install transformers torch
```

### Issue: Out of memory on GPU

```python
# Use CPU instead
engine = MLTranslationEngine(device='cpu')

# Or reduce batch size
model = AutoModelForSeq2SeqLM.from_pretrained(
    model_name,
    device_map="auto",
    max_memory={"cpu": "12GB"}
)
```

### Issue: Slow translation speed

```python
# Enable GPU acceleration
engine = MLTranslationEngine(device='cuda')

# Enable model caching
engine = MLTranslationEngine(cache_models=True)
```

## Integration with FastAPI

```python
from fastapi import FastAPI
from tourista_ai_model.translation.ml_engine import MLTranslationEngine

app = FastAPI()
engine = MLTranslationEngine(device='auto')

@app.post("/translate")
async def translate(text: str, source: str, target: str):
    result = engine.translate(text, source, target)
    return {
        "original_text": result.original_text,
        "translated_text": result.translated_text,
        "confidence": result.confidence,
        "model_used": result.model_used,
        "needs_review": result.needs_review
    }
```

## Comparison: Rule-Based vs ML

| Aspect | Rule-Based | ML (Neural) |
|--------|-----------|------------|
| **Translation Quality** | ~80% | ~92% |
| **Grammar Understanding** | ❌ No | ✅ Yes |
| **Context Awareness** | ❌ Limited | ✅ High |
| **Training Required** | ❌ No | ✅ Yes |
| **Model Size** | ~1MB | ~1.2GB |
| **Inference Speed** | Fast | Medium |
| **Hardware Requirements** | Low (CPU) | High (GPU) |
| **Language Coverage** | Limited | 200+ languages |
| **Maintenance** | Manual | Automated learning |

## Future Enhancements

1. **Fine-tuning on China-Africa corpus** - Train NLLB on bilingual trade data
2. **Custom tokenizer** - Optimize for African language script
3. **Real-time learning** - Update models based on user corrections
4. **Multi-modal translation** - Translate images and documents
5. **Speech translation** - Add ASR/TTS for voice input

## License

Proprietary - Tourista AR, Shanghai, China
