
$(document).ready(function() {
    var socket = io.connect(window.location.hostname);
    var tweets = new Array();
    var index = 0;
    var done = false;
    socket.on('data', function(data)
    {
        if(done) return;
        done = true;
        var ROWS = 11;
        var MULT = 300;
        tweets = data;
        var time = new Date(tweets[tweets.length-1].time*1000);
        console.log(parseInt(time.getTime()/1000));

        var num = tweets.length-1;
        console.log(tweets[num].time);
        var width = $(document).width();

        var INT = 7;
        var open = new Array();
        var todelete = new Array();

        for (var x = 0; x < ROWS; x++)
        {
            open[x] = parseInt(time.getTime()/1000);
        }

        setInterval(function()
        {
            time.setTime(time.getTime()-1000*MULT/2);
            v//ar actualtime = new Date(time.getTime()-4*60*60*1000);
            $("#current-time").text(time.toLocaleString());
            var curr = parseInt(time.getTime()/1000);
            console.log(curr+" "+parseInt(tweets[num].time));
            while(todelete.length > 0 && todelete[0][0] > curr)
            {
                $('#'+todelete[0][1]).remove();
                todelete.splice(0,1);
            }
            if(todelete.length == 0 && curr - tweets[num].time > 2 * MULT)
            {
                time.setTime(time.getTime()-(curr-tweets[num].time)*1000 + 1000);
            }
        }, 500);

        setInterval(function()
        {
            
            var curr = parseInt(time.getTime()/1000);
            while (num >= 0 && tweets[num].time > curr)
            {
                console.log("Checking: " + curr+" "+tweets[num].time);
                var i = 5;
                var index = -1;
                var full = true;
                
                for (var diff = 0; diff <= ROWS/2; diff++)
                {
                    index = i-diff;
                    if (open[index] > curr)
                    {
                        open[index] = curr - MULT*INT;
                        $('.tweets').append("<div class=\"tweetbox\" id=\""+num+"\" style=\"top:"+(25*index+150)+"px; color:"+color(tweets[num])+"\">"+tweets[num].text+"</div>");
                        todelete.push([curr-MULT*15, num]);
                        $('#'+num).animate({right:"+="+(2*width)+"px"}, 15000, "linear");
                        num--;
                        full = false;
                        break;
                    }

                    index = i+diff;
                    if (open[index] > curr)
                    {
                        open[index] = curr - MULT*INT;
                        $('.tweets').append("<div class=\"tweetbox\" id=\""+num+"\" style=\"top:"+(25*index+150)+"px; color:"+color(tweets[num])+"\">"+tweets[num].text+"</div>");
                        todelete.push([curr-MULT*15, num]);
                        $('#'+num).animate({right:"+="+(2*width)+"px"}, 15000, "linear");
                        num--;
                        full = false;
                        break;
                    }
                }
                if(full) break;
            }
        }, 500);
    });
    socket.on('new_tweet', function(data) {
        
        $('#last-update').text(new Date().toTimeString());
        $('.new-tweet').text(data.text);
    });
    
})
function color(tweet)
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
    return color;
}
function prepend(tweet)
{
    $('#test').prepend("<span></span>").prepend("<p style=\"color:"+color(tweet)+"\">Text: "+tweet['text']+"</p>");
}