/**
 * Module dependencies.
 */
var express = require('express')
  , io = require('socket.io')
  , http = require('http')
  , twitter = require('ntwitter')
  , _ = require('underscore')
  , path = require('path')
  , fs = require('fs');

//Create an express app
var app = express();

//Create the HTTP server with the express app as an argument
var server = http.createServer(app);

// IMPORTANT!!
//You will need to get your own key. Don't worry, it's free. But I cannot provide you one
//since it will instantiate a connection on my behalf and will drop all other streaming connections.
//Check out: https://dev.twitter.com/ You should be able to create an application and grab the following
//crednetials from the API Keys section of that application.
/*var api_key = 'HJC58RkbqZeHo0Z6sesPrKWRc';               // <---- Fill me in
var api_secret = '2pDKqITFdoqRZlVFJvQ1iDfE6kyMqlDxcDlOpC6NuV6nAn5Jl4';            // <---- Fill me in
var access_token = '1007063444-nU2zSoqqvoOrKtttK6RBL4YK7PQ0UvnZAVb0GFo';          // <---- Fill me in
var access_token_secret = 'C7SYtnNCX5mAZLFvhP5QaYam5iTnvokOfKQ7LlDFEBEL4';   // <---- Fill me in
*/

var api_key = 'pue278QEfBJtbyWBXfnbBA';               // <---- Fill me in
var api_secret = 'WtYadmJb3atkSW6VKFS52WqHWNtnsfxyGmk9oiuTw4';            // <---- Fill me in
var access_token = '2436381469-k5jBECUwClQEVU1P8IuxM2ysP67yOVmBk9kpxN0';          // <---- Fill me in
var access_token_secret = '0AXmv8ekjvVmXYoAZKc3O7EJQotA9mhwPub1gA32Ulh18';   // <---- Fill me in

// Twitter symbols array.
var watchSymbols = ['@Columbia', 'columbia university', '#ColumbiaUniversity', '#Barnard', '#BarnardCollege', '@BarnardCollege'];
var tweets = [];
var sents = {};
initialize();

//Generic Express setup
app.set('port', process.env.PORT || 3000);
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(require('stylus').middleware(__dirname + '/public'));
app.use(express.static(path.join(__dirname, 'public')));

//We're using bower components so add it to the path to make things easier
app.use('/components', express.static(path.join(__dirname, 'components')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

//Our only route! Render it with the current watchList
app.get('/', function(req, res) {
	res.json({'data':tweets});
});

//Start a Socket.IO listen
var sockets = io.listen(server);

//Set the sockets.io configuration.
//THIS IS NECESSARY ONLY FOR HEROKU!
sockets.configure(function() {
  sockets.set('transports', ['xhr-polling']);
  sockets.set('polling duration', 10);
});

//If the client just connected, give them fresh data!
sockets.sockets.on('connection', function(socket) { 
    //socket.emit('data', watchList);
});

// Instantiate the twitter connection
var t = new twitter({
    consumer_key: api_key,
    consumer_secret: api_secret,
    access_token_key: access_token,
    access_token_secret: access_token_secret
});

t.stream('statuses/filter', { track: watchSymbols }, function(stream) {

  //We have a connection. Now watch the 'data' event for incomming tweets.
  stream.on('data', function(tweet) {
      console.log(tweet.text);
      tweets.push({"time" : Date.parse(tweet.created_at)/1000, "text" : tweet.text, "sent":calc_sentiment(tweet.text)});
      fs.writeFileSync('./tweets.txt', JSON.stringify(tweets));
  });
});

//Create the server
server.listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});


function initialize()
{
    var lines = fs.readFileSync('./tweets.txt', 'utf8').split("\n");
    
    for (var i = 0; i < lines.length-1; i++)
    {
      var data = lines[i].split("\t");
      var time = parseInt(data[0]);
      var sent = parseFloat(data[1]);
      var text = data[2];
      var dict = {"time": time, "text" : text, "sent" : sent};
      tweets.push(dict);
    }

    lines = fs.readFileSync('./sent.txt', 'utf8');
    sents = JSON.parse(lines);
}

function calc_sentiment(tweet)
{
  var value = 0.0;
  var words = tweet_words(tweet);
  var edited = false;
  for (var i = 0; i < words.length; i++)
  {
    if (sents[words[i]] != null)
    {
      value += sents[words[i]];
      edited = true;
    }
  }
  if (!edited) return 0
  return value
}

function tweet_words(tweet)
{
  
  var tweet_string = removePunc(tweet);
  tweet_string = strip(tweet_string);
  var result = tweet_string.split(" ");
  for (var i = 0; i < result.length; i++)
  {
    result[i]=result[i].toLowerCase();
  }
  return result;
}
function removePunc(tweet)
{
  var tweet_string = "";
  var punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";
  for (var i = 0; i < punctuation.length; i++)
  {
    var p = punctuation.charAt(i);
    tweet_string = "";
    for (var j = 0; j < tweet.length; j++)
    {

      var c = tweet.charAt(j);
      //console.log(p+" "+c);
      if(p==c)
      {
        tweet_string += " ";
      }
      else
      {
        tweet_string += c;
      }
    }
    tweet = tweet_string;
  }
  return tweet_string;
}
function strip(text)
{
  var a = "";
  for (var i = 0; i < text.length; i++)
  {
    var c = text.charAt(i);
    if (text.charCodeAt(i) >= 128 || c=='\n' || c=='\t')
      a += ' ';
    else
      a += c;
  }
    
  return a;
}


