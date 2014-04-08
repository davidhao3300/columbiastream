#!/usr/bin/python
# -*- coding: latin-1 -*-

from flask import redirect, session, url_for, request
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, lm
from flask.ext.tweepy import Tweepy

@app.route('/', methods = ['GET'])
def index():
	app.config.setdefault('TWEEPY_CONSUMER_KEY', 'HJC58RkbqZeHo0Z6sesPrKWRc')
	app.config.setdefault('TWEEPY_CONSUMER_SECRET', '2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4')
	app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', '1007063444-nU2zSoqqvoOrKtttK6RBL4YK7PQ0UvnZAVb0GFo')
	app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', 'C7SYtnNCX5mAZLFvhP5QaYam5iTnvokOfKQ7LlDFEBEL4')

	tweepy = Tweepy(app)
	return "Hi!"