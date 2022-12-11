from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from news.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('registr/', registr, name='registr'),
    path('authors/', authors, name='authors'),
    path('login/', user_login, name='login'),
    path('', HomeNews.as_view(), name = 'home'),
    path('admin/', admin.site.urls),
    path('podpiska/<int:user_id>', podpiska, name='podpiska'),
    path('news/', include('news.urls')),
    path('logout/', logout_user, name='logout'),
    path('profil/<int:user_pk>/', profil, name='profil'),
    path('person/<int:person_pk>/', person, name='person'),
    # path('', home, name = 'home'),
    path('category/<int:category_id>/', categories2, name = 'category'),
    ]


if settings.DEBUG:          # для отображения картинок в режиме отладки
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
