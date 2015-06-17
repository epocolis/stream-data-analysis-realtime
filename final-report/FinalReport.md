## Real Time detection of Symptoms of illness in Toronto using twitter data


## Introduction

In the field of public health and safety it is critical for health authorities to be able to quickly detected outbreaks of illnesses or diseases. In addition to traditional methods, social media nows provides an additional channel to detect the outbreak of diseases or illnesses.

Approximately 500 million tweets are sent everyday, according to twitter usage statistics. People share their thoughts and experience about everything in their tweets. These thoughts also involves information about their health. It is this willingness to share information of this nature publicly that makes twitter data a valuable source of real time data for the detection and monitoring of illness.

This project involves the development of a big data product that will attempt to detect symptoms of illness in tweets. The tool will monitor the tweets being sent by residents of Toronto, classify and visualize the symptoms of illness related tweets. The project will utilize state of the art big data tools and proven text analytics algorithms.

## Dataset

This project utilized the tweets produced by users of twitter that originated in the city of Toronto. Approximately 2.8 million Tweets are were collected.

The code used to collect the tweets data is available here: [TwitterCollector.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/PythonTwitterCollector/twitterCollector.py)

The twitter data is provided in json format. The schema/structure of this data is shown below.


## The schema for a tweet

The schema/structure of the tweet data collected was generated and printed using the following snippet of code:

```python
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
# Create the DataFrame
df = sqlContext.jsonFile("twitter_stream.20150519-084907.json")
# Show the content of the DataFrame
df.show()
# Print the schema in a tree format
df.printSchema()


```

### The data format of a single tweet.

```
root
 |-- _corrupt_record: string (nullable = true)
 |-- contributors: string (nullable = true)
 |-- coordinates: struct (nullable = true)
 |    |-- coordinates: array (nullable = true)
 |    |    |-- element: double (containsNull = true)
 |    |-- type: string (nullable = true)
 |-- created_at: string (nullable = true)
 |-- entities: struct (nullable = true)
 |    |-- hashtags: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- text: string (nullable = true)
 |    |-- media: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- display_url: string (nullable = true)
 |    |    |    |-- expanded_url: string (nullable = true)
 |    |    |    |-- id: long (nullable = true)
 |    |    |    |-- id_str: string (nullable = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- media_url: string (nullable = true)
 |    |    |    |-- media_url_https: string (nullable = true)
 |    |    |    |-- sizes: struct (nullable = true)
 |    |    |    |    |-- large: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |    |-- medium: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |    |-- small: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |    |-- thumb: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |-- type: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |-- symbols: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- text: string (nullable = true)
 |    |-- trends: array (nullable = true)
 |    |    |-- element: string (containsNull = true)
 |    |-- urls: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- display_url: string (nullable = true)
 |    |    |    |-- expanded_url: string (nullable = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- url: string (nullable = true)
 |    |-- user_mentions: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- id: long (nullable = true)
 |    |    |    |-- id_str: string (nullable = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |    |-- screen_name: string (nullable = true)
 |-- extended_entities: struct (nullable = true)
 |    |-- media: array (nullable = true)
 |    |    |-- element: struct (containsNull = true)
 |    |    |    |-- display_url: string (nullable = true)
 |    |    |    |-- expanded_url: string (nullable = true)
 |    |    |    |-- id: long (nullable = true)
 |    |    |    |-- id_str: string (nullable = true)
 |    |    |    |-- indices: array (nullable = true)
 |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |-- media_url: string (nullable = true)
 |    |    |    |-- media_url_https: string (nullable = true)
 |    |    |    |-- sizes: struct (nullable = true)
 |    |    |    |    |-- large: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |    |-- medium: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |    |-- small: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |-- thumb: struct (nullable = true)
 |    |    |    |    |    |-- h: long (nullable = true)
 |    |    |    |    |    |-- resize: string (nullable = true)
 |    |    |    |    |    |-- w: long (nullable = true)
 |    |    |    |-- type: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |    |    |-- video_info: struct (nullable = true)
 |    |    |    |    |-- aspect_ratio: array (nullable = true)
 |    |    |    |    |    |-- element: long (containsNull = true)
 |    |    |    |    |-- duration_millis: long (nullable = true)
 |    |    |    |    |-- variants: array (nullable = true)
 |    |    |    |    |    |-- element: struct (containsNull = true)
 |    |    |    |    |    |    |-- bitrate: long (nullable = true)
 |    |    |    |    |    |    |-- content_type: string (nullable = true)
 |    |    |    |    |    |    |-- url: string (nullable = true)
 |-- favorite_count: long (nullable = true)
 |-- favorited: boolean (nullable = true)
 |-- filter_level: string (nullable = true)
 |-- geo: struct (nullable = true)
 |    |-- coordinates: array (nullable = true)
 |    |    |-- element: double (containsNull = true)
 |    |-- type: string (nullable = true)
 |-- id: long (nullable = true)
 |-- id_str: string (nullable = true)
 |-- in_reply_to_screen_name: string (nullable = true)
 |-- in_reply_to_status_id: long (nullable = true)
 |-- in_reply_to_status_id_str: string (nullable = true)
 |-- in_reply_to_user_id: long (nullable = true)
 |-- in_reply_to_user_id_str: string (nullable = true)
 |-- lang: string (nullable = true)
 |-- place: struct (nullable = true)
 |    |-- bounding_box: struct (nullable = true)
 |    |    |-- coordinates: array (nullable = true)
 |    |    |    |-- element: array (containsNull = true)
 |    |    |    |    |-- element: array (containsNull = true)
 |    |    |    |    |    |-- element: double (containsNull = true)
 |    |    |-- type: string (nullable = true)
 |    |-- country: string (nullable = true)
 |    |-- country_code: string (nullable = true)
 |    |-- full_name: string (nullable = true)
 |    |-- id: string (nullable = true)
 |    |-- name: string (nullable = true)
|-- possibly_sensitive: boolean (nullable = true)
 |-- retweet_count: long (nullable = true)
 |-- retweeted: boolean (nullable = true)
 |-- source: string (nullable = true)
 |-- text: string (nullable = true)
 |-- timestamp_ms: string (nullable = true)
 |-- truncated: boolean (nullable = true)
 |-- user: struct (nullable = true)
 |    |-- contributors_enabled: boolean (nullable = true)
 |    |-- created_at: string (nullable = true)
 |    |-- default_profile: boolean (nullable = true)
 |    |-- default_profile_image: boolean (nullable = true)
 |    |-- description: string (nullable = true)
 |    |-- favourites_count: long (nullable = true)
 |    |-- follow_request_sent: string (nullable = true)
 |    |-- followers_count: long (nullable = true)
 |    |-- following: string (nullable = true)
 |    |-- friends_count: long (nullable = true)
 |    |-- geo_enabled: boolean (nullable = true)
 |    |-- id: long (nullable = true)
 |    |-- id_str: string (nullable = true)
 |    |-- is_translator: boolean (nullable = true)
 |    |-- lang: string (nullable = true)
 |    |-- listed_count: long (nullable = true)
 |    |-- location: string (nullable = true)
 |    |-- name: string (nullable = true)
 |    |-- notifications: string (nullable = true)
 |    |-- profile_background_color: string (nullable = true)
 |    |-- profile_background_image_url: string (nullable = true)
 |    |-- profile_background_image_url_https: string (nullable = true)
 |    |-- profile_background_tile: boolean (nullable = true)
 |    |-- profile_banner_url: string (nullable = true)
 |    |-- profile_image_url: string (nullable = true)
 |    |-- profile_image_url_https: string (nullable = true)
 |    |-- profile_link_color: string (nullable = true)
 |    |-- profile_sidebar_border_color: string (nullable = true)
 |    |-- profile_sidebar_fill_color: string (nullable = true)
 |    |-- profile_text_color: string (nullable = true)
 |    |-- profile_use_background_image: boolean (nullable = true)
 |    |-- protected: boolean (nullable = true)
 |    |-- screen_name: string (nullable = true)
 |    |-- statuses_count: long (nullable = true)

```

## Approach

Summary of approach:

The tweets were collected and then manually labelled[1:illness symptom, 0:non illness symptom]. The text of tweets were then used to generate feature vectors for each tweet. The feature vectors along with the labels of each tweet was then used to train naive bayes classifier model. This model was then used to classify tweets streamed in real-time. Below the details of the approach is presented.

The following block diagram illustrates the steps to be taken throughout this project.

![Approach](https://raw.githubusercontent.com/LeotisBuchanan/stream-data-analysis-realtime/master/final-report/process.png)


1. ** Tweet collection **
   1. A python application was written to stream and store tweets originating from within Toronto, Canada. The collected tweets were stored on the local file system for later analysis. Approximately 2.8 Million tweets were collected during the period May 19, 2015 to June 4, 2015.

    The following python application was used to performed the collection, [TwitterDataCollector.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/data_collection/twitterCollector.py)

    To ensure continous collection [supervisord](http://supervisord.org/)
    was used to ensure that in the event that the application was terminated, it would be automatically restarted.

2. ** Tweet Cleaning and transformation **

   The following steps were taken to clean and transform the data. The objective of this phase was to transform the data into a form that could be used to trained the classifier.

    1. **Filtering:** [543 terms]
       (https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/data/freebase-symptoms-just-terms.data) used to describe symptoms of illness were obtained from  [freebase](https://www.freebase.com/medicine/symptom?instances=). These terms were used to filter all non illness symptom tweets. The filtering of the tweets were performed using the following pyspark application:

      [FilterAndConvertToCSV.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/filterandConvertToCSV.py).

    2. **Data transformation:** The following fields were extracted from each collected tweet.
      * **id**: the id of the tweet.
      * **created_at**: the time the tweet was      tweeted.
      * **lat**: the latitude from which this tweet was tweeted.
      * **lon**: the longitude from which this tweet was tweeted.
      * **text**: the text of the tweet.


    3. **Text Preprocessing and feature generation:**
       The following processes was perform on the the text of each tweet:
       * Tokenization: The text of each tweet was broken into a list of tokens.
       * Stop words removal: Stops such as "a, this, that .." was removed from all the tweet text
       * Stemming: Each word/token in the tokens word list were then [stemmed](https://en.wikipedia.org/wiki/Stemming)
       * Each of the stemmed tweet text were then converted to [feature vectors](https://en.wikipedia.org/wiki/Feature_vector).



## Training of the Classifier


1.The preprocessed labelled tweets were used as test and training data for a naive bayes classifier. The following code was     used to train and save the model to file. [trainNaiveBayesModel.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/naive_bayes_tweet_classifier/trainNaiveandCreateNaiveBayesModel.py)
2. The labelled  tweets was split into two parts 70% of the labelled tweets were used as training data, while the remaining 30% were used as test data.


## Classifying tweets in Real Time.

1. A [spark](http://) application was created that   allowed the incoming stream of tweets to be classified and written to disk in realtime. The architecture of the system is shown below.

<p align="center">
  <img src="https://raw.githubusercontent.com/LeotisBuchanan/stream-data-analysis-realtime/master/final-report/realtimetweetsystem_arch.png"/>
  <h3 align="center">System architecture</h3>
</p>

The code for the system can be found here [Source Code]
(https://github.com/LeotisBuchanan/stream-data-analysis-realtime/tree/master/code)

The functionality of each system components are as follows:

* **Twitter Stream API(1):** This is provided by twitter see [Twitter API](http://https://dev.twitter.com/streaming/overview)

* ** Twitter Kafka Producer(2)** This preprocess the incoming tweet stream, it extracts the required fields from the incoming tweet.It then generates a message having the extracted fields as its body. Using kafka allows the system to scale out significantly by adding more kafka nodes.This get a better understanding of t
he functionality of this component, you can read the source code here: [TwitterKafkaProducer](https://raw.githubusercontent.com/LeotisBuchanan/stream-data-analysis-realtime/master/code/producer/TwitterKafkaProducer.py)

* ** Twitter Kafka Consumer(3):** The messages produced by the Twitter Kafka producer are consumed by this component. Each tweet text is converted to a feature vector. The raw tweets are also stored for later use.

* ** Naive Bayes Classifier(4) :** The vectorized tweet text is then fed to into the classifier. The classifier then automatically labels the tweet text as 0(non-illness symptom) or 1(illness symptom).

* ** The classified tweets are then stored in a nosql database for later visualization and analysis.


### Results

We collected 2.8 million tweets, after filtering the tweets using the freebase terms,The number of tweets containing the
illness symptoms were about 1000. After manually labelling the tweets only about two hundred were tweets stating the symptoms of sender illness. The other issue was that many of the tweets collected did not have user location enabled.

## Conclusions

In this project a data product was successfully created, that classifies tweets in real time as being illness related and non illness related. The data product used apache spark, a fast and general engine for large-scale data processing computer tool and apache kafka.The tool was developed entirely in python. The architecture of the tool, allows the tool to process large quantity of data(tweets) without any modifications.

We used collected tweets to train and test a naive bayes classifier model. This model was then used in real time to classify tweets streamed from twitter live feed.

All the code for the project is available on github.
