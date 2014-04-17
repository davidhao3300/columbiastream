
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
    var color = "#000000";
    if (tweet.sent < 0)
    {
        if(tweet.set > -0.75) color = "#" + (-1*parseInt(tweet.sent*340)).toString(16) + "0000";
        else color = "#FF0000";
    }
    else if (tweet.sent > 0)
    {
        if (tweet.sent < 0.75)
        {
            color = "#00" + (parseInt(tweet.sent *340)).toString(16) +"00";
        }
        else color = "#00FF00";
    }
    /*
    if (tweet.sent >= 0.3)
    {
        color = "#00ff00";
    }
    else if (tweet.sent > -0.3)
    {
        var red = (127 - 425 * tweet.sent);
        var green = (127 + 425 * tweet.sent);
        var blue = (425 * tweet.sent);
        if (blue < 0) blue += 128;
        else blue = 128- blue;
        color = "#" + red.toString(16) + green.toString(16) + blue.toString(16);
    }*/
    $('#test').prepend("<span></span>").prepend("<p>Sentiment: "+tweet.sent+"</p>").prepend("<p>Time: "+tweet.time+"</p>").prepend("<p style=\"color:"+color+"\">Text: "+tweet['text']+"</p>");

}