from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models


class BookListView(generic.ListView):
    model = models.Book
    template_name = 'library/book_list.html'
    paginate_by = 6
    

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


