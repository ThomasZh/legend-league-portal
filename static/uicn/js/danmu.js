(function() {
        var jsfiles = new Array("jquery.cookie.js","_init.js");
        var agent = navigator.userAgent;
        var docWrite = (agent.match("MSIE") || agent.match("Safari"));
        if(docWrite) {
            var allScriptTags = new Array(jsfiles.length);
        }
        var host = new Array("http://s1.ui.cn/js/","http://danmu.ui.cn/");    //鏂囦欢鐨勬墍鍦ㄧ洰褰�
        for (var i=0, len=jsfiles.length; i<len; i++) {
            if (docWrite) {
                    allScriptTags[i] = "<script src='" + host[i] + jsfiles[i] + "'></script>";
                } else {
                    var s = document.createElement("script");
                    s.src = host[i] + jsfiles[i];
                    var h = document.getElementsByTagName("head").length ? document.getElementsByTagName("head")[0] : document.body;                h.appendChild(s);
                }
            }
            if (docWrite) {
                document.write(allScriptTags.join(""));
            }
})();


$(function() {

    $('body').append('<link rel="stylesheet" href="http://danmu.ui.cn/res/danmu.css">');
    ob = $("<div class='barrage'></div>").appendTo('body');

    ob_d = $("<div class='barrage_box cl'></div>").appendTo(ob);

    $(".barrage_box").append("<a class='portrait z' href='javascript:;'></a>");
    $(".barrage_box").append(" <div class='z p'></div>");
    $(".barrage_box").append(" <div class='close z'></div>");

    img = $(" <img src='' alt=''>").appendTo(".barrage_box .portrait");

    content = $("<a title='' href='' target='_blank'></a>").appendTo(".barrage_box .p");

    $(".barrage_box .close").append("<a title='' href='javascript:;'></a>")
    $(".barrage_box .close a").append("<i class='icon-close'></i>")

    // $(".barrage_box").mouseover(function(){
    //     $(this).find('.close').show();
    // })

    // $(".barrage_box").mouseout(function(){
    //     $(this).find('.close').hide();
    // })

    content.click(function(){
        $.get("http://danmu.ui.cn/click?id="+$(this).attr('id'))
        window.open($(this).attr('href'),'_blank');
        return false;
    });

function run(){

    $.ajaxSettings.async = false;
    $.getJSON('http://danmu.ui.cn/?callback=?',function(data){
        info = data;

        var speed=info.set.speed;
        var looptime = info.set.looptime;

        var is_loop = false;
        var pixel = parseInt(info.set.pixel);
        var i=0;
        var invalid = info.set.invalid;
        var MyMar;
        var is_loop_run = false;

        var window_width=$(window).width() + 500;
        var index_id;
        index=0;


        if(info.set.state){
            total = info.data.length;
            img.attr('src',info['data'][index]['download'] + '/' + info['data'][index]['image']);
            content.attr({'href':info['data'][index]['url'],'id':info['data'][index]['id']}).empty().append(info['data'][index]['content']);
            index_id = info['data'][index]['id'];
            MyMar=setInterval(Marquee,1);
            is_loop = true

        }

        function Marquee(){

            if(is_loop){
                clearInterval(MyMar);
                MyMar=setInterval(Marquee,speed);
                is_loop = false;
            }


            ob.css('margin-right',i);

            if(i > window_width ){
                i = 0;

                ob.css('margin-right',i);

                index += 1;
                if(index + 1> total){
                    if(parseInt(info.set.isloop) == 0){
                        clearInterval(MyMar);
                        return false;
                    }else{
                        index = 0;
                        img.attr('src',info['data'][index]['download'] + '/' + info['data'][index]['image']);
                        content.attr({'href':info['data'][index]['url'],'id':info['data'][index]['id']}).empty().append(info['data'][index]['content']);
                    }
                }else{
                    img.attr('src',info['data'][index]['download'] + '/' +info['data'][index]['image']);
                    content.attr({'href':info['data'][index]['url'],'id':info['data'][index]['id']}).empty().append(info['data'][index]['content']);
                }
                index_id = info['data'][index]['id'];
                clearInterval(MyMar);
                MyMar=setInterval(Marquee,looptime);
                is_loop = true
            }

            i += pixel;
        }

        ob_d.mouseover(function(){
            clearInterval(MyMar);
        });

        ob_d.mouseout(function(){
            MyMar=setInterval(Marquee,speed);
        });

        $('.barrage .barrage_box .close').click(function(){
            clearInterval(MyMar);
            ob_d.unbind();
            $(this).parents('.barrage').hide();
            $.cookie('barrage','hide',{expires:parseInt(invalid),domain:'.ui.cn'});
            $.get("http://danmu.ui.cn/close?id="+index_id);
        })

    });
};

function do_run(){
    clearTimeout(do_time);
    run();
}

if($.cookie('barrage') != 'hide'){
   do_time = setTimeout(do_run,starttime);
}


});
