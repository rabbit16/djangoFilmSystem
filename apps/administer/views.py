from django.shortcuts import render
import json

# Create your views here.
from django.views import View
from users.models import Seat, Studio


class index(View):
    def get(self, request):
        return render(request, 'admin/index.html')


class filmPublish(View):
    def get(self, request):
        return render(request, 'admin/filmPublish.html')


class filmManage(View):
    def get(self, request):
        return render(request, 'admin/docs_manage.html')


class initialize(View):
    def post(self, request):
        Studio.objects.all().delete()
        Seat.objects.all().delete()
        studios = [
            [1, "萝卜厅", "小型厅", 8, 10, 1],
            [2, "牛奶厅", "小型厅", 8, 10, 1],
            [3, "觥筹厅", "小型厅", 8, 10, 1],
            [4, "繁星厅", "中型厅", 12, 14, 1],
            [5, "蓝天厅", "中型厅", 12, 14, 1],
            [6, "月亮厅", "中型厅", 12, 14, 1],
            [7, "长江亭", "imax", 12, 14, 1.4],
            [8, "黎明亭", "imax", 12, 14, 1.4],
        ]
        formats = [
            [8, 10, '小型厅', 1000],
            [12, 14, '中型厅', 2000],
            [12, 14, 'imax', 3000],
        ]
        for i in studios:
            Studio.objects.create(Studio_id=i[0],
                                  Studio_name=i[1],
                                  Studio_type=i[2],
                                  Seating=i[3] * i[4],
                                  price_weight=i[5])

        for i in formats:
            idx = 0
            for j in range(i[0]):
                for k in range(i[1]):
                    idx = idx + 1
                    Seat.objects.create(Seat_id=i[3] + idx,
                                        Seat_name="{}排{}列".format(j + 1, k + 1),
                                        )

        return json.dumps({
            "errno": '1'
        })
