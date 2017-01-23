
$(function(){
//琛ㄥ崟鐐瑰嚮鍏虫敞
	var followBtn = $(".h-follow-check .check");
		// followBtn.find("em").hide();

	followBtn.click(function(){
		if($(this).siblings("input[type='checkbox']").attr("checked")==undefined){
		    $(this).find("em").show();
		    $(this).siblings("input[type='checkbox']").attr("checked",true)
		}else{
		    $(this).find("em").hide();
		    $(this).siblings("input[type='checkbox']").attr("checked",false)
		}
	});

// 楦℃堡
	$(".h-soup li i").click(function(){
		var soupBtn = $(this).parent();
		$(".h-soup li").removeClass("open");
		soupBtn.addClass("open");
	});

//鏂囩珷銆佽璁″笀閫夐」鍗�

	// tabSwitch('.h-article-btn a','.h-article-box ul');
	tabSwitch('.h-member-btn a','.h-member-box ul');

// 鎻愮ず璇偣鍑讳竴娆″悗娑堝け
	$('.switch-tip').click(function(){
		$(this).siblings('.tips').remove();
	});



});

// 閫夐」鍗″垏鎹�
tabSwitch = function(btn,item) {
	$(item).hide();
	$(item).eq(0).show();
	$(btn).click(function(){
		var index = $(this).index();
		$(btn).removeClass('on');
		$(btn).eq(index).addClass('on');
		$(item).hide();
		$(item).eq(index).show();
	});
};
