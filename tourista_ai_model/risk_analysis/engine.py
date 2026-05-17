"""
Risk Analysis Module for Tourista AR
Cash-based Payment Solutions & Unbanked Population Risk Assessment
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math

class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"

class RiskCategory(Enum):
    PAYMENT_RISK = "payment_risk"
    FRAUD_RISK = "fraud_risk"
    COMPLIANCE_RISK = "compliance_risk"
    OPERATIONAL_RISK = "operational_risk"
    CURRENCY_RISK = "currency_risk"
    LOGISTICS_RISK = "logistics_risk"
    REPUTATIONAL_RISK = "reputational_risk"

class PaymentMethod(Enum):
    CASH = "cash"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    AGENT_COLLECTION = "agent_collection"
    CRYPTO = "cryptocurrency"
    LETTER_OF_CREDIT = "letter_of_credit"

@dataclass
class RiskFactor:
    factor_id: str
    category: RiskCategory
    name: str
    description: str
    severity: RiskLevel
    probability: float
    impact: float
    indicators: List[str]
    mitigation_strategies: List[str]
    monitoring_required: bool

@dataclass
class RiskAssessment:
    assessment_id: str
    transaction_id: Optional[str]
    counterparty_id: str
    counterparty_type: str
    payment_method: PaymentMethod
    transaction_amount: float
    currency: str
    risk_score: float
    risk_level: RiskLevel
    identified_risks: List[RiskFactor]
    overall_assessment: str
    recommendations: List[str]
    required_verifications: List[str]
    approval_status: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class UnbankedProfile:
    user_id: str
    country: str
    region: str
    mobile_money_registered: bool
    mobile_money_provider: Optional[str]
    has_cash_collection_point: bool
    nearest_agent_distance_km: float
    id_document_type: Optional[str]
    verification_level: str
    transaction_history_months: int
    avg_transaction_size: float
    transaction_frequency_per_month: int
    trust_score: float

class RiskAnalysisEngine:
    def __init__(self):
        self.risk_models = self._initialize_risk_models()
        self.mobile_money_networks = self._initialize_mobile_money_networks()
        self.fraud_patterns = self._initialize_fraud_patterns()
        self.compliance_rules = self._initialize_compliance_rules()
        self.assessment_history: List[RiskAssessment] = []

    def _initialize_risk_models(self) -> Dict[str, Dict]:
        return {
            "cash_risk": {
                "weight": 0.35,
                "factors": {
                    "large_cash_amount": {"threshold": 1000, "risk_boost": 0.2},
                    "unverified_counterparty": {"risk_boost": 0.15},
                    "first_transaction": {"risk_boost": 0.25},
                    "high_risk_region": {"risk_boost": 0.2}
                }
            },
            "mobile_money_risk": {
                "weight": 0.25,
                "factors": {
                    "unregistered_number": {"risk_boost": 0.2},
                    "new_account": {"risk_boost": 0.15},
                    "high_transaction_value": {"threshold": 500, "risk_boost": 0.1},
                    "rapid_successive_transactions": {"risk_boost": 0.15}
                }
            },
            "cross_border_risk": {
                "weight": 0.40,
                "factors": {
                    "currency_mismatch": {"risk_boost": 0.1},
                    "documentation_incomplete": {"risk_boost": 0.2},
                    "logistics_uncertain": {"risk_boost": 0.15},
                    "regulatory_change": {"risk_boost": 0.1}
                }
            }
        }

    def _initialize_mobile_money_networks(self) -> Dict[str, Dict]:
        return {
            "ecocash": {
                "country": "Zimbabwe",
                "provider": "Econet",
                "daily_limit": 500,
                "monthly_limit": 2000,
                "verification_required": ["national_id"],
                "known_issues": ["network_congestion", "system_outages"],
                "fraud_prevalence": "medium"
            },
            "onemoney": {
                "country": "Zimbabwe",
                "provider": "NetOne",
                "daily_limit": 400,
                "monthly_limit": 1500,
                "verification_required": ["national_id"],
                "known_issues": ["limited_agent_network"],
                "fraud_prevalence": "medium"
            },
            "m_pesa": {
                "country": "Kenya",
                "provider": "Safaricom",
                "daily_limit": 150000,
                "monthly_limit": 500000,
                "verification_required": ["national_id", "biometrics"],
                "known_issues": [],
                "fraud_prevalence": "low"
            },
            "snapscan": {
                "country": "South Africa",
                "provider": "SnapScan",
                "daily_limit": 5000,
                "monthly_limit": 20000,
                "verification_required": ["mobile_number"],
                "known_issues": ["limited_merchant_network"],
                "fraud_prevalence": "low"
            },
            "zapper": {
                "country": "South Africa",
                "provider": "Zapper",
                "daily_limit": 5000,
                "monthly_limit": 20000,
                "verification_required": ["mobile_number", "email"],
                "known_issues": ["technical_issues"],
                "fraud_prevalence": "low"
            }
        }

    def _initialize_fraud_patterns(self) -> List[Dict]:
        return [
            {
                "pattern_name": "round_amount_suspicion",
                "description": "Transactions with perfectly round amounts",
                "risk_boost": 0.15,
                "indicators": ["amount % 100 == 0", "no cents/ decimals"]
            },
            {
                "pattern_name": "velocity_fraud",
                "description": "Rapid multiple transactions in short period",
                "risk_boost": 0.25,
                "indicators": ["transactions > 3 in 1 hour", "same recipient multiple times"]
            },
            {
                "pattern_name": "phishing_indicators",
                "description": "User interaction patterns suggesting phishing",
                "risk_boost": 0.3,
                "indicators": ["unusual_login_time", "multiple_failed_verifications", "location_mismatch"]
            },
            {
                "pattern_name": "new_account_abuse",
                "description": "Newly created accounts with immediate high-value transactions",
                "risk_boost": 0.35,
                "indicators": ["account_age < 7 days", "first_transaction > 1000"]
            },
            {
                "pattern_name": "cash_splitting",
                "description": "Large transaction split into multiple smaller ones to avoid limits",
                "risk_boost": 0.4,
                "indicators": ["multiple_transactions within_minutes", "cumulative_amount > limit"]
            }
        ]

    def _initialize_compliance_rules(self) -> Dict[str, Dict]:
        return {
            "aml_thresholds": {
                "zimbabwe": {
                    "report_threshold": 10000,
                    "enhanced_monitoring": 5000,
                    "suspicious_activity": 1000
                },
                "south_africa": {
                    "report_threshold": 50000,
                    "enhanced_monitoring": 25000,
                    "suspicious_activity": 10000
                },
                "kenya": {
                    "report_threshold": 80000,
                    "enhanced_monitoring": 50000,
                    "suspicious_activity": 20000
                },
                "china": {
                    "report_threshold": 50000,
                    "enhanced_monitoring": 20000,
                    "suspicious_activity": 10000
                }
            },
            "kyc_requirements": {
                "low_risk": {
                    "max_transaction": 500,
                    "required_docs": ["phone_number"]
                },
                "medium_risk": {
                    "max_transaction": 5000,
                    "required_docs": ["national_id", "phone_number"]
                },
                "high_risk": {
                    "max_transaction": 10000,
                    "required_docs": ["national_id", "proof_of_address", "biometrics"]
                }
            },
            "currency_controls": {
                "zimbabwe": {
                    "restrictions": ["USD_export_limited", "ZWL_conversion_restricted"],
                    "reporting_required": ["all_transactions_over_500", "cross_border_payments"]
                },
                "south_africa": {
                    "restrictions": ["ZAR_export_limits"],
                    "reporting_required": ["cross_border_transfers_over_10000"]
                }
            }
        }

    def assess_transaction_risk(self, transaction_data: Dict,
                              counterparty_profile: Optional[UnbankedProfile] = None) -> RiskAssessment:
        base_risk_score = 0.5

        payment_method = PaymentMethod(transaction_data.get("payment_method", "cash"))
        amount = float(transaction_data.get("amount", 0))
        currency = transaction_data.get("currency", "USD")
        buyer_country = transaction_data.get("buyer_country", "China")
        seller_country = transaction_data.get("seller_country", "Zimbabwe")
        transaction_type = transaction_data.get("type", "B2B")

        identified_risks = []

        if payment_method == PaymentMethod.CASH:
            cash_risks = self._analyze_cash_risk(amount, counterparty_profile, transaction_data)
            identified_risks.extend(cash_risks)
            base_risk_score += self.risk_models["cash_risk"]["weight"] * 0.3

        elif payment_method == PaymentMethod.MOBILE_MONEY:
            mm_risks = self._analyze_mobile_money_risk(amount, counterparty_profile, transaction_data)
            identified_risks.extend(mm_risks)
            base_risk_score += self.risk_models["mobile_money_risk"]["weight"] * 0.2

        cross_border_risks = self._analyze_cross_border_risk(buyer_country, seller_country, transaction_data)
        identified_risks.extend(cross_border_risks)
        base_risk_score += self.risk_models["cross_border_risk"]["weight"] * 0.25

        fraud_risks = self._detect_fraud_patterns(transaction_data)
        identified_risks.extend(fraud_risks)
        base_risk_score += len(fraud_risks) * 0.05

        compliance_risks = self._check_compliance_requirements(amount, buyer_country, seller_country)
        identified_risks.extend(compliance_risks)

        risk_score = min(base_risk_score, 1.0)
        risk_level = self._determine_risk_level(risk_score)

        assessment = RiskAssessment(
            assessment_id=f"risk_{transaction_data.get('transaction_id', 'unknown')}_{int(datetime.now().timestamp())}",
            transaction_id=transaction_data.get("transaction_id"),
            counterparty_id=transaction_data.get("counterparty_id", ""),
            counterparty_type=transaction_data.get("counterparty_type", "unknown"),
            payment_method=payment_method,
            transaction_amount=amount,
            currency=currency,
            risk_score=risk_score,
            risk_level=risk_level,
            identified_risks=identified_risks,
            overall_assessment=self._generate_assessment_text(risk_level, identified_risks),
            recommendations=self._generate_recommendations(risk_level, identified_risks, payment_method),
            required_verifications=self._determine_required_verifications(identified_risks, risk_level),
            approval_status=self._determine_approval_status(risk_level)
        )

        self.assessment_history.append(assessment)
        return assessment

    def _analyze_cash_risk(self, amount: float, profile: Optional[UnbankedProfile],
                         transaction_data: Dict) -> List[RiskFactor]:
        risks = []

        if amount > 1000:
            risks.append(RiskFactor(
                factor_id="large_cash_amount",
                category=RiskCategory.PAYMENT_RISK,
                name="Large Cash Transaction",
                description=f"Transaction amount {amount} exceeds recommended cash limit",
                severity=RiskLevel.HIGH,
                probability=0.8,
                impact=0.7,
                indicators=["amount > 1000", "payment_method = cash"],
                mitigation_strategies=[
                    "Split into multiple mobile money transactions",
                    "Use bank transfer for amounts > 5000",
                    "Consider escrow service"
                ],
                monitoring_required=True
            ))

        if not profile or profile.verification_level == "unverified":
            risks.append(RiskFactor(
                factor_id="unverified_counterparty",
                category=RiskCategory.FRAUD_RISK,
                name="Unverified Counterparty",
                description="Counterparty has not completed identity verification",
                severity=RiskLevel.MEDIUM,
                probability=0.6,
                impact=0.6,
                indicators=["no_kyc_verification", "no_id_on_file"],
                mitigation_strategies=[
                    "Request identity verification before transaction",
                    "Start with smaller transaction to build trust",
                    "Use escrow service for protection"
                ],
                monitoring_required=True
            ))

        if not profile or profile.transaction_history_months < 3:
            risks.append(RiskFactor(
                factor_id="new_counterparty",
                category=RiskCategory.FRAUD_RISK,
                name="New Counterparty",
                description="Limited transaction history with this counterparty",
                severity=RiskLevel.MEDIUM,
                probability=0.5,
                impact=0.5,
                indicators=["transaction_history < 3 months", "total_transactions < 5"],
                mitigation_strategies=[
                    "Request references from previous partners",
                    "Start with smaller transaction amount",
                    "Consider using Trade Assurance"
                ],
                monitoring_required=True
            ))

        return risks

    def _analyze_mobile_money_risk(self, amount: float, profile: Optional[UnbankedProfile],
                                  transaction_data: Dict) -> List[RiskFactor]:
        risks = []
        provider = transaction_data.get("mobile_money_provider")
        if provider:
            provider = provider.lower()
        else:
            provider = ""

        provider_info = self.mobile_money_networks.get(provider, {})

        if not profile or not profile.mobile_money_registered:
            risks.append(RiskFactor(
                factor_id="unregistered_mobile_money",
                category=RiskCategory.PAYMENT_RISK,
                name="Unregistered Mobile Money Account",
                description=f"Mobile money account not properly registered or verified",
                severity=RiskLevel.HIGH,
                probability=0.7,
                impact=0.6,
                indicators=["account_status != active", "no_verification"],
                mitigation_strategies=[
                    "Verify mobile money account registration",
                    "Confirm identity with provider",
                    "Use alternative verified payment method"
                ],
                monitoring_required=True
            ))

        if provider_info.get("daily_limit", 0) < amount:
            risks.append(RiskFactor(
                factor_id="exceeds_daily_limit",
                category=RiskCategory.OPERATIONAL_RISK,
                name="Transaction Exceeds Daily Limit",
                description=f"Amount {amount} exceeds {provider} daily limit of {provider_info.get('daily_limit', 0)}",
                severity=RiskLevel.MEDIUM,
                probability=0.8,
                impact=0.4,
                indicators=[f"amount > {provider_info.get('daily_limit', 0)}", f"provider = {provider}"],
                mitigation_strategies=[
                    "Split transaction across multiple days",
                    "Request temporary limit increase from provider",
                    "Use alternative payment method for large amounts"
                ],
                monitoring_required=False
            ))

        if provider_info.get("fraud_prevalence") == "high":
            risks.append(RiskFactor(
                factor_id="high_fraud_network",
                category=RiskCategory.FRAUD_RISK,
                name="High Fraud Prevalence Network",
                description=f"{provider} network has elevated fraud rates in region",
                severity=RiskLevel.MEDIUM,
                probability=0.6,
                impact=0.5,
                indicators=[f"fraud_prevalence = high", f"provider = {provider}"],
                mitigation_strategies=[
                    "Verify recipient carefully before sending",
                    "Use confirmation codes for large transfers",
                    "Document all communications"
                ],
                monitoring_required=True
            ))

        return risks

    def _analyze_cross_border_risk(self, buyer_country: str, seller_country: str,
                                  transaction_data: Dict) -> List[RiskFactor]:
        risks = []

        currency_pair = f"{buyer_country}-{seller_country}"
        high_volatility_currencies = {
            "China-Zimbabwe": ["CNY-ZWL", "CNY-USD"],
            "China-Nigeria": ["CNY-NGN"],
            "China-Ethiopia": ["CNY-ETB"]
        }

        if currency_pair in high_volatility_currencies:
            risks.append(RiskFactor(
                factor_id="currency_fluctuation",
                category=RiskCategory.CURRENCY_RISK,
                name="High Currency Volatility",
                description=f"Currency pair {currency_pair} has high volatility",
                severity=RiskLevel.MEDIUM,
                probability=0.7,
                impact=0.6,
                indicators=["currency_pair in high_volatility_list", "no_hedging"],
                mitigation_strategies=[
                    "Use stable currency (USD) for pricing",
                    "Implement price adjustment clauses",
                    "Consider currency hedging instruments"
                ],
                monitoring_required=True
            ))

        restricted_countries = {
            "zimbabwe": ["USD_export_restrictions", "currency_controls_active"],
            "south_africa": ["capital_controls_considered"]
        }

        if seller_country.lower() in restricted_countries:
            for restriction in restricted_countries[seller_country.lower()]:
                risks.append(RiskFactor(
                    factor_id="regulatory_restriction",
                    category=RiskCategory.COMPLIANCE_RISK,
                    name=f"Regulatory Restriction: {restriction}",
                    description=f"{seller_country} has active {restriction}",
                    severity=RiskLevel.HIGH,
                    probability=0.6,
                    impact=0.7,
                    indicators=[f"country in restricted_list", f"restriction = {restriction}"],
                    mitigation_strategies=[
                        "Consult with compliance team",
                        "Ensure all documentation is complete",
                        "Budget for potential delays"
                    ],
                    monitoring_required=True
                ))

        return risks

    def _detect_fraud_patterns(self, transaction_data: Dict) -> List[RiskFactor]:
        detected_risks = []

        amount = float(transaction_data.get("amount", 0))
        if amount > 0 and amount % 100 == 0 and amount % 1000 != 0:
            detected_risks.append(RiskFactor(
                factor_id="round_amount_pattern",
                category=RiskCategory.FRAUD_RISK,
                name="Suspicious Round Amount Pattern",
                description="Transaction amount is suspiciously round",
                severity=RiskLevel.LOW,
                probability=0.4,
                impact=0.3,
                indicators=["amount % 100 == 0"],
                mitigation_strategies=["Verify transaction purpose with counterparty"],
                monitoring_required=False
            ))

        velocity = transaction_data.get("velocity_count", 0)
        if velocity > 3:
            detected_risks.append(RiskFactor(
                factor_id="high_velocity_transaction",
                category=RiskCategory.FRAUD_RISK,
                name="High Velocity Transaction Pattern",
                description=f"{velocity} transactions detected in short period",
                severity=RiskLevel.MEDIUM,
                probability=0.6,
                impact=0.5,
                indicators=[f"velocity_count > 3"],
                mitigation_strategies=[
                    "Delay processing to verify legitimacy",
                    "Contact user to confirm transactions",
                    "Implement additional verification step"
                ],
                monitoring_required=True
            ))

        return detected_risks

    def _check_compliance_requirements(self, amount: float, buyer_country: str,
                                    seller_country: str) -> List[RiskFactor]:
        risks = []

        for country_key, country in [("buyer", buyer_country), ("seller", seller_country)]:
            country_lower = country.lower()
            if country_lower in self.compliance_rules["aml_thresholds"]:
                thresholds = self.compliance_rules["aml_thresholds"][country_lower]

                if amount >= thresholds["suspicious_activity"]:
                    risks.append(RiskFactor(
                        factor_id="aml_report_required",
                        category=RiskCategory.COMPLIANCE_RISK,
                        name="AML Reporting Required",
                        description=f"Transaction amount {amount} triggers AML reporting in {country}",
                        severity=RiskLevel.MEDIUM,
                        probability=0.9,
                        impact=0.4,
                        indicators=[f"amount >= {thresholds['suspicious_activity']}"],
                        mitigation_strategies=[
                            "Complete all required AML documentation",
                            "Report to compliance team",
                            "Maintain transaction records"
                        ],
                        monitoring_required=True
                    ))

        return risks

    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        if risk_score >= 0.8:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.65:
            return RiskLevel.HIGH
        elif risk_score >= 0.45:
            return RiskLevel.MEDIUM
        elif risk_score >= 0.25:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL

    def _generate_assessment_text(self, risk_level: RiskLevel,
                                risks: List[RiskFactor]) -> str:
        high_severity_risks = [r for r in risks if r.severity in [RiskLevel.CRITICAL, RiskLevel.HIGH]]

        if risk_level == RiskLevel.CRITICAL:
            return "This transaction presents critical risk and requires immediate escalation to senior management. Multiple high-severity risk factors identified. Transaction should not proceed without enhanced due diligence and approval."
        elif risk_level == RiskLevel.HIGH:
            return "This transaction presents significant risk requiring careful review. Multiple risk factors identified including potential compliance and fraud concerns. Additional verification required before approval."
        elif risk_level == RiskLevel.MEDIUM:
            return "This transaction presents moderate risk that can be managed with standard controls. Some risk factors identified that require monitoring. Standard verification procedures should be followed."
        elif risk_level == RiskLevel.LOW:
            return "This transaction presents low risk with manageable factors. Limited risk indicators identified. Standard processing with routine monitoring is appropriate."
        else:
            return "This transaction presents minimal risk. Very few or no risk factors identified. Standard processing can proceed."

    def _generate_recommendations(self, risk_level: RiskLevel,
                                 risks: List[RiskFactor],
                                 payment_method: PaymentMethod) -> List[str]:
        recommendations = []

        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            recommendations.append("Escalate to senior risk manager for review")
            recommendations.append("Conduct enhanced due diligence (EDD)")
            recommendations.append("Request additional documentation from counterparty")

        if payment_method == PaymentMethod.CASH:
            recommendations.append("Consider alternative payment method (mobile money, bank transfer)")
            recommendations.append("Use escrow service for protection")

        if any(r.category == RiskCategory.CURRENCY_RISK for r in risks):
            recommendations.append("Fix pricing in USD to avoid currency fluctuation")
            recommendations.append("Include price adjustment clause in contract")

        if any(r.category == RiskCategory.COMPLIANCE_RISK for r in risks):
            recommendations.append("Ensure all compliance documentation is complete")
            recommendations.append("File required reports with authorities")

        if any(r.category == RiskCategory.FRAUD_RISK for r in risks):
            recommendations.append("Implement additional verification steps")
            recommendations.append("Set up transaction monitoring alerts")
            recommendations.append("Verify counterparty identity independently")

        return recommendations

    def _determine_required_verifications(self, risks: List[RiskFactor],
                                        risk_level: RiskLevel) -> List[str]:
        verifications = []

        if risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]:
            verifications.extend([
                "identity_verification",
                "address_verification",
                "business_verification",
                "source_of_funds_verification"
            ])
        elif risk_level == RiskLevel.MEDIUM:
            verifications.extend([
                "identity_verification",
                "business_verification"
            ])
        else:
            verifications.append("basic_identity_verification")

        if any(r.category == RiskCategory.COMPLIANCE_RISK for r in risks):
            verifications.append("compliance_documentation")

        if any(r.category == RiskCategory.CURRENCY_RISK for r in risks):
            verifications.append("currency_risk_disclosure")

        return list(set(verifications))

    def _determine_approval_status(self, risk_level: RiskLevel) -> str:
        status_map = {
            RiskLevel.CRITICAL: "rejected_requires_review",
            RiskLevel.HIGH: "pending_enhanced_review",
            RiskLevel.MEDIUM: "pending_standard_review",
            RiskLevel.LOW: "approved_with_monitoring",
            RiskLevel.MINIMAL: "auto_approved"
        }
        return status_map[risk_level]

    def assess_counterparty_risk(self, profile: UnbankedProfile) -> Dict:
        risk_score = 0.5

        if not profile.mobile_money_registered:
            risk_score += 0.15

        if profile.verification_level == "unverified":
            risk_score += 0.2

        if profile.transaction_history_months < 6:
            risk_score += 0.1

        if profile.avg_transaction_size > 5000:
            risk_score += 0.1

        if profile.trust_score < 0.5:
            risk_score += 0.15

        risk_factors = []
        if not profile.mobile_money_registered:
            risk_factors.append("No mobile money registration - limited digital payment options")
        if profile.nearest_agent_distance_km > 10:
            risk_factors.append(f"Agent distance {profile.nearest_agent_distance_km}km may affect cash handling")
        if not profile.id_document_type:
            risk_factors.append("No ID verification on file")
        if profile.transaction_frequency_per_month > 20:
            risk_factors.append("High transaction frequency - monitor for unusual patterns")

        return {
            "counterparty_id": profile.user_id,
            "country": profile.country,
            "risk_score": min(risk_score, 1.0),
            "risk_level": self._determine_risk_level(risk_score),
            "risk_factors": risk_factors,
            "recommendations": self._generate_counterparty_recommendations(profile, risk_score),
            "trust_score": profile.trust_score,
            "verified": profile.verification_level in ["verified", "high"]
        }

    def _generate_counterparty_recommendations(self, profile: UnbankedProfile,
                                             risk_score: float) -> List[str]:
        recommendations = []

        if not profile.mobile_money_registered:
            recommendations.append("Help counterparty register with mobile money provider")

        if profile.verification_level != "verified":
            recommendations.append("Complete identity verification process")

        if risk_score > 0.6:
            recommendations.append("Start with smaller transaction amounts to build trust")
            recommendations.append("Use escrow service for initial transactions")

        if profile.transaction_history_months < 6:
            recommendations.append("Allow time to establish transaction history")
            recommendations.append("Monitor transactions closely for first 6 months")

        return recommendations

    def get_payment_recommendation(self, amount: float, buyer_profile: Dict,
                                  seller_profile: Dict) -> Dict:
        payment_methods = []

        if amount <= 500:
            payment_methods.append({
                "method": "mobile_money",
                "recommendation": "recommended",
                "reason": "Optimal for small transactions, low fees, instant transfer",
                "providers": ["ecocash", "onemoney", "m_pesa"]
            })

        if amount <= 5000:
            payment_methods.append({
                "method": "mobile_money",
                "recommendation": "suitable",
                "reason": "Good for medium transactions, moderate fees",
                "providers": ["ecocash", "onemoney", "m_pesa"]
            })

        if amount > 1000:
            payment_methods.append({
                "method": "bank_transfer",
                "recommendation": "recommended",
                "reason": "Better for large transactions, provides audit trail",
                "providers": ["standard_chartered", "stanbic", "first_bank"]
            })

        if amount > 5000:
            payment_methods.append({
                "method": "escrow_service",
                "recommendation": "strongly_recommended",
                "reason": "Protects both parties for high-value cross-border transactions",
                "providers": ["tourista_escrow"]
            })

        recommended_method = payment_methods[0]["method"] if payment_methods else "cash"

        return {
            "amount": amount,
            "recommended_method": recommended_method,
            "alternative_methods": payment_methods,
            "risk_mitigation": self._suggest_payment_risk_mitigation(recommended_method, amount),
            "fees_estimate": self._estimate_payment_fees(recommended_method, amount)
        }

    def _suggest_payment_risk_mitigation(self, method: str, amount: float) -> List[str]:
        mitigations = {
            "mobile_money": [
                "Confirm recipient number before sending",
                "Use confirmation code for amounts > 1000",
                "Document transaction with screenshot"
            ],
            "bank_transfer": [
                "Verify bank account details carefully",
                "Request confirmation from beneficiary",
                "Keep transfer receipt"
            ],
            "cash": [
                "Meet in safe, public location",
                "Count money before exchange",
                "Consider using secure cash collection service"
            ],
            "escrow_service": [
                "Agree on inspection period before release",
                "Clearly define release conditions",
                "Keep all communication on platform"
            ]
        }
        return mitigations.get(method, [])

    def _estimate_payment_fees(self, method: str, amount: float) -> Dict:
        fee_structures = {
            "mobile_money": {"percentage": 0.02, "fixed": 0.5, "max": 10},
            "bank_transfer": {"percentage": 0.01, "fixed": 25, "max": 100},
            "cash": {"percentage": 0.0, "fixed": 0, "max": 0},
            "escrow_service": {"percentage": 0.03, "fixed": 5, "max": 50}
        }

        fees = fee_structures.get(method, {"percentage": 0, "fixed": 0})

        estimated_fee = (amount * fees.get("percentage", 0)) + fees.get("fixed", 0)
        max_fee = fees.get("max", float('inf'))
        actual_fee = min(estimated_fee, max_fee) if max_fee else estimated_fee

        return {
            "method": method,
            "estimated_fee": round(actual_fee, 2),
            "currency": "USD",
            "fee_percentage": fees.get("percentage", 0) * 100,
            "note": "Actual fees may vary"
        }
