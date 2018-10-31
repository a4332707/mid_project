from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
# 转发模板
from cart_app.models import TBook, DCategory, TAddress, User


def index(request):
    return render(request,'manage_sys/index.html')


def add(request):
    return render(request,'manage_sys/main/add.html')

# 添加逻辑
def add_logic(request):
    name=request.POST.get('name')
    author=request.POST.get('author')
    publish_house=request.POST.get('publish_house')
    publish_date=request.POST.get('publish_date')
    variety=request.POST.get('variety')

    # 存入数据库 外键存了DCategory对象
    TBook(book_name=name,book_category=DCategory.objects.get(category_name=variety),
          book_author=author,
          publish_time=publish_date,book_publish=publish_house).save()
    print(name,author,publish_date,publish_house,variety)
    return JsonResponse(1,safe=False)

# 分页显示商品列表
def list(request):
    book = TBook.objects.all()
    category2=DCategory.objects.all()
    length=len(book)
    page_num=request.GET.get('num')


    page = Paginator(object_list=book, per_page=12).page(page_num)
    num_pages=page.paginator.num_pages

    return render(request,'manage_sys/main/list.html',{'book':page,'page_num':page_num,
                                                       'num_pages':num_pages,'length':length,
                                                       'category2':category2})


# 跳转增加商品父类别页面
def zjsp(request):
    return render(request,'manage_sys/main/zjsp.html')
# 增加父类别功能实现
def zjsp_logic(request):
    category=request.POST.get('category')
    print(category)
    parent_categor(name=category).save()
    return JsonResponse(1,safe=False)

from manage_app.models import parent_categor # 导入父类别表
# 跳转增加商品子类别页面
def zjzlb(request):
    parent_category=parent_categor.objects.all()
    # print('父类别',parent_category,len(parent_category))
    return render(request,'manage_sys/main/zjzlb.html',{"parent_category":parent_category})

#  实现增加子类别功能
def zjzlb_logic(request):
    d_category=request.POST.get('d_category')
    number=request.POST.get('number')
    variety=request.POST.get('variety')
    print(variety,type(variety),'variety  类型')
    id=parent_categor.objects.get(name=variety).id
    print("收到子目录",d_category,number)
    DCategory(category_name=d_category,book_counts=number,category_pid_id=id).save()
    print('存入数据库成功')
    return JsonResponse(1,safe=False)

# 跳转商品类别
def splb(request):
    category1=parent_categor.objects.all()
    print(category1,type(category1))
    length = len(category1)
    page_num = request.GET.get('num')

    page = Paginator(object_list=category1, per_page=5).page(page_num)
    num_pages = page.paginator.num_pages

    return render(request, 'manage_sys/main/splb.html', {'category1': page, 'page_num': page_num,
                                                         'num_pages': num_pages,
                                                        'length': length,
                                                         })

    # return render(request,'manage_sys/main/splb.html',{'category1':category1})

def splb_logic(request):
    pass


# 跳转到地址列表
def dzlist(request):
    address = TAddress.objects.all()
    print(address, type(address))
    user = User.objects.all()
    print(user,type(user))
    length = len(address)
    page_num = request.GET.get('num')

    page = Paginator(object_list=address, per_page=5).page(page_num)
    num_pages = page.paginator.num_pages

    return render(request, 'manage_sys/main/dzlist.html', {'address': page, 'page_num': page_num,
                                                         'num_pages': num_pages,'length': length,
                                                           'user':user})

    # return render(request,'manage_sys/main/dzlist.html')





def test(request):
    return render(request,'manage_sys/main/test.html')


# 管理系统 从书库删除
def db_del(request):
    book_id=request.POST.get('book_id')
    print('商品管理系统的删除',book_id)
    TBook.objects.get(pk=book_id).delete()
    print('删除成功')
    return JsonResponse(1,safe=False)

# 删除地址
def address_del(request):
    address_id=request.POST.get('address_id')
    print('商品管理系统的删除',address_id)
    TAddress.objects.get(pk=address_id).delete()
    print('删除成功')
    return JsonResponse(1,safe=False)

# 删除一级目录
def category_del(request):
    category_id=request.POST.get('address_id')
    print('商品管理系统的删除',category_id)
    parent_categor.objects.get(pk=category_id).delete()
    print('删除成功')
    return JsonResponse(1,safe=False)