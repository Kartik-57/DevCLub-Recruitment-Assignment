from django.http import Http404
from django.shortcuts import render
from .models import Book

def index(request):
    all_books = Book.objects.all()
    return render(request, 'books/index.html', {'all_books': all_books}) 

def detail(request, book_id):
    try: 
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'books/detail.html', {'book': book}) 
