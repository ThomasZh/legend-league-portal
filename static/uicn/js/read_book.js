
	// 绂佺敤a鏍囩锛屼笉鍙偣鍑�
	$('.disable').removeAttr('href');
	$('.disable').removeAttr('onclick');
	// 婊戣繃寰蒋鍥炬爣鏄剧ず涓嬭浇
	$("a.allow .icon-microsoft").hover(
	  function () {
	  	$(this).removeClass("icon-microsoft");
	    $(this).addClass("icon-download2");
	  },
	  function () {
	    $(this).removeClass("icon-download2");
	    $(this).addClass("icon-microsoft");
	  }
	);
	// 婊戣繃鑻规灉鍥炬爣鏄剧ず涓嬭浇
	$("a.allow .icon-mac").hover(
	  function () {
	  	$(this).removeClass("icon-mac");
	    $(this).addClass("icon-download2");
	  },
	  function () {
	    $(this).removeClass("icon-download2");
	    $(this).addClass("icon-mac");
	  }
	);

	// 鏉傚織榧犳爣绉诲叆鏄剧ず閬僵灞�
	$(".mag-img").mouseover(function(){

		$(this).find('.mag-shade *').stop();
		$(this).find(".mag-shade")
		.stop()
		.show()
		.animate({
			opacity: '1',
		}, "slow");

		$(this).find(".mag-shade h1").animate({
			bottom: '253px',
			opacity: '1',
		}, "slow");

		$(this).find(".mag-shade p").animate({
			bottom: '35px',
			opacity: '1',
		}, "slow");

	});

	// 鏉傚織榧犳爣绉诲嚭闅愯棌閬僵灞�
	$(".mag-img").mouseleave(function(){

		$(this).find(".mag-shade *").stop();

		$(this).find(".mag-shade")
		.stop()
		.hide()
		.animate({
			opacity: '0',
		}, "slow");

		$(this).find(".mag-shade h1").animate({
			bottom: '-50px',
			opacity: '0',
		}, "slow");

		$(this).find(".mag-shade p").animate({
			bottom: '-150px',
			opacity: '0',
		}, "slow");
		// $(this).find(".mag-shade").hide();
	});

	//鍥句功婊戣繃鏄剧ず褰撳墠鏈熶細鍛樹綔鍝侀泦灏侀潰
	$(function(){

		$("#work li img").hide();
		$("#work li img").eq(0).show();
		$("#work li a").eq(0).addClass("active");

		$("#work li").mouseover(function(){
			$("#work li").find("a").removeClass();
			$(this).find("a").addClass("active");
			$("#work li").find("img").hide();
			$(this).find("img").show();
		})

		$("#work li").mouseleave(function(){

			$("#work li img").hide();
			$("#work img").eq(0).show();
			$("#work a").removeClass();
			$("#work a").eq(0).addClass("active");

		});
	});

	// 婊戣繃鍥句功鍚戜笂绉诲姩
	$(".book-img").hover(function(){
		$(this).parent().stop().animate({

			marginTop: '15px'
		}, "fast");
	},function(){
		$(this).parent().stop().animate({

			marginTop: '20px'
		}, "fast");
	});

	// 鐐瑰嚮涓嬭浇閾炬帴
	$('.link a').click(function() {
		var index = $(this).index();
		$.get('/booknums?book_id='+$(this).attr('data-id'), function(e) {

		})
	});

	$('.cover').cover();

		
