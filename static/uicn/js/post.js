/*!
 * description: 棣栭〉鍒楄〃灞曠ず鏁堟灉
 * require: jquery-1.10.2.js
 * relevancy: post.css
 *
 * date: 2015-07-10
 * update:
 */

$(function(){
	// 婊戣繃鏄剧ず闃村奖妗�
	$(document).on('mouseenter', '.post li', function(){
	    $(this).find('.user').addClass('on'); //鐢ㄦ埛鍚嶅彉棰滆壊
	    $(this).find('.shade')
	        .stop()
	        .animate({ opacity : '1'}, 300)
	});
	$(document).on('mouseleave', '.post li', function(){
	    $(this).find('.user').removeClass('on');
	    $(this).find('.shade')
	        .stop()
	        .animate({ opacity : '0'}, 300)
	});

});
