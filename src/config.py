"""
Configuration management for the Social Media Analysis project.
Centralizes all settings and paths for easy maintenance.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SRC_DIR = PROJECT_ROOT / "src"

# Data file paths
RAW_DATA_PATH = DATA_DIR / "twitter_data.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_twitter_data.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_tweets.csv"

# Model configuration
NLTK_STOPWORDS_LANG = "english"
VADER_COMPOUND_THRESHOLD = 0.05  # Sentiment classification threshold

# Topic Modeling
NUM_TOPICS = 5
LDA_MAX_ITERATIONS = 100
RANDOM_STATE = 42

# Data validation
MIN_TEXT_LENGTH = 5
MAX_TEXT_LENGTH = 500

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Config:
    """Configuration class for accessing project settings."""
    
    # Paths
    PROJECT_ROOT = PROJECT_ROOT
    DATA_DIR = DATA_DIR
    RAW_DATA_PATH = RAW_DATA_PATH
    CLEANED_DATA_PATH = CLEANED_DATA_PATH
    PROCESSED_DATA_PATH = PROCESSED_DATA_PATH
    
    # Model settings
    NLTK_STOPWORDS_LANG = NLTK_STOPWORDS_LANG
    VADER_COMPOUND_THRESHOLD = VADER_COMPOUND_THRESHOLD
    NUM_TOPICS = NUM_TOPICS
    LDA_MAX_ITERATIONS = LDA_MAX_ITERATIONS
    RANDOM_STATE = RANDOM_STATE
    
    # Data validation
    MIN_TEXT_LENGTH = MIN_TEXT_LENGTH
    MAX_TEXT_LENGTH = MAX_TEXT_LENGTH
    
    # Logging
    LOG_LEVEL = LOG_LEVEL
    LOG_FORMAT = LOG_FORMAT
    
    @classmethod
    def get_data_dir(cls):
        """Get data directory path."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        return cls.DATA_DIR
    
    @classmethod
    def validate_paths(cls):
        """Validate that all required paths exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        return True
