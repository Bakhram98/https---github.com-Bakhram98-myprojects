from msilib.schema import CreateFolder
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, News, Profil
from .forms import NewsForm, UserRegistrForm, UserLoginForm
from django.views.generic import ListView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
'''
class CreateViews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
'''
class HomeNews(ListView):  # Наследуется от ListView, используется для передачи всех записей таблицы. Они сохраняются в переменную object_list, которую нужно использовать в шаблоне
    model = News   #  С какой таблицы будет брать данные
    template_name = 'news/home.html'  #  Здесь задаётся шаблон, который мы хотим использовать, если не хотим использовать тот, который по умолчанию
    context_object_name = 'news'  # Здесь задаётся имя для данных, которое мы хотим использовать, если не хотим использовать object_list
    extra_context = {'name': 'Главная'}    # Для передачи дополнительных переменных. Желательно использовать только для статичных данных

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Взяли старые данные контекста
        context['name'] = 'Главная' # Добавили необходимые данные в контекст
        categories = Category.objects.all()
        context['categories'] = categories
        return context

    def queryset(self):  #  Если нужен отфильтрованный набор записей
        return News.objects.all()
     

def my_posts(request):
    return HttpResponse("Hello world!") 

def home(request):
    news = News.objects.all()
    categories = Category.objects.all()
    context = {'news': news, 'name': "Название новости", 'categories' : categories}
    return render(request, 'news/home.html', context)   

def categories2(request, category_id):
    news = News.objects.filter(category_id = category_id)
    cat = Category.objects.get(pk = category_id)
    categories = Category.objects.all()
    context = {'news': news, 'name': "Название новости", 'categories' : categories, 'cat' : cat}
    return render(request, 'news/categories.html', context)      
# Create your views here

def show_news(request, news_id):
    tek_news = News.objects.get(pk = news_id)
    categories = Category.objects.all()
    context = {'tek_novost': tek_news, 'categories' : categories}
    return render(request, 'news/tek_novost.html', context)  

def my_podpiski(request, user_pk):
    podpiski = Profil.objects.get(user__pk__exact = user_pk).podpiski.all()
    podpiski2 = []
    for i in podpiski:
        name = Profil.objects.get(user__pk__exact = i.pk)
        podpiski2.append(name)
    context = {'podpiski': podpiski2}
    return render(request, 'news/my_podpiski.html', context)  

def authors(request):
    authors = Profil.objects.all()
    context = {'authors': authors}
    return render(request, 'news/authors.html', context)     

def podpiska(request, user_id):  # Обработка подписки. Остаёмся на том же шаблоне со списком постов этого автора
    name = Profil.objects.get(user__pk__exact = user_id)  # Тот пользователь, на которого будем подписываться
    name2 = Profil.objects.get(user__pk__exact = request.user.pk)  # Текущий пользователь
    name2.podpiski.add(name.user)
    prowerka_podpiski = name2.podpiski.filter(pk = name.user.pk).exists()
    profil_posts = News.objects.filter(author__user__pk__exact = user_id)
    categories = Category.objects.all()
    context = {'person_posts': profil_posts, 'categories' : categories, 'name': name, 'name2': name2, 'prowerka_podpiski': prowerka_podpiski}
    return render(request, 'news/person_posts.html', context)      

def otpiska(request, user_id):  # Обработка подписки. Остаёмся на том же шаблоне со списком постов этого автора
    name = Profil.objects.get(user__pk__exact = user_id)  # Тот пользователь, от которого будем подписываться
    name2 = Profil.objects.get(user__pk__exact = request.user.pk) # Текущий пользователь
    name2.podpiski.remove(name.user)
    prowerka_podpiski = name2.podpiski.filter(pk = name.user.pk).exists()
    profil_posts = News.objects.filter(author__user__pk__exact = user_id)
    categories = Category.objects.all()
    context = {'person_posts': profil_posts, 'categories' : categories, 'name': name, 'name2': name2, 'prowerka_podpiski': prowerka_podpiski}
    return render(request, 'news/person_posts.html', context)       

def profil(request, user_pk):
    name = Profil.objects.get(user__pk__exact = user_pk)

    if request.user.is_authenticated:
        name2 = Profil.objects.get(user__pk__exact = request.user.pk)  # Текущий пользователь
        prowerka_podpiski = name2.podpiski.filter(pk = name.user.pk).exists()
    else:
        name2 = False
        prowerka_podpiski = False

    profil_posts = News.objects.filter(author__user__pk__exact = user_pk)
    categories = Category.objects.all()
    context = {'person_posts': profil_posts, 'categories' : categories, 'name': name, 'name2': name2, 'prowerka_podpiski': prowerka_podpiski}
    return render(request, 'news/person_posts.html', context)    

def person(request, person_pk):
    name = Profil.objects.get(user__pk__exact = person_pk)
    name2 = Profil.objects.get(user__pk__exact = request.user.pk)  # Текущий пользователь
    person_posts = News.objects.filter(author__user__pk__exact = person_pk)
    categories = Category.objects.all()
    prowerka_podpiski = name2.podpiski.filter(pk = name.user.pk).exists()
    context = {'person_posts': person_posts, 'categories' : categories, 'name': name, 'name2': name2, 'prowerka_podpiski': prowerka_podpiski}
    return render(request, 'news/person_posts.html', context)     

def user_login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)  #  В логине всегда в этом месте есть дата
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {'categories' : categories, 'form' : form}    
    return render(request, 'news/login.html', context)   

def registr(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UserRegistrForm(request.POST)
        if form.is_valid():  #  Если даные проходят валидацию, то все данные попадают в словарь form.cleaned_data
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы зарегистрированы!')
            p1 = Profil(content = ' ', user = request.user)
            p1.save()
            return redirect('home')
        else:
            messages.error(request, 'ошибка!')    
    else:
        form = UserRegistrForm()
    context = {'name': "Название новости", 'categories' : categories, 'form' : form}   
    return render(request, 'news/registr.html', context)  

def logout_user(request):
    logout(request)
    return redirect('login')
       

def add_news(request):
    form = NewsForm()
    if request.method == 'POST':
        
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():  #  Если даные проходят валидацию, то все данные попадают в словарь form.cleaned_data
            news = form.save(commit= False)

            news.author = Profil.objects.get(user = request.user)
            news.save()
            # news = News.objects.create(**form.cleaned_data)  #  С помощью ** мы автоматически добавляем все данные в таблицу
            return redirect(news)

    

    categories = Category.objects.all()
    context = {'categories' : categories, 'form' : form}
    return render(request, 'news/add_news.html', context)     
