from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Book, Request, Review
from .forms import UserForm
from django.contrib.auth.decorators import login_required

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

        
