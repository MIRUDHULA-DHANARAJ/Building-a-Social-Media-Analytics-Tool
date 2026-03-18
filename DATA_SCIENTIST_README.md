# 📊 Social Media Analytics Engine

**ML-Powered Sentiment Analysis & Topic Modeling Platform**

Analyze 160K+ social media comments using natural language processing and machine learning to extract sentiment insights and discover discussion themes.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![ML](https://img.shields.io/badge/ML-Scikit--learn-brightgreen)
![NLP](https://img.shields.io/badge/NLP-VADER_LDA-orange)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)

---

## 🎯 Data Science Use Case

**Problem:** Understand public sentiment and discussion themes in social media at scale  
**Solution:** Apply NLP + ML techniques to classify, analyze, and visualize sentiment patterns  
**Impact:** Actionable insights for marketers, researchers, and business stakeholders

---

## 🔬 ML/NLP Techniques Used

### Sentiment Analysis
- **VADER (Valence Aware Dictionary and sEntiment Reasoner)**
  - Rule-based sentiment scoring (no training required)
  - Outputs: Negative, Neutral, Positive, Compound scores
  - Perfect for social media text with emojis and slang
  - Compound score: -1 (most negative) to +1 (most positive)

### Topic Modeling
- **Latent Dirichlet Allocation (LDA)**
  - Unsupervised learning to discover hidden themes
  - Identifies main topics discussed in comments
  - Outputs: Top keywords per topic, topic distribution

### Text Preprocessing
- Tokenization (NLTK)
- Stopword removal
- Lowercasing & normalization
- Special character & URL removal
- Ready for ML models

### Statistical Analysis
- Distribution analysis (positive/negative/neutral percentages)
- Compound score statistics (mean, std, distribution)
- Trend analysis over time
- Comment-level insights

---

## 📊 Dataset & Results

### Data
- **Source:** Social media (Reddit, Twitter samples)
- **Size:** 160,000+ comments
- **Features:** Text, metadata, timestamps
- **Processing:** Complete pipeline from raw → analyzed

### Sentiment Distribution
```
Total Comments: 162,973

Positive:  58,321 (35.8%)  🟢
Negative:  41,892 (25.7%)  🔴
Neutral:   62,760 (38.5%)  ⚪

Average Compound Score: +0.18
```

### Model Performance
- **Processing Speed:** 160K comments in 2-3 minutes
- **Coverage:** 100% of comments (no failures)
- **Output Quality:** Interpretable sentiment scores + topics
- **Scalability:** Handles large datasets efficiently

---

## 🛠️ Data Science Stack

| Tool | Purpose | Why Used |
|------|---------|----------|
| **Python 3.8+** | Core language | Standard for data science |
| **Pandas** | Data manipulation | Industry standard |
| **Scikit-learn** | ML algorithms | LDA, vectorization, utilities |
| **NLTK** | NLP tasks | Tokenization, stopwords |
| **VADER** | Sentiment analysis | Fast, accurate for social media |
| **Plotly** | Visualization | Interactive, publication-quality |
| **Streamlit** | Dashboard/UI | Fast prototyping, deployment |

---

## 📁 Project Structure

```
Social-Media-Analysis/
├── src/
│   ├── preprocessing.py         # Text cleaning & tokenization
│   ├── sentiment_analyzer.py    # VADER sentiment scoring
│   ├── topic_model.py           # LDA topic modeling
│   ├── data_loader.py           # Data ingestion & validation
│   └── utils.py                 # Helper functions
│
├── notebooks/
│   ├── Data_Understanding.ipynb      # EDA & exploration
│   ├── Data_Preprocessing.ipynb       # Text preprocessing
│   └── Vader_Processing.ipynb        # Sentiment analysis walkthrough
│
├── app.py                       # Streamlit dashboard
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

---

## 🚀 Quick Start

### 1️⃣ Install
```bash
pip install -r requirements.txt
```

### 2️⃣ Run Dashboard
```bash
streamlit run app.py
```

### 3️⃣ Analyze
- Select "Use Sample Data" (160K pre-analyzed comments)
- Or upload your own CSV with a `text` column
- View sentiment distribution and trends

---

## 📈 Dashboard Features

### Visualizations
- **Sentiment Distribution Pie Chart** - Positive vs Negative vs Neutral
- **Compound Score Histogram** - Distribution of sentiment intensities
- **Sentiment Timeline** - Trends over time with moving average
- **Top Comments** - Best positive/negative comments by sentiment strength

### Analysis Metrics
- Total comment count
- Sentiment percentages & counts
- Average sentiment score
- Comment statistics (length, etc.)
- Raw data explorer

### Data Processing
- Real-time sentiment analysis
- Automatic data validation
- Missing value handling
- Text preprocessing applied

---

## 🔍 How the Analysis Works

### 1. Data Loading
```python
# Load comments from CSV
df = pd.read_csv('social_media_data.csv')
```

### 2. Text Preprocessing
```python
# Clean text: lowercase, remove URLs, tokenize
cleaned_text = preprocess(raw_text)
tokens = tokenize(cleaned_text)
```

### 3. Sentiment Analysis
```python
# Score sentiment with VADER
scores = analyzer.polarity_scores(text)
# Output: {'neg': 0.0, 'neu': 0.548, 'pos': 0.452, 'compound': 0.6}
sentiment = 'positive' if scores['compound'] > 0.05 else 'negative'/'neutral'
```

### 4. Topic Modeling (Optional)
```python
# Discover main themes using LDA
lda = LatentDirichletAllocation(n_topics=5)
topics = lda.fit_transform(vectorized_text)
```

### 5. Visualization
```python
# Create interactive dashboard
sentiment_pie_chart()      # Distribution
compound_histogram()       # Intensity
sentiment_timeline()       # Trends
top_comments()             # Examples
```

---

## 📊 Key Insights You Can Extract

✅ **Sentiment Trends** - How sentiment changes over time  
✅ **Topic Analysis** - What people are discussing  
✅ **Extreme Opinions** - Most positive/negative comments  
✅ **Sentiment Distribution** - Proportion of each class  
✅ **Emotional Intensity** - Average sentiment strength  
✅ **Anomalies** - Unusual sentiment patterns  

---

## 🎓 Learning Outcomes

This project teaches:
- 📚 **NLP Fundamentals** - Text preprocessing, tokenization
- 🤖 **Machine Learning** - Sentiment analysis, topic modeling
- 📊 **Data Analysis** - Statistical analysis, distribution analysis
- 📈 **Visualization** - Creating actionable charts
- 💻 **Python Data Science** - Pandas, Scikit-learn, NLTK
- 🚀 **Production ML** - Deploying models to dashboards

---

## 💡 Real-World Applications

**Marketing Teams**
- Monitor brand sentiment in real-time
- Identify trending topics and conversations
- Track campaign perception

**Content Creators**
- Understand audience reaction to content
- Identify what resonates with followers
- Optimize for positive engagement

**Researchers**
- Analyze public opinion on topics
- Study discussion trends
- Collect large datasets for analysis

**Business Intelligence**
- Market sentiment monitoring
- Competitive intelligence
- Crisis detection (negative sentiment spikes)

---

## 🐛 Troubleshooting

### Dashboard won't load?
```bash
streamlit run app.py --logger.level=debug
```

### VADER scores seem off?
- VADER is optimized for social media (handles slang, emojis, caps)
- Check compound score: >0.05 = positive, <-0.05 = negative, else neutral

### Topic modeling not showing results?
- Ensure you have 50+ documents minimum
- Use cleaned text for better topics
- Adjust NUM_TOPICS in config.py

---

## 📚 Resources

- [VADER Paper](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM14/paper/viewPaper/8109)
- [NLTK Documentation](https://www.nltk.org)
- [Scikit-learn ML](https://scikit-learn.org)
- [Understanding LDA](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)
- [Streamlit Docs](https://docs.streamlit.io)

---

## 🎯 Next Steps for Data Scientists

1. **Explore the Data** - Run `Data_Understanding.ipynb` for EDA
2. **Understand Preprocessing** - Review `preprocessing.py`
3. **Learn VADER** - Check `Vader_Processing.ipynb`
4. **Modify Models** - Experiment with LDA parameters
5. **Deploy Dashboard** - Share insights with Streamlit Cloud
6. **Extend Analysis** - Add new visualization, metrics, or models

---

## 💼 Interview Answer

> *"I built an end-to-end sentiment analysis system for social media text. The project demonstrates core data science skills: I performed EDA to understand the data, applied VADER for sentiment classification, used LDA for unsupervised topic discovery, and created statistical summaries. I then built an interactive Streamlit dashboard to visualize the insights - showing sentiment distribution, trends, and examples. The system processes 160K+ comments and demonstrates how to turn raw text data into actionable business insights through NLP and ML techniques."*

---

## 📊 Project Statistics

- **Lines of Code:** ~2,000
- **Data Points:** 160,000+
- **ML Models:** VADER + LDA
- **Dashboard Load:** <5 seconds
- **Analysis Time:** 2-3 minutes for 160K comments
- **Frameworks:** Scikit-learn, NLTK, Streamlit

---

**Data Science in Action: From Raw Text to Insights** 📊

Made with ❤️ by a data scientist who believes in interpretable, actionable insights.

---

## 🌟 Show Support

- ⭐ Star if this helps with your data science journey
- 🍴 Fork and modify for your use case
- 📢 Share with fellow data scientists

Happy analyzing! 🚀
