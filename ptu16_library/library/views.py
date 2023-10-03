from django.shortcuts import render, get_object_or_404
from . import models


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
    return render(
        request, 
        'library/author_list.html', 
        {'author_list': models.Author.objects.all()}
    )


def author_detail(request, pk):
    return render(
        request,
        'library/author_detail.html',
        {'author': get_object_or_404(models.Author, pk=pk)}
    )
