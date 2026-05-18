"""
ML-Powered Translation Engine for Tourista AR
Uses Hugging Face Transformers for Neural Machine Translation

Supports:
- Chinese (Mandarin)
- English
- Shona (Zimbabwe)
- Zulu (South Africa)
- Xhosa (South Africa)
- Ndebele (Zimbabwe)
"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline,
    MarianMTModel,
    MarianTokenizer
)
import torch
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import warnings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

warnings.filterwarnings('ignore')


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    model_used: str
    processing_time_ms: float
    business_terms_found: List[str]
    local_slang_found: List[str]
    needs_review: bool


class MLTranslationEngine:
    """
    Neural Machine Translation Engine using Hugging Face Transformers
    Supports Chinese, English, and African languages (Shona, Zulu, Xhosa, Ndebele)
    """
    
    SUPPORTED_LANGUAGES = {
        'zh': 'Chinese (Mandarin)',
        'en': 'English',
        'sn': 'Shona (Zimbabwe)',
        'zu': 'Zulu (South Africa)',
        'xh': 'Xhosa (South Africa)',
        'nd': 'Ndebele (Zimbabwe)'
    }
    
    MODEL_REGISTRY = {
        ('en', 'zh'): 'Helsinki-NLP/opus-mt-en-zh',
        ('zh', 'en'): 'Helsinki-NLP/opus-mt-zh-en',
        ('en', 'sn'): 'facebook/nllb-200-distilled-600M',
        ('sn', 'en'): 'facebook/nllb-200-distilled-600M',
        ('en', 'zu'): 'facebook/nllb-200-distilled-600M',
        ('zu', 'en'): 'facebook/nllb-200-distilled-600M',
        ('en', 'xh'): 'facebook/nllb-200-distilled-600M',
        ('xh', 'en'): 'facebook/nllb-200-distilled-600M',
        ('en', 'nd'): 'facebook/nllb-200-distilled-600M',
        ('nd', 'en'): 'facebook/nllb-200-distilled-600M',
        ('zh', 'sn'): 'facebook/nllb-200-distilled-600M',
        ('sn', 'zh'): 'facebook/nllb-200-distilled-600M',
        ('zh', 'zu'): 'facebook/nllb-200-distilled-600M',
        ('zu', 'zh'): 'facebook/nllb-200-distilled-600M',
    }
    
    def __init__(self, device: Optional[str] = None, cache_models: bool = True):
        """
        Initialize ML Translation Engine
        
        Args:
            device: 'cuda', 'cpu', or 'auto' (default: auto-detect)
            cache_models: Whether to cache loaded models in memory
        """
        self.device = self._get_device(device)
        self.cache_models = cache_models
        self.model_cache: Dict[str, Tuple[Any, Any]] = {}
        self.business_terms_db = self._load_business_terms()
        self.slang_db = self._load_slang_database()
        
        logger.info(f"ML Translation Engine initialized on device: {self.device}")
        logger.info(f"Supported languages: {', '.join(self.SUPPORTED_LANGUAGES.values())}")
    
    def _get_device(self, device: Optional[str]) -> str:
        """Auto-detect best device"""
        if device:
            return device
        if torch.cuda.is_available():
            return 'cuda'
        return 'cpu'
    
    def _load_business_terms(self) -> Dict[str, Dict[str, str]]:
        """Load business terminology database"""
        return {
            'handicrafts': {
                'zh': '手工艺品', 'sn': 'zvigadzi', 'zu': 'izincwadi',
                'xh': 'izinto zokusebenza', 'en': 'handicrafts'
            },
            'payment': {
                'zh': '付款', 'sn': 'mutengo', 'zu': 'imali',
                'xh': 'imali', 'en': 'payment'
            },
            'invoice': {
                'zh': '发票', 'sn': 'chit-chip', 'zu': 'invoice',
                'xh': 'invoice', 'en': 'invoice'
            },
            'supplier': {
                'zh': '供应商', 'sn': 'mutengesi', 'zu': 'umthengisi',
                'xh': 'umthengisi', 'en': 'supplier'
            },
            'buyer': {
                'zh': '买家', 'sn': 'mugadziri', 'zu': 'umthengi',
                'xh': 'umthengi', 'en': 'buyer'
            },
            'shipping': {
                'zh': '运输', 'sn': 'kutumira', 'zu': 'ukuthumela',
                'xh': 'ukuthumela', 'en': 'shipping'
            },
            'customs': {
                'zh': '海关', 'sn': 'customs', 'zu': 'customs',
                'xh': 'customs', 'en': 'customs'
            },
            'negotiate': {
                'zh': '谈判', 'sn': 'kushungurudza', 'zu': 'ukuxoxisana',
                'xh': 'ukuxoxisana', 'en': 'negotiate'
            },
            'wholesale': {
                'zh': '批发', 'sn': 'hugele', 'zu': 'ngokumisi',
                'xh': 'ngokumisi', 'en': 'wholesale'
            },
            'retail': {
                'zh': '零售', 'sn': 'retail', 'zu': 'retail',
                'xh': 'retail', 'en': 'retail'
            },
            'currency': {
                'zh': '货币', 'sn': 'mari', 'zu': 'imali',
                'xh': 'imali', 'en': 'currency'
            },
            'USD': {
                'zh': '美元', 'sn': 'USD', 'zu': 'USD',
                'xh': 'USD', 'en': 'USD'
            },
            'CNY': {
                'zh': '人民币', 'sn': 'CNY', 'zu': 'CNY',
                'xh': 'CNY', 'en': 'CNY'
            }
        }
    
    def _load_slang_database(self) -> Dict[str, Dict[str, str]]:
        """Load local slang and colloquial expressions"""
        return {
            'boss': {'sn': 'baba', 'zu': 'bhala', 'xh': 'bhuti', 'en': 'boss'},
            'expensive': {'sn': 'hureba', 'zu': 'mukolu', 'xh': 'buyiselo', 'en': 'expensive'},
            'cheap': {'sn': 'ranga', 'zu': 'ng含猛', 'xh': 'rhweletswa', 'en': 'cheap'},
            'money': {'sn': 'mari', 'zu': 'imali', 'xh': 'imali', 'en': 'money'},
            'today': {'sn': 'nhasi', 'zu': 'namuhla', 'xh': 'namhlanje', 'en': 'today'},
            'tomorrow': {'sn': 'mere', 'zu': 'kusasa', 'xh': 'ngomso', 'en': 'tomorrow'},
            'okay': {'sn': 'ndawonye', 'zu': 'kuyaph', 'xh': 'kuyanye', 'en': 'okay'},
        }
    
    def _get_model(self, source_lang: str, target_lang: str) -> Tuple[Any, Any]:
        """Load and cache translation model"""
        model_key = f"{source_lang}-{target_lang}"
        
        if model_key in self.model_cache:
            return self.model_cache[model_key]
        
        if (source_lang, target_lang) in self.MODEL_REGISTRY:
            model_name = self.MODEL_REGISTRY[(source_lang, target_lang)]
        else:
            model_name = self.MODEL_REGISTRY.get((target_lang, source_lang))
            if model_name and model_name == 'facebook/nllb-200-distilled-600M':
                model_key_temp = f"{target_lang}-{source_lang}"
                if model_key_temp in self.model_cache:
                    base_model, base_tokenizer = self.model_cache[model_key_temp]
                    logger.info(f"Using reversed model for {model_key}")
                    if self.cache_models:
                        self.model_cache[model_key] = (base_model, base_tokenizer)
                    return base_model, base_tokenizer
            
            logger.warning(f"No dedicated model for {model_key}, using NLLB-200")
            model_name = 'facebook/nllb-200-distilled-600M'
        
        logger.info(f"Loading model: {model_name} for {model_key}")
        
        try:
            if 'nllb' in model_name.lower():
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            else:
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
            
            model = model.to(self.device)
            model.eval()
            
            if self.cache_models:
                self.model_cache[model_key] = (model, tokenizer)
            
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            raise
    
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        context: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate text using Neural Machine Translation
        
        Args:
            text: Text to translate
            source_language: Source language code (zh, en, sn, zu, xh, nd)
            target_language: Target language code
            context: Optional context ('trade', 'tourism', 'finance')
        
        Returns:
            TranslationResult with translation and metadata
        """
        import time
        start_time = time.time()
        
        if source_language == target_language:
            return TranslationResult(
                original_text=text,
                translated_text=text,
                source_language=source_language,
                target_language=target_language,
                confidence=1.0,
                model_used="identity",
                processing_time_ms=0.0,
                business_terms_found=[],
                local_slang_found=[],
                needs_review=False
            )
        
        try:
            model, tokenizer = self._get_model(source_language, target_language)
            
            lang_code = self._get_nllb_code(target_language) if 'nllb' in str(type(model)).lower() else target_language
            
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            if 'nllb' in str(type(model)).lower():
                inputs['forced_bos_token_id'] = tokenizer.lang_code_to_id[lang_code]
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
            
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            confidence = self._estimate_confidence(text, translated_text)
            
            business_terms = self._detect_business_terms(text)
            slang_terms = self._detect_slang(text, source_language)
            
            needs_review = confidence < 0.8 or len(slang_terms) > 0
            
            processing_time = (time.time() - start_time) * 1000
            
            return TranslationResult(
                original_text=text,
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language,
                confidence=confidence,
                model_used=str(type(model).__name__),
                processing_time_ms=processing_time,
                business_terms_found=business_terms,
                local_slang_found=slang_terms,
                needs_review=needs_review
            )
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=f"[Translation failed: {str(e)}]",
                source_language=source_language,
                target_language=target_language,
                confidence=0.0,
                model_used="error",
                processing_time_ms=(time.time() - start_time) * 1000,
                business_terms_found=[],
                local_slang_found=[],
                needs_review=True
            )
    
    def _get_nllb_code(self, lang_code: str) -> str:
        """Map language code to NLLB format"""
        nllb_codes = {
            'zh': 'eng_Latn',
            'en': 'eng_Latn',
            'sn': 'sna_Latn',
            'zu': 'zul_Latn',
            'xh': 'xho_Latn',
            'nd': 'nbl_Latn'
        }
        
        if lang_code == 'zh':
            return 'zho_Hans'
        return nllb_codes.get(lang_code, 'eng_Latn')
    
    def _estimate_confidence(self, original: str, translated: str) -> float:
        """Estimate translation confidence based on heuristics"""
        confidence = 0.85
        
        if len(translated) < len(original) * 0.3:
            confidence -= 0.2
        elif len(translated) > len(original) * 3:
            confidence -= 0.1
        
        if '[' in translated and ']' in translated:
            confidence -= 0.15
        
        special_chars = sum(1 for c in translated if not c.isalnum() and c not in ' .,!?-')
        if special_chars > len(translated) * 0.3:
            confidence -= 0.1
        
        return max(0.5, min(0.99, confidence))
    
    def _detect_business_terms(self, text: str) -> List[str]:
        """Detect business terminology in text"""
        text_lower = text.lower()
        found_terms = []
        
        for term in self.business_terms_db:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _detect_slang(self, text: str, language: str) -> List[str]:
        """Detect local slang in text"""
        text_lower = text.lower()
        found_slang = []
        
        if language in ['sn', 'zu', 'xh', 'nd']:
            for slang in self.slang_db:
                if slang in self.slang_db[slang].get(language, '').lower():
                    found_slang.append(slang)
        
        return found_slang
    
    def batch_translate(
        self,
        texts: List[str],
        source_language: str,
        target_language: str,
        context: Optional[str] = None
    ) -> List[TranslationResult]:
        """Translate multiple texts efficiently"""
        results = []
        
        for text in texts:
            result = self.translate(text, source_language, target_language, context)
            results.append(result)
        
        return results
    
    def translate_with_fallback(
        self,
        text: str,
        source_language: str,
        target_language: str,
        context: Optional[str] = None
    ) -> TranslationResult:
        """
        Translate with fallback to dictionary-based translation
        Used when ML model fails or confidence is low
        """
        primary_result = self.translate(text, source_language, target_language, context)
        
        if primary_result.confidence >= 0.85 and not primary_result.needs_review:
            return primary_result
        
        logger.info(f"Using fallback for: {text[:50]}...")
        
        from tourista_ai_model.translation.engine import TranslationEngine
        fallback_engine = TranslationEngine()
        fallback_result = fallback_engine.translate(text, source_language, target_language)
        
        if primary_result.confidence > fallback_result.confidence:
            return primary_result
        else:
            return TranslationResult(
                original_text=text,
                translated_text=fallback_result.translated_text,
                source_language=source_language,
                target_language=target_language,
                confidence=fallback_result.confidence,
                model_used="dictionary_fallback",
                processing_time_ms=0.0,
                business_terms_found=primary_result.business_terms_found,
                local_slang_found=primary_result.local_slang_found,
                needs_review=True
            )


class HybridTranslationEngine:
    """
    Hybrid Translation Engine combining ML and Rule-based approaches
    Uses ML for primary translation, rules for domain-specific terms
    """
    
    def __init__(self):
        self.ml_engine = MLTranslationEngine()
        self.rule_engine = TranslationEngine()
        logger.info("Hybrid Translation Engine initialized")
    
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        context: Optional[str] = None
    ) -> TranslationResult:
        """
        Hybrid translation: ML + Rule-based enhancement
        """
        ml_result = self.ml_engine.translate(text, source_language, target_language, context)
        
        if ml_result.confidence >= 0.9:
            logger.info(f"High confidence ML translation: {ml_result.confidence}")
            return ml_result
        
        logger.info(f"Enhancing ML translation with rules: confidence={ml_result.confidence}")
        
        rule_result = self.rule_engine.translate(text, source_language, target_language)
        
        enhanced_text = self._enhance_translation(
            ml_result.translated_text,
            rule_result.translated_text,
            text,
            source_language,
            target_language
        )
        
        return TranslationResult(
            original_text=text,
            translated_text=enhanced_text,
            source_language=source_language,
            target_language=target_language,
            confidence=max(ml_result.confidence, rule_result.confidence),
            model_used="hybrid_ml_rules",
            processing_time_ms=ml_result.processing_time_ms,
            business_terms_found=ml_result.business_terms_found + rule_result.business_terms_found,
            local_slang_found=ml_result.local_slang_found,
            needs_review=ml_result.needs_review or rule_result.needs_review
        )
    
    def _enhance_translation(
        self,
        ml_text: str,
        rule_text: str,
        original: str,
        source: str,
        target: str
    ) -> str:
        """Enhance ML translation with rule-based terms"""
        enhanced = ml_text
        
        if '[' in rule_text and ']' in rule_text:
            missing_terms = []
            parts = rule_text.split('[')
            for part in parts[1:]:
                if ']' in part:
                    term = part.split(']')[0]
                    if term not in enhanced:
                        missing_terms.append(term)
            
            if missing_terms:
                enhanced = f"{enhanced} [{', '.join(missing_terms)}]"
        
        return enhanced


if __name__ == "__main__":
    print("="*70)
    print("ML TRANSLATION ENGINE - TEST")
    print("="*70)
    
    engine = MLTranslationEngine()
    
    test_cases = [
        ("Hello, I want to buy handicrafts", "en", "zh"),
        ("我想买高质量的非洲手工艺品", "zh", "en"),
        ("Ndiri kutsvaga mutengesi wezvigadzi", "sn", "en"),
        ("Imali yakawanda", "zu", "en"),
    ]
    
    for text, source, target in test_cases:
        print(f"\n🌐 {source.upper()} → {target.upper()}")
        print(f"   Original: {text}")
        
        result = engine.translate(text, source, target)
        print(f"   Translated: {result.translated_text}")
        print(f"   Confidence: {result.confidence:.2%}")
        print(f"   Model: {result.model_used}")
        print(f"   Time: {result.processing_time_ms:.2f}ms")
        
        if result.business_terms_found:
            print(f"   Business Terms: {', '.join(result.business_terms_found)}")
    
    print("\n" + "="*70)
    print("Testing Hybrid Engine...")
    print("="*70)
    
    hybrid = HybridTranslationEngine()
    
    test_text = "I want to buy handicrafts from Zimbabwe"
    result = hybrid.translate(test_text, "en", "zh")
    print(f"\nHybrid Translation:")
    print(f"   Original: {test_text}")
    print(f"   Translated: {result.translated_text}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Model: {result.model_used}")
