//骞垮憡鐐瑰嚮閲�
$(document).on('click','.adimg',function(){

   var ad = $(this).attr('rel');

   $.post('/adnum',{ad:ad}, function(e) {

   })
})


//杞挱鍥剧偣鍑婚噺
$('.adv_img').click(function(){
     var ad = $(this).attr('rel');

     $.post('/adnum',{'ad':ad,'stat':1}, function(e) {

     })

 })


 //寤惰繜鍔犺浇
$(document).ready(function(){
     $('.imgloadinglater').lazyload({
         threshold : -100, //璺濈100鍍忕礌瑙﹀彂
         effect : "fadeIn" //鏄剧ず鐗规晥
     });
 });
 //棣栭〉鏂囩珷鍒楄〃鏁堟灉
 $('.h-article-list li').hover(function(){
     $(this).addClass('on').prev('li').addClass('oe');
 },function(){
     $(this).removeClass('on').prev('li').removeClass('oe');
 })
