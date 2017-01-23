$(function(){

	//寤惰繜鍔犺浇
	$('.imgloadinglater').lazyload({
		threshold : -100, //璺濈100鍍忕礌瑙﹀彂
		effect : "fadeIn" //鏄剧ず鐗规晥
	});


    //鑱屼綅鏂瑰悜閫夋嫨
    $(document).on('click','.job_type a',function(){
        var Iner = $(this).attr('rel');
        $(this).addClass('on').siblings().removeClass('on');
        $("input[name=jobtype]").val(Iner);
    })


	//鑷畾涔変笅鎷夋
	$(document).on("click",".ui_select .ui_select_val",function(event){
		var parent = $(this).parent(),
			parentLi = parent.find('dd').length,		//鑾峰彇li鐨勪釜鏁�
			parentHeihgt = parent.find(".ui_select_list dd").height();//鑾峰彇li鐨勯珮搴�

		//鐐瑰嚑涓嬩竴涓彍鍗曞厛璁╂墍鏈夌殑闅愯棌
		$(".ui_select").removeClass('open');
		parent.addClass('open');
		//澶т簬7涓坊鍔犳粴鍔ㄦ潯
		if(parentLi > 7){
			parent.find(".ui_select_list").css({
				height:7*parentHeihgt,
			})
		}
		//闃绘鍐掓场
		event.stopPropagation();
	});
	//閫夋嫨鍐呭
	$(document).on("click",".ui_select .ui_select_list dd a",function(){
		var oText = $(this).text(), //鑾峰彇褰撳墠鐨則ext
			oR    = $(this).attr('rel'), //鑾峰彇鐐瑰嚮鐨剅el
			parents = $(this).parents('.ui_select');
		//缁檚pan 浼犲€�
		parents.find("span").addClass('Selcolor').html(oText);
		//缁檌nput 浼犲€�
		parents.find("input").val(oR);
		$(this).parent().addClass('on').siblings().removeClass('on');
	});
	//document 鎿嶄綔
	$(document).click(function(){
		//鐐瑰嚮闅愯棌涓嬫媺妗�
		$(".ui_select").removeClass('open');
	})
	//鑷畾涔変笅鎷夋 end

	//妯℃€佹
	$(document).on('click','[data-click]',function(){
		var $This = $(this),
			$dataCk = $This.attr('data-click');
			//杩欎釜鐜板疄瀵瑰簲data-click鐨勫睘鎬�
			modalShow();

		$(document).on('click','.modal-close',function(){
			modalHide();
		})

		/*$(document).on('click','.modal',function(){
			modalHide();
		})*/

		$(document).on('click','.modal_content',function(e){
			var e = e || event;
			e.stopPropagation();
			//鍘婚櫎妯℃€佹select 涓嬫媺
			$(".ui_select").removeClass('open');
		})
		//鏄剧ず
		function modalShow(){
			$($dataCk).addClass('in').show();
			$(".modal-backdrop").addClass('in');
			$("body").addClass('modal-open');
		}
		//闅愯棌
		function modalHide(){
			$($dataCk).hide().removeClass('in');
			$(".modal-backdrop").removeClass('in');
			$("body").removeClass('modal-open');
		}

	})

	//妯℃€佹 end
	var EmailReg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;

	$(document).on("click",".edit_email",function(){
		$("input[name=jobemail]").attr('disabled',false).focus();
	})

	//鎰忚鍙嶉 show
	$("#Fan_kui").click(function(e){
		$(".qa_content").toggleClass('open');
		e.stopPropagation();
	})


	//鎰忚鍙嶉 sub
	$("#job_qa").click(function(){
		var Textqa = $(".job_textqa"),
			emailqa = $(".job_qaemali");
		if(!Textqa.val()){
			globalTip({"msg":"鎮ㄧ殑鍙嶉闂涓嶈兘涓虹┖","setTime":3});
			return false;
		}
		if(!emailqa.val()){
			globalTip({"msg":"鎮ㄧ殑閭涓嶈兘涓虹┖","setTime":3});
			return false;
		}
		if(!EmailReg.test(emailqa.val())){
			globalTip({"msg":"璇峰～鍐欐纭偖绠�","setTime":3});
			return false;
		}

		$.ajax({
			url:"/temail",
			type:"post",
			data:{econt:Textqa.val(),ehremail:emailqa.val()},
			dataType:'json',
			success: function(msg){
				if(msg.stats=='ok'){
					globalTip(msg.msg);
					//鎴愬姛闅愯棌鍙嶉妗�
					 $(".qa_content").removeClass('open');
				}else{
					globalTip(msg.msg);
				}
			}
		})

	})
	$(document).on('click',function(){
		$(".qa_content").removeClass('open');
	})
	$(document).on('click','.qa_content',function(e){
		e.stopPropagation();
	});



/* end */
});
