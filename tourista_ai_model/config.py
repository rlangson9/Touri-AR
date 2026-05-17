"""
Tourista AR Proprietary AI Model
China-Africa Cross-Border Super App Model
IP: Tourista AR - Shanghai, China
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class Language(Enum):
    CHINESE = "zh"
    ENGLISH = "en"
    SHONA = "sn"
    NDEBELE = "nd"
    ZULU = "zu"
    XHOSA = "xh"

class MarketRegion(Enum):
    CHINA = "china"
    ZIMBABWE = "zimbabwe"
    SOUTH_AFRICA = "south_africa"
    EAST_AFRICA = "east_africa"
    WEST_AFRICA = "west_africa"

class TransactionType(Enum):
    B2B = "business_to_business"
    B2C = "business_to_consumer"
    C2C = "consumer_to_consumer"
    CROSS_BORDER_TRADE = "cross_border_trade"
    TOURISM_SERVICE = "tourism_service"

@dataclass
class ModelConfig:
    model_name: str = "TouristaAI-ChinaAfrica-v1.0"
    version: str = "1.0.0"
    language: str = "multilingual"
    max_token_limit: int = 2048
    temperature: float = 0.7
    top_p: float = 0.9
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0

    translation_languages: List[str] = field(default_factory=lambda: [
        "zh", "en", "sn", "nd", "zu", "xh"
    ])

    supported_regions: List[str] = field(default_factory=lambda: [
        "china", "zimbabwe", "south_africa"
    ])

    api_timeout: int = 30
    cache_enabled: bool = True
    cache_ttl: int = 3600

    enable_context_compression: bool = True
    max_context_length: int = 4096

    risk_threshold_high: float = 0.8
    risk_threshold_medium: float = 0.5
    risk_threshold_low: float = 0.3

    ar_confidence_threshold: float = 0.75
    matching_similarity_threshold: float = 0.7

    def __post_init__(self):
        self.supported_languages = {
            "zh": "Chinese (Mandarin)",
            "en": "English",
            "sn": "Shona (Zimbabwe)",
            "nd": "Ndebele (Zimbabwe)",
            "zu": "Zulu (South Africa)",
            "xh": "Xhosa (South Africa)"
        }

        self.business_terminology = {
            "zh-en": self._load_chinese_english_terms(),
            "zh-sn": self._load_chinese_shona_terms(),
            "zh-nd": self._load_chinese_ndebele_terms(),
            "zh-zu": self._load_chinese_zulu_terms(),
            "zh-xh": self._load_chinese_xhosa_terms()
        }

    def _load_chinese_english_terms(self) -> Dict[str, str]:
        return {
            "买家": "buyer",
            "卖家": "seller",
            "供应商": "supplier",
            "订单": "order",
            "付款": "payment",
            "物流": "logistics",
            "清关": "customs clearance",
            "关税": "tariff",
            "发票": "invoice",
            "合同": "contract",
            "报价": "quotation",
            "样品": "sample",
            "批发": "wholesale",
            "零售": "retail",
            "集装箱": "container",
            "海运": "shipping",
            "空运": "air freight",
            "人民币": "CNY/RMB",
            "美元": "USD",
            "信用证": "letter of credit",
            "电汇": "wire transfer"
        }

    def _load_chinese_shona_terms(self) -> Dict[str, str]:
        return {
            "买家": "mudzi",
            "卖家": "mutengesi",
            "供应商": "mut 제공자",
            "价格": "mutengo",
            "付款": "kubhadhara",
            "订单": "order",
            "欢迎": "欢迎 (makadii)",
            "谢谢": "thank you (maita)",
            "你好": "hello (Mhoroi)",
            "港口": "port (porti)",
            "货物": "goods (zvinhu)",
            "质量": "quality (quality)",
            "数量": "quantity (quantity)",
            "折扣": "discount (discount)",
            "谈判": "negotiation (negotiation)"
        }

    def _load_chinese_ndebele_terms(self) -> Dict[str, str]:
        return {
            "买家": "umthengi",
            "卖家": "umdayi",
            "供应商": "umthengisi",
            "价格": "intengo",
            "付款": "ukuhlawula",
            "订单": "iodolo",
            "欢迎": "欢迎 (uswele)",
            "谢谢": "thank you (ngiyabonga)",
            "你好": "hello (sawubona)",
            "港口": "port (isikhwama)",
            "货物": "goods (izinto)",
            "质量": "quality (umkhiqizo)",
            "数量": "quantity (inani)",
            "折扣": "discount (isaphulelo)",
            "谈判": "negotiation (ukuxoxisana)"
        }

    def _load_chinese_zulu_terms(self) -> Dict[str, str]:
        return {
            "买家": "umthengi",
            "卖家": "umdayi",
            "供应商": "umthengisi",
            "价格": "intengo",
            "付款": "ukukhokha",
            "订单": "iodolo",
            "欢迎": "欢迎 (wakwethu)",
            "谢谢": "thank you (ngiyabonga)",
            "你好": "hello (sawubona)",
            "港口": "port (isikhwama)",
            "货物": "goods (izinto)",
            "质量": "quality (ikholi)",
            "数量": "quantity (inani)",
            "折扣": "discount (isaphulelo)",
            "谈判": "negotiation (ukuxoxisana)"
        }

    def _load_chinese_xhosa_terms(self) -> Dict[str, str]:
        return {
            "买家": "umthengi",
            "卖家": "umdayi",
            "供应商": "umthengisi",
            "价格": "intengo",
            "付款": "ukuhlawula",
            "订单": "iodolo",
            "欢迎": "欢迎 (moleni)",
            "谢谢": "thank you (enkosi)",
            "你好": "hello (molo)",
            "港口": "port (isikhwama)",
            "货物": "goods (izinto)",
            "质量": "quality (umgangatho)",
            "数量": "quantity (inani)",
            "折扣": "discount (isaphulelo)",
            "谈判": "negotiation (ukuxoxisana)"
        }

    def get_supported_language_name(self, code: str) -> str:
        return self.supported_languages.get(code, "Unknown")

    def get_business_term(self, source_lang: str, target_lang: str, term: str) -> Optional[str]:
        key = f"{source_lang}-{target_lang}"
        return self.business_terminology.get(key, {}).get(term)

class APIConfig:
    base_url: str = "https://api.tourista-ar.ai/v1"
    api_key: Optional[str] = None
    api_version: str = "v1"
    request_timeout: int = 30
    max_retries: int = 3
    rate_limit: int = 100

class ChinaAfricaTradeConfig:
    supported_currencies: List[str] = field(default_factory=lambda: [
        "CNY", "USD", "ZAR", "ZWL", "EUR"
    ])

    payment_methods: Dict[str, List[str]] = field(default_factory=lambda: {
        "china": ["Alipay", "WeChat Pay", "UnionPay", "Bank Transfer", "Letter of Credit"],
        "zimbabwe": ["Ecocash", "OneMoney", "Bank Transfer", "Cash", "Mobile Money"],
        "south_africa": ["SnapScan", "Zapper", "Bank Transfer", "Cash", "Credit Card"]
    })

    logistics_partners: Dict[str, List[str]] = field(default_factory=lambda: {
        "china": ["DHL", "FedEx", "COSCO", "CMA CGM", "Maersk"],
        "zimbabwe": ["Transmed", "Bimbabwe", "N Richards", "Truck Safari"],
        "south_africa": ["SAPO", "Courier It", "Fastway", "Aramex"]
    })

    customs_requirements: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "china": {
            "import_duty_rate": 0.10,
            "vat_rate": 0.13,
            "required_documents": ["commercial_invoice", "packing_list", "bill_of_lading", "certificate_of_origin"]
        },
        "zimbabwe": {
            "import_duty_rate": 0.25,
            "vat_rate": 0.15,
            "required_documents": ["bill_of_entry", "import_license", "proforma_invoice", "certificate_of_origin"],
            "special_requirements": ["RFID_tracking", "quality_inspection_certificate"]
        },
        "south_africa": {
            "import_duty_rate": 0.20,
            "vat_rate": 0.15,
            "required_documents": ["bill_of_entry", "import_permit", "commercial_invoice", "certificate_of_origin"],
            "special_requirements": ["SABS_approval", "phytosanitary_certificate"]
        }
    })

    risk_factors: List[str] = field(default_factory=lambda: [
        "currency_fluctuation",
        "political_instability",
        "logistics_delay",
        "payment_default",
        "quality_dispute",
        "customs_hold",
        "fraud_risk",
        "compliance_risk"
    ])

CONFIG = ModelConfig()
API_CONFIG = APIConfig()
TRADE_CONFIG = ChinaAfricaTradeConfig()
