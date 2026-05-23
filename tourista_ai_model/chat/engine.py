"""
Tourista AR Chat Engine
AI Assistant for China-Africa Cross-Border Trade & Travel
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re

@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ChatResponse:
    content: str
    intent: str
    confidence: float
    suggestions: List[str] = field(default_factory=list)
    related_actions: List[str] = field(default_factory=list)
    language_detected: str = "en"

class ChatEngine:
    def __init__(self, translation_engine=None, matching_system=None, 
                 recommendation_engine=None, risk_engine=None, ar_engine=None):
        self.translation_engine = translation_engine
        self.matching_system = matching_system
        self.recommendation_engine = recommendation_engine
        self.risk_engine = risk_engine
        self.ar_engine = ar_engine
        
        self.conversation_history: Dict[str, List[ChatMessage]] = {}
        
        self.intent_patterns = {
            "translation": [
                r"translate|翻译|traduire|tafsiri",
                r"how do (?:you )?say|怎么说|comment dit-on",
                r"what does .* mean|.*是什么意思",
                r"in (?:chinese|english|shona|ndebele|zulu|xhosa)"
            ],
            "product_search": [
                r"find (?:products?|suppliers?|sellers?)",
                r"looking for|我想找|寻找|cherche",
                r"buy|purchase|购买|acheter",
                r"source|sourcing|采购"
            ],
            "supplier_match": [
                r"match|匹配|correspondre",
                r"connect with|connecter avec",
                r"find (?:buyers?|suppliers?|partners?)",
                r"trade partner|贸易伙伴"
            ],
            "price_inquiry": [
                r"price|价格|prix|bei",
                r"cost|成本|coût",
                r"how much|多少钱|combien",
                r"quote|报价|devis"
            ],
            "tourism": [
                r"tour|travel|visit|旅游|旅行|visiter",
                r"safari|victoria falls|kruger",
                r"attractions?|destinations?|景点",
                r"things to do|做什么"
            ],
            "payment": [
                r"pay|payment|付款|payer",
                r"mobile money|ecocash|mpesa",
                r"transfer|汇款|virement",
                r"how to pay|如何付款"
            ],
            "shipping": [
                r"ship|shipping|运输|expédition",
                r"delivery|deliver|交货|livraison",
                r"logistics|物流|logistique",
                r"customs|海关|douane"
            ],
            "risk_assessment": [
                r"risk|风险|risque",
                r"safe|safety|安全|sûr",
                r"trust|verify|信任|验证",
                r"scam|fraud|诈骗|fraude"
            ],
            "greeting": [
                r"^(hi|hello|hey|你好|您好|bonjour|sawubona|molo)",
                r"good (?:morning|afternoon|evening)",
                r"how are you|你好吗|comment allez-vous"
            ],
            "help": [
                r"help|帮助|aide|musa",
                r"what can you do|你能做什么",
                r"how does this work|怎么用"
            ],
            "ar_experience": [
                r"ar|augmented reality|增强现实",
                r"scan|recognize|识别",
                r"point camera|摄像头",
                r"product preview|产品预览"
            ]
        }
        
        self.responses = {
            "greeting": {
                "en": "Hello! Welcome to Touri AI, your China-Africa trade and travel assistant. I can help you with translations, finding suppliers, product recommendations, tourism experiences, and more. How can I assist you today?",
                "zh": "您好！欢迎来到Touri AI，您的中非贸易和旅行助手。我可以帮助您翻译、寻找供应商、产品推荐、旅游体验等。请问有什么可以帮助您的？",
                "sn": "Mhoroi! Wakawirwa ku Touri AI, mubatsiri wenyu weChina-Africa. Ndingakubatsirei nekushandura, kutsvaga vatengesi, uye zvimwe. Ndingakubatsirei sei nhasi?",
                "nd": "Sawubona! Siyalemukela ku Touri AI, umsizi wakho we-China-Africa. Ngingakusiza ngokuhumusha, ukufuna abathengisi, kanye nokunye. Ngingakusiza kanjani namhlanje?"
            },
            "help": {
                "en": "I'm Touri AI, specialized for China-Africa cross-border trade and travel. Here's what I can help with:\n\n🌐 **Translation**: Translate between Chinese, English, Shona, Ndebele, Zulu, and Xhosa\n\n📦 **Trade**: Find suppliers, buyers, products, and get trade recommendations\n\n💰 **Payments**: Payment methods including mobile money for unbanked users\n\n🚚 **Logistics**: Shipping and customs guidance\n\n🎯 **Matching**: Connect with verified trade partners\n\n🦁 **Tourism**: Discover African destinations and experiences\n\n📱 **AR**: Augmented reality product previews and tourism experiences\n\nJust ask me anything!",
                "zh": "我是Touri AI，专注于中非跨境贸易和旅行。我可以帮助您：\n\n🌐 **翻译**：中文、英文、绍纳语、恩德贝莱语、祖鲁语和科萨语互译\n\n📦 **贸易**：寻找供应商、买家、产品，获取贸易推荐\n\n💰 **支付**：包括无银行账户用户的移动支付方式\n\n🚚 **物流**：运输和海关指导\n\n🎯 **匹配**：连接经过验证的贸易伙伴\n\n🦁 **旅游**：发现非洲目的地和体验\n\n📱 **AR**：增强现实产品预览和旅游体验\n\n请随时问我！"
            },
            "translation": {
                "en": "I can translate between Chinese, English, Shona, Ndebele, Zulu, and Xhosa. Just tell me what you'd like to translate and to which language!",
                "zh": "我可以在中文、英文、绍纳语、恩德贝莱语、祖鲁语和科萨语之间进行翻译。请告诉我您想翻译什么内容！"
            },
            "product_search": {
                "en": "I can help you find products and suppliers from Africa. What type of products are you looking for? Popular categories include:\n\n• Agricultural products (coffee, cocoa, shea butter)\n• Minerals and gemstones\n• Textiles and crafts\n• Natural ingredients",
                "zh": "我可以帮您寻找非洲的产品和供应商。您在寻找什么类型的产品？热门类别包括：\n\n• 农产品（咖啡、可可、乳木果油）\n• 矿物和宝石\n• 纺织品和工艺品\n• 天然原料"
            },
            "tourism": {
                "en": "Africa offers incredible experiences! I can recommend:\n\n🦁 **Wildlife Safaris** - Kruger Park, Serengeti, Masai Mara\n\n💦 **Victoria Falls** - One of the world's natural wonders\n\n🏔️ **Mountain Adventures** - Kilimanjaro, Drakensberg\n\n🏖️ **Beach Destinations** - Zanzibar, Cape Town\n\nWhich type of experience interests you?",
                "zh": "非洲提供令人难以置信的体验！我可以推荐：\n\n🦁 **野生动物狩猎** - 克鲁格公园、塞伦盖蒂、马赛马拉\n\n💦 **维多利亚瀑布** - 世界自然奇观之一\n\n🏔️ **山地探险** - 乞力马扎罗、德拉肯斯堡\n\n🏖️ **海滩目的地** - 桑给巴尔、开普敦\n\n您对哪种体验感兴趣？"
            },
            "payment": {
                "en": "For China-Africa trade, I can recommend payment methods:\n\n📱 **Mobile Money** (for unbanked users):\n• Ecocash (Zimbabwe)\n• M-Pesa (Kenya, Tanzania)\n• MTN Mobile Money\n\n🏦 **Traditional Banking**:\n• Bank Transfer (T/T)\n• Letter of Credit (L/C)\n• Alipay/WeChat Pay (China)\n\nWhich payment method would you like to know more about?",
                "zh": "对于中非贸易，我可以推荐以下支付方式：\n\n📱 **移动支付**（适合无银行账户用户）：\n• Ecocash（津巴布韦）\n• M-Pesa（肯尼亚、坦桑尼亚）\n• MTN Mobile Money\n\n🏦 **传统银行**：\n• 银行转账（T/T）\n• 信用证（L/C）\n• 支付宝/微信支付（中国）\n\n您想了解哪种支付方式？"
            },
            "shipping": {
                "en": "I can help with shipping and logistics between China and Africa:\n\n🚢 **Sea Freight**: COSCO, Maersk, CMA CGM (20-45 days)\n\n✈️ **Air Freight**: DHL, FedEx, Emirates SkyCargo (3-7 days)\n\n🚛 **Land Transport**: Cross-border trucking within Africa\n\n📋 **Customs**: Documentation and clearance guidance\n\nWhat's your shipping need?",
                "zh": "我可以帮助您处理中非之间的运输和物流：\n\n🚢 **海运**：中远、马士基、达飞轮船（20-45天）\n\n✈️ **空运**：DHL、联邦快递、阿联酋航空货运（3-7天）\n\n🚛 **陆运**：非洲境内的跨境卡车运输\n\n📋 **海关**：文件和清关指导\n\n您的运输需求是什么？"
            },
            "risk_assessment": {
                "en": "I can help assess trade risks and verify partners:\n\n✅ **Verification Checks**:\n• Business registration\n• Trade history\n• Quality certifications\n\n⚠️ **Risk Factors I Monitor**:\n• Payment reliability\n• Delivery track record\n• Quality consistency\n• Fraud indicators\n\nWould you like me to assess a specific transaction or partner?",
                "zh": "我可以帮助评估贸易风险和验证合作伙伴：\n\n✅ **验证检查**：\n• 营业执照\n• 贸易历史\n• 质量认证\n\n⚠️ **我监控的风险因素**：\n• 付款可靠性\n• 交货记录\n• 质量一致性\n• 欺诈指标\n\n您想让我评估特定的交易或合作伙伴吗？"
            },
            "ar_experience": {
                "en": "Use our AR features for:\n\n📱 **Product Preview**: Point your camera at products to see details, pricing, and supplier info\n\n🗺️ **Tourism AR**: Scan landmarks for historical info and guided tours\n\n🛍️ **Trade Showers**: Virtual product showcases\n\nTry pointing your camera at a product or landmark!",
                "zh": "使用我们的AR功能：\n\n📱 **产品预览**：将相机对准产品查看详情、价格和供应商信息\n\n🗺️ **旅游AR**：扫描地标获取历史信息和导览\n\n🛍️ **贸易展示**：虚拟产品展示\n\n尝试将相机对准产品或地标！"
            },
            "unknown": {
                "en": "I understand you're asking about trade or travel between China and Africa. Could you provide more details? I can help with:\n\n• Finding products or suppliers\n• Translation services\n• Payment and shipping guidance\n• Tourism recommendations\n• Risk assessment",
                "zh": "我理解您在询问中非之间的贸易或旅行。您能提供更多细节吗？我可以帮助：\n\n• 寻找产品或供应商\n• 翻译服务\n• 支付和运输指导\n• 旅游推荐\n• 风险评估"
            }
        }
        
        self.trade_knowledge = {
            "coffee": {
                "en": "Ethiopian and Zimbabwean specialty coffee is in high demand in China. Prices range from $3-8/kg FOB. Peak season: October-January. Consider direct trade relationships for better margins.",
                "zh": "埃塞俄比亚和津巴布韦的特色咖啡在中国需求旺盛。FOB价格在3-8美元/公斤。旺季：10月至1月。建议建立直接贸易关系以获得更好利润。"
            },
            "shea_butter": {
                "en": "Shea butter from West Africa is popular in Chinese cosmetics. Look for organic and fair-trade certifications. Price: $5-15/kg depending on quality.",
                "zh": "来自西非的乳木果油在中国化妆品市场很受欢迎。寻找有机和公平贸易认证。价格：5-15美元/公斤，取决于质量。"
            },
            "gemstones": {
                "en": "Tanzanite from Tanzania and emeralds from Zambia are sought after in China. Always request certification from reputable labs (GIA, GRS). Consider insurance for high-value shipments.",
                "zh": "坦桑尼亚的坦桑石和赞比亚的祖母绿在中国很受欢迎。务必要求来自知名实验室（GIA、GRS）的证书。高价值货物建议购买保险。"
            },
            "avocado": {
                "en": "African avocados (Kenya, Zimbabwe) are gaining market access to China. Hass variety preferred. Season: March-September. Cold chain logistics essential.",
                "zh": "非洲牛油果（肯尼亚、津巴布韦）正在获得中国市场准入。首选哈斯品种。季节：3月至9月。冷链物流至关重要。"
            }
        }
    
    def detect_language(self, text: str) -> str:
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        if chinese_chars > len(text) * 0.3:
            return "zh"
        
        shona_words = ['makadii', 'mhoroi', 'tatenda', 'maita', 'zvakanaka']
        ndebele_words = ['sawubona', 'ngiyabonga', 'unjani', 'siyalebulela']
        zulu_words = ['sawubona', 'yebo', 'ngiyabonga', 'hamba']
        xhosa_words = ['molo', 'enkosi', 'ewe', 'uxolo']
        
        text_lower = text.lower()
        for word in shona_words:
            if word in text_lower:
                return "sn"
        for word in ndebele_words:
            if word in text_lower:
                return "nd"
        for word in zulu_words:
            if word in text_lower:
                return "zu"
        for word in xhosa_words:
            if word in text_lower:
                return "xh"
        
        return "en"
    
    def detect_intent(self, text: str) -> tuple:
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent, 0.85
        
        return "unknown", 0.5
    
    def extract_entities(self, text: str) -> Dict:
        entities = {
            "products": [],
            "languages": [],
            "locations": [],
            "amounts": []
        }
        
        product_keywords = {
            "coffee": "coffee", "咖啡": "coffee", "café": "coffee",
            "cocoa": "cocoa", "可可": "cocoa",
            "shea": "shea_butter", "乳木果": "shea_butter",
            "avocado": "avocado", "牛油果": "avocado",
            "gemstone": "gemstones", "宝石": "gemstones",
            "tanzanite": "gemstones", "坦桑石": "gemstones"
        }
        
        for keyword, product in product_keywords.items():
            if keyword in text.lower():
                entities["products"].append(product)
        
        language_keywords = {
            "chinese": "zh", "中文": "zh", "中国": "zh",
            "english": "en", "英文": "en",
            "shona": "sn", "绍纳": "sn",
            "ndebele": "nd", "恩德贝莱": "nd",
            "zulu": "zu", "祖鲁": "zu",
            "xhosa": "xh", "科萨": "xh"
        }
        
        for keyword, lang in language_keywords.items():
            if keyword in text.lower():
                entities["languages"].append(lang)
        
        location_keywords = {
            "china": "china", "中国": "china",
            "zimbabwe": "zimbabwe", "津巴布韦": "zimbabwe",
            "south africa": "south_africa", "南非": "south_africa",
            "kenya": "kenya", "肯尼亚": "kenya",
            "ethiopia": "ethiopia", "埃塞俄比亚": "ethiopia",
            "tanzania": "tanzania", "坦桑尼亚": "tanzania"
        }
        
        for keyword, location in location_keywords.items():
            if keyword in text.lower():
                entities["locations"].append(location)
        
        amount_pattern = r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:usd|cny|dollars?|元|人民币)?'
        amounts = re.findall(amount_pattern, text.lower())
        entities["amounts"] = [float(a.replace(',', '')) for a in amounts]
        
        return entities
    
    def generate_response(self, user_id: str, messages: List[Dict], mode: str = "general") -> ChatResponse:
        if not messages:
            return ChatResponse(
                content=self.responses["greeting"]["en"],
                intent="greeting",
                confidence=1.0,
                suggestions=["Find suppliers", "Translate text", "Tourism recommendations"],
                related_actions=["search_products", "translate", "explore_tourism"]
            )
        
        last_message = messages[-1].get("content", "") if messages else ""
        detected_lang = self.detect_language(last_message)
        intent, confidence = self.detect_intent(last_message)
        entities = self.extract_entities(last_message)
        
        response_text = ""
        suggestions = []
        related_actions = []
        
        if intent == "translation":
            if self.translation_engine and entities["languages"]:
                response_text = self.responses["translation"].get(detected_lang, self.responses["translation"]["en"])
            else:
                response_text = self.responses["translation"].get(detected_lang, self.responses["translation"]["en"])
            suggestions = ["Translate to Chinese", "Translate to English", "Translate to Shona"]
            related_actions = ["translate"]
        
        elif intent == "product_search":
            if entities["products"]:
                product = entities["products"][0]
                if product in self.trade_knowledge:
                    response_text = self.trade_knowledge[product].get(detected_lang, self.trade_knowledge[product]["en"])
                else:
                    response_text = self.responses["product_search"].get(detected_lang, self.responses["product_search"]["en"])
            else:
                response_text = self.responses["product_search"].get(detected_lang, self.responses["product_search"]["en"])
            suggestions = ["Find coffee suppliers", "Find gemstone suppliers", "Get price quotes"]
            related_actions = ["search_products", "find_suppliers", "get_quotes"]
        
        elif intent == "supplier_match":
            response_text = "I can help connect you with verified trade partners. Are you looking to buy or sell?"
            suggestions = ["Find buyers", "Find suppliers", "View verified partners"]
            related_actions = ["find_matches", "view_verified_partners"]
        
        elif intent == "tourism":
            response_text = self.responses["tourism"].get(detected_lang, self.responses["tourism"]["en"])
            suggestions = ["Victoria Falls tour", "Safari experiences", "Cape Town attractions"]
            related_actions = ["explore_tourism", "book_tour"]
        
        elif intent == "payment":
            response_text = self.responses["payment"].get(detected_lang, self.responses["payment"]["en"])
            suggestions = ["Ecocash payment", "Bank transfer", "Mobile money options"]
            related_actions = ["payment_methods", "mobile_money"]
        
        elif intent == "shipping":
            response_text = self.responses["shipping"].get(detected_lang, self.responses["shipping"]["en"])
            suggestions = ["Sea freight rates", "Air freight options", "Customs requirements"]
            related_actions = ["shipping_options", "customs_info"]
        
        elif intent == "risk_assessment":
            response_text = self.responses["risk_assessment"].get(detected_lang, self.responses["risk_assessment"]["en"])
            suggestions = ["Verify a supplier", "Assess transaction risk", "Check certifications"]
            related_actions = ["risk_assessment", "verify_partner"]
        
        elif intent == "greeting":
            response_text = self.responses["greeting"].get(detected_lang, self.responses["greeting"]["en"])
            suggestions = ["Find products", "Translate", "Tourism info"]
            related_actions = ["search_products", "translate", "explore_tourism"]
        
        elif intent == "help":
            response_text = self.responses["help"].get(detected_lang, self.responses["help"]["en"])
            suggestions = ["Find suppliers", "Translate text", "Tourism recommendations"]
            related_actions = ["search_products", "translate", "explore_tourism"]
        
        elif intent == "ar_experience":
            response_text = self.responses["ar_experience"].get(detected_lang, self.responses["ar_experience"]["en"])
            suggestions = ["Try AR product scan", "Tourism AR", "Product preview"]
            related_actions = ["ar_scan", "ar_tourism"]
        
        else:
            if entities["products"]:
                product = entities["products"][0]
                if product in self.trade_knowledge:
                    response_text = self.trade_knowledge[product].get(detected_lang, self.trade_knowledge[product]["en"])
                else:
                    response_text = self.responses["unknown"].get(detected_lang, self.responses["unknown"]["en"])
            else:
                response_text = self.responses["unknown"].get(detected_lang, self.responses["unknown"]["en"])
            suggestions = ["Find suppliers", "Translate", "Get recommendations"]
            related_actions = ["search_products", "translate", "get_recommendations"]
        
        if mode == "trade":
            if "Find suppliers" not in suggestions:
                suggestions.insert(0, "Find suppliers")
            if "Get trade recommendations" not in suggestions:
                suggestions.append("Get trade recommendations")
        elif mode == "travel":
            if "Tourism recommendations" not in suggestions:
                suggestions.insert(0, "Tourism recommendations")
        
        return ChatResponse(
            content=response_text,
            intent=intent,
            confidence=confidence,
            suggestions=suggestions[:4],
            related_actions=related_actions,
            language_detected=detected_lang
        )
