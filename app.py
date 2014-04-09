#!/usr/bin/python
# -*- coding: latin-1 -*-

from flask import Flask, redirect, session, url_for, request, g, render_template, request
from flask.ext.tweepy import Tweepy
from tweepy.streaming import StreamListener
from flask.ext.socketio import SocketIO, emit
from threading import Timer, Thread
import json
import csv
import string
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import time

consumer_key="HJC58RkbqZeHo0Z6sesPrKWRc"
consumer_secret="2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4"
access_token="1007063444-nU2zSoqqvoOrKtttK6RBL4YK7PQ0UvnZAVb0GFo"
access_token_secret="C7SYtnNCX5mAZLFvhP5QaYam5iTnvokOfKQ7LlDFEBEL4"

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
api = None
sent_dict = dict()
socketio = SocketIO(app)

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
	def on_data(self, data):
		#print data
		dic = json.loads(data)
		print dic
		sent = calc_sentiment(dic['text'])
		socketio.emit('tweet', {'text': dic['text'], 'id': dic['id_str'], 'sent':sent}, namespace='/test')
		return True

	def on_error(self, status):
		print status

@socketio.on('connect', namespace='/test')
def test_connect():
	emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
	print('Client disconnected')

@app.before_request
def before_request():
	if api == None:
		initialize()

@app.route('/', methods = ['GET'])
def index():
	return render_template("index.html")

def initialize():
	global api, sent_dict
	if api != None:
		return "Already initialized"
	app.config.setdefault('TWEEPY_CONSUMER_KEY', consumer_key)
	app.config.setdefault('TWEEPY_CONSUMER_SECRET', consumer_secret)
	app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', access_token)
	app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', access_token_secret)
	test = Tweepy(app)
	api = test.api
	
	sent_filename = "output.txt"
	sent_reader = open(sent_filename)
	for inline in sent_reader:
		row=inline.split()
		word = row[0]
		# Strip its punctuation.
		for punctuation in string.punctuation:
			# Remove all the special punctuations 
			# (string.punctuation=!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
			word = word.replace(punctuation, " ")
			# Get the sentiment value.
			value = float(row[1])
			# Set the key-value pair in the dictionary.
			sent_dict[word] = value
	return "Success!"

def listener():
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = Stream(auth, l)
	stream.filter(track=['basketball'])
	#stream.filter(track=['@Columbia', 'columbia university', '#ColumbiaUniversity', '#Barnard', '#BarnardCollege', '@BarnardCollege'])

def tweet_words(tweet):
	"""Return a list of the words in the text of a tweet not
	including punctuation."""
	tweet_string = tweet
	for punctuation in string.punctuation:
		# Removes all the special punctuations 
		tweet_string = tweet_string.replace(punctuation, " ")
	return tweet_string.split()

def calc_sentiment(tweet):
	"""Calcuate the sentiment of a tweet."""
	global sent_dict
	# Initialize value.
	value = 0.0
	# Get the list of words in the tweet.
	words = tweet_words(tweet)
	# Check if any of the words have an actual value.
	edited = False
	# Add every word's sentiment value to the total.
	for word in words:
		# Only if the word is in the sent_dict do you add the value.
		if word in sent_dict:
			value += sent_dict[word]
			edited = True
	# If none of the words were in the sent_dict, return None.
	if not edited:
		return 0
	return value

if __name__ == '__main__':
	Thread(target = listener).start()
	socketio.run(app)
