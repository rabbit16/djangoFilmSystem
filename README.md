创建一个media文件夹
创建一个log文件夹
将media， static，apps设置成根目录，templates设置成模版路径
执行python manage.py makemigrations
然后执行 python manage.py migrate
检查utils文件夹下dbs中的my.cnf文件是否连接的是自己的数据库
运行项目

##2022/5/25 修改人：罗怡婷
修改源码文件：auth\models
主要操作：注释了first_name ，last_name ,date_joined
操作目的：简化User表，删除了一些冗余的属性

##2022/5/28 修改人罗怡婷
建表：场次，包含
主键Times_id,
外键T_studio,
外键T_movie,
内键session_time

改动：
tb_Ticket:
改成：
主键Ticket_id
内键price
内键all_message
外键Ticket_seat
外键Ticket_session（对应新建的表）
外键Ticket_user
内键状态state（0正常，1退票，2已积分）

##2022/5/29 修改人罗怡婷
对users进行模型查询时应该修改对应的auth\models里的源代码
注释first_name ，last_name ,date_joined这三个字段


