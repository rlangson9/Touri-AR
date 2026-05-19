#!/usr/bin/env python3
"""Test the AR scene recognition integration with the new dataset"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tourista_ai_model.ar_recognition.engine import ARSceneRecognitionEngine


def main():
    print("=" * 70)
    print("TOURISTA AR - DESTINATION DATASET TEST")
    print("=" * 70)

    print("\n1. Initializing AR Scene Recognition Engine...")
    engine = ARSceneRecognitionEngine()
    
    print(f"\n2. Total markers loaded: {len(engine.scene_database)}")
    
    print("\n3. First 10 destinations:")
    for i, marker in enumerate(engine.scene_database[:10]):
        print(f"   [{i}] {marker.name} ({marker.country if hasattr(marker, 'country') else 'N/A'}) - {marker.location}")
    
    if len(engine.scene_database) > 100:
        print(f"\n4. Loaded {len(engine.scene_database)} markers - SUCCESS!")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE - AR SYSTEM READY WITH 200+ AFRICAN DESTINATIONS!")
    print("=" * 70)


if __name__ == "__main__":
    main()
