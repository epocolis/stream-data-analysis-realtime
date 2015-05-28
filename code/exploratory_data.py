from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
# Create the DataFrame
df = sqlContext.jsonFile("twitter_stream.20150519-084907.json")
# Show the content of the DataFrame
df.show()
# Print the schema in a tree format
df.printSchema()
#get all the text of the tweets
# Register the DataFrame as a table.
df.registerTempTable("tweet")
results = sqlContext.sql("SELECT id, text FROM tweet")
results_with_text = results.filter(lambda p: p.text not None)
text = results.map(lambda p: p.text)
for t in text.collect():
  print t
