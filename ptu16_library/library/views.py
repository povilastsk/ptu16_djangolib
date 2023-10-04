from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models


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


def index(request):
    context = {
        'num_books': models.Book.objects.count(),
        'num_instances': models.BookInstance.objects.count(),
        'num_available': models.BookInstance.objects.filter(status=0).count(),
        'num_authors': models.Author.objects.count(),
        'genres': models.Genre.objects.all(),
    }
    return render(request, 'library/index.html', context)

def authors(request):
    author_pages = Paginator(models.Author.objects.all(), 4)
    current_page = request.GET.get('page') or 1
    return render(
        request, 
        'library/author_list.html', 
        {'author_list': author_pages.get_page(current_page)}
    )

def author_detail(request, pk):
    return render(
        request,
        'library/author_detail.html',
        {'author': get_object_or_404(models.Author, pk=pk)}
    )


