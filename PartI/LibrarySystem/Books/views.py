from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Availability

class IndexView(generic.ListView):
    template_name='books/index.html'
    context_object_name='all_books'

    def get_queryset(self):
        return Book.objects.all()

class DetailView(generic.DetailView):
    model = Book
    template_name='books/detail.html'

class BookCreate(CreateView):
    model = Book
    fields = ['Author', 'Publisher', 'Book_Title', 'Genre', 'ISBN', 'Book_Cover']

class BookUpdate(UpdateView):
    model = Book
    fields = ['Author', 'Publisher', 'Book_Title', 'Genre', 'ISBN', 'Book_Cover']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('book:index')