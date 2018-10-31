from django.contrib import admin
from django.urls import path, include

from manage_app import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('add/',views.add,name='add'),
    path('add/logic/',views.add_logic,name='add_logic'),

    path('list/',views.list,name='list'),

    path('zjsp/',views.zjsp,name='zjsp'), # 增加商品类别函数
    path('zjsp/logic/',views.zjsp_logic,name='zjsp_logic'),

    path('zjzlb/',views.zjzlb,name='zjzlb'),
    path('zjzlb/logic',views.zjzlb_logic,name='zjzlb_logic'),

    path('splb/',views.splb,name='splb'),
    path('splb/logic/',views.splb_logic,name='splb_logic'),

    path('dzlist/',views.dzlist,name='dzlist'),

    # 删除部分
    path('db_del/',views.db_del,name='db_del'), # 删除书籍
    path('address_del',views.address_del,name='address_del'),
]