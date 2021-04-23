from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Book, Request, Review, User
from .forms import UserForm
from django.contrib.auth.decorators import login_required, permission_required
from datetime import time, date

def index(request):
    all_books = Book.objects.all()
    query = request.GET.get("q")
    if query:
        all_books = all_books.filter(
            Q(Book_Title__icontains=query) |
            Q(Author__icontains=query)
        ).distinct()
        return render(request, 'books/index.html', {'all_books': all_books})
    else:
        return render(request, 'books/index.html', {'all_books': all_books})

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
    success_url = reverse_lazy('books:index')

def SignUp(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                books = Book.objects.filter(user=request.user)
                return render(request, 'books/index.html', {'Book': Book})
    context = {
        "form": form,
    }
    return render(request, 'books/registration_form.html', context)

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user_books = Book.objects.filter(user=request.user)
                return render(request, 'books/index.html', {'Book': user_books})
            else:
                return render(request, 'books/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'books/login.html', {'error_message': 'Invalid login'})
    return render(request, 'books/login.html')

def Logout(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'books/login.html', context)

@permission_required('books.change_request')
def Manage_Requests(request):
    requests = Request.objects.filter(status= 'p')
    books = Book.objects.all()
    
    return render(request, 'books/manage-requests.html', {'requests': requests, 'books': books})

@permission_required('books.change_request')
def accept_request(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.lent_date = date.today()
    request_data.status = 'a'
    if request_data.book.quantity == 1:
        request_data.book.Available = False
    request_data.book.quantity = request_data.book.quantity - 1
    request_data.save()

    return render(request, 'Manage_Requests')

@permission_required('books.change_request')
def reject_request(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.close_date = date.today()
    request_data.status = 'r'
    request_data.save()

    return render(request, 'Manage_Requests')




        
