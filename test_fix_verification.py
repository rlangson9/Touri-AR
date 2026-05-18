#!/usr/bin/env python3
"""
Test verification of the three issues fixed
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tourista_ai_model.translation import ml_engine as translation_ml

def verify_issue_1():
    """Issue 1: Corrupted Zulu translation for 'cheap'"""
    print("\n" + "="*70)
    print("VERIFYING ISSUE 1: Corrupted Zulu translation")
    print("="*70)
    
    slang_db = translation_ml.MLTranslationEngine._load_slang_database(translation_ml.MLTranslationEngine())
    zulu_cheap = slang_db['cheap']['zu']
    
    if zulu_cheap == 'ngababayo':
        print(f"✅ FIXED: Zulu 'cheap' translation is correct: '{zulu_cheap}'")
        return True
    else:
        print(f"❌ NOT FIXED: Found '{zulu_cheap}' instead of 'ngababayo'")
        return False

def verify_issue_2():
    """Issue 2: Incorrect NLLB language code for Chinese"""
    print("\n" + "="*70)
    print("VERIFYING ISSUE 2: Incorrect NLLB code for Chinese")
    print("="*70)
    
    engine = translation_ml.MLTranslationEngine()
    nllb_code = engine._get_nllb_code('zh')
    
    if nllb_code == 'zho_Hans':
        print(f"✅ FIXED: NLLB code for Chinese is correct: '{nllb_code}'")
        return True
    else:
        print(f"❌ NOT FIXED: Found '{nllb_code}' instead of 'zho_Hans'")
        return False

def verify_issue_3():
    """Issue 3: Incorrect slang detection logic"""
    print("\n" + "="*70)
    print("VERIFYING ISSUE 3: Slang detection logic")
    print("="*70)
    
    engine = translation_ml.MLTranslationEngine()
    
    # Test case: Zulu text with 'imali' (money)
    test_text = "Ngifuna imali"
    detected_slang = engine._detect_slang(test_text, 'zu')
    
    if 'money' in detected_slang:
        print(f"✅ FIXED: Slang detection logic works correctly")
        print(f"   Test text: '{test_text}'")
        print(f"   Detected slang: {detected_slang}")
        return True
    else:
        print(f"❌ NOT FIXED: Slang detection logic incorrect")
        print(f"   Test text: '{test_text}'")
        print(f"   Detected slang: {detected_slang}")
        return False

if __name__ == "__main__":
    print("="*70)
    print("ISSUE FIX VERIFICATION")
    print("="*70)
    
    all_passed = verify_issue_1() and verify_issue_2() and verify_issue_3()
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL THREE ISSUES FIXED!")
    else:
        print("❌ Some issues still need fixing")
    print("="*70)
