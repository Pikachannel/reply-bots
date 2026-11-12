import string
from nltk.stem import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

class ToneAnalysis:
    def __init__(self, blocklist: set[str]) -> None:
        self.model = SentimentIntensityAnalyzer()
        self.stemmer = PorterStemmer()
        self.blocklist = {self.stemmer.stem(word) for word in blocklist}


    def get_tone(self, text) -> bool:
        # -- Normalisation
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        words = {self.stemmer.stem(word) for word in text.split()}

        # -- Check if there is a word in blocklsit
        if words & self.blocklist:
            return True
        
        # -- Analyse sentiment of message
        scores = self.model.polarity_scores(text)

        if scores["compound"] < -0.05:
            return True

        return False