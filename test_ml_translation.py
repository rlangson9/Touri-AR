#!/usr/bin/env python3
"""
Test script for ML Translation Engine
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*70)
print("ML TRANSLATION ENGINE - COMPREHENSIVE TEST")
print("="*70)

try:
    from tourista_ai_model.translation.ml_engine import MLTranslationEngine, HybridTranslationEngine
    
    print("\n🚀 Initializing ML Translation Engine...")
    print("   Loading models (this may take a moment on first run)...")
    
    ml_engine = MLTranslationEngine()
    
    print("\n" + "="*70)
    print("TEST 1: Basic Translations")
    print("="*70)
    
    test_cases = [
        ("Hello, I want to buy handicrafts", "en", "zh", "English → Chinese"),
        ("我想买高质量的非洲手工艺品", "zh", "en", "Chinese → English"),
        ("Good morning, how much?", "en", "sn", "English → Shona"),
        ("Unjani, ngubani?", "zu", "en", "Zulu → English"),
        ("Kunjani, ngubani?", "xh", "en", "Xhosa → English"),
    ]
    
    results = []
    for text, source, target, description in test_cases:
        print(f"\n🌐 {description}")
        print(f"   Original: {text}")
        
        try:
            result = ml_engine.translate(text, source, target)
            print(f"   ✅ Translated: {result.translated_text}")
            print(f"   📊 Confidence: {result.confidence:.2%}")
            print(f"   🤖 Model: {result.model_used}")
            print(f"   ⏱️  Time: {result.processing_time_ms:.2f}ms")
            
            if result.business_terms_found:
                print(f"   💼 Business Terms: {', '.join(result.business_terms_found)}")
            
            results.append({
                'description': description,
                'success': True,
                'confidence': result.confidence
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'description': description,
                'success': False,
                'error': str(e)
            })
    
    print("\n" + "="*70)
    print("TEST 2: Business Terminology")
    print("="*70)
    
    business_texts = [
        ("I need invoice for wholesale payment", "en", "zh"),
        ("Supplier confirmed shipping customs clearance", "en", "sn"),
        ("Negotiate wholesale price for handicrafts", "en", "zu"),
    ]
    
    for text, source, target in business_texts:
        print(f"\n💼 Business Text: {text}")
        result = ml_engine.translate(text, source, target)
        print(f"   Translated: {result.translated_text}")
        print(f"   Terms Found: {result.business_terms_found if result.business_terms_found else 'None'}")
    
    print("\n" + "="*70)
    print("TEST 3: Batch Translation")
    print("="*70)
    
    batch_texts = [
        "Hello, how are you?",
        "I want to buy handicrafts",
        "What is the price?",
        "Can you ship to China?",
        "Thank you very much"
    ]
    
    print(f"   Translating {len(batch_texts)} texts...")
    batch_results = ml_engine.batch_translate(batch_texts, "en", "zh")
    
    for i, result in enumerate(batch_results):
        print(f"   {i+1}. {batch_texts[i]}")
        print(f"      → {result.translated_text}")
    
    print("\n" + "="*70)
    print("TEST 4: Hybrid Engine (ML + Rules)")
    print("="*70)
    
    print("\n   Initializing Hybrid Engine...")
    hybrid_engine = HybridTranslationEngine()
    
    hybrid_texts = [
        ("Buy handicrafts wholesale", "en", "zh"),
        ("Ship to Zimbabwe supplier", "en", "sn"),
        ("Negotiate payment invoice", "en", "zu"),
    ]
    
    for text, source, target in hybrid_texts:
        print(f"\n🔄 Hybrid: {text}")
        result = hybrid_engine.translate(text, source, target)
        print(f"   Translated: {result.translated_text}")
        print(f"   Model: {result.model_used}")
        print(f"   Confidence: {result.confidence:.2%}")
    
    print("\n" + "="*70)
    print("TEST 5: Performance Benchmark")
    print("="*70)
    
    import time
    
    single_text = "I want to buy high-quality African handicrafts from verified supplier"
    
    print(f"\n   Benchmarking single translation...")
    iterations = 3
    
    times = []
    for i in range(iterations):
        start = time.time()
        result = ml_engine.translate(single_text, "en", "zh")
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)
        print(f"   Run {i+1}: {elapsed:.2f}ms")
    
    avg_time = sum(times) / len(times)
    print(f"\n   Average translation time: {avg_time:.2f}ms")
    
    print("\n" + "="*70)
    print("TEST RESULTS SUMMARY")
    print("="*70)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    print(f"\n✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count > 0:
        avg_confidence = sum(r['confidence'] for r in results if r['success']) / success_count
        print(f"📊 Average Confidence: {avg_confidence:.2%}")
    
    print("\n" + "="*70)
    print("🎉 ML TRANSLATION ENGINE TEST COMPLETED!")
    print("="*70)
    
    print("\n🚀 Next Steps:")
    print("   1. Install required packages: pip install transformers torch")
    print("   2. First run will download models (~1-2GB)")
    print("   3. Use GPU for faster translation (CUDA)")
    print("   4. Integrate with FastAPI endpoints")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\n💡 To fix this, install the required packages:")
    print("   pip install transformers torch")
    print("   pip install accelerate  # for better performance")
    
except Exception as e:
    print(f"\n❌ Test Failed: {e}")
    import traceback
    traceback.print_exc()
