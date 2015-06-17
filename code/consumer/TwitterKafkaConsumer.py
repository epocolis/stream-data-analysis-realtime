"""
# TwitterKafkaConsumer.py- Consume Tweet messages and classify them
# as 1[illness symptom]  or 0 [non illness symptom]
#
# Copyright (C) 2015  Leotis Buchanan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

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



# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
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

def processText(tweet_tuple):

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
    result =  '{id},{created},{lat},{lon},{text}, {stemmed_text}'.format(id=tweet_id,lat=lat,
                lon=lon,created=created_at,
                text=tweet_txt,stemmed_text=st)
    return result




def featurize(tweet_tuple):
    """
    generate features for this tweet text
    returns: csv line with a the last field
    containing the feature vector for the tweet

    """
    ID_FIELD_IDX = 0
    CREATED_AT_IDX = 1
    TIMESTAMP_MS = 2
    LANG_FIELD_IDX = 3
    LON_FIELD_IDX = 4
    LAT_FIELD_IDX = 5
    TEXT_IDX = 6

    TWEET_IDX = 1

    #split the tweet into components id, lang, text, lon, lat etc
    tweet_attrib_list = tweet_tuple[TWEET_IDX].split(",")
    #get the text
    text = tweet_attrib_list[TEXT_IDX]
    #tokenize the text
    word_list = tokenize(text)
    #remove stop words
    word_list = removeStopWords(word_list)
    #remove punctuations
    word_list = removePunctuation(word_list)
    #stemmed the tokens
    word_list = stemmed_tokens(word_list)
    st = " ".join(word_list)
    #hash the words
    htf = HashingTF(50000)
    hashedfeatures = htf.transform(text)
    tweet = tweet_tuple[TWEET_IDX]
    results = {'tweet':tweet, 'features':hashedfeatures}
    return  results

def classify(tweet_hashfeatures_map):
    features = tweet_hashfeatures_map['features')
    #predict the class here, if its 1 return true
    #false otherwise
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: TwitterKafkaConsumer.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    global PUNCTUATION_BC
    global STOPWORDS_BC
    global STEMMER_BC

    sc = SparkContext(appName="TwitterKafkaStreamingConsumer")
    ssc = StreamingContext(sc, 1)

    PUNCTUATION_BC = sc.broadcast(Set(string.punctuation))
    STOPWORDS_BC = sc.broadcast(Set(stopwords.words('english')))
    STEMMER_BC = sc.broadcast(PorterStemmer())

    #load saved model
    #broadcast saved model so that other workers can
    #access it



    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "kafka-consumer", {topic: 1})
    tweets_with_text = kvs.filter(lambda tweet: len(tweet)==2)
    tweet_and_hashedfeatures = tweets_with_text.map(featurize)
    health_tweets = tweet_and_hashedfeatures.filter(classify)
    health_tweets.pprint()


    ssc.start()
    ssc.awaitTermination()
