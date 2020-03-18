from django.db import models

# Create your models here.

class CategoryModel(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEMS=(
        (STATUS_NORMAL,'显示'),
        (STATUS_DELETE,'不显示'),
    )
    name=models.CharField(max_length=20,verbose_name='班级分类')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=STATUS_NORMAL,verbose_name='状态')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='班级分类'
        verbose_name_plural='班级分类'

class PostModel(models.Model):
    category=models.ForeignKey(CategoryModel,on_delete=models.DO_NOTHING,verbose_name='班级分类',max_length=20)
    name=models.CharField(max_length=10,verbose_name='姓名')
    image=models.ImageField(upload_to='images/',verbose_name='图片')
    content=models.CharField(max_length=100,null=True,verbose_name='内容')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='提交内容'
        verbose_name_plural='提交内容'
        ordering=['-created_time']