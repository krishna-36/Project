import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def summarizer_text1(text):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(filtered_words)
    most_common = word_freq.most_common(4)  # Get the 4 most common words
    return most_common
