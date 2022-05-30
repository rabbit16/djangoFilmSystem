index主界面：
get: 返回显示在主界面上的电影 √
以及榜上电影

Login登录：
post:比对并登录 √
以管理员身份登录

Register注册：
post:返回注册成功与否 √

Movie电影：
post：电影添加 √
评论添加

MovieDetail电影细节：
post:返回电影添加：等完善数据库添加评论

Rank积分：
put:刷新积分数据 √

Ticket订单：
post:添加订单数据 √
put:退票
get:重定向到二维码界面

Session场次：
post:添加场次，查询演播厅占用情况，查询电影的场次信息 √

Seat座位：
post:查询当前场次的座位占用情况 √

UserCenter用户中心：
post:显示用户的包括积分内的部分信息

AdminCenter管理员中心：
get:验证管理员权限等级并重定向到电影添加，
场次添加，
收入查看，
管理员添加
界面

Search搜索引擎：
get:根据输入的字符串重定向到符合条件的电影列表
根据选择的标签重定向到电影列表