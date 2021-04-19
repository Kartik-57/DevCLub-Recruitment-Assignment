from django.views import generic
from .models import Book

class IndexView(generic.ListView):
    template_name='books/index.html'
    context_object_name='all_books'

    def get_queryset(self):
        return Book.objects.all()

class DetailView(generic.DetailView):
    model = Book
    template_name='books/detail.html'

class BookCreate(generic.CreateView):
    model = Book
    fields = ['Author', 'Publisher', 'Book_Title', 'Genre', 'ISBN', 'Book_Cover']