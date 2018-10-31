from django.contrib import admin
from django.urls import path, include

from cart_app import views

urlpatterns = [
    path('page/',views.cart_page,name='page'),
    path('indent/',views.indent,name='indent'),
    path('indent/logic/',views.indent_logic,name='indent_logic'),
    path('indent/save/',views.indent_save,name='indent_save'),
    path('indent/ok/',views.indent_OK,name='ok'),
    path('indent/data/',views.indent_data,name='data'),

    path('book_detail_add/',views.book_detail_add,name='book_detail_add'),


    path('addbktocart/',views.addBookToCart,name='addbktocart'),
    path('calculate/',views.cart_calculate,name='calculate'),
    path('divide/',views.cart_divide,name='divide'),
    path('modify/',views.cart_modify,name='modify'),
    path('del/',views.cart_del,name='del'),
    # path('del_many/',views.cart_del_many,name='del_many'),
]