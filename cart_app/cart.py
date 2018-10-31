from django.core.serializers import json

from cart_app.models import TBook


class CartItem:
    def __init__(self,book,amount,dprice):
        self.book=book
        self.amount=amount
        self.dprice=dprice


class Cart:
    def __init__(self):
        self.cartItems=[]
        self.total_price=0
        self.save_price=0

    # 计算总价
    def sum(self):
        # print(22222222)
        self.total_price=0
        self.save_price=0
        # print(3333333333)
        for i in self.cartItems:
            # print(4444444444,i.amount,type(i.amount))
            # print("`````````",i.book.book_dprice,type(i.book.book_dprice))
            # print("`````````",i.book.book_price,type(i.book.book_price))
            i.amount=int(i.amount)
            i.book.book_dprice=int(i.book.book_dprice)
            self.total_price+=i.book.book_dprice*i.amount
            # print(5555555555,i.amount,type(i.amount))
            self.save_price+=(i.book.book_price-i.book.book_dprice)*i.amount
            # print("省的钱",self.save_price,"共花了",self.total_price)
            # print(6666666666,self.save_price)
        return (self.save_price,self.save_price)

    # 添加购物车
    def add(self,book_id ):
        print("book_id",book_id,type(book_id))
        dprice = TBook.objects.get(pk=book_id).book_dprice
        # print("dprice时",dprice)
        for i in self.cartItems:
            # print(i,"00000")
            if "%s"%i.book.book_id == "%s"%book_id:
                # print("i.book isss",i.book)
                i.amount+=1
                # print("折扣价格是",i.dprice)
                i.dprice+=dprice
                self.sum()
                return i.amount
        book=TBook.objects.get(pk=book_id)

        print(book,"11",dprice,"@@@@@@")
        self.cartItems.append(CartItem(book,1,dprice))

        # print(self.cartItems,CartItem(book,1,dprice),book,dprice,"此时cart时")
        self.sum()


    def modify(self,amount,book_id):
        for i in self.cartItems:
            if  str(i.book.book_id) == str(book_id):
                i.amount=amount
                print('cart2的数量',amount)
            self.sum()


    def book_del(self,book_id):
        for i in  self.cartItems:
            # print("!!!!!!!!!!!!",i,book_id)
            # print(i.book.book_id,type(i.book.book_id),book_id,type(book_id))
            if int(i.book.book_id) == int(book_id):
                # print(i,"()()()()()()()")
                self.cartItems.remove(i)
                # print(self.cartItems,"^^^^^^^^^")
        self.sum()

