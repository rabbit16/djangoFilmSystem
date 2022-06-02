import json

from django.contrib.auth import login
from django.shortcuts import render, HttpResponse

# Create your views here.
from django.views import View

# from index.models import User
from users.models import User, Movie as movies, Studio, \
    Seat, Ticket as tickets, Times, Movie_type, Comment
from utils.res_code import to_json_data, Code, error_map
from verifications.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.db.models import Max
from datetime import datetime, timedelta
import hashlib
from django.views.decorators.csrf import csrf_exempt


def discount(user_rank):
    if user_rank >= 400:
        return 0.7
    elif user_rank >= 200:
        return 0.8
    elif user_rank >= 100:
        return 0.9
    else:
        return 1


class Index(View):

    def get(self, request):
        # 获得有安排场次的电影
        movie_onplay = movies.objects.filter(
            id__in=[times['T_movie_id'] for times in
                    Times.objects.filter(session_time__gt=datetime.now()).values()
                    ])
        # 存相应电影的id
        movie_ids = [i['Movie_id'] for i in movie_onplay.values()]
        # 票房数据
        box = [0 for _ in range(len(movie_onplay))]
        # 统计票房
        for i in range(len(movie_onplay)):
            # 当前电影的场次号和对应的价格（原价）
            current_sessions = [
                [session['Times_id'],
                 movie_onplay.values()[i]['Movie_price']]
                for session in
                Times.objects.filter(T_movie_id=movie_ids[i]).values()
            ]
            # 所有当前电影的票价总和
            box[i] = sum([
                session[1] *
                len(tickets.objects.filter(Ticket_session=session[0]))
                for session in current_sessions
            ])
        # 从大到小对box排序,box是电影的票房
        box_new = [[movie_onplay[i], box[i]] for i in range(len(box))]
        box_sort = sorted(box_new, key=lambda x: -x[1])
        movie_top = [i[0] for i in box_sort]
        movie_box = [i[1] for i in box_sort]
        return render(request, "index/index.html", context={
            "hotfilmlefts": movies.objects.filter(hotPlay=True)[:3],
            "hotfilmcenters": movies.objects.filter(hotPlay=True)[3:6],
            "hotfilmrights": movies.objects.filter(hotPlay=True)[6:9],
            "movie_top": movie_top[:10],  # 票房前十的电影
            "movie_box": movie_box[:10],  # 上述电影的票房
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
                                                )
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

    # movie电影添加, comment评论添加
    def post(self, request):
        request_info = json.loads(request.body.decode())
        if request_info.get('request_type') == 'movie':
            movie_info = json.loads(request.body.decode())
            if not movies.objects.all().exists():
                id = 1
            else:
                id = int(movies.objects.all().aggregate(Max('Movie_id'))['Movie_id__max'])
                # 分配一个id
            try:
                if movie_info.is_valid():
                    movie = movies.objects.create(Movie_id=id,
                                                  Movie_name=movie_info.get('Movie_name'),
                                                  Movie_time=movie_info.get('Movie_time'),
                                                  Movie_img=movie_info.get('Movie_img'),
                                                  Movie_price=movie_info.get('Movie_price'),
                                                  Movie_abstract=movie_info.get('Movie_abstract'),
                                                  Movie_hotplay=movie_info.get('Movie_hotplay'),
                                                  )
                    # 添加电影标签
                    for types in movie_info.get('Movie_type'):
                        movie.m_movietype.add(Movie_type.objects.filter(type_name=types)[0].type_id)

                data = {
                    'errno': Code.OK
                }
                return to_json_data(data=data)
            except:
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        elif request_info.get('request_type') == 'comment':
            comment_info = json.loads(request.body.decode())
            target = movies.objects.filter(Movie_id=comment_info.get('Movie_id'))
            if target.exists():
                target = target[0]
                if not Comment.objects.all().exists():
                    id = 1
                else:
                    id = int(Comment.objects.all().aggregate(Max('Comment_id'))['Comment_id__max'])
                    # 分配一个id
                comments = Comment.objects.create(Comment_id=id,
                                                  Comment_content=comment_info.get('Comment_content'),
                                                  Comment_time=datetime.now(),
                                                  Comment_author=User.objects.get(id=comment_info.get('author')),
                                                  Comment_movie=target,
                                                  Comment_likes=0)
                if comment_info.get('son'):
                    comments.parent = Comment.objects.get(Comment_id=comment_info.get('son'))

            else:
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
        else:
            return to_json_data(errno=Code.REQUEST, errmsg=error_map[Code.REQUEST])

    # like评论点赞， info电影信息更改
    def put(self, request):
        request_info = json.loads(request.body.decode())
        if request_info.get('request_type') == 'like':
            comment_info = json.loads(request.body.decode())
            comment = Comment.objects.filter(Comment_id=comment_info.get('Comment_id'))
            comment.update(Comment_likes=comment[0].Comment_likes + 1)
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        elif request_info.get('request_type') == 'info':
            new_info = json.loads(request.body.decode())
            movie = movies.objects.filter(Movie_id=new_info.get('Movie_id'))
            if new_info.get('abstract_change'):
                movie.update(abstract=new_info.get('abstract'))
            if new_info.get('hotPlay_change'):
                movie.update(hotPlay=new_info.get('hotPlay'))
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)


#
class MovieDetail(View):

    def get(self, request, movie_id):
        movie = movies.objects.get(Movie_id=movie_id)
        movie_types = Movie_type.objects.filter(movie__Movie_id=movie_id)
        types = [i.type_name for i in movie_types]
        data = {
            'single_movie': movie,
            'movie_type': ",".join(types),
            'comments': Comment.objects.filter(Comment_movie=movie),
        }
        return render(request, "index/movieDetail.html", data)


#
class Rank(View):

    def get(self, request):
        return render(request, "index/rank.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })

    # 刷新积分数据
    def put(self):
        tics = tickets.objects.filter(state=1)
        for changes in tics:
            user = User.objects.filter(id=changes.Ticket_user)
            user.update(Rank=user[0].Rank + changes.price)
        tics.update(state=2)
        return json.dumps({
            "errno": '1'
        })


#
class Ticket(View):

    def get(self, request, movie_id):
        sessions = Times.objects.filter(T_movie=movies.objects.get(Movie_id=movie_id).id)
        movie = movies.objects.get(Movie_id=movie_id)
        data = {
            'sessions': sessions,
            'movie': movie
        }
        return render(request, "index/ticket.html", data)

    @csrf_exempt
    def post(self, request, movie_id):
        try:
            request_info = json.loads(request.body.decode())
        except:
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
            # return
        if request_info.get('request_type') == 'buy':
            # ticinfo = json.loads(request.body.decode())
            # time = datetime.now()
            # time_str = time.strftime('%Y%m%d%H%M')[2:]
            # ticket_id = int(time_str + "%04d" % ticinfo.get('Seat_id') + "%02d" % ticinfo.get('Studio_id'))
            # rate_discount = discount(User.objects.get(id=ticinfo.get("user_id")).Integral)
            # session = Times.objects.get(Times_id=ticinfo.get('session_id'))
            # movie_price = movies.objects.get(Movie_id=session.T_movie).Movie_price
            # price_discount = rate_discount * movie_price

            try:
                # if ticinfo.is_valid():
                # tickets.objects.create(Ticket_id=ticket_id,
                #                            Ticket_seat=ticinfo.get('Seat_id'),
                #                            Ticket_session=ticinfo.get('Studio_id'),
                #                            price=price_discount,
                #                            Ticket_user=ticinfo.get("user_id"),
                #                            state=1,
                #                            )
                data = {
                    'errno': Code.OK
                }
                return to_json_data(data=data)
            except:
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        elif request_info.get('request_type') == 'refund':
            ticinfo = json.loads(request.body.decode())
            target = tickets.objects.filter(Ticket_id=ticinfo.get('id'))
            if not target.exists():
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
            session = Times.objects.filter(Times_id=target[0].Ticket_session)
            if not session.exists():
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.NODATA])
            if session[0].session_time < datetime.now():  # 超过了退款时间
                return to_json_data(errno=Code.OUTTIME, errmsg=error_map[Code.OUTTIME])
            # 审查完毕，可以退票程序
            target.update(state=3)
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        elif request_info.get('request_type') == 'occupy':
            request_info = json.loads(request.body.decode())
            session_id = int(request_info.get('screening'))
            # 获得当前场次的占用信息
            occupied = tickets.objects.filter(Ticket_session=session_id, state=1).values()
            seat_list = Seat.objects.filter(Seat_id__in=[i['Ticket_seat_id'] for i in occupied]).values()
            seats = [{'seat_occupied': i['Seat_name']} for i in seat_list]
            return to_json_data(data={'seat_dict': seats}, errno=Code.OK)
        else:
            return to_json_data(errno=Code.REQUEST, errmsg=error_map[Code.REQUEST])

class Session(View):

    # 添加场次
    def post(self, request):
        request_info = json.loads(request.body.decode())
        request_type = request_info.get('type')
        # add:添加场次，occupy:查询演播厅占用情况
        if request_type == 'add':
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
        elif request_type == 'occupy':
            studio_info = json.loads(request.body.decode())
            occupies = Times.objects.filter(T_studio=studio_info.get('studio_id'), session_time__gt=datetime.now())
            return to_json_data(data=occupies)
        else:
            return to_json_data(errno=Code.REQUEST, errmsg=error_map[Code.REQUEST])


class UserCenter(View):
    def post(self, request):
        user = User.objects.filter(id=request.get('user_id'))
        if not user.exists():
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
        return to_json_data(data=user[0])

    # name:更改用户名，password:更改密码
    def put(self, request):
        request_info = json.loads(request.body.decode())
        request_type = request_info.get('type')
        if request_type == 'name':
            user = User.objects.filter(id=request.get('user_id'))
            if not user.exists():
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
            user.update(name=request_info.get('name'))
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        elif request_type == 'password':
            user = User.objects.filter(id=request.get('user_id'))
            if not user.exists():
                return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])
            m = hashlib.md5()
            m.update(request_info.get('password').encode())
            new_password = m.hexdigest()
            user.update(password=new_password)
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        else:
            return to_json_data(errno=Code.REQUEST, errmsg=error_map[Code.REQUEST])


class AdminCenter(View):
    def get(self, request):
        request_info = json.loads(request.body.decode())
        user = User.objects.get(id=request_info.get('user_id'))
        if request_info.get('type') == 'movie':
            if user.is_superuser | user.buyManager:
                return render(request, "index/movie_add.html")
            else:
                return to_json_data(errno=Code.PERMIT, errmsg=error_map[Code.PERMIT])
        elif request_info.get('type') == 'session':
            if user.is_superuser | user.buyManager:
                return render(request, "index/session_add.html")
            else:
                return to_json_data(errno=Code.PERMIT, errmsg=error_map[Code.PERMIT])
        elif request_info.get('type') == 'box':  # 票房收入
            if user.is_superuser:
                # 存相应电影的id
                movie_info = [[i['Movie_id'], i['Movie_name']] for i in movies.objects.all().values()]
                # 票房数据
                box = [sum([j['price'] for j in
                            tickets.objects.filter(Ticket_session__T_movie_id=movie_info[i][0],
                                                   state__in=[1, 3])])
                       for i in
                       range(len(movie_info))]
                # 统计票房
                data = {
                    'box': box,
                    'movie_info': movie_info,
                }
                return render(request, "index/box_list.html", data)
            else:
                return to_json_data(errno=Code.PERMIT, errmsg=error_map[Code.PERMIT])
        elif request_info.get('type') == 'admin_add':  # 添加管理员
            if user.is_superuser:
                return render(request, "index/admin_add.html")
            else:
                return to_json_data(errno=Code.PERMIT, errmsg=error_map[Code.PERMIT])

    # 添加管理员
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
                                                )
                login(request, user)
            data = {
                'errno': Code.OK
            }
            return to_json_data(data=data)
        except:
            return to_json_data(errno=Code.NODATA, errmsg=error_map[Code.PICERROR])


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
class Search(View):

    def get(self, request):
        return render(request, "index/search.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })

class Who(View):

    def get(self, request):
        return render(request, "index/who.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })


class TicketMedium(View):

    def get(self, request):
        return render(request, "index/ticketMedium.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })