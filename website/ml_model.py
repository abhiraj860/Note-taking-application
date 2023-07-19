from flask import Flask
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

app = Flask(__name__)

def nltk_vader_sentiment(str):
        sentimentColors = [
                "#FF0000", "#8B0000", "#B22222", "#DC143C", "#CD5C5C", "#F08080", "#FF6347",
                "#FF7F50", "#FF8C00", "#FFA500", "#FFD700", "#F0E68C", "#EEE8AA", "#FFFF00",
                "#FFFFE0", "#FFFACD", "#FFFFF0", "#F0FFF0", "#90EE90", "#32CD32", "#008000"
        ]


        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(str)
        return scores["compound"], sentimentColors[int(round(scores["compound"], 1) * 10 + 10)]

    
   