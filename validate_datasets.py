#!/usr/bin/env python3
"""
Tourista AR AI Model - Dataset Validation Script
Validates that all datasets are properly formatted and compatible
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tourista_ai_model.data_loader import DataLoader

def validate_datasets():
    print("="*70)
    print("TOURISTA AR AI MODEL - DATASET VALIDATION")
    print("="*70)

    print("\nInitializing data loader...")
    loader = DataLoader()

    print("\n" + "-"*70)
    print("VALIDATION RESULTS")
    print("-"*70)

    datasets = loader.list_all_datasets()

    print(f"\n✅ Total datasets found: {len(datasets)}")

    info = loader.get_dataset_info()

    all_valid = True

    for name, details in info.items():
        print(f"\n📊 Dataset: {name}")
        print(f"   Status: ", end="")

        if details['has_data']:
            print("✅ Has data")
        else:
            print("❌ Empty dataset")
            all_valid = False

        print(f"   Rows: {details['rows']}")
        print(f"   Columns: {details['columns']}")
        print(f"   Column Names:")
        for col in details['column_names']:
            print(f"     - {col}")

        if details['rows'] < 10:
            print(f"   ⚠️  WARNING: Dataset has less than 10 rows - needs expansion")

    print("\n" + "-"*70)
    print("ENGINE INTEGRATION TEST")
    print("-"*70)

    tests = [
        ("Translation Data", loader.get_translation_data, "Translation Engine"),
        ("Matching Data", loader.get_matching_data, "Matching System"),
        ("Risk Data", loader.get_risk_data, "Risk Analysis Engine"),
        ("Trade Rules Data", loader.get_trade_rules_data, "Recommendation Engine"),
        ("FAQ Data", loader.get_faq_data, "Chatbot System"),
        ("Tourism Data", loader.get_tourism_data, "Tourism Engine")
    ]

    for dataset_name, getter_func, engine_name in tests:
        data = getter_func()
        if data is not None and not data.empty:
            print(f"\n✅ {dataset_name} → {engine_name}")
            print(f"   Rows loaded: {len(data)}")
        else:
            print(f"\n❌ {dataset_name} → {engine_name}")
            print(f"   ERROR: Failed to load dataset")
            all_valid = False

    print("\n" + "-"*70)
    print("FINAL VALIDATION")
    print("-"*70)

    if all_valid:
        print("\n✅ ALL DATASETS VALIDATED SUCCESSFULLY")
        print("\nThe datasets are properly formatted and compatible with the model.")
        print("All engines can access their required data.")
    else:
        print("\n⚠️  SOME DATASETS NEED ATTENTION")
        print("\nPlease review the warnings above and expand the datasets as needed.")

    print("\n" + "="*70)
    print("VALIDATION COMPLETE")
    print("="*70)

    return all_valid

if __name__ == "__main__":
    success = validate_datasets()
    sys.exit(0 if success else 1)
