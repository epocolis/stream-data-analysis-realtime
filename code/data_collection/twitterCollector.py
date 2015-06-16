#!/usr/bin/env python
"""
TwitterCollector - Collects and store tweets from twitter live streaming api
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



#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json, time, sys
#Variables that contains the user credentials to access Twitter API


access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api = None):
        self.root_dir = '/home/linode/PythonTwitterCollector/collected_streaming_data/'
        self.counter = 0
        self.fprefix = "twitter_stream"
        self.log = open(self.root_dir + 'log' + '.'
                               + time.strftime('%Y%m%d-%H%M%S') + '.txt', 'w')

        self.output = open(self.root_dir + self.fprefix + '.'
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.log.write("Started: " + time.strftime('%Y%m%d-%H%M%S'))

    def on_data(self, data):
        if  'in_reply_to_status' in data:
            self.on_status(data)
        return True

    def on_status(self, status):
        self.output.write(status + "\n")
        self.counter += 1
        print "tweets collected {count}".format(count=self.counter)
        return


    def on_limit(self, track):
        self.log.write(track + "\n")
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        self.log.write('Error: ' + str(status_code) + "\n")
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        self.log.write("Timeout, sleeping for 60 seconds...\n")
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    nlat = 43.855458
    wlon = -79.639219
    slat = 43.581024
    elon = -79.116897
    #North Latitude: 43.855458 South Latitude: 43.581024 , East Longitude: -79.116897 West Longitude: -79.639219
    GEOBOX_TORONTO = [wlon,slat, elon,nlat]
    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.filter(locations=GEOBOX_TORONTO)
