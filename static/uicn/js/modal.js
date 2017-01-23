/*!
 * description: 寮规
 * require: jquery-1.10.2.js
 * relevancy: modal.css
 *
 * date: 2015-08-27
 * update: (2015-XX-XX XX:XX)
 */
var comid;
$(document).on('click','[data-target]',function(){
	comid = $(this).attr('rel');
	// 鑾峰彇寮规id
	var modalBox = $(this).attr('data-target');
	var modalBoxPos = $(modalBox).find(".modal-effect");

	// 鏄剧ず寮规
	modal(modalBox,modalBoxPos);


});

modalPostion = function(pos) {
	//鑾峰彇鏀瑰彉涔嬪悗鐨勫搴�
	var changeWidth=$(window).width();
	var changeHeight=$(window).height();
	// 鑾峰彇DIV瀹藉害
	var smallW = $(pos).width();
	var smallH = $(pos).height();
	//璁＄畻瀹藉害淇敼姣斾緥
	var divChangeWidth	=	(changeWidth - smallW) / 2;
	var divChangeHeight	=	(changeHeight - smallH) / 2;
	// 瓒呰繃涓€灞忓箷鐨勪笂涓嬩笉灞呬腑缁檓argin鍊�
	if( divChangeHeight > 0 ) {
		$(pos).css('top', divChangeHeight);
		$(pos).css('left', divChangeWidth);
	} else {
		$(pos).css('left', divChangeWidth);
		$(pos).css('margin', "30px 0");
	}
};

modal = function(box,pos) {
	// 娴姩绐楀彛瀹氫綅
	modalPostion(pos);

	// 鏄剧ず
	$('body').addClass('modal-open').append('<div class="modal-backdrop"></div>');
	$('body').css('padding-right','15px');
	$(box).addClass("in");

	$(window).resize(function(){
		// 娴姩绐楀彛瀹氫綅
		modalPostion(pos);
	});

	// 鐐瑰嚮鍏抽棴鎸夐挳浠ュ強閬僵灞傛椂鍏抽棴娴姩灞�
	$('.icon-close, .close-btn, .modal-backdrop').bind('click', function(){
		$(box).removeClass("in");
		$('.modal-backdrop').remove();
		$('body').removeClass("modal-open");
		$('body').css('padding-right','0');
	});
};
