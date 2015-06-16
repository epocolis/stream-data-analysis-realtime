"""

filterandConvertToCSV.py- filter tweets and convert tweets from json to 
csv.
Copyright (C) 2015  Leotis Buchanan
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
## Spark Application - execute with spark-submit

## Imports
from pyspark import SparkConf, SparkContext,SparkFiles
from pyspark.sql import SQLContext
from sets import Set
import csv
import StringIO
import sys
import re

## Module Constants
DATA_PATH = "data/raw_tweets/"
FILTER_TERMS_FILE_PATH = "data/filter/freebase-symptoms-just-terms.txt"
PROCESSED_DATA_PATH = "data/processed/"
APP_NAME = "FilterAndConvertToCSV"

## Closure Functions
"""
def generateCSV(tweet):
  result = ""
  if tweet.text:
    t = tweet.text.encode('utf-8')
    #remove the commas from the tweet text
    t = t.replace(",", "")
    #remove the non-ascii stuff, smiley faces etc
    t = re.sub(r'\W+', ' ', t)
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
  return result+"," + "0"
"""

"""
  performs a simple filter by terms
"""

def healthFilter(tweet):
  if tweet.text:
    t = tweet.text.encode('utf-8')
    tweets_set = Set(t.split())
    if filter_terms_set_bc.value.intersection(tweets_set):
      return True
    else:
      return False
  else:
    return False

"""
  write the rdd to storage
"""

def writeRecords(records):
    """Write out CSV lines"""
    default_label = "0"
    output = StringIO.StringIO()
    writer = csv.DictWriter(output,fieldnames = ["id","lat", "lon", "lang","created_at","text","label"])
    for record in records:
      if record.text:
        text = record.text.encode('utf-8')
        text = text.replace(",", "")
        #remove everything except alphanumeric characters
        text = re.sub(r'\W+', ' ', text)
      else:
        text = ""
      coord = record.coordinates
      lat = ""
      lon = ""
      if coord:
        lat = coord.coordinates[0]
        lon = coord.coordinates[0]
      writer.writerow({'id':record.id ,'lat':lat, 'lon':lon, 'lang':record.lang,'created_at':record.created_at, 'text':text ,'label':default_label})

    return [output.getvalue()]




## Main functionality

def main(sc):
  sqlContext = SQLContext(sc)
  df = sqlContext.jsonFile(DATA_PATH)
  #add the filter file
  sc.addFile(FILTER_TERMS_FILE_PATH)
  filter_terms = sc.textFile(SparkFiles.get("freebase-symptoms-just-terms.txt"))
  global filter_terms_set_bc
  filter_terms_set_bc = sc.broadcast(Set(filter_terms.collect()))
  # Register the DataFrame as a table.
  df.registerTempTable("tweet")
  results = sqlContext.sql("SELECT id,user.id,user.lang,created_at, coordinates,text FROM tweet where user.lang='en'")
  #filter tweets to find health related tweets
  filter_health_tweets = results.rdd.filter(healthFilter)
  filter_health_tweets.mapPartitions(writeRecords).saveAsTextFile("output/")


if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    # Execute Main functionality
    main(sc)


