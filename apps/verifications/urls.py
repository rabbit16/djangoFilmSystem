from django.urls import path, re_path
from verifications import views
app_name = 'verifications'
urlpatterns = [
    path('pics/<uuid:img_codes>/', views.ImageCode.as_view(), name='register'),
    path('username/<username>/', views.UserNameCheck.as_view(), name='username_check'),
    path('mobiles/<mobile>/', views.MobileCheck.as_view(), name='mobile')
    # path("login/", views.Login.as_view(), name="login")
]