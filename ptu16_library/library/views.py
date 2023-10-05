from typing import Any
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.db.models.query import QuerySet, Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models


class UserBookListView(LoginRequiredMixin, generic.ListView):
    model = models.BookInstance
    template_name = "library/book_user_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(reader=self.request.user)
        return queryset

    
class BookListView(generic.ListView):
    model = models.Book
    template_name = 'library/book_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['search'] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__last_name__istartswith=query)
            )
        return queryset

class BookDetailView(generic.DetailView):
    model = models.Book
    template_name = 'library/book_detail.html'


def index(request: HttpRequest):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': models.Book.objects.count(),
        'num_instances': models.BookInstance.objects.count(),
        'num_available': models.BookInstance.objects.filter(status=0).count(),
        'num_authors': models.Author.objects.count(),
        'genres': models.Genre.objects.all(),
        'num_visits': num_visits,
    }
    return render(request, 'library/index.html', context)

def authors(request: HttpRequest):
    author_pages = Paginator(models.Author.objects.all(), 4)
    current_page = request.GET.get('page') or 1
    return render(
        request, 
        'library/author_list.html', 
        {'author_list': author_pages.get_page(current_page)}
    )

def author_detail(request: HttpRequest, pk: int):
    return render(
        request,
        'library/author_detail.html',
        {'author': get_object_or_404(models.Author, pk=pk)}
    )


