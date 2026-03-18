"""
Stock Market Sentiment Analysis Dashboard
Real-time visualization of investor sentiment from Reddit discussions
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

from src.config import Config
from src.data_loader import DataLoader
from src.preprocessing import TextPreprocessor
from src.sentiment_analyzer import SentimentAnalyzer
from src.utils import setup_logger

logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Social Media Analytics Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .positive { color: #2ecc71; font-weight: bold; }
    .negative { color: #e74c3c; font-weight: bold; }
    .neutral { color: #95a5a6; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load sentiment analyzer (cached)."""
    return SentimentAnalyzer()


@st.cache_data
def load_data_cached(filepath):
    """Load data (cached)."""
    loader = DataLoader(filepath)
    df = loader.load()
    return df


def analyze_sentiment_batch(texts, analyzer):
    """Analyze sentiment for texts."""
    return [analyzer.analyze_text(text) if pd.notna(text) else None for text in texts]


def create_sentiment_distribution_chart(df):
    """Create sentiment distribution pie chart."""
    if 'sentiment_label' not in df.columns or df['sentiment_label'].isna().all():
        return None
    
    sentiment_counts = df['sentiment_label'].value_counts()
    if len(sentiment_counts) == 0:
        return None
    
    colors = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#95a5a6'}
    
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Sentiment Distribution",
        color_discrete_map=colors,
        hole=0.4
    )
    return fig


def create_compound_score_chart(df):
    """Create sentiment score histogram."""
    if 'sentiment_compound' not in df.columns or df['sentiment_compound'].isna().all():
        return None
    
    fig = px.histogram(
        df,
        x='sentiment_compound',
        nbins=50,
        title="Sentiment Score Distribution",
        labels={'sentiment_compound': 'Compound Score'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        annotation_text="Neutral Line"
    )
    
    return fig


def create_sentiment_timeline(df):
    """Create sentiment over time chart."""
    if 'created_utc' not in df.columns or 'sentiment_compound' not in df.columns:
        return None
    
    if df['sentiment_compound'].isna().all():
        return None
    
    df_sorted = df.sort_values('created_utc')
    df_sorted['rolling_sentiment'] = df_sorted['sentiment_compound'].rolling(window=20, min_periods=1).mean()
    
    fig = px.line(
        df_sorted,
        x='created_utc',
        y='rolling_sentiment',
        title="Sentiment Trend (20-comment moving average)",
        labels={
            'created_utc': 'Time',
            'rolling_sentiment': 'Average Sentiment'
        }
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    return fig


def display_top_comments(df, sentiment_type='positive', limit=5):
    """Display top comments by sentiment."""
    if 'sentiment_compound' not in df.columns:
        st.warning("No sentiment data available")
        return
    
    if sentiment_type == 'positive':
        top = df.nlargest(limit, 'sentiment_compound')
    elif sentiment_type == 'negative':
        top = df.nsmallest(limit, 'sentiment_compound')
    else:
        top = df.iloc[df['sentiment_compound'].abs().argsort()[:limit]]
    
    for idx, row in top.iterrows():
        score = row.get('sentiment_compound', 0)
        sentiment = '🟢 Positive' if score > 0.05 else '🔴 Negative' if score < -0.05 else '⚪ Neutral'
        
        with st.container():
            st.markdown(f"**{sentiment}** (Score: {score:.2f})")
            st.markdown(f"_{row.get('text', '')[:200]}..._")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"👤 {row.get('author', 'Unknown')}")
            with col2:
                st.caption(f"⬆️ {row.get('score', 0)} upvotes")
            with col3:
                st.caption(f"r/{row.get('subreddit', 'N/A')}")
            
            st.divider()


def main():
    """Main dashboard function."""
    
    # Header
    st.title("� Social Media Analytics Engine")
    st.markdown("Real-time sentiment analysis and insights from social media communities")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        data_source = st.radio(
            "Data Source:",
            ["Use Sample Data", "Upload CSV", "Collect from Reddit"]
        )
        
        st.markdown("---")
        st.subheader("📊 About")
        st.info(
            "This dashboard analyzes sentiment from social media discussions "
            "using VADER sentiment analysis and topic modeling. "
            "Collect data from Reddit, Twitter, or upload your own."
        )
    
    # Load data based on source
    df = None
    
    if data_source == "Use Sample Data":
        st.info("Loading sample processed data...")
        try:
            # Try processed data first
            try:
                df = load_data_cached(str(Config.PROCESSED_DATA_PATH))
            except:
                # Fallback to cleaned data
                df = load_data_cached(str(Config.CLEANED_DATA_PATH))
            
            # Check if sentiment analysis needed
            if 'sentiment_compound' not in df.columns or df['sentiment_compound'].isna().all():
                st.warning("⏳ Running sentiment analysis on data... (this may take 30 seconds)")
                analyzer = load_models()
                df = analyzer.analyze_dataframe(df, 'text')
                st.success("✅ Sentiment analysis complete!")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()
    
    elif data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} rows")
            
            if st.button("Analyze Sentiment"):
                analyzer = load_models()
                with st.spinner("Analyzing sentiment..."):
                    df = analyzer.analyze_dataframe(df, 'text' if 'text' in df.columns else df.columns[0])
                st.success("Analysis complete!")
    
    elif data_source == "Collect from Reddit":
        st.warning("⚠️ Reddit API collection requires credentials")
        st.markdown("""
        To enable Reddit data collection:
        1. Go to https://www.reddit.com/prefs/apps
        2. Create a "script" app
        3. Add credentials to `src/reddit_collector.py`
        4. Run: `python collect_reddit_data.py`
        5. Upload the generated CSV
        """)
    
    # Display metrics if data loaded
    if df is not None and len(df) > 0:
        st.markdown("---")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📝 Total Comments",
                f"{len(df):,}",
                delta="Real-time data"
            )
        
        with col2:
            if 'sentiment_label' in df.columns:
                positive_count = len(df[df['sentiment_label'] == 'positive'])
                st.metric("🟢 Positive", f"{positive_count:,}")
        
        with col3:
            if 'sentiment_label' in df.columns:
                negative_count = len(df[df['sentiment_label'] == 'negative'])
                st.metric("🔴 Negative", f"{negative_count:,}")
        
        with col4:
            if 'sentiment_compound' in df.columns and not df['sentiment_compound'].isna().all():
                avg_sentiment = df['sentiment_compound'].mean()
                st.metric(
                    "📊 Avg Sentiment",
                    f"{avg_sentiment:.2f}",
                    delta=f"{'Bullish 📈' if avg_sentiment > 0 else 'Bearish 📉'}"
                )
            else:
                st.metric("📊 Avg Sentiment", "N/A")
        
        # Charts
        st.markdown("---")
        st.subheader("📊 Sentiment Analysis")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            dist_chart = create_sentiment_distribution_chart(df)
            if dist_chart:
                st.plotly_chart(dist_chart, use_container_width=True)
        
        with chart_col2:
            score_chart = create_compound_score_chart(df)
            if score_chart:
                st.plotly_chart(score_chart, use_container_width=True)
        
        # Timeline
        timeline_chart = create_sentiment_timeline(df)
        if timeline_chart:
            st.plotly_chart(timeline_chart, use_container_width=True)
        
        # Top comments
        st.markdown("---")
        st.subheader("💬 Top Comments")
        
        if 'sentiment_compound' in df.columns and not df['sentiment_compound'].isna().all():
            tab1, tab2, tab3 = st.tabs(["🟢 Most Positive", "🔴 Most Negative", "⚪ Most Neutral"])
            
            with tab1:
                display_top_comments(df, 'positive', 3)
            
            with tab2:
                display_top_comments(df, 'negative', 3)
            
            with tab3:
                display_top_comments(df, 'neutral', 3)
        else:
            st.info("Top comments will appear after sentiment analysis")
        
        # Data explorer
        st.markdown("---")
        st.subheader("🔍 Data Explorer")
        
        if st.checkbox("Show raw data"):
            st.dataframe(
                df[['text', 'sentiment_compound', 'sentiment_label']].head(20),
                use_container_width=True
            )
        
        # Statistics
        st.markdown("---")
        st.subheader("📈 Statistics")
        
        if 'sentiment_label' in df.columns and not df['sentiment_label'].isna().all():
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            
            with stat_col1:
                positive_pct = len(df[df['sentiment_label']=='positive']) / len(df) * 100
                st.metric("Positive Ratio", f"{positive_pct:.1f}%")
            
            with stat_col2:
                negative_pct = len(df[df['sentiment_label']=='negative']) / len(df) * 100
                st.metric("Negative Ratio", f"{negative_pct:.1f}%")
            
            with stat_col3:
                neutral_pct = len(df[df['sentiment_label']=='neutral']) / len(df) * 100
                st.metric("Neutral Ratio", f"{neutral_pct:.1f}%")
        else:
            st.info("Statistics will appear after sentiment analysis")
    
    else:
        st.warning("👆 Please load or upload data to get started")


if __name__ == "__main__":
    main()
