"""
add licence and copyright stuff
"""
## Spark Application - execute with spark-submit

## Imports
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from sets import Set

## Module Constants
DATA_PATH = "data/raw_tweets/"
FILTER_TERMS_FILE_PATH = "/data/filter/freebase-symptoms-just-terms.data"
PROCESSED_DATA_PATH = "/data/processed/"
APP_NAME = "FilterAndConvertToCSV"

## Closure Functions

def generateCSV(tweet):
  result = ""
  if tweet.text:
    t = tweet.text.encode('utf-8')
    #remove the commas from the tweet text
    t = t.replace(",", "")
  else:
    t = ""

  if tweet.coordinates:
    c = tweet.coordinates
    lat = c.coordinates[0]
    lon = c.coordinates[1]
    result =  '{id},{created},{lat},{lon},{text}'.format(id=tweet.id,lat=lat, lon=lon,
                                                         text=t,created=tweet.created_at)
  else:
    lat = ""
    lon = ""
    result =  '{id},{created},{lat},{lon},{text}'.format(id=tweet.id,lat=lat, lon=lon,
                                                         text=t,created=tweet.created_at)
  return result


"""
  performs a simple filter by terms
"""

def healthFilter(tweet):
  if tweet.text:
    t = tweet.text.encode('utf-8')
    tweets_set = Set(t.split())
    if filter_terms_set.intersection(tweets_set):
      return True
    else:
      return False
  else:
    return False

"""
  write the rdd to storage
"""
def writeRDD(rddFile, path):
  rddFile.saveAsTextFile(path)


## Main functionality

def main(sc):
  sqlContext = SQLContext(sc)
  df = sqlContext.jsonFile(DATA_PATH)
  #add the filter file
  sc.addFile(FILTER_TERMS_FILE_PATH)
  filter_terms = sc.textFile(SparkFiles.get("freebase-symptoms-just-terms.txt"))
  filter_terms_set = Set(filter_terms.collect())
  # Register the DataFrame as a table.
  df.registerTempTable("tweet")
  results = sqlContext.sql("SELECT id,user.id,user.lang,created_at, coordinates,text FROM tweet where user.lang='en'")
  #filter tweets to find health related tweets
  filter_health_tweets = results.rdd.filter(healthFilter)
  writeRDD(filter_health_tweets)



if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    # Execute Main functionality
    main(sc)
