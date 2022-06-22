import email
from django import forms
import re
from django.core.exceptions import ValidationError


# send mail ---->

class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))


# register ------------------->
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegisterForms(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',help_text='help_text', widget=forms.TextInput(attrs={'class':'form-control','autofocus':None,'autocomplete':'off'})) # 'autocomplete':'off' - убрать подсказки
    first_name = forms.CharField(label='Ваше Имя', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Ваше Фамилия', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль',help_text='Пароль должен содержать Буквы и цифры', widget= forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget= forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2') 


# login --------------->
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}))
    password = forms.CharField(label='Пароль', widget= forms.PasswordInput(attrs={'class':'form-control','autocomplete':'off'}))



# Форма связанная с моделью --------->
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
    # дост. все переменные с класса News исп. не реком.
        # fields = '__all__'
        fields = ['title', 'content', 'is_published','category' ]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={
                'class':'form-control',
                 'rows': 5}
                ),
            'category': forms.Select(attrs={'class':'form-control'})
        }
        # регул валидатор для title
    def clean_title(self):
        title = self.cleaned_data['title']

        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
   
# форма не связанная с моделью ------>
'''
from .models import Category

class NewsForm(forms.Form):
    title = forms.CharField(max_length=200,label='Название ', widget=forms.TextInput(attrs={'class':'form-control'}))#widget-указ. класс для верстки в html
    content = forms.CharField(label='Текст ',widget=forms.Textarea(attrs={
        'class':'form-control', 
        'rows':5
        }))
    photo = forms.ImageField(label='Изображение ',required=False)
    is_published = forms.BooleanField(initial=True,label='Oпублекованно ',widget=forms.CheckboxInput(attrs={'class':'form-check-label'}) )
    category =  forms.ModelChoiceField(empty_label='Выберете категорию ',label='Категория ',queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
'''
