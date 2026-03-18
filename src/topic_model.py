"""
Topic modeling module.
Implements LDA (Latent Dirichlet Allocation) and other topic modeling approaches.

TODO: Implement topic modeling functionality
"""

import logging
from typing import List, Dict, Tuple

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

from src.config import Config
from src.utils import setup_logger

logger = setup_logger(__name__)


class TopicModeler:
    """
    Performs topic modeling on document collections.
    
    Attributes:
        num_topics: Number of topics to extract
        model: Fitted topic model
        vectorizer: Text vectorizer
    """
    
    def __init__(self, num_topics: int = None):
        """
        Initialize TopicModeler.
        
        Args:
            num_topics: Number of topics (default from config)
        """
        self.num_topics = num_topics or Config.NUM_TOPICS
        self.model = None
        self.vectorizer = None
        logger.info(f"TopicModeler initialized with {self.num_topics} topics")
    
    def prepare_corpus(self, texts: List[str], min_df: int = 2, 
                      max_df: float = 0.8) -> Tuple[np.ndarray, object]:
        """
        Prepare text corpus for topic modeling.
        
        Args:
            texts: List of text documents
            min_df: Minimum document frequency
            max_df: Maximum document frequency ratio
        
        Returns:
            Tuple of (document-term matrix, vectorizer)
        """
        logger.info(f"Preparing corpus with {len(texts)} documents")
        
        try:
            # Create count vectorizer for LDA
            self.vectorizer = CountVectorizer(
                max_df=max_df,
                min_df=min_df,
                stop_words='english',
                lowercase=True
            )
            
            doc_term_matrix = self.vectorizer.fit_transform(texts)
            logger.info(f"Corpus prepared: {doc_term_matrix.shape}")
            
            return doc_term_matrix, self.vectorizer
        
        except Exception as e:
            logger.error(f"Error preparing corpus: {str(e)}")
            raise
    
    def fit_lda(self, texts: List[str]) -> 'TopicModeler':
        """
        Fit LDA topic model.
        
        Args:
            texts: List of text documents
        
        Returns:
            Self for chaining
        """
        logger.info(f"Fitting LDA model with {len(texts)} documents")
        
        try:
            # Prepare corpus
            doc_term_matrix, _ = self.prepare_corpus(texts)
            
            # Fit LDA model
            self.model = LatentDirichletAllocation(
                n_components=self.num_topics,
                max_iter=Config.LDA_MAX_ITERATIONS,
                random_state=Config.RANDOM_STATE,
                verbose=0
            )
            
            self.model.fit(doc_term_matrix)
            logger.info("LDA model fitting complete")
            
            return self
        
        except Exception as e:
            logger.error(f"Error fitting LDA model: {str(e)}")
            raise
    
    def get_topics(self, n_words: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        """
        Extract top N words for each topic.
        
        Args:
            n_words: Number of top words per topic
        
        Returns:
            Dictionary mapping topic_id to list of (word, weight) tuples
        """
        if self.model is None or self.vectorizer is None:
            logger.warning("Model not fitted yet")
            return {}
        
        topics = {}
        feature_names = self.vectorizer.get_feature_names_out()
        
        for topic_idx, topic in enumerate(self.model.components_):
            top_indices = topic.argsort()[-n_words:][::-1]
            top_words = [
                (feature_names[i], topic[i]) 
                for i in top_indices
            ]
            topics[topic_idx] = top_words
        
        return topics
    
    def predict_topics(self, texts: List[str]) -> np.ndarray:
        """
        Predict topic distribution for new texts.
        
        Args:
            texts: List of text documents
        
        Returns:
            Array of shape (n_documents, n_topics) with topic probabilities
        """
        if self.model is None or self.vectorizer is None:
            logger.error("Model not fitted")
            raise ValueError("Model must be fitted before prediction")
        
        try:
            doc_term_matrix = self.vectorizer.transform(texts)
            topic_distribution = self.model.transform(doc_term_matrix)
            return topic_distribution
        
        except Exception as e:
            logger.error(f"Error predicting topics: {str(e)}")
            raise
    
    def add_topics_to_dataframe(self, df: pd.DataFrame, text_column: str,
                                topic_name: str = 'dominant_topic') -> pd.DataFrame:
        """
        Add dominant topic predictions to dataframe.
        
        Args:
            df: Input dataframe
            text_column: Name of text column
            topic_name: Name for new topic column
        
        Returns:
            Dataframe with new topic column
        """
        logger.info(f"Adding topics to dataframe ({len(df)} rows)")
        
        try:
            # Get topic distributions
            texts = df[text_column].tolist()
            topic_dist = self.predict_topics(texts)
            
            # Get dominant topic for each document
            df[topic_name] = np.argmax(topic_dist, axis=1)
            df[f'{topic_name}_confidence'] = np.max(topic_dist, axis=1)
            
            logger.info("Topics added successfully")
            return df
        
        except Exception as e:
            logger.error(f"Error adding topics: {str(e)}")
            raise
