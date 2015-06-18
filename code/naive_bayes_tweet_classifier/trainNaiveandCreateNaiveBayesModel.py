"""



This module performs the following functions:
1- Loads the tweets from storage
2- Tokenize the tweets
3- remove stop words
4- remove punctuation


"""
import string
import json
import sys
#spark libraries
from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import NaiveBayes

#global constants
INPUT_LABEL_TWEETS_DATA_PATH = "data/input/labeledtweets"
NAIVE_BAYES_MODEL_PATH = "model/naivebayes"


from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint


def generatedHashedFeatures(tweet):
    #get label from tweet
    #get text from tweet

    htf = HashingTF(50000)
    lp = LabeledPoint("0", htf.transform(text))
    return lp



def main(sc, argv):
    #read the filter tweets from file
    tweets_rdd = sc.textFile(INPUT_LABEL_TWEETS_DATA_PATH)
    # Create an RDD of LabeledPoints using category labels as labels and tokenized, hashed text as feature vectors
    features_hashed = tweets_rdd.map(generatedHashedFeatures)
    # persist the RDD so it won't have to be re-created later
    features_hashed.persist()
    #randomly split the data into test and training data
    training_data, testing_data = features_hashed.randomSplit([0.7, 0.3])
    #finally train a naive bayes model
    naivebayes_model = NaiveBayes.train(training_data)


APP_NAME = "TrainAndCreateNaiveBayesModel"

if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
    # Execute Main functionality
    args_list = sys.argv[1:]
    main(sc, args_list)
