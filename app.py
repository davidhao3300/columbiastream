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
from gevent import monkey; monkey.patch_all()
import gevent
import getpass

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

consumer_key="HJC58RkbqZeHo0Z6sesPrKWRc"
consumer_secret="2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4"
access_token="1007063444-nU2zSoqqvoOrKtttK6RBL4YK7PQ0UvnZAVb0GFo"
access_token_secret="C7SYtnNCX5mAZLFvhP5QaYam5iTnvokOfKQ7LlDFEBEL4"

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
server = None
sent_dict = dict()

def broadcast_msg(ns_name, event, *args):
	global server
	pkt = dict(type="event",
			   name=event,
			   args=args,
			   endpoint=ns_name)

	for sessid, socket in server.sockets.iteritems():
		socket.send_packet(pkt)

class StdOutListener(StreamListener):
	""" A listener handles tweets are the received from the stream.
	This is a basic listener that just prints received tweets to stdout.

	"""
	def __init__(self):
		initialize()
	def on_data(self, data):
		#print data
		dic = json.loads(data)
		#print dic
		sent = calc_sentiment(dic['text'])
		print dic['text']
		broadcast_msg('/tweets', 'tweet', {'text': dic['text'], 'id': dic['id_str'], 'sent':sent})
		#socketio.emit('tweet', {'text': dic['text'], 'id': dic['id_str'], 'sent':sent}, namespace='/test')
		return True

	def on_error(self, status):
		print status

def initialize():
	global sent_dict
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

class Application(object):
	def __init__(self):
		self.buffer = []

	def __call__(self, environ, start_response):
		path = environ['PATH_INFO'].strip('/') or 'index.html'

		if path.startswith('static/') or path == 'index.html':
			try:
				data = open(path).read()
			except Exception:
				return not_found(start_response)

			if path.endswith(".js"):
				content_type = "text/javascript"
			elif path.endswith(".css"):
				content_type = "text/css"
			elif path.endswith(".swf"):
				content_type = "application/x-shockwave-flash"
			else:
				content_type = "text/html"

			start_response('200 OK', [('Content-Type', content_type)])
			return [data]

		if path.startswith("socket.io"):
			socketio_manage(environ, {'/tweet': BaseNamespace})
		else:
			return not_found(start_response)

def not_found(start_response):
    start_response('404 Not Found', [])
    return ['<h1>Not Found</h1>']

if __name__ == '__main__':
	Thread(target = listener).start()
	server = SocketIOServer(('0.0.0.0', 8080), Application(), resource="socket.io", policy_server=True, policy_listener=('0.0.0.0', 10843))
	
	server.serve_forever()
