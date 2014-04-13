$(document).ready(function()
  {
      for (var i = 0; i < 10; i++)
      {
          $('body').append("<p style=\"top:"+i*12+"px; color:red;right:-100px;position:absolute\">Test</p>");
      }
  }
  );

var time = 0;
var list = new Array();
for (var x = 0; x < 10; x++)
{
    list[x] = 0;
}

setInterval(function()
            {
                time++;
        
            }, 1000
            );
setInterval(function()
            {
                var i = 0;
                for (; i < 10; i++)
                {
                    if (list[i] < time)
                    {
                        console.log(list[i]+" "+time);
                        list[i] = time+7;
                        console.log(list[i]+" "+time);
                        $('p:nth-child('+(i+1)+')').css('right', '0px');
                        break;
                    }
                }
                
                test(i);},1000);
function test(i) {
                    $('p:nth-child('+(i+1)+')').animate({right:"+="+($(document).width())},7000, "linear", function(){});
                }