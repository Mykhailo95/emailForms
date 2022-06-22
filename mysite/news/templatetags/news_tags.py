# для создание тегов урок 20
# https://docs.djangoproject.com/en/4.0/howto/custom-template-tags/
from django import template
from news.models import Category
from django.db.models import Count, F 

# для работы этого файда нужно ввести
register = template.Library()

@register.simple_tag(name='any_name_category')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('news/list_categories.html') #указ. путь к коду
def show_categories():
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)# категория еоторая меньше 1 не будет вывод на экран
    categories = Category.objects.annotate(cnt=Count('news',F('news__is_published'))).filter(cnt__gt=0)#F('news__is_published') для показа только те которые в админке показыв
    return {'categories':categories}


'''
# для передачи оргументов в html код
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='Hello', arg2='world'):
    categories = Category.objects.all()
    return {"categories": categories, "arg1": arg1, "arg2": arg2}
'''