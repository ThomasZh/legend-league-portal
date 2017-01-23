// description: 鏂板鑸�
// date: 2015-10-21
// header.v1.css
// update:3
$(function() {
	// 鎼滅储杈撳叆闅愯棌涓嬫媺鑿滃崟
	$(".search-val").keydown(function(){
		$('.search-select ul').hide();
	});
	//婊戣繃瀵艰埅鏄剧ず瀛愬鑸�
	$(".nav-hd li").hover( function () {
		$(this).addClass("open");
	    $(this).find(".subnav-hd").show();
	 },function () {
		$(this).removeClass("open");
	    $(this).find(".subnav-hd").hide();
	});

	$('#quickTab .tab-wrap').find('a').each(function(){
  		var tmpurl=$(this).attr('href') +'&random='+ Math.random();
  		$(this).attr('href',tmpurl);
	});
	//鐐瑰嚮鍘诲姩鎬佹秷鎭彁绀�;
	// $('#quickTab ul li').click(function(){

	// 	var weizhi = String($(this).index())+',';

	// 	var span = $(this).find('span');
	// 	var bellspan = $('.icon-bell').nextAll('span');
	// 	if(span.length==1){
	// 		var cat = $(this).attr('rel');
	// 		var bellnum = bellspan.text();
	// 			bellnum =parseInt(bellnum);
	// 		var yidu=0;
	// 		var data ={
	// 					uid:navuid,
	// 					cat:cat
	// 					};

	// 		var host = window.location.host;
	// 		if(host=='www.ui.cn'){
	// 			$.ajax({
 //                    type:'get',
 //                    dataType:'json',
 //                    url:'/delnotice',
 //                    data:data,
 //                    success:function(data){
 //                        if ( data.state == true ) {
 //                        	span.remove();
 //                        	yidu = data.yiread;
 //                        	bellnum = bellnum - yidu;
 //                        	if(bellnum>0){
 //                        		bellspan.text(bellnum);
 //                        	}else{
 //                        		bellspan.prevAll('.icon-bell').css('color','#CED7DE')
 //                        		bellspan.remove();
 //                        	}
 //                        	nav_loc = nav_loc.replace(weizhi,'');
 //                        }else{
 //                        }
 //                    },
 //                    error:function(){
 //                    }
	//                 });
	// 		}else if(host.indexOf('ui.cn')){
	// 			$.ajax({
 //                    type:'post',
 //                    dataType:'jsonp',
 //                    url:'http://www.ui.cn/delnotice',
 //                    data:data,
 //                    jsonpCallback:'DFEDFE',
 //                    success:function(data){
 //                        if ( data.state == true ) {
 //                        	span.remove();
 //                        	yidu = data.yiread;
 //                        	bellnum = bellnum - yidu;
 //                        	if(bellnum>0){
 //                        		bellspan.text(bellnum);
 //                        	}else{
 //                        		bellspan.prevAll('.icon-bell').css('color','#CED7DE')
 //                        		bellspan.remove();
 //                        	}
 //                        	nav_loc = nav_loc.replace(weizhi,'');
 //                        }else{
 //                        }
 //                    },
 //                    error:function(){
 //                    }
	//                 });
	// 		}

	// 	}

	// });
//鍏煎涓汉涓績,绔嬪嵆婵€娲荤殑鏍峰紡銆�
$(".jsemailverify").parent('div').parent('li').css("background","#fff7e7").find('a').addClass('f14').css('display','block');

$(".quick-item").hover( function () {
	$(this).addClass('on');
	$(this).find('.quick-menu').show();
},function () {
$(this).removeClass('on');
	$(this).find('.quick-menu').hide();
});


$(".quick-item").mouseenter(function(){
	if($(this).find('.quick-menu').attr('id')=='quickTab' && nav_loc.length>0){
		var navi = nav_loc.substr(0,1); // 鑾峰彇绗竴涓睍寮€S
		navi = parseInt(navi);
		tabNav.eq(navi).trigger('click');//榛樿鏈夊姩鎬� 灞曞紑椤�
	}
});




	// 娑堟伅閫夐」鍗�
	$(".quick-tab .tab-wrap .tab-cont").hide();
	$(".quick-tab .tab-wrap .tab-cont").eq(0).show();
	$(".quick-tab .tab-bar li").eq(0).addClass('on');

	var tabNav = $(".quick-tab .tab-bar li");
	tabNav.click(function(){
		var index = $(".quick-tab .tab-bar li").index(this);  //鑾峰彇褰撳墠鐐瑰嚮li鐨勭储寮曞€�

		tabNav.removeClass('on');
		tabNav.eq(index).addClass('on');
		$(".quick-tab .tab-wrap ul").hide();
		$(".quick-tab .tab-wrap ul").eq(index).show();
	});

	$(".search-hd-btn").click(function(ev){
      var ev = ev || event, // enent鍋氬吋瀹�
            isTrue = $(".search-hd").is(".on"); // 鍒ゆ柇.search-hd鏄惁鏄睍寮€鐘舵€�
      ev.stopPropagation(); // 闃绘鍐掓场
      if($(".search-hd").addClass('on').find('input').val() == ""){ // 鍦ㄨ緭鍏ユ娌℃湁鏂囧瓧鏃舵墽琛�
            if(isTrue){ // isTrue绛変簬 true 绉婚櫎on锛宖alse灏辨坊鍔爋n
            	$(".search-hd").removeClass('on').find('input').blur();
            	$('.search-select ul').hide();
            }else{
            	$(".search-hd").addClass('on').find('input').focus();
            }
      }else{ //鎻愪氦浜嬩欢search-hd
      	$(".search-hd").find('input').focus();
      	if(isTrue){
      		$("#searchForm").submit();
      	}else{

      	}
      }
	})
$(".search-filter").click(function(ev){
	 ev.stopPropagation();
})
$(document).click(function(){
	$(".search-hd").removeClass('on').find('input').blur();
});
	//鍥炶溅鎻愪氦
	$(document).on("keydown","#keywords",function(e){
		var keyVal = $(this).val();
		var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
		if(keyVal=='' && keyCode==13){
			e.preventDefault();
		}
	})

	// 鎼滅储鍒嗙被
	$(".search-filter").hover(function(){
		$(this).find('ul').show();
	},function(){
		$(this).find('ul').hide();
	})
	// selectBoxSer (".search-filter");
	$(".search-filter ul a").click(function(){
		var textVal = $(this).text();
		var tVal = $(this).attr("data-rel");
		$(".search-filter ul li").removeClass("on");
		$(this).parent().addClass("on");
		$("#sType").val(tVal);
		$(this).parents(".search-filter").find(".tit").text(textVal);
		$(this).parents(".search-filter").find(".options").hide();
		return false;
	});

	// 鎼滅储鎻愮ず
	selectBoxSer (".search-select");
	$(".search-select ul a").click(function(){
		var textVal = $(this).text();
		$(".search-val").val(textVal);
		$(this).parents(".search-select").find(".options").hide();
		// $(".search-hd").find('input').focus();鎼滅储涓嬫媺閫夋嫨鍚庤幏鍙栫劍鐐�
		return false;
	});

});
// 鎼滅储閫夐」涓嬫媺
selectBoxSer = function(box){
	$(box).click(function(){
		var $this = $(this);
		$this.blur();
		var options = $this.find('.options').css('display');

	if( options == 'none' && $(".search-val[type=text]").val()=="" ){	//
		$this.find(".options").show();

	} else {
		$this.find(".options").hide();
	}
	/*鐐瑰嚮浠讳綍鍦版柟鍏抽棴灞�*/
	$(document).click(function(event){
		var tar = $(event.target).attr("class");
		if( tar != $this ){
			$this.find(".options").hide();
		}
	});
	return false;

});
	$('.noti_img').parent().parent().addClass("nl");
	$('.noti_img').parent().find('br').remove();
	$('.tab-wrap ul li a').find('br').remove();
};
