from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from django import forms

class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = News
        fields = '__all__'





# для отред. вида таблицы на админке
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

    list_display = ('id','title','category','created_at','update_at','is_published') # 'get_photo' добавить изображение в таблицу
    list_display_links = ('id', 'title') # для перехода на публ. при наж. в админке
    search_fields = ('title', 'content') # для поиска статьи по загаловку и тексту
    list_editable = ('is_published',) # для редактирование этого поля
    list_filter = ('is_published','category')  #для фильтрирование 
    fields = ('title','category','content','photo', 'get_photo','is_published','views','created_at','update_at') #пок. всех полей в самом редактируемой новости
    readonly_fields = ('get_photo','views','created_at','update_at') # эти пункты недьзя редоктировать
    save_on_top = True #Для перемещение кнопок сохранение на верх 

    # Для вывода изобр. в админке как html код 
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width = '55' >")
        else:
            return '-'
    get_photo.short_description = 'Изображение'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id', 'title') 
    search_fields = ('title',) 


admin.site.register(News, NewsAdmin)
admin.site.register(Category,CategoryAdmin)

# h1
admin.site.site_title = 'Управление Новостями'
admin.site.site_header = 'Управление Новостями'