$(function(){
	$('.in_two_hot_left_bot a:nth-child(2n)').css({'float':'right'});
	$('.in_two_tj_left_bot a:nth-child(2n)').css({'float':'right'});
	$('.in_ts_hot_left_bot a:nth-child(2n)').css({'float':'right'});


	// 热门景区和精彩推荐tab切换
	$('.in_two_title ul li').eq(0).addClass('in_two_title_hover');
	$('.in_two_mian > div').eq(0).show();
	$('.in_two_title ul li').each(function(){
		var Index=$(this).index();
		$(this).click(function(){
			$(this).addClass('in_two_title_hover').siblings().removeClass('in_two_title_hover');
			$('.in_two_mian > div').eq(Index).show().siblings().hide();
		});
	});
	



	// 选择目的地
	$('.in_left_one span').click(function(){
		$('.in_mdd').toggle();		
	});

	$('#mdd_min > div').each(function(){
		var Mindex=$(this).index();
		$(this).find('.mdd_min_title a').click(function(){
			var Tindex=$(this).index();
			$(this).parent().parent().addClass('add').siblings().removeClass('add');			
			$(this).addClass('mdd_min_title_hover').siblings().removeClass('mdd_min_title_hover');
			$(this).parent().parent().find('li').eq(Tindex).show().siblings().hide();
			$(this).parent().parent().find('ul').show().parent().siblings().find('ul').hide(); 

		});

	});
	$('.mdd_none').click(function(){
		$('.in_mdd').hide();
	});
	

	// 点击空白位置关闭目的地
	$(document).bind('click',function(e){ 
	var e = e || window.event; //浏览器兼容性 
	var elem = e.target || e.srcElement; 
	while (elem) { //循环判断至跟节点，防止点击的是div子元素 
	if (elem.id && elem.id=='choose' || elem.id && elem.id=='dw') { 
	return; 
	} 
	elem = elem.parentNode; 
	} 

	$('#in_mdd').css('display','none'); //点击的不是div或其子元素 
	}); 


	// 手机版导航点击效果
	$('.ph_nav h1').click(function() {
		$(this).hide();
		$(this).parent().find('h2').show();
		$(this).parent().find('ul').show();
	});
	$('.ph_nav h2').click(function() {
		$(this).hide();
		$(this).parent().find('h1').show();
		$(this).parent().find('ul').hide();
	});


	// 手机版切换城市
	$('#dw').click(function(){
		$('.in_mdd').show();
		$('body').css({'overflow':'hidden'});

	});
	$('.mdd_min ul li p a').click(function(){
		$('.in_mdd').hide();
		$('body').css({'overflow':'auto'});
	});







});