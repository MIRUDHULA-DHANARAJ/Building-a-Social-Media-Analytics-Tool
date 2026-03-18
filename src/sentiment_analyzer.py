"""
Sentiment analysis module using VADER.
Analyzes sentiment of text data and provides scoring.
"""

import logging
from typing import Dict, Optional

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.config import Config
from src.utils import setup_logger, classify_sentiment

logger = setup_logger(__name__)


class SentimentAnalyzer:
    """
    Analyzes sentiment of text using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    
    Attributes:
        analyzer: VADER SentimentIntensityAnalyzer instance
    """
    
    def __init__(self):
        """Initialize SentimentAnalyzer with VADER."""
        self.analyzer = SentimentIntensityAnalyzer()
        logger.info("SentimentAnalyzer initialized with VADER")
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary with sentiment scores
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            logger.debug("Empty or invalid text provided")
            return {
                'negative': 0.0,
                'neutral': 0.0,
                'positive': 0.0,
                'compound': 0.0,
                'sentiment': 'neutral'
            }
        
        try:
            scores = self.analyzer.polarity_scores(text)
            scores['sentiment'] = classify_sentiment(scores['compound'])
            return scores
        
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return {
                'negative': 0.0,
                'neutral': 0.0,
                'positive': 0.0,
                'compound': 0.0,
                'sentiment': 'error'
            }
    
    def analyze_batch(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
        
        Returns:
            List of sentiment score dictionaries
        """
        logger.info(f"Analyzing sentiment for {len(texts)} texts")
        
        results = [
            self.analyze_text(text) if pd.notna(text) else None 
            for text in texts
        ]
        
        logger.info(f"Sentiment analysis complete")
        return results
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str, 
                         create_classification: bool = True) -> pd.DataFrame:
        """
        Analyze sentiment for all texts in dataframe.
        
        Args:
            df: Input dataframe
            text_column: Name of text column to analyze
            create_classification: If True, add sentiment classification column
        
        Returns:
            Dataframe with new sentiment columns
        """
        logger.info(f"Analyzing sentiment for {len(df)} rows")
        
        # Analyze all texts
        sentiment_data = df[text_column].apply(
            lambda x: self.analyze_text(x) if pd.notna(x) else None
        )
        
        # Extract individual scores
        df['sentiment_negative'] = sentiment_data.apply(
            lambda x: x.get('negative', 0.0) if x and isinstance(x, dict) else 0.0
        )
        df['sentiment_positive'] = sentiment_data.apply(
            lambda x: x.get('positive', 0.0) if x and isinstance(x, dict) else 0.0
        )
        df['sentiment_neutral'] = sentiment_data.apply(
            lambda x: x.get('neutral', 0.0) if x and isinstance(x, dict) else 0.0
        )
        df['sentiment_compound'] = sentiment_data.apply(
            lambda x: x.get('compound', 0.0) if x and isinstance(x, dict) else 0.0
        )
        
        if create_classification:
            df['sentiment_label'] = sentiment_data.apply(
                lambda x: x.get('sentiment', 'neutral') if x and isinstance(x, dict) else 'neutral'
            )
        
        logger.info("Sentiment analysis complete")
        return df
    
    def get_sentiment_summary(self, df: pd.DataFrame, 
                             label_column: str = 'sentiment_label') -> Dict:
        """
        Get summary statistics of sentiment distribution.
        
        Args:
            df: Dataframe with sentiment labels
            label_column: Name of sentiment label column
        
        Returns:
            Dictionary with sentiment summary
        """
        if label_column not in df.columns:
            logger.warning(f"Column '{label_column}' not found in dataframe")
            return {}
        
        labels_count = df[label_column].value_counts()
        total = len(df)
        
        summary = {
            'total_texts': total,
            'positive': int(labels_count.get('positive', 0)),
            'negative': int(labels_count.get('negative', 0)),
            'neutral': int(labels_count.get('neutral', 0)),
            'positive_pct': float(labels_count.get('positive', 0) / total * 100),
            'negative_pct': float(labels_count.get('negative', 0) / total * 100),
            'neutral_pct': float(labels_count.get('neutral', 0) / total * 100),
        }
        
        logger.info(f"Sentiment Summary: {summary}")
        return summary
