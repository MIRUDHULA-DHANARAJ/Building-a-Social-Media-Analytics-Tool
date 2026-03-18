"""
Text preprocessing module.
Handles text cleaning, tokenization, and normalization.
"""

import re
import logging
from typing import List

import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from src.config import Config
from src.utils import setup_logger

logger = setup_logger(__name__)


class TextPreprocessor:
    """
    Preprocesses raw text data for analysis.
    
    Attributes:
        stopwords_set: Set of stopwords for filtering
    """
    
    def __init__(self):
        """Initialize TextPreprocessor with stopwords."""
        try:
            self.stopwords_set = set(stopwords.words(Config.NLTK_STOPWORDS_LANG))
            logger.info("TextPreprocessor initialized successfully")
        except Exception as e:
            logger.error(f"Error loading stopwords: {str(e)}")
            self.stopwords_set = set()
    
    @staticmethod
    def lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower() if isinstance(text, str) else text
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r"http\S+|www\S+", "", text)
    
    @staticmethod
    def remove_special_characters(text: str) -> str:
        """Remove special characters, keep only alphanumeric and spaces."""
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)
    
    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """Remove extra whitespace."""
        return re.sub(r"\s+", " ", text).strip()
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words and remove stopwords.
        
        Args:
            text: Text to tokenize
        
        Returns:
            List of filtered words
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return []
        
        try:
            words = word_tokenize(text)
            filtered_words = [
                word for word in words 
                if word.lower() not in self.stopwords_set and len(word) > 2
            ]
            return filtered_words
        except Exception as e:
            logger.warning(f"Error tokenizing text: {str(e)}")
            return []
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize text into sentences.
        
        Args:
            text: Text to tokenize
        
        Returns:
            List of sentences
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            return []
        
        try:
            return sent_tokenize(text)
        except Exception as e:
            logger.warning(f"Error sentence tokenizing: {str(e)}")
            return [text]
    
    def preprocess(self, text: str) -> str:
        """
        Apply full preprocessing pipeline.
        
        Args:
            text: Raw text to preprocess
        
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return ""
        
        # Apply preprocessing steps
        text = self.lowercase(text)
        text = self.remove_urls(text)
        text = self.remove_special_characters(text)
        text = self.remove_extra_whitespace(text)
        
        return text
    
    def preprocess_with_tokenization(self, text: str) -> dict:
        """
        Apply preprocessing and tokenization.
        
        Args:
            text: Raw text to preprocess
        
        Returns:
            Dictionary with cleaned text and tokens
        """
        if not isinstance(text, str) or pd.isna(text):
            return {
                "original": text,
                "cleaned": "",
                "sentences": [],
                "words": []
            }
        
        cleaned = self.preprocess(text)
        
        return {
            "original": text,
            "cleaned": cleaned,
            "sentences": self.tokenize_sentences(cleaned),
            "words": self.tokenize_words(cleaned)
        }
    
    def process_dataframe(self, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        """
        Apply preprocessing to all texts in dataframe.
        
        Args:
            df: Input dataframe
            text_column: Name of text column
        
        Returns:
            Dataframe with new 'cleaned_text' and 'tokens' columns
        """
        logger.info(f"Processing {len(df)} texts from column '{text_column}'")
        
        # Preprocess texts
        df['cleaned_text'] = df[text_column].apply(
            lambda x: self.preprocess(x) if pd.notna(x) else ""
        )
        
        # Tokenize words
        df['tokens'] = df['cleaned_text'].apply(self.tokenize_words)
        
        # Remove rows with no tokens
        initial_size = len(df)
        df = df[df['tokens'].apply(len) > 0]
        removed = initial_size - len(df)
        
        logger.info(f"Processing complete. Removed {removed} rows with no valid tokens.")
        
        return df
