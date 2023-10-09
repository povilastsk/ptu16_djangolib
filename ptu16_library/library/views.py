from typing import Any
from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from . import models, forms


class UserBookReserveView(LoginRequiredMixin, generic.CreateView):
    model = models.BookInstance
    form_class = forms.BookInstanceForm
    success_url = reverse_lazy('user_books')
    template_name = 'library/user_book_form.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(models.Book, pk=self.kwargs['book_pk'])
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['book'] = get_object_or_404(models.Book, pk=self.kwargs['book_pk'])
        initial['status'] = 1
        initial['reader'] = self.request.user
        initial['due_back'] = date.today() + timedelta(days=7)
        return initial

    def form_valid(self, form: forms.BookInstanceForm) -> HttpResponse:
        form.instance.book = get_object_or_404(models.Book, pk=self.kwargs['book_pk'])
        form.instance.status = 1
        form.instance.reader = self.request.user
        messages.success(self.request, f"""{form.instance.book} is reserved 
as {form.instance.unique_id} for you until {form.instance.due_back}.""")
        return super().form_valid(form)
    

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


class BookDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Book
    template_name = 'library/book_detail.html'
    form_class = forms.BookReviewForm

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['book'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial

    def post(self, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: forms.BookReviewForm) -> HttpResponse:
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, 'Review posted successfully.')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})


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


