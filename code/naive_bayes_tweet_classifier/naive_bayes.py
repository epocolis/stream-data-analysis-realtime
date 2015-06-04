import string
import json 

#nltk libraries
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#spark libraries
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes


PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()


# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
    tokens = word_tokenize(text)
    tokens_lowercased = [t.lower() for t in tokens]
    return tokens_lowercased

def removeStopWords(word_list):
    word_list_no_stopwords = [w for w in word_list if not w in STOPWORDS]
    return word_list_no_stopwords


def stemmed_tokens(word_list):
    stemmed = [STEMMER.stem(w) for w in word_list]
    stemmed_words_list= [w for w in stemmed if w]
    return stemmed_words_list


def removePunctuation(word_list):
    """
     remove all the punctuations from the given
     list of tokens
    """
    no_punctuation_list = []
    for word in word_list:
        punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
        no_punctuation_list.append(punct_removed)
    return no_punctuation_list
