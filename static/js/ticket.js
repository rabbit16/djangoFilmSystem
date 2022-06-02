let $ticket = $('.movie-contain');  // 获取购票表单元素
const container = document.querySelector(".container");////返回class为container的dom
			const seats = document.querySelectorAll(".row .seat:not(.occupied)");
			const count = document.getElementById("count");
			const total = document.getElementById("total");
			const screeningSelect = document.getElementById("screening");
			const movieSelect = document.getElementById("movie");
			let ticketPrice = +movieSelect.value;//加+代表Number,不加代表字符串
			let screeningID = 0;
			populateUI();
			movieSelect.addEventListener('change',e=>// 电影下拉框事件监听
			{
				ticketPrice=+e.target.value;//意思是:某一个option的值强行变成Number赋值给票价
				setMovieData(e.target.selectedIndex,e.target.value);
				//console.log(e.target.selectedIndex,e.target.value);//index从0开始,值为value
				undateSeletedCount();
			});//下拉框改变时

			//新加
			screeningSelect.addEventListener('change',e=>// 电影下拉框事件监听
			{
				screeningID=e.target.value;
				// TODO 清空样式
				// let seats = document.querySelectorAll(".row .seat:not(.occupied)");
				let seat_me = document.querySelectorAll(".row .seat");  // seat occupied
				let arry = [];
				for (let i = 0; i < seat_me.length; i++) {
					arry.push(seat_me[i].getAttribute('title'))
				}
				console.log(seats)
				console.log(arry)
				// console.log(screeningID);
				// $ticket.submit(function (e){
				// 	//1、创建请求参数
				// 	let SdataParams = {
				// 		"screening": screeningID,
				// 		"request_type": "occupy",
				// 	};
				// 	//2、创建ajax请求
				// 	$.ajax({
				// 	  // 请求地址
				// 	  url: "/ticket_update/",  // url尾部需要添加/
				// 	  // url: "{% url 'ticket_update' %}",  // url尾部需要添加/
				// 	  // 请求方式
				// 	  type: "GET",
				// 	  data: JSON.stringify(SdataParams),
				// 	  // 请求内容的数据类型（前端发给后端的格式）
				// 	  contentType: "application/json; charset=utf-8",//将文字内容指定为json格式
				// 	  // 响应数据的格式（后端返回给前端的格式）
				// 	  dataType: "json",
				// 	})
				// 	// console.log(SdataParams)
				// 	.done(function (log) {
				// 		if (log.errno === "0") {
				// 		  // 登录成功
				// 		  message.showSuccess('恭喜你，传呼成功！');
				// 		  setTimeout(() => {
				// 			// 登录成功之后重定向到主页
				// 			window.location.href = '/';
				// 		  }, 1000)
				// 		} else {
				// 		  // 注册失败，打印错误信息
				// 		  message.showError(log.errmsg);
				// 		}
				// 	})
				// })
					//1、创建请求参数
					// let SdataParams = {
					// 	"screening": screeningID,
					// 	"request_type": "occupy",
					// };
					let SdataParams = {
						"screening": screeningID,
						"request_type": "occupy",
					};
					//2、创建ajax请求  这里要设置
					$.ajaxSetup({
					  data: {csrfmiddlewaretoken: '{% csrf_token %}' },
					});
					$.ajax({
					  // 请求地址
					  url: "",  // url尾部需要添加/
					  // url: "{% url 'ticket_update' %}",  // url尾部需要添加/
					  // 请求方式
					  type: "POST",
					  data: JSON.stringify(SdataParams),
					  // 请求内容的数据类型（前端发给后端的格式）
					  contentType: "application/json; charset=utf-8",//将文字内容指定为json格式
					  // 响应数据的格式（后端返回给前端的格式）
					  dataType: "json",
					})
					// console.log(SdataParams)
					.done(function (log) {
						if (log.errno === "0") {
						  // 登录成功
						  message.showSuccess('恭喜你，传呼成功！');

						  let seat_dict = log.seat_dict;
						  for (let i = 0; i < seat_me.length; i++) {
								// arry.push(seat_me[i].getAttribute('title'))
							  if (seat_dict.get(seat_me[i].getAttribute('title'), 0) !== 0){
								  seat_me[i].classList.add("occupied")
							  }
							}
						  // console.log(seat_me)
						  // for (let i = 0; i < seat_me.length; i++) {
							//   if (seat_me[i].class === "seat occupied"){
							// 	  seat_me[i].classList.add("occupied")
							//   }
							// }
						  // setTimeout(() => {
							// // 登录成功之后重定向到主页
							// window.location.href = '/';
						  // }, 1000)
						} else {
						  // 注册失败，打印错误信息
						  message.showError(log.errmsg);
						}
					})
			});//下拉框改变时


			container.addEventListener("click",e=>// 座位点击事件
			{
				if(e.target.classList.contains("seat")&&!e.target.classList.contains("occupied"))//意识是如果e.target标签中包含seat的话并且e.target中不包含occupied
				{
					e.target.classList.toggle("selected"); //若classList中存在给定的值，删除它，否则，添加它
					undateSeletedCount();
				}
			});

			$ticket.submit(function (e){
				//1、创建请求参数
				let OdataParams = {
					"count": count.innerText,
					"total": total.innerText,
				};
				//2、创建ajax请求
				$.ajaxSetup({
					data: {csrfmiddlewaretoken: '{% csrf_token %}' },
				});
				$.ajax({
					// 请求地址
					url: "",  // url尾部需要添加/
					// url: "{% url 'ticket_update' %}",  // url尾部需要添加/
					// 请求方式
					type: "POST",
					data: JSON.stringify(OdataParams),
					// 请求内容的数据类型（前端发给后端的格式）
					contentType: "application/json; charset=utf-8",//将文字内容指定为json格式
					// 响应数据的格式（后端返回给前端的格式）
					dataType: "json",
				})
				console.log(OdataParams)
				.done(function (log) {
					if (log.errno === "0") {
						// 登录成功
						message.showSuccess('订票成功！');
						setTimeout(() => {
							// 登录成功之后重定向到主页
							window.location.href = '/';
						  }, 1000)
					} else {
						// 注册失败，打印错误信息
						message.showError(log.errmsg);
					}
				})
			})





			function setMovieData(movieIndex, moviePrice)//保存电影索引值和票价
			{
				//保存到本地存储中
				localStorage.setItem("selectedMovieIndex", movieIndex);//电影索引值
				localStorage.setItem("selectedMoviePrice", moviePrice);//票价
			}
			function undateSeletedCount()/// 更新座位数及总票价
			{
				const selectedSeats=document.querySelectorAll(".row .seat.selected");
				//console.log(selectedSeats);//如果这里要有值得点击某一个座位
				const seatsIndex=[...selectedSeats].map(seat=>[...seats].indexOf(seat));//把点击的座位
				//console.log(...seats);//这以上的两句的意思是:点击的[...selectedSeats].map(seat)在[...seats].indexOf(seat)中第一次出现的索引值.
				//保存到本地存储中.
				localStorage.setItem("selectedSeats",JSON.stringify(seatsIndex));//意思是因为是数组所以转换为字符串然后保存到本地存储中.

				 const selectedSeatsCount = selectedSeats.length;//点击的数量
				  count.innerText = selectedSeatsCount;//数量(座位)
				  total.innerText = selectedSeatsCount * ticketPrice;//*起来的票价
				  /**/
				  //console.log( "座位"+count.innerText ,"票价"+total.innerText);
			}
			function populateUI() {// 获取本地数据并渲染样式
				const selectedSeats=JSON.parse(localStorage.getItem("selectedSeats"));//点击的
				if(selectedSeats!=null&&selectedSeats.length>0)
				{//意思是:保存起来的点击的正方形。不为空并且至少有一个的话.
					seats.forEach((seat,index)=>//遍历渲染颜色
						{
							if(selectedSeats.indexOf(index)>-1)
							{
								seat.classList.add("selected");
							}
						});
				}
				  const selectedMovieIndex = localStorage.getItem("selectedMovieIndex");
				  //意思是option的index值,在不为空的条件下,点击的是哪一个就赋值设置哪一个·的座位与票价。
				  // movieSelect.selectedIndex 代表哪一个option从0开始
				   if (selectedMovieIndex !== null) {
	    				movieSelect.selectedIndex = selectedMovieIndex;
				   }
			}

			//三件套
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
			$.ajaxSetup({
			beforeSend: function (xhr, settings) {
			  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			  }
			}
		  });