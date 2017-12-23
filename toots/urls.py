from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.by_author, name='author'),
    path('tag/<int:tag_id>/', views.by_tag, name='tag'),
]
