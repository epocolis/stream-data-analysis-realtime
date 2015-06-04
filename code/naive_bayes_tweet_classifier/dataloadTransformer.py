"""
This module performs the following functions:
1- Loads the tweets from storage
2- Tokenize the tweets
3- remove stop words
4- remove punctuation

input: 
output: 


"""
import string
import json 
import sys
#nltk libraries
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

#spark libraries
from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes

from sets import Set

#global constants

INPUT_DATA_PATH = "data/processed"

# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
    tokens = word_tokenize(text)
    tokens_lowercased = [t.lower() for t in tokens]
    return tokens_lowercased

def removeStopWords(word_list):
    word_list_no_stopwords = [w for w in word_list if not w in STOPWORDS_BC.value]
    return word_list_no_stopwords


def stemmed_tokens(word_list):
    stemmed = [STEMMER_BC_value.stem(w) for w in word_list]
    stemmed_words_list= [w for w in stemmed if w]
    return stemmed_words_list


def removePunctuation(word_list):
    """
     remove all the punctuations from the given
     list of tokens
    """
    no_punctuation_list = []
    for word in word_list:
        punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION_BC.value])
        no_punctuation_list.append(punct_removed)
    return no_punctuation_list


def processText(tweet):
  if tweet.text:
    text = tweet.text
    word_list = tokenize(text)
    word_list = removeStopWords(word_list)
    word_list = removePunctuation(word_list)
    word_list = stemmed_tokens(word_list)
  else:
      return []

def main(sc, argv):
    global PUNCTUATION_BC
    global STOPWORDS_BC
    global STEMMER_BC
    PUNCTUATION_BC = sc.broadcast(Set(string.punctuation))
    STOPWORDS_BC = sc.broadcast(Set(stopwords.words('english')))
    STEMMER_BC = sc.broadcast(PorterStemmer())

    #read the filter tweets from file
    df = sqlContext.jsonFile(INPUT_DATA_PATH)
    df.registerTempTable("tweet")
    results = sqlContext.sql("SELECT id,user.id,user.lang,created_at, coordinates,text FROM tweet where user.lang='en'")
    transformed_tweet = results.map(processText)

APP_NAME = "DataLoadTransformer"

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    # Execute Main functionality
    args_list = sys.argv[1:]
    main(sc, args_list)
