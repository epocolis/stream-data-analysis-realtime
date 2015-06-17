## Real Time detection of Symptoms of illness in Toronto using twitter data


## Introduction

In the field of public health and safety it is critical for health authorities to be able to quickly detected outbreaks of illnesses or diseases. In addition to traditional methods, social media nows provides an additional channel to detect the outbreak of diseases or illnesses.

Approximately 500 million tweets are sent everyday, according to twitter usage statistics (Twitter usage stats). People share their thoughts and experience about everything in their tweets. These thoughts also involves information about their health. It is this willingness to share information of this nature publicly that makes twitter data a valuable source of real time data for the detection and monitoring of illness.

This project involves the development a big data product that will attempt to detect the outbreak/occurrence of illness. The tool will monitor the tweets being sent by residents of Toronto, classify and visualize the symptoms of illness related tweets. The project will utilize state of the art big data tools and proven text analytics algorithms.
First provide the context of the problem and then state the problem (your main research question). Second, write briefly that what are you proposing to solve this problem (don’t write details of the solution here).
The research problem and question should be clearly specified here

## Dataset

This project will utilize the tweets produced by users of twitter that originates/originated in the city of Toronto. Tweets are currently being collected. At the time of writing this article around 1.2G of tweets have been collected and stored.

The code use to collect the tweets data is available here: [TwitterCollector.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/PythonTwitterCollector/twitterCollector.py)

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


Give the description of the dataset that you are using along with the individual attributes you will or will not use in your analysis.
Also mention the source of the dataset (where did you get it from). In case the data is curated and created by you please explain the details.
Descriptive statistics of the attributes and datasets can also be provided here.

Approach

## Approach

Summary of approach:

The tweets were collected and then manually labelled[1:illness symptom, 0:non illness symptom]. The text of tweets were then used to generate feature vectors for each tweet. The feature vectors along with the labels of each tweet was then used to train naive bayes classifier model. This model was then used to classify tweets streamed in real-time. Below the details of the approach is presented.  

The following block diagram illustrates the steps to be taken throughout this project.

![Approach](https://raw.githubusercontent.com/LeotisBuchanan/stream-data-analysis-realtime/master/docs/steps.png)


1. ** Data collection **
   1. A python application was written to stream and store tweets originating from within Toronto, Canada. The collected tweets were stored on the local file system for later analysis. Approximately 2.8 Million tweets were collected during the period May 19, 2015 to June 4, 2015.

    The following python application was used to performed the collection, [TwitterDataCollector.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/data_collection/twitterCollector.py)

    To ensure continous collection [supervisord](http://supervisord.org/)
    was used to ensure that in the event that the application was terminated, it would be automatically restarted.

2. ** Data Cleaning and transformation **

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



## Training of Classifier


1.The preprocessed labelled tweets were used as test and training data for a naive bayes classifier. The following code was     used to train and save the model to file. [trainNaiveBayesModel.py](https://github.com/LeotisBuchanan/stream-data-analysis-realtime/blob/master/code/naive_bayes_tweet_classifier/trainNaiveandCreateNaiveBayesModel.py)
2. The labelled  tweets was split into two parts 70% of the labelled tweets were used as training data, while the remaining 30% were used as test data.


## Classifying tweets in Real Time.

1. The classification of tweets in real time was achieve using the following 

4.
5. 1. Collect tweets
   * In this phase a python application will be developed to stream and store about 4 Gigabyte of geo bounded tweets. Only tweets that originate within Toronto will be collected.
   * The collected tweets will be store in there raw form in and hadoop cluster.

2. Exploratory Data Analysis
   * Apache spark will then be used to perform exploratory data analysis on the collected tweets. The objective of this exercise will be to understand the structure and characteristics of the data.

3. Clean and Transform the data
   * A reusable spark app will be written, to clean and transform the data.The following transformation will be done:
     * Tokenization.
     * Stemming
     * Hashing

4. Store Transformed data in HDFS.
5. Features creation.
   * A spark app will be written, that retrieves the data from HDFS and use to generate features to be  used by the classifier.

6. Train a NLP text classifier
   * The features created in 5 along with symptom data scraped from wikipedia, will be used as training input to generate a text classification model for the twitter data.
   * The classifier will automatically label tweets as symptom or no symptom.
   * The parameters for the classifier will be stored in hdfs for later access.

7. Create Kafka Twitter Producer
   * This producer will be used to connect to the twitter stream. It will generate a message whenever a new tweet arrives. This message will contain the tweet. The message that is generated can be consumed by multiple consumers.

8. Consume and classify tweet.
   * A spark app will be written that consumes, transforms , generate features and classify the incoming tweet message received from the module in 7. This app will reuse the classifier created in [6]. The tweet will classified as a symptom or non-symptom.

9. Send Classification to Dashboard.
   * The spark app from [8] will send the classification to a dashboard application. This dashboard will be composed   of a map of Toronto and other charts. The function of the dashboard will be to visualize the location and count of illness and other metrics in near real time.



## Classifying tweets in real time.




First, create a block diagram for the steps of your approach to clearly provide an overview. For example, if you first scrapped twitter, second applied NLP techniques to extract keywords, third labelled the tweets as positive and negative using a set of keywords, and fourth build a classifier, then you should create a box for each of the steps with arrows connecting one step to the next one. A sample block diagram is shown below.

Second, explain each of the steps in detail. What are you planning to do in each step or have already done. For example, in the above case you would create subheadings for each of the steps.
Step 1: <Name of the step>
Write details of the step 1. If there is any source code that you’d like to share then provide the link of the Github.
Step 2: <Name of the step>
Write details of the step 2. If there is any source code that you’d like to share then provide the link of the Github.
Step N: <Name of the step>
Write details of the step N. If there is any source code that you’d like to share then provide the link of the Github.

### Results

## Plot location of symtoms related tweets
## Plot time distribution of symptoms related tweets
## plot graph showing histogram of various symptoms, comparing the frequency
## plot graph showing percentage of tweets that were health related verse not health related
## plot graph showing the most mention symptom


## classifier evaluation
##  provide the confusion matrix
##  the accuracy of the classifier
##  provide the ROC AUC CURVE


##Conclusions




## Future work




##References


arts showing the results
2. Write description of the tables and charts, such that they show the usefulness for an organization
3. Identify the evaluation measures, such as accuracy, precision, recall, etc.

Conclusions

Give a short summary (one to two paragraphs) of your analysis and conclude the discussion by defining the usefulness of your analysis.
