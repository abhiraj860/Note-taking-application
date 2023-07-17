from flask import Flask
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
    
app = Flask(__name__)

def nltk_vader_sentiment(str):
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(str)
        # sentiment = ""
        # if scores["compound"] >= 0.05:
        #     sentiment = "Positive"
        # elif scores["compound"] <= -0.05:
        #     sentiment = "Negative"
        # else:
        #     sentiment = "Mixed"
        return scores["compound"]

    
   