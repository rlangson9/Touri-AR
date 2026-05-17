#!/usr/bin/env python3
"""
Tourista AR - Mobile App Integration Test
Demonstrates how the AI Model integrates with a cross-border super app
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

class TouristaAppIntegration:
    def __init__(self, api_base_url=API_BASE_URL):
        self.api_base_url = api_base_url
        self.session = requests.Session()
    
    def test_translation_feature(self):
        """Test multi-language translation for in-app use"""
        print("\n📱 Testing Translation Feature...")
        print("-" * 60)
        
        test_cases = [
            {
                "text": "I want to buy high-quality African handicrafts",
                "source": "en",
                "target": "zh",
                "description": "English → Chinese (Buyer)"
            },
            {
                "text": "我想买高质量的非洲手工艺品",
                "source": "zh",
                "target": "en",
                "description": "Chinese → English (Supplier)"
            },
            {
                "text": "Ndiri kutenga zvigadzi zvine hunyanzvi",
                "source": "sn",
                "target": "zh",
                "description": "Shona → Chinese (Local Vendor)"
            },
            {
                "text": "Imali yakawanda",
                "source": "zu",
                "target": "en",
                "description": "Zulu → English"
            }
        ]
        
        for case in test_cases:
            try:
                response = self.session.post(
                    f"{self.api_base_url}/translate",
                    json={
                        "text": case["text"],
                        "source_language": case["source"],
                        "target_language": case["target"]
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ {case['description']}")
                    print(f"   Source: {case['text']}")
                    print(f"   Target: {result['translated_text']}")
                    print(f"   Confidence: {result['confidence']:.2%}\n")
                else:
                    print(f"❌ {case['description']} - Error: {response.status_code}")
            except Exception as e:
                print(f"❌ {case['description']} - Exception: {e}")
    
    def test_buyer_registration(self):
        """Test buyer registration flow"""
        print("\n📱 Testing Buyer Registration...")
        print("-" * 60)
        
        buyer_data = {
            "user_id": "CN_BUYER_001",
            "name": "张伟",
            "role": "chinese_buyer",
            "country": "China",
            "region": "Shanghai",
            "email": "zhangwei@chinabuyer.cn",
            "phone": "+8613800138000",
            "languages": ["zh", "en"],
            "business_type": "import_trading",
            "product_interests": ["handicrafts", "textiles", "coffee", "tea"],
            "preferred_payment_methods": ["bank_transfer", "mobile_money"],
            "budget_range_min": 1000,
            "budget_range_max": 10000
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/users/register",
                json=buyer_data
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Buyer Registered Successfully")
                print(f"   Success: {result['success']}")
                print(f"   User ID: {result['user_id']}")
                return result['user_id']
            else:
                print(f"❌ Registration Failed: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"❌ Registration Exception: {e}")
            return None
    
    def test_supplier_registration(self):
        """Test supplier registration flow"""
        print("\n📱 Testing Supplier Registration...")
        print("-" * 60)
        
        supplier_data = {
            "user_id": "ZW_SUPPLIER_001",
            "name": "Tawanda Mutasa",
            "role": "african_supplier",
            "country": "Zimbabwe",
            "region": "Harare",
            "email": "tawanda@zimbabwesupplier.co.zw",
            "phone": "+263772123456",
            "languages": ["en", "sn"],
            "business_type": "crafts_production",
            "product_offers": ["handicrafts", "wood_carvings", "pottery"],
            "verification_status": "verified",
            "rating": 4.8,
            "total_transactions": 100
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/users/register",
                json=supplier_data
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Supplier Registered Successfully")
                print(f"   Success: {result['success']}")
                print(f"   User ID: {result['user_id']}")
                return result['user_id']
            else:
                print(f"❌ Registration Failed: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"❌ Registration Exception: {e}")
            return None
    
    def test_product_listing(self):
        """Test product listing for suppliers"""
        print("\n📱 Testing Product Listing...")
        print("-" * 60)
        
        product_data = {
            "product_id": "PROD_ZW_001",
            "supplier_id": "ZW_SUPPLIER_001",
            "name": "Hand-carved Wooden Elephant",
            "category": "handicrafts",
            "description": "Beautiful hand-carved wooden elephant from Zimbabwe",
            "price": 85.00,
            "currency": "USD",
            "available_quantity": 50,
            "min_order_quantity": 5,
            "location": "Harare, Zimbabwe",
            "images": ["elephant_1.jpg", "elephant_2.jpg"]
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/products/register",
                json=product_data
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Product Listed Successfully")
                print(f"   Success: {result['success']}")
                print(f"   Product ID: {result['product_id']}")
                return result['product_id']
            else:
                print(f"❌ Product Listing Failed: {response.json().get('detail', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"❌ Product Listing Exception: {e}")
            return None
    
    def test_matching_engine(self, buyer_id):
        """Test buyer-supplier matching"""
        print("\n📱 Testing Matching Engine...")
        print("-" * 60)
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/matching/find",
                json={
                    "user_id": buyer_id,
                    "match_type": "B2B_TRADE",
                    "limit": 5
                }
            )
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Matching Engine Results")
                print(f"   Found {len(results)} matches")
                if results and isinstance(results, list):
                    for i in range(min(3, len(results))):
                        match = results[i]
                        print(f"\n   Match {i+1}:")
                        print(f"     Supplier ID: {match.get('supplier_id', 'N/A')}")
                        print(f"     Country: {match.get('country', 'N/A')}")
                        print(f"     Match Score: {match.get('similarity_score', 0):.2%}")
            else:
                print(f"❌ Matching Failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Matching Exception: {e}")
    
    def test_risk_analysis(self):
        """Test risk analysis for cash-based transactions"""
        print("\n📱 Testing Risk Analysis...")
        print("-" * 60)
        
        transaction_data = {
            "transaction_id": "TXN_2024_0001",
            "counterparty_id": "ZW_SUPPLIER_001",
            "counterparty_type": "supplier",
            "payment_method": "mobile_money",
            "amount": 2500,
            "currency": "USD",
            "buyer_country": "China",
            "seller_country": "Zimbabwe",
            "mobile_money_provider": "ecocash"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/risk/assess",
                json=transaction_data
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Risk Assessment Completed")
                print(f"   Risk Score: {result.get('risk_score', 0):.2%}")
                print(f"   Risk Level: {result.get('risk_level', 'unknown').upper()}")
                print(f"   Approval Status: {result.get('approval_status', 'unknown').replace('_', ' ').title()}")
                
                if result.get('identified_risks'):
                    print("\n   Identified Risks:")
                    for risk in result['identified_risks'][:3]:
                        print(f"     • {risk['name']} ({risk['severity'].upper()})")
                
                if result.get('recommendations'):
                    print("\n   Recommendations:")
                    for rec in result['recommendations'][:3]:
                        print(f"     • {rec}")
            else:
                print(f"❌ Risk Analysis Failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Risk Analysis Exception: {e}")
    
    def test_recommendations(self, user_id):
        """Test personalized recommendations"""
        print("\n📱 Testing Recommendations...")
        print("-" * 60)
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/recommendations",
                json={
                    "user_id": user_id,
                    "user_type": "chinese_buyer",
                    "limit": 5
                }
            )
            if response.status_code == 200:
                results = response.json()
                print(f"✅ Recommendations Generated")
                print(f"   Found {len(results)} recommendations")
                if results and isinstance(results, list):
                    for i in range(min(3, len(results))):
                        rec = results[i]
                        print(f"\n   Recommendation {i+1}:")
                        print(f"     Type: {rec['recommendation_type'].replace('_', ' ').title()}")
                        print(f"     Title: {rec['title']}")
                        print(f"     Priority: {rec['priority_score']:.2%}")
            else:
                print(f"❌ Recommendations Failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Recommendations Exception: {e}")
    
    def test_ar_tourism(self):
        """Test AR tourism experience"""
        print("\n📱 Testing AR Tourism Experience...")
        print("-" * 60)
        
        tourism_spots = ["victoria_falls", "great_zimbabwe", "table_mountain"]
        
        for spot_id in tourism_spots[:2]:
            try:
                response = self.session.get(f"{self.api_base_url}/ar/tourism/{spot_id}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ AR Experience: {result.get('name', 'N/A')}")
                    print(f"   Country: {result.get('country', 'N/A')}")
                    print(f"   Best Season: {result.get('best_season', 'N/A')}")
                    
                    if result.get('tour_options'):
                        print("   Tour Options:")
                        for tour in result['tour_options'][:2]:
                            print(f"     • {tour['name']}: ${tour['price_usd']} ({tour['duration']})")
                    print()
                else:
                    print(f"❌ AR Tourism Failed for {spot_id}: {response.status_code}")
            except Exception as e:
                print(f"❌ AR Tourism Exception for {spot_id}: {e}")
    
    def test_health_check(self):
        """Test API health status"""
        print("\n📱 Testing API Health...")
        print("-" * 60)
        
        try:
            response = self.session.get(f"{self.api_base_url}/health")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API Health Check")
                print(f"   Status: {result['status'].upper()}")
                print(f"   Version: {result['version']}")
                print(f"   Services:")
                for service, status in result.get('services', {}).items():
                    print(f"     • {service}: {status}")
                return True
            else:
                print(f"❌ API Unhealthy: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health Check Failed: {e}")
            return False
    
    def run_full_integration_test(self):
        """Run complete app integration test"""
        print("=" * 70)
        print("TOURISTA AR - MOBILE APP INTEGRATION TEST")
        print("=" * 70)
        
        if not self.test_health_check():
            print("\n❌ API Server is not running! Please start the server first.")
            return
        
        self.test_translation_feature()
        buyer_id = self.test_buyer_registration()
        self.test_supplier_registration()
        self.test_product_listing()
        
        if buyer_id:
            self.test_matching_engine(buyer_id)
            self.test_recommendations(buyer_id)
        
        self.test_risk_analysis()
        self.test_ar_tourism()
        
        print("\n" + "=" * 70)
        print("✅ ALL INTEGRATION TESTS COMPLETED!")
        print("=" * 70)
        print("\n📱 Tourista AR AI Model is ready for mobile app integration!")

if __name__ == "__main__":
    integration = TouristaAppIntegration()
    integration.run_full_integration_test()
