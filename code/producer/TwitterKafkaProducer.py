#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#



from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import arrow
import os
import json, time, sys
from kafka import KafkaClient,SimpleProducer, SimpleConsumer
import json
import re

access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

class TwitterStreamListener(StreamListener):
    def __init__(self, api = None):
        #connect to the kafka broker
        #need to handle error
        self.topic = "tweet"
        self.kafka = KafkaClient("localhost:9092")
        self.producer = SimpleProducer(self.kafka)


    def on_data(self, data):
        if  'in_reply_to_status' in data:
            self.on_status(data)
        return True

    def on_status(self, data):
        tweet = json.loads(data)
        text = tweet.get('text',' ')
        coord = tweet.get('coordinates', None)
        created_at = tweet.get('created_at'," ")
        id = tweet.get('id', ' ')
        lang = tweet.get('lang',' ')
        user = tweet.get('user',"user")
        timestamp = tweet.get('timestamp_ms'," ")
        timestamp = arrow.get(timestamp)
        text = re.sub(r'\W+', ' ', text)
        lon,lat = "",""
        print tweet.keys()
        if coord:
            lon = coord['coordinates'][0]
            lat = coord['coordinates'][1]
            
        tweet_csv = "{id}, {created_at}, {timestamp},{lang}, {lon}, {lat},{text},0".format(id=id,created_at=created_at,timestamp=timestamp,lang=lang,
                     lon=lon, lat=lat,text=text)


        if lang == 'en':
            print tweet_csv
            self.producer.send_messages(self.topic, tweet_csv)
        else:
            print "not english"
            print tweet_csv
        return


    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return

if __name__ == '__main__':
    l = TwitterStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    nlat = 43.855458
    wlon = -79.639219
    slat = 43.581024
    elon = -79.116897
    #North Latitude: 43.855458 South Latitude: 43.581024 , East Longitude: -79.116897 West Longitude: -79.639219
    GEOBOX_TORONTO = [wlon,slat, elon,nlat]
    stream.filter(locations=GEOBOX_TORONTO)

