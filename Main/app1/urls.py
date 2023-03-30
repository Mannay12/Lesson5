from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration),
    path('login/', views.login),
    path('home/', views.home),
    path('blog/', views.blog, name='blog'),
    path('contacts/', views.contacts),
    path('add_post/', views.add_post),
    path('user_post/', views.user_post),
    path('base/', views.base, name='base'),
    path('name/', views.name, name='name'),
]
