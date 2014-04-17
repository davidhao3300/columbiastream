import json;
from datetime import datetime
from tweepy import OAuthHandler
from tweepy import Stream, Status
consumer_key="HJC58RkbqZeHo0Z6sesPrKWRc"
consumer_secret="2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4"
access_token="1007063444-nU2zSoqqvoOrKtttK6RBL4YK7PQ0UvnZAVb0GFo"
access_token_secret="C7SYtnNCX5mAZLFvhP5QaYam5iTnvokOfKQ7LlDFEBEL4"

test = open("tweets.txt");
data = json.loads(test.read());
for i in range(1, len(data)):
	if data[i]['time'] < data[i-1]['time']:
		print data[i]['time']
	print datetime.fromtimestamp(data[i]['time'])