$(function(){
	// 寰俊浜岀淮鐮佸垎浜
	$(".icon-weixin1").click(function(event){

		$(this).parent().addClass("on");
		$(".weixin-box").show();

		$(".weixin-box").click(function(event){
			event.stopPropagation();
		})
		$(".icon-close").click(function(){
			infowx();
		});
		$(document).click(function(){
			infowx();
		});
		event.stopPropagation();

		function infowx(){
			$(".weixin-box").hide();
			$(".icon-weixin1").parent().removeClass("on");
		}
	});

	//璇︽儏椤靛洖澶嶈瘎璁烘鏄剧ず闅愯棌
	$(".comment-toggle").on("click",function(){
		$(this).parents(".comment-cont").find(".comment-form-inner").slideDown();
		$(".comment-form-inner .btn-nature").on("click",function(){
			$(this).parents(".comment-form-inner").slideUp();
		});
	});

	//渚ц竟鏍忔樉绀哄揩閫熻瘎璁�
	var QCommentBtn = $(".works-oper-aside a").last();
	QCommentBtn.click(function(){
		if( $(".comment-quick").hasClass("open")){
			$(".comment-quick").removeClass("open");
			$(".comment-quick").slideUp();
		} else {
			$(".comment-quick").addClass("open");
			$(".comment-quick").slideDown();
		}

	});


});
