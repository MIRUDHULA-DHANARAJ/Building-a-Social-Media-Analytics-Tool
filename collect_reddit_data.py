"""
Script to collect Reddit data for stock market sentiment analysis
Run this to gather real data from Reddit
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.reddit_collector import RedditCollector, STOCK_SUBREDDITS
from src.preprocessing import TextPreprocessor
from src.sentiment_analyzer import SentimentAnalyzer
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Main data collection and analysis pipeline."""
    
    print("\n" + "="*60)
    print("📈 Stock Market Sentiment Analysis - Data Collection")
    print("="*60 + "\n")
    
    # Step 1: Get Reddit credentials
    print("⚙️ STEP 1: Reddit API Configuration")
    print("-" * 60)
    print("\nTo collect real Reddit data, you need Reddit API credentials:")
    print("1. Go to: https://www.reddit.com/prefs/apps")
    print("2. Click 'Create an App' → Select 'script'")
    print("3. Copy your client_id, client_secret, and user_agent\n")
    
    client_id = input("Enter your Reddit client_id: ").strip()
    client_secret = input("Enter your Reddit client_secret: ").strip()
    user_agent = input("Enter your user_agent (e.g., 'StockSentir/1.0'): ").strip()
    
    if not all([client_id, client_secret, user_agent]):
        print("❌ Missing credentials. Exiting.")
        return
    
    # Step 2: Collect data
    print("\n🔄 STEP 2: Collecting Reddit Data")
    print("-" * 60)
    
    try:
        collector = RedditCollector(client_id, client_secret, user_agent)
        print(f"✓ Connected to Reddit API\n")
        
        subreddits_str = ', '.join(STOCK_SUBREDDITS)
        print(f"Collecting from: {subreddits_str}\n")
        
        num_posts = int(input("How many posts per subreddit? (default: 100): ") or 100)
        
        df = collector.collect_from_multiple(STOCK_SUBREDDITS, limit=num_posts)
        
        if len(df) == 0:
            print("❌ No data collected. Check your credentials.")
            return
        
        print(f"✓ Collected {len(df)} comments\n")
        
        # Save raw data
        raw_file = collector.save_data(df, 'raw_reddit_data.csv')
        print(f"✓ Saved to: {raw_file}\n")
        
    except Exception as e:
        print(f"❌ Error during collection: {e}")
        print("Check your Reddit credentials and try again.")
        return
    
    # Step 3: Preprocess
    print("\n🧹 STEP 3: Text Preprocessing")
    print("-" * 60)
    
    try:
        prep = TextPreprocessor()
        print("Processing text...")
        
        df = prep.process_dataframe(df, 'text')
        print(f"✓ Processed {len(df)} valid comments\n")
        
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return
    
    # Step 4: Sentiment analysis
    print("\n💭 STEP 4: Sentiment Analysis")
    print("-" * 60)
    
    try:
        analyzer = SentimentAnalyzer()
        print("Running VADER sentiment analysis...")
        
        df = analyzer.analyze_dataframe(df, 'text')
        
        # Get summary
        summary = analyzer.get_sentiment_summary(df)
        
        print(f"✓ Analysis complete!\n")
        print("📊 Summary:")
        print(f"   Total comments: {summary['total_texts']}")
        print(f"   🟢 Positive: {summary['positive_pct']:.1f}%")
        print(f"   🔴 Negative: {summary['negative_pct']:.1f}%")
        print(f"   ⚪ Neutral: {summary['neutral_pct']:.1f}%\n")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return
    
    # Step 5: Save processed data
    print("💾 STEP 5: Saving Results")
    print("-" * 60)
    
    try:
        processed_file = 'data/processed_reddit_data.csv'
        df.to_csv(processed_file, index=False)
        print(f"✓ Saved to: {processed_file}\n")
        
    except Exception as e:
        print(f"❌ Error saving data: {e}")
        return
    
    # Final message
    print("\n" + "="*60)
    print("✅ DATA COLLECTION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: streamlit run app.py")
    print("2. Upload the processed CSV file")
    print("3. View insights in the dashboard!\n")


if __name__ == "__main__":
    main()
