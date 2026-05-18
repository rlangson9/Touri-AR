"""
Matching Module
"""
from .engine import IntelligentMatchingSystem, UserProfile, Product, MatchResult

try:
    from .neural_engine import NeuralMatchingEngine, HybridMatchingEngine
    __all__ = [
        'IntelligentMatchingSystem',
        'UserProfile',
        'Product',
        'MatchResult',
        'NeuralMatchingEngine',
        'HybridMatchingEngine'
    ]
except ImportError:
    __all__ = ['IntelligentMatchingSystem', 'UserProfile', 'Product', 'MatchResult']
