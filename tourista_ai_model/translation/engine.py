"""
Multi-language Translation Engine for Tourista AR
Supports: Chinese, English, Shona, Ndebele, Zulu, Xhosa
Includes business terminology and local slang for China-Africa trade
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from tourista_ai_model.config import Language, ModelConfig

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    business_terms_found: List[str]
    local_slang_found: List[str]
    needs_review: bool

class TranslationEngine:
    def __init__(self, config: Optional[ModelConfig] = None):
        self.config = config or ModelConfig()
        self.cache = {}
        self.term_database = self._initialize_term_database()
        self.slang_database = self._initialize_slang_database()
        self.context_markers = self._initialize_context_markers()

    def _initialize_term_database(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        return {
            "trade": {
                "zh-en": {
                    "进出口": "import_export",
                    "贸易顺差": "trade_surplus",
                    "贸易逆差": "trade_deficit",
                    "最惠国待遇": "most_favored_nation",
                    "原产地证": "certificate_of_origin",
                    "报关单": "customs_declaration",
                    "检验证书": "inspection_certificate"
                },
                "en-zh": {
                    "import_export": "进出口",
                    "trade_surplus": "贸易顺差",
                    "trade_deficit": "贸易逆差",
                    "most_favored_nation": "最惠国待遇",
                    "certificate_of_origin": "原产地证",
                    "customs_declaration": "报关单",
                    "inspection_certificate": "检验证书"
                }
            },
            "payment": {
                "zh-en": {
                    "跨境支付": "cross_border_payment",
                    "移动支付": "mobile_payment",
                    "电子钱包": "e_wallet",
                    "即时到账": "instant_transfer",
                    "分期付款": "installment",
                    "预付款": "advance_payment",
                    "尾款": "balance_payment"
                },
                "en-zh": {
                    "cross_border_payment": "跨境支付",
                    "mobile_payment": "移动支付",
                    "e_wallet": "电子钱包",
                    "instant_transfer": "即时到账",
                    "installment": "分期付款",
                    "advance_payment": "预付款",
                    "balance_payment": "尾款"
                }
            },
            "logistics": {
                "zh-en": {
                    "货运代理": "freight_forwarder",
                    "仓储物流": "warehousing_logistics",
                    "最后一公里": "last_mile_delivery",
                    "清关服务": "clearance_service",
                    "保险服务": "insurance_service",
                    "追踪查询": "tracking_query",
                    "配送中心": "distribution_center"
                },
                "en-zh": {
                    "freight_forwarder": "货运代理",
                    "warehousing_logistics": "仓储物流",
                    "last_mile_delivery": "最后一公里",
                    "clearance_service": "清关服务",
                    "insurance_service": "保险服务",
                    "tracking_query": "追踪查询",
                    "distribution_center": "配送中心"
                }
            },
            "business": {
                "zh-en": {
                    "营业执照": "business_license",
                    "供应商认证": "supplier_verification",
                    "产品质量": "product_quality",
                    "最低起订量": "minimum_order_quantity",
                    "FOB价": "free_on_board_price",
                    "CIF价": "cost_insurance_freight",
                    "EXW价": "ex_works_price"
                },
                "en-zh": {
                    "business_license": "营业执照",
                    "supplier_verification": "供应商认证",
                    "product_quality": "产品质量",
                    "minimum_order_quantity": "最低起订量",
                    "free_on_board_price": "FOB价",
                    "cost_insurance_freight": "CIF价",
                    "ex_works_price": "EXW价"
                }
            }
        }

    def _initialize_slang_database(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        return {
            "shona": {
                "musika": "market/musika",
                "mari": "money/mari",
                "hupenyu": "life/business opportunity",
                "mutengo": "price/value",
                "kusvika": "arrival/delivery",
                "bvisa": "to sell/sort out",
                "goridza": "to transport/carry"
            },
            "ndebele": {
                "umakethe": "market/trading",
                "imali": "money/payment",
                "ukuthengisa": "to sell/market",
                "ukuthwala": "to transport/carry",
                "ibhizinisi": "business/enterprise",
                "ukuhlala": "to stay/reside"
            },
            "zulu": {
                "umakethe": "market/transaction",
                "imali": "money/capital",
                "ukuhwebana": "to trade/exchange",
                "ukuthwala": "to carry/transport",
                "ibhizinisi": "business/venture",
                "ukuhlala": "to stay/remain"
            },
            "xhosa": {
                "umthengiso": "market/sales",
                "imali": "money/currency",
                "ukuthengisa": "to sell/market",
                "ukuthwala": "to transport/carry",
                "ishishini": "business/enterprise",
                "ukuhlala": "to stay/dwell"
            }
        }

    def _initialize_context_markers(self) -> Dict[str, List[str]]:
        return {
            "formal_business": ["合同", "协议", "报价", "订单", "invoice", "contract", "agreement", "quotation"],
            "informal_trade": ["批发", "零售", "market", "trade", "buy", "sell"],
            "tourism": ["旅游", "travel", "hotel", "酒店", "tour", "guide"],
            "payment": ["付款", "支付", "payment", "transfer", "credit"],
            "logistics": ["发货", "收货", "shipping", "delivery", "transport"]
        }

    def translate(self, text: str, source_lang: str, target_lang: str,
                  context: Optional[str] = None) -> TranslationResult:
        if not text or not text.strip():
            return TranslationResult(
                original_text=text,
                translated_text="",
                source_language=source_lang,
                target_language=target_lang,
                confidence=0.0,
                business_terms_found=[],
                local_slang_found=[],
                needs_review=False
            )

        cache_key = f"{source_lang}:{target_lang}:{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        business_terms = self._extract_business_terms(text, source_lang, target_lang)
        local_slang = self._extract_local_slang(text, target_lang)

        if source_lang == "zh" and target_lang in ["sn", "nd", "zu", "xh"]:
            translated = self._translate_chinese_to_african(text, target_lang, context)
        elif source_lang in ["sn", "nd", "zu", "xh"] and target_lang == "zh":
            translated = self._translate_african_to_chinese(text, source_lang, context)
        elif source_lang == "en" and target_lang in ["sn", "nd", "zu", "xh"]:
            translated = self._translate_english_to_african(text, target_lang, context)
        elif source_lang in ["sn", "nd", "zu", "xh"] and target_lang == "en":
            translated = self._translate_african_to_english(text, source_lang, context)
        else:
            translated = self._translate_standard(text, source_lang, target_lang, context)

        confidence = self._calculate_confidence(text, translated, business_terms, local_slang)
        needs_review = self._needs_human_review(translated, confidence, business_terms, local_slang)

        result = TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=source_lang,
            target_language=target_lang,
            confidence=confidence,
            business_terms_found=business_terms,
            local_slang_found=local_slang,
            needs_review=needs_review
        )

        self.cache[cache_key] = result
        return result

    def _translate_chinese_to_african(self, text: str, target_lang: str,
                                     context: Optional[str]) -> str:
        translated_parts = []
        words = self._tokenize_chinese(text)

        for word in words:
            found_term = False
            for category in self.term_database.values():
                if f"{target_lang}" in category:
                    lang_key = f"zh-{target_lang}"
                    if lang_key in category:
                        if word in category[lang_key]:
                            translated_parts.append(category[lang_key][word])
                            found_term = True
                            break

            if not found_term:
                if target_lang == "sn":
                    translated_parts.append(f"[{word}]")
                elif target_lang == "nd":
                    translated_parts.append(f"[{word}]")
                elif target_lang == "zu":
                    translated_parts.append(f"[{word}]")
                elif target_lang == "xh":
                    translated_parts.append(f"[{word}]")

        slang_replacements = self.slang_database.get(target_lang, {})
        result = " ".join(translated_parts)
        for eng, localized in slang_replacements.items():
            result = re.sub(rf'\b{eng}\b', localized.split('/')[0], result, flags=re.IGNORECASE)

        return result

    def _translate_african_to_chinese(self, text: str, source_lang: str,
                                      context: Optional[str]) -> str:
        translated_parts = []
        words = text.split()

        slang_map = self.slang_database.get(source_lang, {})

        for word in words:
            clean_word = re.sub(r'[\[\]]', '', word)
            found_term = False

            for category in self.term_database.values():
                if f"en-zh" in category:
                    if clean_word in category["en-zh"]:
                        translated_parts.append(category["en-zh"][clean_word])
                        found_term = True
                        break

            if not found_term:
                for eng_term, local_term in slang_map.items():
                    if eng_term in word:
                        translated_parts.append(f"[{eng_term}]")
                        found_term = True
                        break

            if not found_term:
                translated_parts.append(word)

        return "".join(translated_parts)

    def _translate_english_to_african(self, text: str, target_lang: str,
                                    context: Optional[str]) -> str:
        translated_parts = []
        words = text.split()

        for word in words:
            found_term = False
            for category in self.term_database.values():
                if f"en-{target_lang}" in category:
                    if word.lower() in category[f"en-{target_lang}"]:
                        translated_parts.append(category[f"en-{target_lang}"][word.lower()])
                        found_term = True
                        break

            if not found_term:
                slang_map = self.slang_database.get(target_lang, {})
                if word.lower() in slang_map:
                    translated_parts.append(slang_map[word.lower()].split('/')[0])
                    found_term = True
                else:
                    translated_parts.append(word)

        return " ".join(translated_parts)

    def _translate_african_to_english(self, text: str, source_lang: str,
                                     context: Optional[str]) -> str:
        translated_parts = []
        words = text.split()

        slang_map = self.slang_database.get(source_lang, {})

        for word in words:
            clean_word = re.sub(r'[\[\]]', '', word).lower()
            found_term = False

            for category in self.term_database.values():
                if f"{source_lang}-en" in category:
                    if clean_word in category[f"{source_lang}-en"]:
                        translated_parts.append(category[f"{source_lang}-en"][clean_word])
                        found_term = True
                        break

            if not found_term:
                for eng_term, local_term in slang_map.items():
                    if eng_term in clean_word or local_term.split('/')[0] in word:
                        translated_parts.append(eng_term)
                        found_term = True
                        break

            if not found_term:
                translated_parts.append(word)

        return " ".join(translated_parts)

    def _translate_standard(self, text: str, source_lang: str, target_lang: str,
                          context: Optional[str]) -> str:
        if source_lang == "zh" and target_lang == "en":
            return self._translate_chinese_to_english(text)
        elif source_lang == "en" and target_lang == "zh":
            return self._translate_english_to_chinese(text)
        else:
            return f"[{target_lang}] {text}"

    def _translate_chinese_to_english(self, text: str) -> str:
        result = text
        for category in self.term_database.values():
            if "zh-en" in category:
                for cn, en in category["zh-en"].items():
                    result = result.replace(cn, en)
        return result

    def _translate_english_to_chinese(self, text: str) -> str:
        result = text
        for category in self.term_database.values():
            if "en-zh" in category:
                for en, cn in category["en-zh"].items():
                    result = result.replace(en, cn)
        return result

    def _tokenize_chinese(self, text: str) -> List[str]:
        return re.findall(r'[\u4e00-\u9fff]+', text)

    def _extract_business_terms(self, text: str, source_lang: str,
                               target_lang: str) -> List[str]:
        found_terms = []
        token_key = f"{source_lang}-{target_lang}"

        for category, languages in self.term_database.items():
            if token_key in languages:
                for term in languages[token_key].keys():
                    if term in text:
                        found_terms.append(term)

        return found_terms

    def _extract_local_slang(self, text: str, target_lang: str) -> List[str]:
        found_slang = []
        slang_map = self.slang_database.get(target_lang, {})

        words = text.lower().split()
        for word in words:
            clean_word = re.sub(r'[\[\],.!?]', '', word)
            for eng_term, local_term in slang_map.items():
                if eng_term in clean_word or local_term.split('/')[0] in clean_word:
                    found_slang.append(eng_term)

        return found_slang

    def _calculate_confidence(self, original: str, translated: str,
                              business_terms: List[str], slang: List[str]) -> float:
        base_confidence = 0.7

        if len(business_terms) > 0:
            base_confidence += 0.1

        if len(slang) > 0:
            base_confidence += 0.1

        if len(translated) > len(original) * 0.8:
            base_confidence += 0.1

        return min(base_confidence, 0.95)

    def _needs_human_review(self, translated: str, confidence: float,
                           business_terms: List[str], slang: List[str]) -> bool:
        if confidence < 0.6:
            return True

        if len(business_terms) > 5:
            return True

        if "[UNKNOWN]" in translated or "[TODO]" in translated:
            return True

        return False

    def batch_translate(self, texts: List[str], source_lang: str,
                       target_lang: str,
                       context: Optional[str] = None) -> List[TranslationResult]:
        return [self.translate(text, source_lang, target_lang, context) for text in texts]

    def get_supported_pairs(self) -> List[Tuple[str, str]]:
        return [
            ("zh", "en"), ("en", "zh"),
            ("zh", "sn"), ("sn", "zh"),
            ("zh", "nd"), ("nd", "zh"),
            ("zh", "zu"), ("zu", "zh"),
            ("zh", "xh"), ("xh", "zh"),
            ("en", "sn"), ("sn", "en"),
            ("en", "nd"), ("nd", "en"),
            ("en", "zu"), ("zu", "en"),
            ("en", "xh"), ("xh", "en")
        ]

    def add_custom_term(self, source_lang: str, target_lang: str,
                       source_term: str, target_term: str,
                       category: str = "custom"):
        if category not in self.term_database:
            self.term_database[category] = {}
        key = f"{source_lang}-{target_lang}"
        if key not in self.term_database[category]:
            self.term_database[category][key] = {}
        self.term_database[category][key][source_term] = target_term

    def clear_cache(self):
        self.cache.clear()
