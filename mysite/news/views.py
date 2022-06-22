from email import message
from django.shortcuts import render

# get Http404 error
from django.shortcuts import get_object_or_404, redirect


from .forms import NewsForm
from .models import News, Category

# mixin
from .utils import MyMixin

from django.views.generic import ListView, DetailView, CreateView
# если не авторезирован заблок путь к добавить новость МИКСИН
from django.contrib.auth.mixins import LoginRequiredMixin
# paginator
from django.core.paginator import Paginator




# этот класс полность заменяет функцию index
class HomeNews(MyMixin, ListView):
    model = News # == news = News.objects.all()
    template_name= 'news/index.html' #по умол. путь до файла_list/html, в конткнт файде меняем {% for item in (news) на object_list %}
    context_object_name = 'news' #для работы с {% for item in news а не (object_list) %}
    # extra_context = {'title': 'Главная'}
    mixin_prop = 'hello world'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная')
        context['mixin_prop'] = self.get_prop()
        return context

    # для отображение новостей у которых стоит галочка на опубликовать
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category') #чтобы при загрузки главной страницы небыло много SQL запросов


# search categpry list
class NewsByCategory(MyMixin,ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False #for error 404 если нет такого в id выводить вместо 500  
    paginate_by = 2 # show 2 news at page

    def get_context_data(self,*,objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context    

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

# for button Read more
class ViewNews(DetailView):
    model = News
    pk_url_kwarg =  'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'

# Форма связанная с моделью
class CreateNews(LoginRequiredMixin,CreateView):
    form_class = NewsForm
    template_name = 'news/add_forms.html'
    login_url = '/admin/' # при вводе ссылки доб. нов. будет выдав форму для фвториз.
    # raise_exception = True #выб. ошибку 403




from .forms import UserRegisterForms, UserLoginForm, ContactForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForms(request.POST)

        if form.is_valid():
            # для авторизации сразу после регестр.
            user = form.save()
            login(request, user)

            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Oшибка регистрации')
    else:
        form = UserRegisterForms()

    return render(request, 'news/register.html', {'form': form})

# login ------------------>
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('login')


# send email ------------------->
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

def form_email (request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], EMAIL_HOST_USER, ['bilak.mihail@mail.ru','bilakmisha34@gmail.com'],fail_silently=True)
            
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('home')
            else:
                print(mail)
                messages.error(request, 'Ошибка отправки')

        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        form = ContactForm()

    return render(request, 'news/email.html',{"form": form})


