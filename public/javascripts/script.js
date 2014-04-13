$(function() {
    var socket = io.connect(window.location.hostname);
    socket.on('data', function(data)
    {
        for (var i = 0; i < data.length; i++)
        {
            prepend(data[i]);
        }
    });
    socket.on('new_tweet', function(data) {
        
        $('#last-update').text(new Date().toTimeString());
        prepend(data);
    });
})

function prepend(tweet)
{
    $('#test').prepend("<span></span>").prepend("<p>Sentiment: "+tweet.sent+"</p>").prepend("<p>Time: "+tweet.time+"</p>").prepend("<p>Text: "+tweet['text']+"</p>");
}