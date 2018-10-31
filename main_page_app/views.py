import math
import os
import random
import string
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.

# 转发注册模板
# def register_page(request):
#     return render(request,'xxx.html')
#
# # 注册逻辑
# def  register_logic(request):
#     email = request.POST.get('email')
#     nickname = request.POST.get('nickname')
#     password = request.POST.get('password')
#     verification_password = request.POST.get('verification_password')
#
#     if password == verification_password:
#         # 异步显示 密码可用
#         pass
#
#     verif_code = request.POST.get('verif_code')
#     return redirect('/register/page/')
#     # 把 邮箱 昵称 密码 存进数据库
from main_page_app.models import Cata, DCategory, TBook, User


# 1是主页,2是购物车

# 主页
from manage_app.models import parent_categor


def index(request):
    category1 = Cata.objects.all()
    category2 = DCategory.objects.all()
    book = TBook.objects.all().order_by('shelves_date')[:8]
    bk_ok = TBook.objects.all().order_by('editor_recommendation')[:8]
    bk_rank = TBook.objects.all().order_by('sales')[:8]

    flag=request.GET.get('flag')

    username = request.session.get("username")
    print(username)
    if username and flag=='1':
        return render(request,'main_page/index.html',{'category1':category1,'category2':category2,'book':book,'bk_ok':bk_ok,'bk_rank':bk_rank,'username':username})
    elif username and flag=='2':
        return redirect('cart:page')
    else:
        return render(request, 'main_page/index.html',
                      {'category1': category1, 'category2': category2, 'book': book, 'bk_ok': bk_ok,
                       'bk_rank': bk_rank})



# 分类查询
def book_list(request):
    pid = request.GET.get("cate1")
    cid = request.GET.get("cate2")
    print("一级目录",pid,type(pid))
    print("二级目录",cid,type(cid))

    cate_name1=parent_categor.objects.get(pk=pid).name

    print('一级目录名称',cate_name1)

    page_num =request.GET.get('num')

    if not page_num:
        page_num = 1
    category1 = Cata.objects.all()
    category2 = DCategory.objects.all()
    cate3= Cata.objects.get(pk=pid)

    if cid:
        book = TBook.objects.filter(book_category=cid)
        cate_name2 = DCategory.objects.get(pk=cid).category_name
        length=len(book)
        page =Paginator(object_list=book,per_page=3).page(page_num)
        num_pages = page.paginator.num_pages
        return render(request, 'main_page/booklist.html', {'category1': category1, 'category2': category2,
                                                           'cate1': pid, 'cate2': cid,
                                                           'cate_name1': cate_name1, 'cate_name2': cate_name2,
                                                           'book': page, 'num_pages': num_pages, 'length': length})
    else:
        cate = cate3.dcategory_set.all()
        # print(cate)
        list1= []
        for i in cate:
            list1.append(i.category_id)
        book = TBook.objects.filter(book_category__in=list1)
        length=len(book)
        # print(book)
        # if page_num:
        page = Paginator(object_list=book,per_page=3).page(page_num)
        num_pages = page.paginator.num_pages

        return render(request, 'main_page/booklist.html',{'category1':category1,'category2':category2,
                                                      'cate1':pid,'cate2':cid,'cate_name1':cate_name1,
                                                      'book': page,'num_pages':num_pages,'length':length})






def login(request):
    return render(request,'login/login.html')

def login_logic(request):
    # 接受 username 和 password
    username = request.POST.get("username")
    password = request.POST.get("password")
    # flag=request.POST.get("flag")
    flag=request.session.get('flag')
    print(username,password,"登录页面收到的flag是",flag)
    if username:
        hash_code=hashlib.md5()
        salt=User.objects.get(user_name=username).salt
        print(salt,'盐')
        password = str(password) + salt
        hash_code.update(password.encode())
        print(hash_code.hexdigest(),'十六进制')

        user = User.objects.filter(user_name=username, hash_code=hash_code.hexdigest())
        print(user,"********")
        if user and flag==1:
            request.session['username']=username
            # username=request.session.get('username')
            return JsonResponse({'status':1,'flag':flag})
        elif user and flag==None:
            request.session['username'] = username
            return JsonResponse({'status':2})
        else:
            return JsonResponse({'status':0,'flag':flag})
    else:
        return redirect('mpa:login')


def login_out(request):
    # request.session.clear()

    flag = request.GET.get('flag')
    del request.session['username']


    if flag==1:
        return redirect('mpa:page')
    elif flag==2:
        return redirect('cart:page')
    else:
        return redirect('mpa:page')

# 转发注册页面
def register(request):
    return render(request,'register/register.html')

# 用户名异步验证
def ajax_username(request):
    username = request.POST.get("username")
    print(username)
    if User.objects.filter(user_name=username):
        print('有重复')
        return HttpResponse('0')
    else:
        print('无重复')
        return HttpResponse('1')

# 密码异步验证
def ajax_password(request):
    password = request.POST.get('password')
    repassword = request.POST.get('repassword')


    print(password,repassword)
    if password != repassword:
        print('有毛病')
        return HttpResponse('0')
    else:
        print('没毛病')
        return HttpResponse('1')


from static.captcha.image import ImageCaptcha
# 生成验证码
def getCaptcha(request):
    image = ImageCaptcha(fonts=[os.path.abspath('code_data/fonts/simkai.ttf')])
    code_list = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 5)
    code = ''.join(code_list)
    request.session['code'] = code
    print("code is:",code)
    # 生成一个验证码图片
    data = image.generate(code)
    return HttpResponse(data,'image/png')

# 核对验证码函数
def checkCaptcha(request):

    realcode = request.session.get('code') # 随机出的验证码
    inputcode = request.POST.get('inputcode') # 输入的验证码
    print(realcode,"qqqqqq")
    print(inputcode,"eeeee")
    if realcode.lower() == inputcode.lower():
        return HttpResponse('0')
    else:
        return HttpResponse('1')

def register_ok(request):
    username =request.session.get('username')
    # request.session['username']=username
    print(username)

    return render(request,'register/register ok.html')

import hashlib
def register_logic(request):
    # 收参
    try:

        username = request.POST.get("username")
        repassword = request.POST.get('repassword')
    # file = request.FILES.get('head_pic')
    # 入库
        print(username,repassword,"66666666")
        # 生成哈希数
        l = '1234567890qweiosdfghjklzxcvbnm,\./!@#$%^&*()'
        salt = ''.join(random.sample(l, 6))
        hash_code=hashlib.md5()
        password=str(repassword)+salt
        hash_code.update(password.encode())
        print(salt,hash_code.hexdigest(),'随机数与其哈希')

        with transaction.atomic():
            User(user_name=username, user_password=repassword,salt=salt,hash_code=hash_code.hexdigest()).save()
            request.session['username']=username
            print('注册成功,准备转到登录成功界面')
            return HttpResponse('1')  # 衔接登陆功能
    except Exception:
        traceback.print_exc()
        # 注册出错，转回注册页面
        return redirect("/mpa/register/")

# 登出
# def login_out(request):
#     return redirect("/mpa/page/")

# 书籍详情页
def book_detail(request):
    book_id=request.GET.get("book_id")
    book=TBook.objects.filter(pk=book_id)
    print(book[0],'000000')
    return render(request,'main_page/Book details.html',{"book":book[0]})


def order_logic(request):
    pass