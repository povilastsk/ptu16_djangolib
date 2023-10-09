from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path("books/my/", views.UserBookListView.as_view(), name="user_books"),
    path('book/<int:book_pk>/reserve/', views.UserBookReserveView.as_view(), name='user_book_reserve'),

]
