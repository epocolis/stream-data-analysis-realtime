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

INPUT_DATA_PATH = "output/"

# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
    """ Parse a line in the Apache Common Log format
    Args:
        logline (str): a line of text in the Apache Common Log format
    Returns:
        tuple: either a dictionary containing the parts of the Apache Access Log and 1,
               or the original invalid log line and 0
    """
    tokens = word_tokenize(text)
    tokens_lowercased = [t.lower() for t in tokens]
    return tokens_lowercased

def removeStopWords(word_list):
    word_list_no_stopwords = [w for w in word_list if not w in STOPWORDS_BC.value]
    return word_list_no_stopwords


def stemmed_tokens(word_list):
    stemmed = [STEMMER_BC.value.stem(w) for w in word_list]
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

    ID_FIELD_IDX = 0
    LAT_FIELD_IDX = 1
    LON_FIELD_IDX = 2
    LANG_FIELD_IDX = 3
    CREATED_AT_IDX = 4
    TEXT_FIELD_INDEX = 5

    tweet = tweet.encode('utf-8')
    tweet_record_list =  tweet.split(",")
    tweet_txt = tweet_record_list[TEXT_FIELD_INDEX]
    tweet_id = tweet_record_list[ID_FIELD_IDX]
    lat = tweet_record_list[LAT_FIELD_IDX]
    lon= tweet_record_list[LON_FIELD_IDX]
    lang = tweet_record_list[LANG_FIELD_IDX]
    created_at = tweet_record_list[CREATED_AT_IDX]
    word_list = tokenize(tweet_txt)
    word_list = removeStopWords(word_list)
    word_list = removePunctuation(word_list)
    word_list = stemmed_tokens(word_list)
    st = " ".join(word_list)
    result =  '{id},{created},{lat},{lon},{text}, {stemmed_text}'.format(id=tweet_id,lat=lat, lon=lon,created=created_at,text=tweet_txt,stemmed_text=st)
    return result



def main(sc, argv):
    global PUNCTUATION_BC
    global STOPWORDS_BC
    global STEMMER_BC
    PUNCTUATION_BC = sc.broadcast(Set(string.punctuation))
    STOPWORDS_BC = sc.broadcast(Set(stopwords.words('english')))
    STEMMER_BC = sc.broadcast(PorterStemmer())

    #read the filter tweets from file
    tweets_rdd = sc.textFile(INPUT_DATA_PATH)
    no_empty_record_rdd = tweets_rdd.filter(lambda x: len(x.split(",")) == 6)
    transformed_tweets = no_empty_record_rdd.map(processText)
    transformed_tweets.saveAsTextFile("data/output/tokenized/")


APP_NAME = "DataLoadTransformer"

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    # Execute Main functionality
    args_list = sys.argv[1:]
    main(sc, args_list)
