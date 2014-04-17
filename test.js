    (function($) {
        $.fn.textWidth = function(){
             var calc = '<span style="display:none">' + $(this).text() + '</span>';
             $('body').append(calc);
             var width = $('body').find('span:last').width();
             $('body').find('span:last').remove();
            return width;
        };
        
        $.fn.marquee = function(args) {
            var that = $(this);
            var textWidth = that.textWidth(),
                offset = that.width(),
                width = offset,
                css = {
                    'text-indent' : that.css('text-indent'),
                    'overflow' : that.css('overflow'),
                    'white-space' : that.css('white-space')
                },
                marqueeCss = {
                    'text-indent' : width,
                    'overflow' : 'hidden',
                    'white-space' : 'nowrap'
                },
                args = $.extend(true, { count: -1, speed: 1e1, leftToRight: false }, args),
                i = 0,
                stop = textWidth*-1,
                dfd = $.Deferred();
            
            function go() {
                if(!that.length) return dfd.reject();
                if(width == stop) {
                    i++;
                    if(i == args.count) {
                        that.css(css);
                        return dfd.resolve();
                    }
                    if(args.leftToRight) {
                        width = textWidth*-1;
                    } else {
                        width = offset;
                    }
                }
                that.css('text-indent', width + 'px');
                if(args.leftToRight) {
                    width++;
                } else {
                    width--;
                }
                setTimeout(go, args.speed);
            };
            if(args.leftToRight) {
                width = textWidth*-1;
                width++;
                stop = offset;
            } else {
                width--;            
            }
            that.css(marqueeCss);
            go();
            return dfd.promise();
        };
    })(jQuery);

$(document).ready(function()
{
$('h1').marquee();
$('h2').marquee({ count: 2 });
$('h3').marquee({ speed: 5 });
$('h4').marquee({ leftToRight: true });
$('h5').marquee({ count: 1, speed: 2 }).done(function() { $('h5').css('color', '#f00'); });
});
/*
$(document).ready(function()
  {
      for (var i = 0; i < 11; i++)
      {
          $('body').append("<p style=\"top:"+i*25+"px; width:1000px; white-space:nowrap; overflow:hidden;right:-1000px;position:absolute\">Test</p>");
      }
  }
  );

var time = 0;
var list = new Array();
for (var x = 0; x < 11; x++)
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
                var i = 5;
                var index=-1;
                for (var diff = 0; diff <= 5; diff++)
                {
                    
                    if (list[i-diff] < time)
                    {
                      index = i-diff;
                        list[index] = time+10;
                        $('p:nth-child('+(index+1)+')').css('right', '-1000px').text("This is tweet #"+time+".................................................................................................................................................");
                        break;
                    }
                    else if(list[i+diff] < time)
                    {
                      index = i+diff;
                      list[index] = time+10;
                        $('p:nth-child('+(index+1)+')').css('right', '-1000px').text("This is tweet #" + time+".................................................................................................................................................");
                        break;
                    }
                }
                
                if(index!=-1)test(index);},1000);
function test(i) {
                    $('p:nth-child('+(i+1)+')').animate({right:"+="+($(document).width())},10000, "linear", function(){});
                }*/