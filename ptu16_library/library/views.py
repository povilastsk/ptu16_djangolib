from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . import models


class BookListView(generic.ListView):
    model = models.Book
    template_name = 'library/book_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['insight'] = "PTU16 books for your self development"
        return context
    

class BookDetailView(generic.DetailView):
    model = models.Book
    template_name = 'library/book_detail.html'

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

def author_detail(request, pk):
    return render(
        request,
        "library/author_detail.html",
        {"author": get_object_or_404(models.Author, pk=pk)}
    )


