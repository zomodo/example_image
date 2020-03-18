from django.contrib import admin
from django.utils.html import format_html
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
import zipstream

from image_app.models import CategoryModel,PostModel

# Register your models here.

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','status','operator']

    def operator(self,obj):
        return format_html(
            "<a href='{}/download/' title='下载班级所有图片'>下载</a>",
            obj.id
        )

    def get_urls(self):     # 重写get_urls
        from django.urls import path
        urlpatterns = [
            path('<path:object_id>/download/',self.admin_site.admin_view(self.download_classimage)),
        ]
        return urlpatterns + super(CategoryAdmin, self).get_urls()

    def download_classimage(self,request,*args,**kwargs):
        id=kwargs['object_id']
        try:
            category=CategoryModel.objects.get(pk=id)
        except CategoryModel.DoesNotExist:
            queryset=[]
        else:
            queryset=category.postmodel_set.all().select_related('category')

        if queryset:
            category_name=CategoryModel.objects.get(pk=id).name
            z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
            for data in queryset:
                file_path = str(data.image.url).strip('/')
                file_name=str(data.name)+'-'+file_path.split('/')[-1]
                z.write(file_path,file_name)

            export_name=escape_uri_path(category_name)
            response = StreamingHttpResponse(z)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; filename={}.zip'.format(export_name)
            return response
        else:
            return None

    operator.short_description='下载图片'


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['category','name','image','content','created_time']
    list_filter = ['category','name','created_time']
    actions = ['download_image']

    def download_image(self, request, queryset):

        if len(queryset)>=2:
            z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
            for data in queryset:
                file_path = str(data.image.url).strip('/')
                file_name=str(data.name)+'-'+file_path.split('/')[-1]
                z.write(file_path,file_name)

            export_name=escape_uri_path(str(len(queryset))+'images')
            response = StreamingHttpResponse(z)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; filename={}.zip'.format(export_name)
            return response

        elif len(queryset)>=1:
            for data in queryset:
                file_path = str(data.image.url).strip('/')
                file_name = str(data.name) + '-' + file_path.split('/')[-1]
                file = open(file_path, 'rb')

                export_name=escape_uri_path(file_name)
                response = FileResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename={}'.format(export_name)
                return response
        else:
            return None

    download_image.short_description = '下载图片'


admin.site.site_header='作业管理'
admin.site.site_title='作业管理'