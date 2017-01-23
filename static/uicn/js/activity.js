// 下拉选择框
$(function(){

    $('.event-select').click(function(ev){
        var selectBox = $(this);
        if( selectBox.hasClass('open') ){
            selectBox.removeClass('open');
        } else{
            selectBox.addClass('open');

            selectBox.find('.select-menu a').click(function(){
                var val = $(this).attr('rel');
                var txt = $(this).html();
                selectBox.find('.select-val').val(val);
                selectBox.find('.selected').html(txt);
            });
        }
        ev.stopPropagation();

    });
    /*点击任何地方关闭层*/
    $(document).click(function(event){
        $('.event-select').removeClass('open');
    });


});
    //兼容ie8
 $(document).ready(function(){
    $(".event-list").find('li:odd').css({"margin-right":"0"});
});
