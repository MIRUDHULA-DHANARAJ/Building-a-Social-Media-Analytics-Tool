"""
Reddit data collector for stock market discussions.
Collects comments from financial subreddits and saves them for analysis.
"""

import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

import praw
from praw.exceptions import PrawcoreException

from src.config import Config
from src.utils import setup_logger

logger = setup_logger(__name__)


class RedditCollector:
    """
    Collects data from Reddit stock market subreddits.
    
    Attributes:
        reddit: PRAW Reddit instance
        subreddits: List of subreddits to monitor
    """
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize Reddit collector with PRAW credentials.
        
        Args:
            client_id: Reddit app client ID
            client_secret: Reddit app client secret
            user_agent: User agent string
        
        Raises:
            PrawcoreException: If authentication fails
        """
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            logger.info("Reddit authentication successful")
        except PrawcoreException as e:
            logger.error(f"Reddit authentication failed: {str(e)}")
            raise
    
    def collect_comments(self, subreddit_name: str, limit: int = 500,
                        time_filter: str = 'day') -> List[Dict]:
        """
        Collect comments from a subreddit.
        
        Args:
            subreddit_name: Name of subreddit (without r/)
            limit: Maximum number of posts to scan
            time_filter: Time filter ('day', 'week', 'month')
        
        Returns:
            List of comment dictionaries
        """
        comments_data = []
        
        try:
            logger.info(f"Collecting from r/{subreddit_name}...")
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get top posts from subreddit
            for post in subreddit.top(time_filter, limit=limit):
                # Replace with best lambda for sorting comments
                post.comments.replace_more(limit=0)
                
                for comment in post.comments.list():
                    try:
                        comments_data.append({
                            'subreddit': subreddit_name,
                            'author': str(comment.author),
                            'text': comment.body,
                            'score': comment.score,
                            'created_utc': datetime.fromtimestamp(comment.created_utc),
                            'post_title': post.title,
                            'post_score': post.score
                        })
                    except Exception as e:
                        logger.debug(f"Error processing comment: {str(e)}")
                        continue
            
            logger.info(f"Collected {len(comments_data)} comments from r/{subreddit_name}")
            return comments_data
        
        except Exception as e:
            logger.error(f"Error collecting from r/{subreddit_name}: {str(e)}")
            return []
    
    def collect_from_multiple(self, subreddits: List[str], limit: int = 500,
                             time_filter: str = 'day') -> pd.DataFrame:
        """
        Collect comments from multiple subreddits.
        
        Args:
            subreddits: List of subreddit names
            limit: Max posts per subreddit
            time_filter: Time filter
        
        Returns:
            Combined dataframe
        """
        all_comments = []
        
        for subreddit in subreddits:
            comments = self.collect_comments(subreddit, limit, time_filter)
            all_comments.extend(comments)
        
        df = pd.DataFrame(all_comments)
        logger.info(f"Total collected: {len(df)} comments")
        
        return df
    
    @staticmethod
    def save_data(df: pd.DataFrame, filename: str = 'raw_reddit_data.csv') -> str:
        """
        Save collected data to CSV.
        
        Args:
            df: Dataframe to save
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        output_path = Config.DATA_DIR / filename
        df.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")
        return str(output_path)


# Example usage configuration
STOCK_SUBREDDITS = [
    'stocks',
    'investing',
    'wallstreetbets',
    'SecurityAnalysis'
]

REDDIT_CONFIG = {
    # GET THESE FROM: https://www.reddit.com/prefs/apps
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'user_agent': 'StockSentimentAnalyzer/1.0'
}
