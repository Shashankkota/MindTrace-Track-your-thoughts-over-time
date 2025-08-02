import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from datetime import datetime
import os

class SentimentAnalyzer:
    def __init__(self):
        """Initialize the sentiment analyzer with VADER"""
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            # Download required NLTK data if not available
            nltk.download('vader_lexicon', quiet=True)
            self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of given text using VADER
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Contains sentiment label and compound score
        """
        if not text or text.strip() == "":
            return {"sentiment": "Neutral", "score": 0.0}
        
        # Get sentiment scores
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        # Classify sentiment based on compound score
        if compound_score >= 0.05:
            sentiment = "Positive"
        elif compound_score <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            "sentiment": sentiment,
            "score": compound_score
        }
    
    def get_sentiment_color(self, sentiment):
        """Get color for sentiment visualization"""
        colors = {
            "Positive": "#28a745",  # Green
            "Neutral": "#6c757d",   # Gray
            "Negative": "#dc3545"   # Red
        }
        return colors.get(sentiment, "#6c757d")
    
    def get_sentiment_emoji(self, sentiment):
        """Get emoji for sentiment display"""
        emojis = {
            "Positive": "😊",
            "Neutral": "😐",
            "Negative": "😔"
        }
        return emojis.get(sentiment, "😐") 