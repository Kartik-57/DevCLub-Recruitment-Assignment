from django.shortcuts import render, get_object_or_404
from .models import Book

def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {'all_books': all_books}) 

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/detail.html', {'book': book}) 

