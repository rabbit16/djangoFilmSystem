创建一个media文件夹
创建一个log文件夹
将media， static，apps设置成根目录，templates设置成模版路径
执行python manage.py makemigrations
然后执行 python manage.py migrate
检查utils文件夹下dbs中的my.cnf文件是否连接的是自己的数据库
运行项目