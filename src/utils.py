"""
Utility functions and logging setup for the project.
"""

import logging
import sys
from typing import Any, Optional

from src.config import Config


def setup_logger(name: str, level: str = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    if level is None:
        level = Config.LOG_LEVEL
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Create formatted handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(Config.LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


def validate_text(text: Any) -> bool:
    """
    Validate if text meets minimum requirements.
    
    Args:
        text: Text to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(text, str):
        return False
    
    if len(text.strip()) < Config.MIN_TEXT_LENGTH:
        return False
    
    if len(text) > Config.MAX_TEXT_LENGTH:
        return False
    
    return True


def classify_sentiment(compound_score: float) -> str:
    """
    Classify sentiment based on VADER compound score.
    
    Args:
        compound_score: VADER compound sentiment score (-1 to 1)
    
    Returns:
        Sentiment classification: 'positive', 'negative', or 'neutral'
    """
    if compound_score >= Config.VADER_COMPOUND_THRESHOLD:
        return "positive"
    elif compound_score <= -Config.VADER_COMPOUND_THRESHOLD:
        return "negative"
    else:
        return "neutral"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Dividend
        denominator: Divisor
        default: Value to return if denominator is zero
    
    Returns:
        Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator
