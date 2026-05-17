"""
Tourista AR AI Model - Data Integration Module
Loads and integrates AI datasets with the model engines
"""

import os
import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path

class DataLoader:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            base_dir = Path(__file__).parent
            data_dir = base_dir / "AI Data sets "

        self.data_dir = Path(data_dir)
        self.datasets = {}
        self._load_all_datasets()

    def _load_all_datasets(self):
        print("Loading AI datasets...")
        print(f"Data directory: {self.data_dir}")

        if not self.data_dir.exists():
            print(f"Warning: Data directory not found: {self.data_dir}")
            return

        csv_files = list(self.data_dir.glob("*.csv"))
        xlsx_files = list(self.data_dir.glob("*.xlsx"))

        for csv_file in csv_files:
            self._load_csv_file(csv_file)

        for xlsx_file in xlsx_files:
            self._load_xlsx_file(xlsx_file)

        print(f"\nLoaded {len(self.datasets)} datasets:")
        for name in self.datasets.keys():
            print(f"  ✓ {name}")

    def _load_csv_file(self, filepath: Path):
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            dataset_name = filepath.stem
            self.datasets[dataset_name] = df
            print(f"  ✓ Loaded {dataset_name}: {len(df)} rows")
        except Exception as e:
            print(f"  ✗ Error loading {filepath.name}: {str(e)}")

    def _load_xlsx_file(self, filepath: Path):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            dataset_name = filepath.stem
            self.datasets[dataset_name] = df
            print(f"  ✓ Loaded {dataset_name}: {len(df)} rows")
        except ImportError:
            print(f"  ⚠ openpyxl not installed. Skipping {filepath.name}")
            print(f"    Install with: pip install openpyxl")
        except Exception as e:
            print(f"  ✗ Error loading {filepath.name}: {str(e)}")

    def get_translation_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'translation' in name.lower() or 'multil' in name.lower():
                return df
        return None

    def get_matching_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'matching' in name.lower() or 'buyer' in name.lower() or 'supplier' in name.lower():
                return df
        return None

    def get_risk_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'cash' in name.lower() or 'payment' in name.lower() or 'unbanked' in name.lower() or 'risk' in name.lower():
                return df
        return None

    def get_trade_rules_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'trade' in name.lower() or 'rules' in name.lower() or 'cross' in name.lower():
                return df
        return None

    def get_faq_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'faq' in name.lower() or 'customer' in name.lower():
                return df
        return None

    def get_tourism_data(self) -> Optional[pd.DataFrame]:
        for name, df in self.datasets.items():
            if 'tourism' in name.lower() or 'travel' in name.lower():
                return df
        return None

    def list_all_datasets(self) -> List[str]:
        return list(self.datasets.keys())

    def get_dataset_info(self) -> Dict[str, Dict]:
        info = {}
        for name, df in self.datasets.items():
            info[name] = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": list(df.columns),
                "has_data": len(df) > 0
            }
        return info


class TranslationDataPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_translation_pairs(self) -> Dict[str, List[Dict]]:
        df = self.data_loader.get_translation_data()

        if df is None or df.empty:
            print("Warning: No translation data found")
            return {}

        pairs = {
            "zh-en": [],
            "zh-sn": [],
            "zh-nd": [],
            "zh-zu": [],
            "en-sn": [],
            "en-nd": [],
            "en-zu": []
        }

        for idx, row in df.iterrows():
            try:
                chinese = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                english = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                local_lang = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                scene = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""

                if chinese and english and chinese != "[fill more]":
                    pairs["zh-en"].append({
                        "source": chinese,
                        "target": english,
                        "scene": scene
                    })

                if english and local_lang and english != "[fill more]" and local_lang != "[fill more]":
                    if "Shona" in str(row.iloc[2]) or "sn" in local_lang.lower():
                        pairs["en-sn"].append({
                            "source": english,
                            "target": local_lang,
                            "scene": scene
                        })
                    if "Zulu" in str(row.iloc[2]) or "zu" in local_lang.lower():
                        pairs["en-zu"].append({
                            "source": english,
                            "target": local_lang,
                            "scene": scene
                        })

            except Exception as e:
                continue

        return pairs

    def get_business_terms(self) -> Dict[str, Dict]:
        terms = {
            "trade": {},
            "payment": {},
            "logistics": {},
            "business": {}
        }

        pairs = self.prepare_translation_pairs()

        for zh_term, en_term in pairs.get("zh-en", []):
            for category in ["trade", "payment", "logistics", "business"]:
                if category in str(pairs.get("zh-en", [])).lower():
                    terms["trade"][zh_term] = en_term

        return terms


class MatchingDataPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_buyer_needs(self) -> List[Dict]:
        df = self.data_loader.get_matching_data()

        if df is None or df.empty:
            return []

        buyer_needs = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 5:
                    need_zh = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    need_en = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    product = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                    country = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
                    category = str(row.iloc[4]) if pd.notna(row.iloc[4]) else ""

                    if need_zh and need_zh != "[fill more]":
                        buyer_needs.append({
                            "need_zh": need_zh,
                            "need_en": need_en,
                            "product": product,
                            "country": country,
                            "category": category
                        })

            except Exception as e:
                continue

        return buyer_needs

    def prepare_supplier_offers(self) -> List[Dict]:
        df = self.data_loader.get_matching_data()

        if df is None or df.empty:
            return []

        supplier_offers = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 4:
                    country = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
                    product = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                    category = str(row.iloc[4]) if pd.notna(row.iloc[4]) else ""

                    if product and product != "[fill more]":
                        supplier_offers.append({
                            "product": product,
                            "country": country,
                            "category": category
                        })

            except Exception as e:
                continue

        return supplier_offers


class RiskDataPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_risk_profiles(self) -> List[Dict]:
        df = self.data_loader.get_risk_data()

        if df is None or df.empty:
            return []

        risk_profiles = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 3:
                    behavior = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    risk_level = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    suggestion = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""

                    if behavior and behavior != "[fill more]":
                        risk_profiles.append({
                            "behavior": behavior,
                            "risk_level": risk_level,
                            "suggestion": suggestion
                        })

            except Exception as e:
                continue

        return risk_profiles


class TradeRulesPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_trade_rules(self) -> List[Dict]:
        df = self.data_loader.get_trade_rules_data()

        if df is None or df.empty:
            return []

        trade_rules = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 3:
                    question = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    answer = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    country = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""

                    if question and question != "[fill more]":
                        trade_rules.append({
                            "question": question,
                            "answer": answer,
                            "country": country
                        })

            except Exception as e:
                continue

        return trade_rules


class TourismDataPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_tourism_spots(self) -> List[Dict]:
        df = self.data_loader.get_tourism_data()

        if df is None or df.empty:
            return []

        tourism_spots = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 5:
                    city = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    country = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                    attraction = str(row.iloc[2]) if pd.notna(row.iloc[2]) else ""
                    description = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
                    price_range = str(row.iloc[4]) if pd.notna(row.iloc[4]) else ""

                    if city and city != "[fill more]":
                        tourism_spots.append({
                            "city": city,
                            "country": country,
                            "attraction": attraction,
                            "description": description,
                            "price_range": price_range
                        })

            except Exception as e:
                continue

        return tourism_spots


class FAQDataPreparer:
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    def prepare_faq_pairs(self) -> List[Dict]:
        df = self.data_loader.get_faq_data()

        if df is None or df.empty:
            return []

        faq_pairs = []

        for idx, row in df.iterrows():
            try:
                if len(row) >= 2:
                    question = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                    answer = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""

                    if question and question != "[fill more]":
                        faq_pairs.append({
                            "question": question,
                            "answer": answer
                        })

            except Exception as e:
                continue

        return faq_pairs


def integrate_datasets_with_model(model):
    print("\n" + "="*70)
    print("INTEGRATING DATASETS WITH AI MODEL")
    print("="*70)

    data_loader = DataLoader()

    print("\n" + "-"*70)
    print("Dataset Overview:")
    print("-"*70)
    info = data_loader.get_dataset_info()
    for name, details in info.items():
        print(f"\n{name}:")
        print(f"  Rows: {details['rows']}")
        print(f"  Columns: {details['columns']}")
        print(f"  Column Names: {', '.join(details['column_names'])}")

    print("\n" + "-"*70)
    print("Preparing data for each engine:")
    print("-"*70)

    translation_prep = TranslationDataPreparer(data_loader)
    translation_pairs = translation_prep.prepare_translation_pairs()
    print(f"\n✓ Translation Pairs:")
    for pair_type, pairs in translation_pairs.items():
        print(f"  {pair_type}: {len(pairs)} pairs")

    matching_prep = MatchingDataPreparer(data_loader)
    buyer_needs = matching_prep.prepare_buyer_needs()
    supplier_offers = matching_prep.prepare_supplier_offers()
    print(f"\n✓ Matching Data:")
    print(f"  Buyer Needs: {len(buyer_needs)}")
    print(f"  Supplier Offers: {len(supplier_offers)}")

    risk_prep = RiskDataPreparer(data_loader)
    risk_profiles = risk_prep.prepare_risk_profiles()
    print(f"\n✓ Risk Profiles: {len(risk_profiles)}")

    trade_prep = TradeRulesPreparer(data_loader)
    trade_rules = trade_prep.prepare_trade_rules()
    print(f"\n✓ Trade Rules: {len(trade_rules)}")

    tourism_prep = TourismDataPreparer(data_loader)
    tourism_spots = tourism_prep.prepare_tourism_spots()
    print(f"\n✓ Tourism Spots: {len(tourism_spots)}")

    faq_prep = FAQDataPreparer(data_loader)
    faq_pairs = faq_prep.prepare_faq_pairs()
    print(f"\n✓ FAQ Pairs: {len(faq_pairs)}")

    print("\n" + "="*70)
    print("DATASET INTEGRATION COMPLETE")
    print("="*70)

    return {
        "translation_pairs": translation_pairs,
        "buyer_needs": buyer_needs,
        "supplier_offers": supplier_offers,
        "risk_profiles": risk_profiles,
        "trade_rules": trade_rules,
        "tourism_spots": tourism_spots,
        "faq_pairs": faq_pairs
    }


if __name__ == "__main__":
    print("Tourista AR AI Model - Dataset Integration Tool")
    print("="*70)

    data_loader = DataLoader()

    info = data_loader.get_dataset_info()

    print("\nAvailable Datasets:")
    print("-"*70)
    for name, details in info.items():
        print(f"\n{name}:")
        print(f"  Rows: {details['rows']}")
        print(f"  Columns: {details['columns']}")
        print(f"  Sample columns: {', '.join(details['column_names'][:3])}")
