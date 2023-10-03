from django.shortcuts import render
from . import models


def index(request):
    context = {
        "num_books": models.Book.objects.count(),
        "num_instances": models.Bookinstance.objects.count(),
        "num_available": models.Bookinstance.objects.filter(status=0).count(),
        "num_authors": models.Author.objects.count(),
        "genres": models.Genre.objects.all(),
    }
    return render(request, "library/index.html", context)


def authors(request):
    return render(
        request, 
        "library/author_list.html", 
        {"author_list": models.Author.objects.all()}
    )