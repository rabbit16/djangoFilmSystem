from django.shortcuts import render

# Create your views here.
from django.views import View


class index(View):
    def get(self, request):
        return render(request, 'admin/index.html')


class filmPublish(View):
    def get(self, request):
        return render(request, 'admin/filmPublish.html')