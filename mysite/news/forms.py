import email
from pyexpat import model
from django import forms  #  модуль для работы с формами
from .models import Category, News
from django.core.exceptions import ValidationError
import re   #  регулярные выражения
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm): # Так мы создаём форму регистрации, если хотим настроить её внешний вид
    
    username = forms.CharField(label='Имя пользователя', widget= forms.TextInput(attrs={"class": "form-control"})) # Для отображения в бутстрапе
    password = forms.CharField(label='Пароль',widget= forms.PasswordInput(attrs={"class": "form-control"}))

class UserRegistrForm(UserCreationForm): # Так мы создаём форму регистрации, если хотим настроить её внешний вид
    
    username = forms.CharField(label='Имя пользователя', widget= forms.TextInput(attrs={"class": "form-control"})) # Для отображения в бутстрапе
    email = forms.EmailField(label='E-mail',widget= forms.EmailInput(attrs={"class": "form-control"}))   # Для отображения в бутстрапе
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class NewsForm(forms.ModelForm):
    class Meta:  #  Здесь опичываем то, как должна выглядеть наша форма
        model = News
        fields = ['title', 'content', 'is_published', 'category']  #  Здесь те поля из таблицы, которые будут в форме
        widgets = {    #   Для отображения в бутстрапе
            'title' : forms.TextInput(attrs={"class": "form-control"}),
            'content' : forms.Textarea(attrs={"class": "form-control"})
        }

    def clean_title(self):  #  Кастомный валидатор, где всегда есть в названии clean и имя валидируемого поля
        title = self.cleaned_data['title']   
        if re.match(r'\d', title): #  Если в начале титле есть цифры
            raise ValidationError('Название не должно начинаться с цифры')
        return title    




"""
Форма, которая создаётся без связи с моделью

class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название', 
    content = forms.CharField(label='Текст', required= False, widget= forms.Textarea(attrs={"class": "form-control"}))  # required говорит о том обязательно ли поле
    is_published = forms.BooleanField(label='Опубликовано', initial= True)  #  initial говорит о том, какое значение по умочанию
    category = forms.ModelChoiceField(label='Категория', queryset= Category.objects.all())
"""    