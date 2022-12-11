from django.contrib import admin
from django.contrib.auth.models import User
from .models import News, Category, Profil

class NewsAdmin(admin.ModelAdmin):   # Создаём нормальное отображение нашего приложения
    list_display = ('id', 'title', 'content', 'created_ad', 'is_published', 'author')
    list_display_links = ('id', 'title')   # Какие поля будут ссылками в админке
    search_fields = ('title', 'content')   # Поля, по которым можно осуществлять поиск в админке
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

class CategoryAdmin(admin.ModelAdmin):   # Создаём нормальное отображение нашего приложения
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title')   # Какие поля будут ссылками в админке
    search_fields = ('title',) 

class ProfilAdmin(admin.ModelAdmin):   # Создаём нормальное отображение нашего приложения
    list_display = ('id', 'content', 'user')
    list_display_links = ('id', 'content', 'user')   # Какие поля будут ссылками в админке
    search_fields = ('content',)

admin.site.register(News, NewsAdmin) # Регистрация приложения в админке. Порядок важен, сначала основное
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profil, ProfilAdmin)

# Register your models here.
