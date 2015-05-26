from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
# Create the DataFrame
df = sqlContext.jsonFile("twitter_stream.20150519-084907.json")
# Show the content of the DataFrame
df.show()
# Print the schema in a tree format
df.printSchema()
