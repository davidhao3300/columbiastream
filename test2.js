$(document).ready(function()
{
    var time = 0;
    var open = new Array();
    var todelete = new Array();
    for (var x = 0; x < 11; x++)
    {
        open[x] = 0;
    }
    var width = $(document).width();
    setInterval(function()
    {
        time++;
        while(todelete.length > 0 && todelete[0][0] < time)
        {
            console.log("Removing "+todelete[0][1]);
            $('#'+todelete[0][1]).remove();
            todelete.splice(0,1);
        }
        console.log(time);
    }, 1000);
    var INT = 10;
    setInterval(function()
    {
        var i = 5;
        var done = false;
        for (var diff = 0; diff <= 5; diff++)
        {
            var index = i-diff;
            if (open[index] < time)
            {
                open[index] = time + MULT*INT;
                $('body').append("<div class=\"tweetbox\" id=\""+time+"\" style=\"top:"+(25*index)+"px\">This is tweet #"+time+".................................................................................................................................................");
                todelete.push([time+15, time]);
                $('#'+time).animate({right:"+="+(2*width)+"px"}, 15000, "linear");
                break;
            }
            index = i+diff;
            if (open[index] < time)
            {
                open[index] = time + MULT*INT;
                $('body').append("<div class=\"tweetbox\" id=\""+time+"\"style=\"top:"+(25*index)+"px\">This is tweet #"+time+".................................................................................................................................................");
                todelete.push([time+15, time]);
                $('#'+time).animate({right:"+="+(2*width)+"px"}, 15000, "linear");
                break;
            }
            }
    }, 1000);
});