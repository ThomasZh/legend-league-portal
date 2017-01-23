

$(function(){
	//棣栧厛灏�#scrollUpf闅愯棌
    $("#scrollUp").hide();
    //褰撴粴鍔ㄦ潯鐨勪綅缃浜庤窛椤堕儴100鍍忕礌浠ヤ笅鏃讹紝璺宠浆閾炬帴鍑虹幇锛屽惁鍒欐秷澶�
    $(function() {
        $(window).scroll(function() {
            if ($(window).scrollTop() > 100) {
                $("#scrollUp").fadeIn();
            } else {
                $("#scrollUp").fadeOut();
            }
        });
        //褰撶偣鍑昏烦杞摼鎺ュ悗锛屽洖鍒伴〉闈㈤《閮ㄤ綅缃�
        $("#scrollUp .arrows").click(function() {
            $('body,html').animate({
                scrollTop: 0
            },
            500);
            return false;
        });
    });

    // 杩斿洖椤堕儴鍔燪Q瀹㈡湇
    $("#scrollUp .arrows").after('<a class="service" title="QQ" target="_blank" href="http://wpa.qq.com/msgrd?v=3&uin=1369535553&site=qq&menu=yes"><i class="icon-qq"></i></a>');
});
