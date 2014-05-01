import json
from datetime import datetime

test = open("tweets.txt");
data = json.loads(test.read());
test.close()
i = 0
for tweet in data:
	print datetime.fromtimestamp(tweet['time'])
test = open("tweets.txt",'w')
test.write(json.dumps(data));
test.close();