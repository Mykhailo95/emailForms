from email.policy import default
from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Наиминование')
    content = models.TextField(blank=True,verbose_name='Кортерт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    update_at = models.DateTimeField(auto_now=True,verbose_name='Обнавлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',blank = True , verbose_name='Фото')
    is_published = models.BooleanField(default=True,verbose_name='Опубликовано')

    category =  models.ForeignKey('Category', on_delete=models.PROTECT, null=True,verbose_name='Категория')#для связки категорий между собой ** & models.PROTECT обесп. защиту от удалений 

    # для работы с Агригатными функциямиб показ сколько в категории существ. статьей from django.db.models import * 
    views = models.IntegerField(default=0) 

    # for Button Read More..
    def  get_absolute_url(self):
        return reverse('view_news', kwargs={'news_id': self.pk})
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at'] #для сорт. загаловков в админ и на стр. 


'''
Для прикрепления каждой темы к категории к которому она относится
например категория Айти и к ней прикрепляется все что с ней 
связано
'''
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категории')#индексирует это поля для быстрого его поиска

    # фун.для созд. ссылки категории пер. по ссылки наим. get_absolute_url - имя обяз.
    def  get_absolute_url(self):
        # reverse(viewname-назв.маршута, urlconf=None, args=None, kwargs=необх. парам. для постр. маршута, current_app=None)
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']