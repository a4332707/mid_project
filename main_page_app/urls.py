from django.contrib import admin
from django.urls import path, include

from main_page_app import views

urlpatterns = [
    path('page/', views.index,name='page'),
    path('list/', views.book_list,name='list'),
    path('detail/',views.book_detail,name='detail'),

    path('login/',views.login,name='login'),
    path('login/logic/',views.login_logic,name='login_logic'),
    path('login/out/',views.login_out,name='login_out'),

    path('register/',views.register,name='register'),
    path('register/logic/',views.register_logic,name='register_logic'),
    path('register/ok/',views.register_ok,name="register_ok"),

    path('ajax_username/',views.ajax_username,name='ajax_username'),
    path('ajax_password/',views.ajax_password,name='ajax_password'),

    path('getcaptcha/',views.getCaptcha,name='getcaptcha'),
    path('checkcaptcha',views.checkCaptcha,name='checkcaptcha'),
]