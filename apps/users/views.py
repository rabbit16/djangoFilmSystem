import json

from django.contrib.auth import login
from django.shortcuts import render

# Create your views here.
from django.views import View

# from index.models import User
from users.models import User
from utils.res_code import to_json_data, Code, error_map
from verifications.forms import RegisterForm


class index(View):

    def get(self, request):
        return render(request, "index/index.html")

    def post(self, request):
        pass

class Login(View):

    def get(self, request):
        return render(request, "index/login.html")

    def post(self, request):
        return json.dumps({
            "errno": '1'
        })
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