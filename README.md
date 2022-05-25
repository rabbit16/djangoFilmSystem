创建一个media文件夹
创建一个log文件夹
将media， static，apps设置成根目录，templates设置成模版路径
执行python manage.py makemigrations
然后执行 python manage.py migrate
检查utils文件夹下dbs中的my.cnf文件是否连接的是自己的数据库
运行项目

2022/5/25 修改人：罗怡婷
你在里面加一句，修改了源码中的什么文件，主要干了什么事，目的是什么
修改源码文件：auth\models
主要操作：注释了first_name ，last_name ,date_joined
操作目的：简化User表，删除了一些冗余的属性