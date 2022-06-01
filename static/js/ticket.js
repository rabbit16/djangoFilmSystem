const container = document.querySelector(".container");////返回class为container的dom
			const seats = document.querySelectorAll(".row .seat:not(.occupied)");
			const count = document.getElementById("count");
			const total = document.getElementById("total");
			const screeningSelect = document.getElementById("screening");
			const movieSelect = document.getElementById("movie");
			let ticketPrice = +movieSelect.value;//加+代表Number,不加代表字符串
			populateUI();
			movieSelect.addEventListener('change',e=>// 电影下拉框事件监听
			{
				ticketPrice=+e.target.value;//意思是:某一个option的值强行变成Number赋值给票价
				setMovieData(e.target.selectedIndex,e.target.value);
				//console.log(e.target.selectedIndex,e.target.value);//index从0开始,值为value
				undateSeletedCount();
			});//下拉框改变时
			container.addEventListener("click",e=>// 座位点击事件
			{
				if(e.target.classList.contains("seat")&&!e.target.classList.contains("occupied"))//意识是如果e.target标签中包含seat的话并且e.target中不包含occupied
				{
					e.target.classList.toggle("selected");
					undateSeletedCount();
				}
			});
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