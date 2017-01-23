/*!
 * description: 鍩硅椤甸潰
 * relevancy: edu.css
 * date: 2015-08-27
 */

$(function(){

	// 灞曞紑绛涢€�
	// $(".edu-screen-show").hide();
	$(".edu-drop").click(function(){
		if( $(this).hasClass("open") ){
			$(this).removeClass("open");
			$(".edu-screen-show").slideUp("slow");
		} else{
			$(this).addClass("open");
			$(".edu-screen-show").slideDown("slow");
		}
	});
	//灞曞紑鍩庡競


	// 鏀粯鏂瑰紡
	$(".pay-label").click(function(){
		$(".pay-label").find("input").removeAttr("checked");
		$(".pay-label").removeClass("on");
		$(this).find("input").attr("checked",true);
		$(this).addClass("on");
	});
	// 閫夋嫨閾惰
	$(".yinhang-box a").click(function(){
		$(".yinhang-box a").removeClass('on');
		$(this).addClass("on");
	})

});
