from django.db import models

# Create your models here.
class parent_categor(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = 'parent_catagory'