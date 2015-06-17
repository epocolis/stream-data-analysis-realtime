from pyspark.sql import SQLContext
from sets import Set
sqlContext = SQLContext(sc)
path = "data/raw_tweets/"
filter_terms_file_path = "freebase-symptoms-just-terms.txt"
df = sqlContext.jsonFile(path)
filter_terms = sc.textFile(filter_terms_file_path)
filter_terms_set = Set(filter_terms.collect())
# Register the DataFrame as a table.
df.registerTempTable("tweet")
results = sqlContext.sql("SELECT id,user.id,user.lang,created_at, coordinates,text FROM tweet where user.lang='en'")

def generateCSV(tweet):
  result = ""
  if tweet.text:
    t = tweet.text.encode('utf-8')

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


#filter tweets to find health related tweets
filter_health_tweets = results.rdd.filter(healthFilter)
