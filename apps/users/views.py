import json

from django.contrib.auth import login
from django.shortcuts import render,HttpResponse

# Create your views here.
from django.views import View

# from index.models import User
from users.models import User, Movie as movies
from utils.res_code import to_json_data, Code, error_map
from verifications.forms import RegisterForm
from django.contrib.auth import authenticate, login


class index(View):

    def get(self, request):
        return render(request, "index/index.html")

    def post(self, request):
        pass

class IndexTest(View):

    def get(self, request):
        return render(request, "index/indexTest.html", context={
            "hotfilmlefts": movies.objects.filter(hotPlay=True)[:3],
            "hotfilmcenters": movies.objects.filter(hotPlay=True)[3:6],
            "hotfilmrights": movies.objects.filter(hotPlay=True)[6:9],
        })

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

#
class Ticket(View):

    def get(self, request):
        return render(request, "index/ticket.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })