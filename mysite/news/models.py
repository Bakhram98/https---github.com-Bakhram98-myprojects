from distutils.command.upload import upload
from email.policy import default
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.urls import reverse_lazy  #  Для построения урл модели
from django.contrib.auth.models import User

# Create your models here.

class Profil(models.Model):
    
    content = models.TextField(blank= True, verbose_name= 'О себе')     # Если Бланк Тру, поле необязательно для заполнения
    
    user = models.ForeignKey(User, on_delete= models.PROTECT, related_name= 'users', blank= True, null= True)
    podpiski = models.ManyToManyField(User, related_name= 'podpiski', blank=True)
    

    def get_absolute_url(self):
        return reverse_lazy('profil', kwargs = {'user_pk' : self.user.pk})  #  Здесь первый аргумент это обязательно ИМЯ категории

    def __str__(self):
        return self.user.username

    class Meta:  # То, как поля будут в админке отображаться
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        # ordering = ['-created_ad']  # Сортировдка по полю


class News(models.Model):
    title = models.CharField(max_length= 30, verbose_name= "Наименование")   # Вербоуз это то, что у нас отображается в админке
    content = models.TextField(blank= True, verbose_name= 'Контент')     # Если Бланк Тру, поле необязательно для заполнения
    created_ad = models.DateTimeField(auto_now_add= True, verbose_name= 'Дата создания')     # Если этот параметр тру, он автоматически проставвляется при создании
    apdated_ad = models.DateTimeField(auto_now= True)     # Обновляется при редактировании записи
    photo = models.ImageField(upload_to= 'media/', blank = True)
    is_published = models.BooleanField(default= True, verbose_name= 'Опубликовано')     # По умолчанию Тру
    category = models.ForeignKey('Category', on_delete= models.PROTECT, null= True)
    views = models.IntegerField(default = 0)
    author = models.ForeignKey(Profil, on_delete= models.PROTECT, null= True, blank= True)

    def get_absolute_url(self):
        return reverse_lazy('news', kwargs = {'news_id' : self.pk})  #  Здесь первый аргумент это обязательно ИМЯ категории

    def __str__(self):
        return self.title

    class Meta:  # То, как поля будут в админке отображаться
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['-created_ad']  # Сортировдка по полю

class Category(models.Model):
    title = models.CharField(max_length= 150, db_index= True)

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs = {'category_id' : self.pk})


    def __str__(self):
        return self.title
        
    class Meta:  # То, как поля будут в админке отображаться
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['title']

