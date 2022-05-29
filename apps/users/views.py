import json

from django.contrib.auth import login
from django.shortcuts import render, HttpResponse

# Create your views here.
from django.views import View

# from index.models import User
from users.models import User, Movie as movies, Studio, Seat, Ticket as tickets, Times
from utils.res_code import to_json_data, Code, error_map
from verifications.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.db.models import Max
from datetime import datetime, timedelta


def discount(user_rank):
    if user_rank >= 400:
        return 0.7
    elif user_rank >= 200:
        return 0.8
    elif user_rank >= 100:
        return 0.9
    else:
        return 1


class index(View):

    def get(self, request):
        return render(request, "index/index.html", context={
            "hotfilmlefts": movies.objects.filter(hotPlay=True)[:3],
            "hotfilmcenters": movies.objects.filter(hotPlay=True)[3:6],
            "hotfilmrights": movies.objects.filter(hotPlay=True)[6:9],
        })

    def post(self, request):
        pass


class IndexTest(View):

    def get(self, request):
        return render(request, "index/indexTest.html")
        #               , context={
        #     "hotfilmlefts": movies.objects.filter(hotPlay=True)[:3],
        #     "hotfilmcenters": movies.objects.filter(hotPlay=True)[3:6],
        #     "hotfilmrights": movies.objects.filter(hotPlay=True)[6:9],
        # })

    def post(self, request):
        pass


class Login(View):

    def get(self, request):
        return render(request, "index/login.html")

    # def post(self, request):
    #     return json.dumps({
    #         "errno": '1'
    #     })
    def post(self, request):

        user_info = json.loads(request.body.decode())
        username = user_info.get("username")
        password = user_info.get("password")
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(request, username=username, password=password)
        try:
            # 验证如果用户不为空
            if user is not None:
                # login方法登录
                login(request, user)
                # data = {
                #     'errno': Code.OK
                # }
            return to_json_data(errno=Code.OK, errmsg=error_map[Code.OK])
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        #     # 返回登录成功信息
        #     # return HttpResponse('index.html')
        #     return redirect("/index/") #这点确实不会，等学长
        #     # return render(request, 'index.html')
        # else:
        #     # 返回登录失败信息
        #     return HttpResponse('登陆失败，未注册或密码错误！')


#
class Register(View):

    def get(self, request):
        return render(request, "index/register.html")

    def post(self, request):
        userInfo = json.loads(request.body.decode())
        if userInfo["gender"] == 'male':
            userInfo["gender"] = True
        else:
            userInfo["gender"] = False
        registerForm = RegisterForm(userInfo)

        try:
            if registerForm.is_valid():
                user = User.objects.create_user(username=registerForm.cleaned_data.get('username'),
                                                password=registerForm.cleaned_data.get('password'),
                                                mobile=registerForm.cleaned_data.get('mobile'),
                                                email=registerForm.cleaned_data.get('email'),
                                                sex=registerForm.cleaned_data.get("gender"),
                                                name=registerForm.cleaned_data.get("real_name"),
                                                birthday=registerForm.cleaned_data.get("birthday")
                                                )  # TODO 并没有写完整
                login(request, user)
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])


#
class Movie(View):

    def get(self, request):
        return render(request, "index/movie.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })

    def add(self, request):
        movie_info = json.loads(request.body.decode())
        if not movies.objects.all().exists():
            id = 1
        else:
            id = int(movies.objects.all().aggregate(Max('Movie_id'))['Movie_id__max'])
            # 分配一个id
        try:
            if movie_info.is_valid():
                movies.objects.create(Movie_id=id,
                                      Movie_name=movie_info.get('Movie_name'),
                                      Movie_time=movie_info.get('Movie_time'),
                                      Movie_img=movie_info.get('Movie_img'),
                                      Movie_price=movie_info.get('Movie_price'),
                                      Movie_abstract=movie_info.get('Movie_abstract'),
                                      Movie_hotplay=movie_info.get('Movie_hotplay'),
                                      )
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        return 0


#
class MovieDetail(View):

    def get(self, request):
        return render(request, "index/movieDetail.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })


#
class Rank(View):

    def get(self, request):
        return render(request, "index/rank.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })

    def refresh(self):
        tics = tickets.objects.filter(PRI_CHOICES=1)
        for changes in tics:
            user = User.objects.filter(id=changes.Ticket_user)
            user.update(Rank=user[0].Rank + changes.price)
            changes.update(PRI_CHOICES=3)
        return json.dumps({
            "errno": '1'
        })


#
class Ticket(View):

    def get(self, request):
        return render(request, "index/ticket.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })

    def add(self, request):
        ticinfo = json.loads(request.body.decode())
        time = datetime.now()
        time_str = time.strftime('%Y%m%d%H%M')[2:]
        ticket_id = int(time_str + "%04d" % ticinfo.get('Seat_id') + "%02d" % ticinfo.get('Studio_id'))
        rate_discount = discount(User.objects.filter(id=ticinfo.get("user_id"))[0].Integral)
        session = Times.objects.filter(Times_id=ticinfo.get('session_id'))[0]
        movie_price = movies.objects.filter(Movie_id=session.T_movie)[0].Movie_price
        session_rate = Studio.objects.filter(Studio_id=session.T_studio)[0].price_weight
        price_discount = rate_discount * movie_price * session_rate

        try:
            if ticinfo.is_valid():
                tickets.objects.create(Ticket_id=ticket_id,
                                       Ticket_seat=ticinfo.get('Seat_id'),
                                       Ticket_session=ticinfo.get('Studio_id'),
                                       price=price_discount,
                                       Ticket_user=ticinfo.get("user_id"),
                                       PRI_CHOICES=1,
                                       )
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        return 0


class Session(View):

    def get(self, request):
        return render(request, "index/movie.html")

    def query(self, request):
        movie_info = json.loads(request.body.decode())
        query_id = movie_info.get('Movie_id')
        sessions = Times.objects.filter(T_movie=query_id)

    # 给定场次查询该场次已安排的时间点
    def search(self, request):

        studio_info = json.loads(request.body.decode())
        occupies = Times.objects.filter(T_studio=studio_info.get('studio_id'), session_time__gt=datetime.now())
        return occupies

    # 添加场次
    def add(self, request):
        session_info = json.loads(request.body.decode())
        check_time = session_info.get('session_time')
        conflict = Times.objects.filter(T_studio=session_info.get('studio_id'),
                                        session_time__range=[check_time + timedelta(hours=-3),
                                                             check_time + timedelta(hours=3)])
        if not bool(conflict):  # 冲突集合不为空，当前时间段被占用
            return to_json_data(errno=Code.CONFLICT, errmsg=error_map[Code.CONFLICT])
        if not Times.objects.all().exists():
            id = 1
        else:
            id = int(movies.objects.all().aggregate(Max('Times_id'))['Times_id__max'])
            # 分配一个id
        try:
            if session_info.is_valid():
                Times.objects.create(Times_id=id,
                                     T_studio=session_info.get('studio_id'),
                                     T_movie=session_info.get('movie_id'),
                                     session_time=session_info.get('session_time'),
                                     )
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
        return 0



# class Studio_add(View):
#     def post(self, request):
#         studio_info = json.loads(request.body.decode())
#         if not Studio.objects.all().exists():
#             id = 1
#         else:
#             id = int(Studio.objects.all().aggregate(Max('Studio_id'))['Studio_id__max'])
#             # 分配一个id
#         try:
#             if studio_info.is_valid():
#                 # 添加演播厅信息
#                 movies.objects.create(Stuidio_id=id,
#                                       Studio_name=studio_info.get('Studio_name'),
#                                       Studio_type=studio_info.get('Studio_type'),
#                                       price_weight=studio_info.get('price_weight'),
#                                       )
#
#             data = {
#                 'errno': Code.OK
#             }
#
#             return to_json_data(data=data)
#         except:
#             return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
#         return 0
