import decimal
from macpath import split
import uuid as uuid
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
# 转发购物车页面
from cart_app.cart import Cart
from cart_app.models import TBook, User, TAddress


# 转发模板
def cart_page(request):
    cart = request.session.get('cart')
    print('cart时',cart)
    if cart:
        return render(request, 'cart/car.html', {"cart": cart.cartItems})
    else:
        return render(request,'cart/car.html')

# 把书添加进购物车
def addBookToCart(request):
    book_id = request.GET.get("book_id")
    # cart=Cart()
    # request.session['cart']=cart
    cart=request.session.get('cart')
    print("此时的session内的cart是",cart)
    if cart:
        print("如果cart已经存在于",cart)
        cart.add(book_id)
        request.session["cart"] = cart
    else:
        print("若不在",cart)
        cart = Cart()
        cart = cart.add(book_id)
        request.session["cart"] = cart


    # request.session["cart"]=cart
        print('添加后')
        print(cart)
    return redirect('cart:page')

#细节页添加
def book_detail_add(request):
    pass


# 加法逻辑
def cart_calculate(request):
    print(666)
    book_id=int(request.POST.get("book_id"))

    cart = request.session.get('cart') # 读
    cart.add(book_id) # 加入
    # print(7777)
    request.session['cart']=cart #存
    cart=request.session.get('cart') # 再读
    for i in  cart.cartItems: # 遍历出里面所有的商品
        # print(i,"$$$$$$")
        # print(i.book.book_id,type(i.book),"%%%%%%")
        # print(i.amount,type(i.amount),"*******")
        if i.book.book_id == book_id: # 如果有商品ID 与 要操作的商品ID相同
            # book=TBook.objects.get(pk=book_id)
            # print(i.amount,i.dprice,cart.total_price,cart.save_price,"$$$$$$$")
            dprice=i.amount*i.book.book_dprice
            # print("每本书共花",dprice)
            request.session['cart'] = cart
            return JsonResponse({'cart_plus':i.amount,'dprice':dprice,
                                 'total_price':cart.total_price,'save_price':cart.save_price}) # 数据传回模板


# 减法逻辑
def cart_divide(request):
    book_id=int(request.POST.get("book_id")) # 接收到模板传来的数据

    cart = request.session.get('cart')  # 读
    for i in  cart.cartItems: # 遍历购物车中的商品
        if i.book.book_id == book_id: # 找到对应的那一个
            if i.amount>1: # 如果他的数量大于
                i.amount-=1 # 那就减一
                print("商品数量是",i.amount)

                request.session['cart']=cart # 写入购物车
                cart=request.session['cart']
                cart.sum()

                dprice=i.amount*i.book.book_dprice
                print("总共",cart.total_price,"省了",cart.save_price)

                return JsonResponse({'cart_divide':i.amount,'dprice':dprice,
                                     'total_price':cart.total_price,'save_price':cart.save_price})
            else:
                return JsonResponse(0)


def cart_modify(request):
    book_id = int(request.POST.get("book_id"))  # 接收到模板传来的数据
    amount =int(request.POST.get("amount"))
    print(book_id,amount)
    cart = request.session.get('cart')  # 读
    print("都到了",cart)
    for i in cart.cartItems:  # 遍历购物车中的商品
        print("遍历购物车",i)
        print("ID是几 类型",i.book.book_id,type(i.book.book_id),book_id,type(book_id))
        if i.book.book_id == book_id:  # 找到对应的那一个
            print("书的ID",book_id)
            i.amount=amount
            print("赋值成功",i.amount)

            request.session['cart'] = cart  # 写入购物车
            cart = request.session['cart']
            cart.sum()

            dprice = i.amount * i.book.book_dprice
            print("总共", cart.total_price, "省了", cart.save_price)

            return JsonResponse({'cart_divide': i.amount, 'dprice': dprice,
                                     'total_price': cart.total_price, 'save_price': cart.save_price})




def cart_del(request):
    book_id=request.POST.get('book_id')
    print('商品管理系统的删除',book_id)
    cart = request.session['cart']
    print(cart,book_id,"&*((&*&(*&")
    cart.book_del(book_id)
    request.session['cart']=cart
    print('删除成功',cart)
    return HttpResponse(1)


# 转发地址页面
def indent(request):
    username = request.session.get('username')

    if username:
        user_id = User.objects.get(user_name=username).user_id  # 通过用户名那个拿到其对应的用户ID
        print(user_id, username, "username和id")
        address_qs = TAddress.objects.filter(user_id=user_id)  # 通过用户ID查到用户名下的所有地址
        print(address_qs, type(address_qs), "address_qs的参数")
        cart2=request.session.get("cart2")
        print("cart2实际",cart2,len(cart2.cartItems))
        for i in cart2.cartItems:
            print('数量是',i.amount)
        return render(request,'cart/indent.html',{'address':address_qs,'book':cart2.cartItems})

    else:
        return redirect('mpa:login_logic')

def indent_data(request):

    cart2 = Cart()
    request.session['cart2'] = cart2
    book_id = request.GET.get('book_id')  # 选中的书的ID
    print("循环前的ID", book_id)
    # cart=request.session.get('cart')
    # flag=request.GET.get('flag')
    # request.session['flag']=flag
    # print("flaggggg",flag,type(flag))
    n = 0
    for i in book_id.split(","):
        print("加入cart2的书ID", i,type(i))
        n += 1
        if n%2:
            a=i
            cart2.add(i)
            # cart.book_del(i)
            print("id是",a)
            # request.session['cart2']=cart2
            continue
        else:
            b=i
            print("数量",b)
        cart2.modify(b,a)

        request.session['cart2']=cart2
    for j in cart2.cartItems:
        print(j.amount,'数量是是是')
    print(a,b,cart2.cartItems,len(cart2.cartItems),"cart2的参数")
    # request.session['cart2'] = cart2
    # cart2=request.session.get('cart2')
    # print("cart2的数据",cart2,len(cart2.cartItems))
    return JsonResponse(1,safe=False)


def indent_logic(request):
    user_id=request.POST.get('id')
    # print(user_id)
    address = TAddress.objects.get(pk=user_id)

    return JsonResponse({'name': address.name, 'detail_address': address.detail_address,
                    'zipcode':address.zipcode,'telphone':address.telphone,
                    'mobile_phone':address.addr_mobile})

def indent_save(request):
    name=request.POST.get('name')
    detail_address=request.POST.get('detail_address')
    zipcode=request.POST.get('zipcode')
    telphone=request.POST.get('telphone')
    mobile_phone=request.POST.get('mobile_phone')
    username=request.session.get('username')

    user_id = User.objects.get(user_name=username).user_id

    cart=Cart()
    request.session['cart']=cart
    print(name,detail_address,zipcode,telphone,mobile_phone,user_id) # 验证已拿到数据
    TAddress(name=name,detail_address=detail_address,zipcode=zipcode,
             telphone=telphone,addr_mobile=mobile_phone,user_id=user_id).save()
    return redirect('cart:ok')


def indent_OK(request):
    uuid1=uuid.uuid4()
    uuid2= str(uuid1).replace('-','')
    uuid3=uuid2+"zkf"
    return render(request,'cart/indent ok.html',{'uuid':uuid3})


