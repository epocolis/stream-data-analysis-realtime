from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
# Create the DataFrame
#load all the json files in the directory
path = "/data/raw_tweets/"
df = sqlContext.jsonFile(path)
# Show the content of the DataFrame
df.show()
# Print the schema in a tree format
df.printSchema()
#get all the text of the tweets
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


tweetCSV = results.map(generateCSV)
