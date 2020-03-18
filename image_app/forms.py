from django import forms
import time

from .models import PostModel,CategoryModel

class PostForm(forms.ModelForm):
    category=forms.ModelChoiceField(
        queryset=CategoryModel.objects.filter(status=CategoryModel.STATUS_NORMAL),
        empty_label='请选择班级',
        label='班级',
    )

    name=forms.CharField(
        label='姓名',
    )

    image=forms.ImageField(
        label='图片',
        # widget=forms.FileInput(attrs={'multiple':True}) # 上传多张图片
    )

    content=forms.CharField(
        label='内容',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder':'  选填',
            }
        )
    )

    def clean_image(self):
        cleaned_image=self.cleaned_data['image']
        image_name=time.strftime('%Y%m%d%H%M%S')
        image_type=cleaned_image.name.split('.')[-1]
        cleaned_image.name=image_name+'.'+image_type

        return cleaned_image

    class Meta:
        model=PostModel
        fields=('category','name','image','content')