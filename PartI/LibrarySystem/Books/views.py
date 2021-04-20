from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Book, Availability
from .forms import UserForm

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

class UserFormView(View):
    form_class = UserForm
    template_name = 'books/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

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
                    return redirect('books:index')

        return render(request, self.template_name, {'form':form})

        
