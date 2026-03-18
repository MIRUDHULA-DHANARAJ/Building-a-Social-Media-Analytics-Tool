"""
Data loading and validation module.
Handles loading, validation, and basic preprocessing of datasets.
"""

import pandas as pd
from typing import Optional, Tuple
import logging

from src.config import Config
from src.utils import setup_logger, validate_text

logger = setup_logger(__name__)


class DataLoader:
    """
    Handles loading and validating social media data.
    
    Attributes:
        data_path: Path to data file
        df: Loaded dataframe
    """
    
    def __init__(self, data_path: str):
        """
        Initialize DataLoader.
        
        Args:
            data_path: Path to CSV file
        """
        self.data_path = data_path
        self.df = None
        logger.info(f"DataLoader initialized with path: {data_path}")
    
    def load(self) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Returns:
            Loaded dataframe
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or invalid
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded {len(self.df)} rows")
            return self.df
        
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise FileNotFoundError(f"Data file not found at {self.data_path}")
        
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise ValueError(f"Error loading data: {str(e)}")
    
    def validate(self, required_columns: Optional[list] = None) -> Tuple[bool, list]:
        """
        Validate data integrity.
        
        Args:
            required_columns: List of required column names
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if self.df is None:
            errors.append("Data not loaded. Call load() first.")
            return False, errors
        
        # Check for empty dataframe
        if len(self.df) == 0:
            errors.append("Dataframe is empty")
            return False, errors
        
        # Check required columns
        if required_columns:
            missing_cols = [col for col in required_columns if col not in self.df.columns]
            if missing_cols:
                errors.append(f"Missing columns: {missing_cols}")
        
        # Check for all NaN columns
        nan_columns = self.df.columns[self.df.isna().all()].tolist()
        if nan_columns:
            errors.append(f"Columns with all NaN values: {nan_columns}")
        
        logger.info(f"Data validation: {'PASSED' if not errors else 'FAILED'}")
        return len(errors) == 0, errors
    
    def get_stats(self) -> dict:
        """
        Get basic statistics about the dataset.
        
        Returns:
            Dictionary with dataset statistics
        """
        if self.df is None:
            return {}
        
        stats = {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "memory_usage": self.df.memory_usage(deep=True).sum() / 1024**2,  # MB
            "null_values": self.df.isna().sum().to_dict(),
            "columns": self.df.columns.tolist(),
            "dtypes": self.df.dtypes.to_dict()
        }
        return stats
    
    def filter_by_text_length(self, text_column: str) -> pd.DataFrame:
        """
        Filter dataframe to keep only valid text entries.
        
        Args:
            text_column: Name of text column
        
        Returns:
            Filtered dataframe
        """
        if self.df is None:
            logger.warning("Dataframe not loaded")
            return pd.DataFrame()
        
        original_size = len(self.df)
        
        # Apply validation
        self.df = self.df[self.df[text_column].apply(validate_text)]
        
        filtered_size = len(self.df)
        logger.info(f"Filtered {original_size - filtered_size} rows based on text length")
        
        return self.df
    
    def head(self, n: int = 5) -> pd.DataFrame:
        """
        Get first n rows of data.
        
        Args:
            n: Number of rows
        
        Returns:
            First n rows
        """
        if self.df is None:
            return pd.DataFrame()
        return self.df.head(n)
