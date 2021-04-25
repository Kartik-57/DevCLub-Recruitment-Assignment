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
from datetime import time, date, timedelta

def index(request):
    all_books = Book.objects.all()
    query = request.GET.get("q")
    if query:
        all_books = all_books.filter(
            Q(Book_Title__icontains=query) |
            Q(Author__icontains=query) |
            Q(Genre__icontains=query) |
            Q(ISBN__icontains=query) 
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
                return render(request, 'books/index.html', {'all_books': Book})
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
                user_requests = Request.objects.filter(user=request.user)
                user_books = []
                rejected_books = []
                pending_books = []
                for req in user_requests:
                    if req.status in ['a']:
                        user_books.append(req.book)
                    elif req.status in ['p']:
                        pending_books.append(req.book)
                    else:
                        rejected_books.append(req.book)
                return render(request, 'books/index.html', {'all_books': user_books, 'rejected': rejected_books, 'pending': pending_books})
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
    requests = Request.objects.filter(status = 'p')
    lent = Request.objects.filter(status = 'a').order_by("-lent_date")
    ext = Request.objects.filter(extend = True)
    books = Book.objects.all()
    
    return render(request, 'books/manage-requests.html', {'requests': requests, 'books': books, 'ext': ext, 'lent':lent})

@permission_required('books.change_request')
def accept_request(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.lent_date = date.today()
    request_data.status = 'a'
    request_data.close_date = date.today()+timedelta(days=30)
    if request_data.book.quantity == 1:
        request_data.book.Available = False
    request_data.book.quantity = request_data.book.quantity - 1
    request_data.book.save()
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

@login_required()
def make_request(request):
    book_id = request.GET.get('request_id')

    book_detail = Book.objects.get(id = book_id)
    data = Request(book = book_detail, user = request.user, request_date = date.today())
    data.save()

    return render(request, 'index')

@login_required()
def profile(request):
    req_pending = Request.objects.filter(user = request.user, status = 'p').order_by("-request_date")
    req_close =  Request.objects.filter(user = request.user, status = 'c').order_by("-close_date")
    req_accepted =  Request.objects.filter(user = request.user, status = 'a').order_by("-lent_date")
    req_return = Request.objects.filter(user = request.user, status = 'r').order_by("-return_date")
    req_rejected = Request.objects.filter(user = request.user, status = 'n').order_by("-request_date")
    user = request.user
    context = {
        'p': req_pending,
        'c': req_close,
        'a': req_accepted,
        'n': req_return,
        'r': req_rejected
    }
    return render(request, 'books/profile.html', {'context' : context, 'user':user})

@login_required
def cancel_request(request):
    request_id = request.GET.get('request_id')
    Request.objects.filter(id=request_id).delete()

    return render(request, 'books/profile.html')

@login_required
def extend_request(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.extend = True
    request_data.save()
    
    return render(request, 'books/profile.html')

@permission_required('books.change_request')
def accept_ext(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.close_date = request_data.close_date + timedelta(days=10)
    request_data.extend = False
    request_data.save()

    return render(request, 'Manage_Requests')

@permission_required('books.change_request')
def reject_ext(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.extend = False
    request_data.save()

    return render(request, 'Manage_Requests')

@permission_required('books.change_request')
def return_book(request):
    request_id = request.GET.get('request_id')
    request_data = Request.objects.get(id = request_id)
    request_data.return_date = date.today()
    request_data.status = 'n'
    if request_data.book.quantity == 0:
        request_data.book.Available = True
    request_data.book.quantity = request_data.book.quantity + 1
    request_data.book.save()
    request_data.save()

    return render(request, 'Manage_Requests')






        
