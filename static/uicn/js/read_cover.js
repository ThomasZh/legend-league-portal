(function($, window, document, undefined) {
	$.fn.cover = function() {
		var ele = $(this);
		for (var i = 0; i < ele.length; i++) {
			eve($(ele[i]));
		};
		function eve(obj) {
			obj.find("li img").hide();
			obj.find("li img").eq(0).show();
			obj.find("li a").eq(0).addClass("active");

			obj.find("li").mouseover(function(){
				obj.find("li").find("a").removeClass();
				$(this).find("a").addClass("active");
				obj.find("li").find("img").hide();
				$(this).find("img").show();
			})

			obj.find("li").mouseleave(function(){

				obj.find("li img").hide();
				obj.find("img").eq(0).show();
				obj.find("a").removeClass();
				obj.find("a").eq(0).addClass("active");

			});
		}
	}
})(jQuery, window, document);
