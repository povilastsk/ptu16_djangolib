from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path("books/", views.BookListView.as_view(), name="books"),
    
]
