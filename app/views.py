#!/usr/bin/python
# -*- coding: latin-1 -*-

from flask import redirect, session, url_for, request
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, lm
import tweepy

@app.route('/', methods = ['GET'])
def index():
    if 'oauth_token' in request.form:
        print request.form['oauth_token']
    auth = tweepy.OAuthHandler("HJC58RkbqZeHo0Z6sesPrKWRc", "2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4")
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
    session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    return redirect(redirect_url)