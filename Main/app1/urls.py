from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='base'),
    path('registration/', views.register, name='registration'),
    path('login/', views.login, name='login'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('create_post', views.create_post, name='create_post'),
    path('user_post/', views.user_post, name='user_post'),
    path('name/', views.name, name='name'),
    path('home/', views.home, name='home'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('logout/', views.logout_user, name='logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:post_slug>/comment_delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('post/<slug:post_slug>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('view_profile/<str:username>/', views.view_profile, name='view_profile'),
    path("like/<slug:post_slug>/", views.like, name="like"),
]
