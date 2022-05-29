from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager as _UserManager, AbstractUser


class UserManager(_UserManager):
    def create_superuser(self, username, password, email=None, **extra_fields):
        super().create_superuser(username=username, email=email, password=password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = ['mobile']
    name = models.CharField(max_length=20,help_text="用户真实姓名", verbose_name="用户真实姓名",error_messages={"message": "名字格式出错"} )
    ticketManager = models.BooleanField(verbose_name="票务管理员", help_text="票务管理员", default=False)
    buyManager = models.BooleanField(verbose_name="售票员", help_text="售票员", default=False)
    mobile = models.CharField(max_length=11, verbose_name='手机号', help_text="手机号", unique=True,error_messages={'unique': "该手机号已注册"})
    registration_data = models.DateTimeField(verbose_name="注册时间", help_text="注册时间",default=timezone.now)
    sex = models.BooleanField(verbose_name="性别", help_text="性别", default=True)
    birthday = models.DateTimeField(verbose_name="生日", help_text="生日", default=timezone.now)
    Integral = models.IntegerField(help_text="积分", verbose_name="积分")
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'

    def __str__(self):
        return self.mobile

class Seat(models.Model):
    Seat_id = models.IntegerField(help_text="座位id", verbose_name="座位id")
    Seat_name = models.CharField(max_length=20, verbose_name="座位编号", help_text="座位编号")
    s_stu = models.ManyToManyField('Studio')
    class Meta:
        db_table = 'tb_Seat'
        verbose_name = '座位'
    def __str__(self):
        return self.Seat_name

class Studio(models.Model):
    Studio_id = models.IntegerField(help_text="演播厅id",verbose_name="演播厅id")
    Studio_name = models.CharField(max_length=20, help_text="演播厅名称", verbose_name="演播厅名称")
    Studio_type = models.CharField(max_length=20, help_text="演播厅类型", verbose_name="演播厅类型")
    Seating = models.CharField(max_length=20, help_text="座位个数", verbose_name="座位个数")
    price_weight = models.FloatField(verbose_name="价格权重", help_text="价格权重", default=0)

    class Meta:
        db_table = 'tb_Studio'
        verbose_name = '演播厅'

    def __str__(self):
        return self.Studio_id

class Movie_type(models.Model):  # 电影标签
    # Romance = models.CharField(max_length=20, help_text="爱情片", verbose_name="爱情片")
    # Drama = models.CharField(max_length=20, help_text="剧情片", verbose_name="剧情片")
    # Comedy = models.CharField(max_length=20, help_text="喜剧片", verbose_name="喜剧片")
    # Ethics = models.CharField(max_length=20, help_text="伦理片", verbose_name="伦理片")
    # Literature= models.CharField(max_length=20, help_text="文艺片", verbose_name="文艺片")
    # Music = models.CharField(max_length=20, help_text="音乐片", verbose_name="音乐片")
    # Animation = models.CharField(max_length=20, help_text="动漫片", verbose_name="动漫片")
    # Martial_arts = models.CharField(max_length=20, help_text="武侠片", verbose_name="武侠片")
    # costume = models.CharField(max_length=20, help_text="古装片", verbose_name="古装片")
    # horror = models.CharField(max_length=20, help_text="恐怖片", verbose_name="恐怖片")
    # thriller = models.CharField(max_length=20, help_text="惊悚片", verbose_name="惊悚片")
    # Crime = models.CharField(max_length=20, help_text="犯罪片", verbose_name="犯罪片")
    # Suspense = models.CharField(max_length=20, help_text="悬疑片", verbose_name="悬疑片")
    # Documentary = models.CharField(max_length=20, help_text="纪录片", verbose_name="纪录片")
    # War = models.CharField(max_length=20, help_text="战争片", verbose_name="战争片")
    # Science= models.CharField(max_length=20, help_text="科幻片", verbose_name="科幻片")
    type_id = models.IntegerField(verbose_name="标签序号", help_text="标签序号")
    type_name = models.CharField(max_length=20, help_text="电影标签", verbose_name="电影标签")

    class Meta:
        db_table = "tb_movie_type"
        verbose_name = "电影标签"

    def __str__(self):
        return self.type_name

class Movie(models.Model):
    Movie_id = models.IntegerField(help_text="电影id", verbose_name="电影id")
    Movie_name = models.CharField(max_length=20, verbose_name='电影名', help_text="电影名")
    Movie_time = models.DateTimeField(verbose_name="电影上映时间", help_text="电影上映时间", default=timezone.now)
    Movie_img = models.URLField(max_length=100, verbose_name="电影图片", help_text="电影图片")
    Movie_price = models.FloatField(verbose_name="电影原价", help_text="电影原价", default=0)
    Movie_director=models.CharField(max_length=20, verbose_name='导演名', help_text="导演名")
    m_movietype = models.ManyToManyField(Movie_type)
    abstract = models.TextField(max_length=500, verbose_name="简介", help_text="简介", default="")
    hotPlay = models.BooleanField(verbose_name="是否为热映", help_text="是否为热映", default=False)
    class Meta:
        ordering = ['-Movie_time']
        db_table = 'tb_Movie'
        verbose_name = '电影'

    def __str__(self):
        return self.Movie_name



class Times(models.Model):  # 电影场次
    Times_id = models.IntegerField(help_text="场次id",verbose_name="场次id")
    T_studio = models.ForeignKey('Studio', on_delete=models.CASCADE)
    T_movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    session_time = models.DateTimeField(verbose_name="场次时间", help_text="场次时间", default=timezone.now)

    class Meta:
        db_table = "tb_occupy"
        verbose_name = "电影场次"

    def __str__(self):
        return self.Times_id


class Ticket(models.Model):
    Ticket_id = models.IntegerField(help_text="订单号",verbose_name="订单号")
    # Seat_id = models.IntegerField(max_length=20, help_text="座位id", verbose_name="座位id")
    # Seat_name = models.CharField(max_length=20, help_text="座位名称", verbose_name="座位名称")
    # Studio_id = models.IntegerField(max_length=20, help_text="演播厅id", verbose_name="演播厅id")
    # Studio_name = models.CharField(max_length=20, help_text="演播厅名称", verbose_name="演播厅名称")
    # Movie_name = models.CharField(max_length=20, verbose_name='电影名' , help_text="电影名")
    # Movie_time = models.DateTimeField(verbose_name="电影时间", help_text="电影时间")
    # s_user = models.ForeignKey(User, on_delete=models.CASCADE)+
    price = models.FloatField(verbose_name="电影票的价格", help_text="电影票的价格")
    Ticket_seat = models.ForeignKey('Seat', on_delete=models.CASCADE)
    Ticket_session = models.ForeignKey('Times', on_delete=models.CASCADE)
    Ticket_user = models.ForeignKey('User', on_delete=models.CASCADE)
    PRI_CHOICES = [
        (1, "正常"),
        (2, "退票"),
        (3, "已积分")
    ]
    state = models.IntegerField(choices=PRI_CHOICES, verbose_name="电影票状态", help_text="电影票状态")
    class Meta:
        db_table = 'tb_Ticket'
        verbose_name = '电影票'

    def __str__(self):
        return self.Ticket_id



class Comment(models.Model):
    Comment_id = models.IntegerField(help_text="评论id",verbose_name="评论id")
    Comment_content = models.TextField(help_text="评论内容", verbose_name="评论内容")
    Comment_time = models.DateTimeField(verbose_name="评论时间", help_text="评论时间", default=timezone.now)
    Comment_likes = models.IntegerField(help_text="点赞数",verbose_name="点赞数")
    Comment_author = models.ForeignKey('User', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-Comment_time', '-Comment_id']
        db_table = 'tb_Comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name  # 显示的复数名称

    def to_dict_data(self):
        comment_dict = {
            'Comment_id': self.Comment_id,
            'Comment_content': self.Comment_content,
            'Comment_author': self.Comment_author.username,
            'Comment_time': self. Comment_time.strftime('%Y年%m月%d日 %H:%M'),
            'parent': self.parent.to_dict_data() if self.parent else None,
        }
        return comment_dict

    def __str__(self):
        return self.Comment_id