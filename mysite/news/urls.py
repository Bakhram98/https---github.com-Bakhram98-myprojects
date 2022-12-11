from django.urls import path
from .views import *

urlpatterns = [
    path('', my_posts),
    path('<int:news_id>/', show_news, name='news'),
    #path('add_news/', add_news, name='add_news'),
    path('add_news/', add_news, name='add_news'),
    ]