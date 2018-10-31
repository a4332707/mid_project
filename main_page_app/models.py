from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Cata(models.Model):
    name = models.CharField(max_length=50,null=False)
    class Meta:
        db_table = 'parent_catagory'

class DCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=20)
    book_counts = models.IntegerField()
    category_pid = models.ForeignKey(Cata,on_delete=True,db_column='category_pid')
    class Meta:
        db_table = 'd_category'


class DOrderiterm(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    shop_bookid = models.ForeignKey('TBook', models.DO_NOTHING, db_column='shop_bookid')
    shop_ordid = models.ForeignKey('TOrder', models.DO_NOTHING, db_column='shop_ordid')
    shop_num = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'd_orderiterm'


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    telphone = models.CharField(max_length=20)
    addr_mobile = models.CharField(max_length=20)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        db_table = 't_address'


class TBook(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=128)
    book_author = models.CharField(max_length=64)
    book_publish = models.CharField(max_length=128)
    publish_time = models.DateTimeField()
    revision = models.IntegerField()
    book_isbn = models.CharField(max_length=64)
    word_count = models.CharField(max_length=64)
    page_count = models.IntegerField()
    open_type = models.CharField(max_length=20)
    book_paper = models.CharField(max_length=64)
    book_wrapper = models.CharField(max_length=64)
    book_category = models.ForeignKey(DCategory, models.DO_NOTHING, db_column='book_category')
    book_price = models.DecimalField(max_digits=10, decimal_places=2)
    book_dprice = models.DecimalField(max_digits=10, decimal_places=2)
    editor_recommendation = models.CharField(max_length=200)
    content_introduction = models.CharField(max_length=200)
    author_introduction = models.CharField(max_length=200)
    menu = models.CharField(max_length=200, )
    media_review = models.CharField(max_length=200)
    digest_image_path = models.CharField(max_length=200)
    product_image_path = models.CharField(max_length=200)
    series_name = models.CharField(max_length=200)
    printing_time = models.DateTimeField()
    impression = models.CharField(max_length=64)
    stock = models.IntegerField()
    shelves_date = models.DateTimeField()
    customer_socre = models.DecimalField(max_digits=3, decimal_places=2)
    book_status = models.IntegerField()
    sales = models.IntegerField()

    class Meta:
        db_table = 't_book'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.IntegerField()
    create_date = models.DateTimeField()
    price = models.IntegerField()
    status = models.IntegerField()
    order_uid = models.ForeignKey('User', models.DO_NOTHING, db_column='order_uid')
    order_addrid = models.ForeignKey(TAddress, models.DO_NOTHING, db_column='order_addrid')

    class Meta:
        db_table = 't_order'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=20)
    user_name = models.CharField(max_length=30)
    user_status = models.IntegerField()
    salt=models.CharField(max_length=50)
    hash_code=models.CharField(max_length=50)

    class Meta:
        db_table = 't_user'


