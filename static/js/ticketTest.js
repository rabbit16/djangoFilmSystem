$(function () {
  let $screening = $('#screening');

    // 获取用户选择的内容
    let sScreening = $("#screening option:selected").val();

    // 发起传递场次请求
    // 1、创建请求参数
    let SdataParams = {
      "screening": sScreening,
      "request_type": "occupy",
    };

    // 2、创建ajax请求
    $.ajax({
      // 请求地址
      url: "/ticket/",  // url尾部需要添加/
      // 请求方式
      type: "POST",
      data: JSON.stringify(SdataParams),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",//将文字内容指定为json格式
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (log) {
        if (log.errno === "0") {
          // 登录成功
          message.showSuccess('恭喜你，登录成功！');
           setTimeout(() => {
            // 登录成功之后重定向到主页
            window.location.href = '/';
          }, 1000)
        } else {
          // 注册失败，打印错误信息
          message.showError(log.errmsg);
        }
      })
  // });


  // // 判断用户名是否已经注册
  // function fn_check_username() {
  //   let sUsername = $username.val();  // 获取用户名字符串
  //   let sPassword = $password.val(); //获取用户密码字符串
  //   let sReturnValue = "";
  //
  //   if (sUsername === "") {
  //     message.showError('用户名不能为空！');
  //     return
  //   }
  //   if (sPassword === "") {
  //     message.showError('密码不能为空！');
  //     return
  //   }
  //
  //   if (!(/^\w{5,20}$/).test(sUsername)) {
  //     message.showError('请输入5-20个英文字符的用户名');
  //     return
  //   }
  //
  //   // 发送ajax请求，去后端查询用户名是否存在
  //   $.ajax({
  //     url: '/username/' + sUsername + '/',
  //     type: 'GET',
  //     dataType: 'json',
  //     async: false//这里要是True就是异步，如果是False就是同步
  //   })
  //     .done(function (log) {
  //       if (log.data.count == 0) {
  //         message.showError(log.data.username + '未注册，请先注册！');
  //         sReturnValue = ""
  //       } else {
  //         message.showInfo(log.data.username + '已注册！');
  //         sReturnValue = ""
  //       }
  //     })
  //     .fail(function () {
  //       message.showError('服务器超时，请重试！');
  //       sReturnValue = ""
  //     });
  //
  //   // 发送ajax请求，去后端查询密码是否匹配
  //   $.ajax({
  //     url: '/password/' + sPassword + '/',
  //     type: 'GET',
  //     dataType: 'json',
  //     async: false//这里要是True就是异步，如果是False就是同步
  //   })
  //     .done(function (log) {
  //       if (log.data.password !== sPassword) {
  //         message.showError(log.data.password + '密码输入错误！');
  //         sReturnValue = ""
  //       } else {
  //         message.showInfo(log.data.password + '密码正确！');
  //         sReturnValue = "success"
  //       }
  //     })
  //     .fail(function () {
  //       message.showError('服务器超时，请重试！');
  //       sReturnValue = ""
  //     });
  //   return sReturnValue
  // }


  // get cookie using jQuery
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });
  // generateImageCode()
});