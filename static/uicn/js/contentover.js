// JavaScript Document

$(document).ready(function(){

    $(document).on('mouseenter', '.Inspir-list li', function(){
        $(this).find('.iInspir-cover-user').addClass('col'); //鐢ㄦ埛鍚嶅彉棰滆壊
        $(this).find('.iInspir-cover-user i').show();
        $(this).find('.iInspir-block')
            .stop()
            .animate({ opacity : '1'}, 300)
            .addClass('op');
    });
    $(document).on('mouseleave', '.Inspir-list li', function(){
        $(this).find('.iInspir-cover-user').removeClass('col');
        $(this).find('.iInspir-cover-user i').hide();
        $(this).find('.iInspir-block')
            .stop()
            .animate({ opacity : '0'}, 300)
            .removeClass('op')
    });


    /* 鐏垫劅 */
    $(document).on('mouseenter', '.content_list li', function(){
        $(this).find('.border')
            .stop()
            .animate({ opacity : '1'}, 300)
            .removeClass('hide')
            .addClass('show');
    });
    $(document).on('mouseleave', '.content_list li', function(){
        $(this).find('.border')
            .stop()
            .animate({ opacity : '0'}, 300)
            .removeClass('show')
            .addClass('hide');
    });


})
