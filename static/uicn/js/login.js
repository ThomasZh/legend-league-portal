$(function() {
  //鐢ㄦ埛妗嗗け鍘汇€佸緱鍒扮劍鐐逛簨浠跺鐞�

  var userdel = $('#username').val();
  $('#username').blur(function() {
    if ($.trim($(this).val()).length <= 0) {
      $(this).val(userdel)
      $(this).parent().removeClass('login-on');
    } else {
      $(this).parent().addClass('login-on');
    }
  }).focus(function() {
    $(this).parent().addClass('login-on');
    if ($(this).val() == userdel)
      $(this).val('');
      userdel = "";
  });

  var passdel = $('#password').val();
  $('#password').blur(function() {
    if ($.trim($(this).val()).length <= 0) {
      $(".la_password").remove();
      $(this).parent().removeClass('login-on');
    } else {
      $(this).parent().addClass('login-on');
    }
  }).focus(function() {
    $(this).parent().addClass('login-on');
    $(".la_password").remove();
    if ($(this).val() == passdel)
      $(this).val('');
      passdel = "";
  });
  var code = $('input[name=code]').val();
  var verify = false;
  $('input[name=code]').blur(function() {
    if ($.trim($(this).val()).length <= 0) {
      $(this).val(code);
      $(this).parent().removeClass('login-on');
    } else {
      $(this).parent().addClass('login-on');
    }
  }).focus(function() {
    $(this).parent().addClass('login-on');
    if ($(this).val() == code)
      $(this).val('');
  });

  $('#login-button').click(function() {
    var data={};
    var username = $.trim($('#username').val());
    if (username.length <= 0 || username == userdel) {
      globalTip({
        'msg': '璇峰～鍐欑敤鎴峰悕鎴栭偖绠�'
      });
      $('#username').focus();
      return false;
    }
    data.username = username;

    password = $.trim($('#password').val());

    if (password.length <= 0 || password == passdel) {
      globalTip({
        'msg': '璇峰～鍐欏瘑鐮�'
      });
      $('#password').focus();
      return false;
    }

    data.password = $.md5(password);

    if (verify) {
      if ($.trim($('input[name=code]').val()).length <= 0 || $('input[name=code]').val() == code) {
        globalTip({
          'msg': '璇峰～鍐欓獙璇佺爜'
        });
        $('input[name=code]').focus();
        return false;
      }
      data.code = $.trim($('input[name=code]').val());
    }

    $('#login-button').attr('disabled', 'true');
    $.ajax({
      type: 'post',
      url: 'check',
      dataType: "json",
      data: data,
      success: function(msg) {
        if (200 == msg['code']) {
          globalTip(msg);
        } else if (101 == msg['code']) {
          alert(msg.msg);
          $('#login-button').removeAttr("disabled");
        } else {
          globalTip(msg);
          $('#login-button').removeAttr("disabled");
        }
        if (msg.verify) {
          verify = msg.verify;
          $('#verify').removeClass('hide');
          $('input[name=code]').focus();
          $('.fg-code-pic img').trigger('click');
        }
        return false;
      },
      error: function() {
        redirectTip('缃戠粶寮傚父,鍒锋柊閲嶈瘯', true, '/login', 3);
      }
    });
    return false;
  });
  $(window).keydown(function(event) {
    switch (event.keyCode) {
      case 13:
        $('#login-button').trigger('click');
        break;
    }
  });
});
